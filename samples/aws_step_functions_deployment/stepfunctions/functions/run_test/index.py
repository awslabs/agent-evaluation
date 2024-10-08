import yaml
import datetime
import os
import threading
import time
import boto3
import uuid

from agenteval.runner import Runner
from agenteval.plan import Plan

from aws_lambda_powertools import Logger

logger = Logger()
s3_client = boto3.client('s3')


def handler(event, context):
    
    scenario = event['scenario']
    agent_id = event['agent_id']
    agent_alias_id = event['agent_alias_id']
    agent_alias_name = event['agent_alias_name']
    bucket_name = os.environ["EVALUATION_BUCKET"]
    uid = uuid.uuid4()

    user_profile = {
        'demographic': scenario['demography'],
        'household_size': scenario['household_size'],
        'appliances': scenario['appliances'],
        'energy_usage': scenario['energy_usage'],
        'tariff': scenario['tarrif'],
        'payment_type': scenario['payment_type']
    }
    
    profile_str = yaml.safe_dump(user_profile, default_flow_style=False, sort_keys=False)
    
    yaml_data = {
        'evaluator': {
            'model': 'claude-3',
        },
        'target': {
            'type': 'bedrock-agent',
            'bedrock_agent_id': agent_id,
            'bedrock_agent_alias_id': agent_alias_id
        },
        'tests': {
            'provide recommendation to customer in need': {
                'profile': user_profile,
                'max_turns': 10,
                'steps': [
                    'Ask the agent how you can reduce your energy bills',
                    'Respond to the agents questions using the details in:',
                    profile_str,
                    'Respond to the agents questions using the details in:',
                    profile_str,
                    'Respond to the agents questions using the details in:',
                    profile_str,
                    'Respond to the agents questions using the details in:',
                    profile_str
                ],
                'expected_results': [
                    'The agent asks the user questions to create a profile',
                    'The agent asks the user questions to create a profile',
                    'The agent asks the user questions to create a profile',
                    'The agent asks the user questions to create a profile',
                    'The agent returns a recommendation'
                ]
            }
        }
    }


    # Convert to YAML
    yaml_output = yaml.safe_dump(yaml_data, sort_keys=False, default_flow_style=False)
    
    yaml_dir = "/tmp/plan"
    local_yaml_path = f"{yaml_dir}/agenteval.yml"
    os.makedirs(os.path.dirname(local_yaml_path), exist_ok=True)

    with open(local_yaml_path,"w") as file:
        file.write(yaml_output)
    
        
    plan = Plan.load(plan_dir=yaml_dir, filter=None)
    
            
    now = datetime.datetime.now()
    created_at = now.strftime("%Y-%m-%d %H:%M:%S")
    test_result_dir = f"/tmp/results/"
    
    
    runner = Runner(
        plan=plan,
        verbose=False,
        num_threads=None, 
        work_dir = test_result_dir
    )
    
    try:
        
        runner_thread = threading.Thread(target=runner.run)
        runner_thread.start()
        num_completed = 0
        
        while num_completed < runner.num_tests:
            time.sleep(1)
            num_completed = len(list(filter(lambda x:x != None, runner.results.values())))
            
        runner_thread.join()
        now = datetime.datetime.now()
        status = "completed"
        finished_at = now.strftime("%Y-%m-%d %H:%M:%S")
        
        test_passed_rate = (
            f"{runner.num_tests - runner.num_failed}/ {runner.num_tests}"
            )
        
        
        with open(os.path.join(test_result_dir, "agenteval_summary.md")) as f:
            result = f.read()
        
        s3_key = f"results/agent={agent_id}/alias={agent_alias_name}/test_id={uid}/results.md"      
        s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=result)

    
    except Exception as e:
        logger.error(f"Error running the test: {e}")
        status = "error"
        
        
    return{
        'created_at': created_at,
        'finished_at':finished_at,
        'target_type': yaml_data["target"]["type"],
        'status': status,
        'test_passed_rate':test_passed_rate
    }
        