import json
import boto3
import uuid
from aws_lambda_powertools import Logger

logger = Logger()

def handler(event, context):
    
    bedrock_agent = boto3.client('bedrock-agent')
    
    agent_alias = str(uuid.uuid4())
    agent_id = event["update_output"]["agentid"]
    
    logger.info("Creating Agent Alias")
    try:
        alias_resp = bedrock_agent.create_agent_alias(
        agentAliasName=agent_alias,
        agentId=agent_id
        )
        logger.info(f"Create Alias Response: {alias_resp}")
    
    except Exception as e:
        logger.error(f"Error creating alias: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error creating alias')
        }


    agent_id = alias_resp["agentAlias"]["agentId"]
    agent_alias_id = alias_resp["agentAlias"]["agentAliasId"]
    agent_alias_name = alias_resp["agentAlias"]["agentAliasName"]
    
    return {
        'prompt': event['prompt'],
        'agent_id':agent_id,
        'agent_alias_id': agent_alias_id,
        'agent_alias_name': agent_alias_name,
        'scenarios': event['scenarios']
    }