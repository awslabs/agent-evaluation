import boto3
import json
import os

s3_client = boto3.client('s3')
bedrock_agent = boto3.client('bedrock-agent')

# from aws_lambda_powertools import Logger, Tracer

# tracer = Tracer()
# logger = Logger()

def handler(event, context):

    agent_id = event["update_output"]["agentid"]

    response = bedrock_agent.get_agent(
    agentId=agent_id
    )
    
    agent_status = response["agent"]["agentStatus"]
    
    return {
        'statusCode': 200,
        'agent_id': agent_id,
        'agent_status': agent_status
    }
