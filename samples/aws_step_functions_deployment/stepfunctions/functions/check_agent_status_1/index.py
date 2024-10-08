import boto3

s3_client = boto3.client('s3')
bedrock_agent = boto3.client('bedrock-agent')

from aws_lambda_powertools import Logger
logger = Logger()

def handler(event, context):

    agent_id = event["agent_id"]
    logger.info(f"Getting agent status for agent: {agent_id}")
    try:
        response = bedrock_agent.get_agent(
            agentId=agent_id
        )
        agent_status = response["agent"]["agentStatus"]
        logger.info(f"Agent status: {agent_status}")
        return {
            'statusCode': 200,
            'agent_id': agent_id,
            'agent_status': agent_status
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': f"Erorr getting agent: {e}"
        } 
