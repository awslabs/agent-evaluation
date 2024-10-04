import boto3
import json
import os

s3_client = boto3.client('s3')

from aws_lambda_powertools import Logger

logger = Logger()

def handler(event, context):

    bucket = event["detail"]["bucket"]["name"]
    key = event["detail"]["object"]["key"]
    
    logger.info("Fetching scenarios")
    try: 
        scenario_json = s3_client.get_object(Bucket=bucket, Key=key)
        text = json.loads(scenario_json["Body"].read())
        logger.info(text)
    except Exception as e:
        logger.error(f"Error getting object: {e}")
        

    prompts = text['prompts']
    profiles = text['customer_profiles']


    # Generate scenarios
    scenarios = []
    
    for prompt in prompts:
        item = {
            'prompt': prompt['prompt'],
            'scenarios': profiles
            }
        scenarios.append(item)
    
    
    return {
        'statusCode': 200,
        'agent_id': text["agent_id"],
        'agent_name': text["agent_name"],
        'body': scenarios
    }
    