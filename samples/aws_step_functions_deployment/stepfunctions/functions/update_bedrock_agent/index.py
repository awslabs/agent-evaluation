import boto3
import os
from aws_lambda_powertools import Logger

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):

    agent_id = event["agent_id"]
    agent_name=event["agent_name"]
    agent_role = os.environ['AGENT_ROLE']

    model = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    instruction = event['prompt']
        
    bedrock_agent = boto3.client('bedrock-agent')
    
    logger.info("Updating Agent")
    try: 
        
        update_resp = bedrock_agent.update_agent(
            agentId=agent_id,
            agentName=agent_name,
            agentResourceRoleArn=agent_role,
            foundationModel=model,
            instruction=instruction,
            
        )
        logger.info(f"Update agent response: {update_resp}")
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        return {
            'statusCode': 500,
            'error': "Error updating agent"
        }
    
    logger.info("Preparing Agent")    
    try:
        prep_resp = bedrock_agent.prepare_agent(agentId=agent_id)
        logger.info(f"Prepaing Agent response: {prep_resp}")
    except Exception as e:
        logger.error(f"Error preparing agent : {e}")
        return {
            'statusCode': 500,
            'error': "Error preparing agent"
        }
    
    return {
        'statusCode': 200,
        'agentid':agent_id
    }

