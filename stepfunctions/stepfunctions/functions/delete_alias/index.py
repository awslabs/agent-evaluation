import json
import boto3
import uuid
import os

def handler(event, context):
    # TODO implement

    #pass in from step function but for now
    
    agent_id = event["agent_id"]
    agent_alias_id = event["agent_alias_id"]
    
    bedrock_agent = boto3.client('bedrock-agent')
    
    response = bedrock_agent.delete_agent_alias(
    agentAliasId=agent_alias_id,
    agentId=agent_id
)
    
    
    return {
        'statusCode': 200,
        'agentid':agent_id
    }

