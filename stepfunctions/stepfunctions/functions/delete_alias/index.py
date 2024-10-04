import json
import boto3
import uuid
import os
from aws_lambda_powertools import Logger

logger = Logger()

def handler(event, context):

    
    agent_id = event["agent_id"]
    agent_alias_id = event["agent_alias_id"]
    
    bedrock_agent = boto3.client('bedrock-agent')
    logger.info("Deleting Agent Alias")
    try:
        response = bedrock_agent.delete_agent_alias(
        agentAliasId=agent_alias_id,
        agentId=agent_id
        )
        logger.info(f"Delete alias response: {response}")

    except Exception as e:
        logger.error(f"Error deleting agent alias : {e}")
    
    return {
        'statusCode': 200,
        'agentid':agent_id
    }

