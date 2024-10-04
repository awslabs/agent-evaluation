import boto3
import json
import os

s3_client = boto3.client('s3')
bedrock_agent = boto3.client('bedrock-agent')

from aws_lambda_powertools import Logger
logger = Logger()

def handler(event, context):

    agent_id = event["update_output"]["agentid"]
    
    logger.info("Getting agent status")
    try:
        response = bedrock_agent.get_agent(
        agentId=agent_id
        )
        agent_status = response["agent"]["agentStatus"]
        logger.info(f"Agent status: {agent_status}")
        
    except Exception as e:
        logger.error(f"Erorr getting agent: {e}")
    
    agent_status = response["agent"]["agentStatus"]
    
    return {
        'statusCode': 200,
        'agent_id': agent_id,
        'agent_status': agent_status
    }
