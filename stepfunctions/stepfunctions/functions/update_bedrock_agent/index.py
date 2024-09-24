import json
import boto3
import uuid
import os

def handler(event, context):
    # TODO implement

    #pass in from step function but for now
    
    agent_id = event["agent_id"]
    agent_name=event["agent_name"]
    agent_role = os.environ['AGENT_ROLE']

    # role = "arn:aws:iam::905418302891:role/service-role/AmazonBedrockExecutionRoleForAgents_LED91O3XKK"
    model = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    instruction = event['prompt']
        
    bedrock_agent = boto3.client('bedrock-agent')
    update_resp = bedrock_agent.update_agent(
        agentId=agent_id,
        agentName=agent_name,
        agentResourceRoleArn=agent_role,
        foundationModel=model,
        instruction=instruction,
        
    )
    
    prep_resp = bedrock_agent.prepare_agent(agentId=agent_id)
    
    
    return {
        'statusCode': 200,
        'agentid':agent_id
    }

