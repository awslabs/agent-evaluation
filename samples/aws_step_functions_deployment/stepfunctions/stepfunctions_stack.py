import os 
import pathlib

import aws_cdk as cdk

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_stepfunctions_tasks as tasks,
    aws_events as events,
    aws_events_targets as targets,
    aws_stepfunctions as sfn,
    aws_iam as iam
)
from constructs import Construct
from .layer import Layer 
import platform

runtime = _lambda.Runtime.PYTHON_3_12


platform_mapping = {
    "x86_64": _lambda.Architecture.X86_64,
    "arm64": _lambda.Architecture.ARM_64
}
architecture = platform_mapping[platform.uname().machine]

class StepfunctionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        evaluation_bucket = cdk.aws_s3.Bucket(
            self,
            "EvaluationBucket",
            event_bridge_enabled=True
            )
        
        powertools_layer = Layer(
            self,
            "PowertoolsLayer",
            architecture=architecture,
            runtime=runtime,
            path=os.path.join(
                pathlib.Path(__file__).parent.resolve().parent,
                "layers",
                "aws-lambda-powertools"
            )
        )

        agenteval_layer = Layer(
            self,
            "AgentEvalLayer",
            architecture=architecture,
            runtime=runtime,
            path=os.path.join(
                pathlib.Path(__file__).parent.resolve().parent,
                "layers",
                "agent-evaluation"
            )
        )
        
        generate_map_function = _lambda.Function(
            self,
            "GenerateMapFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "generate_map",
                )
            ),
            layers=[powertools_layer.layer_version]
        )

        generate_map_step = tasks.LambdaInvoke(
            self,
            "Generate Map State",
            lambda_function = generate_map_function,
            payload=sfn.TaskInput.from_json_path_at("$"),
            output_path=sfn.JsonPath.string_at("$.Payload")
            )
        
           
        get_status_function_1 = _lambda.Function(
            self,
            "GetStatusFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "check_agent_status_1",
                )
            ),
            layers=[powertools_layer.layer_version]
        )
            
        get_status_step_1 = tasks.LambdaInvoke(
            self,
            "Get Status 1",
            lambda_function=get_status_function_1,
            payload=sfn.TaskInput.from_json_path_at("$"),
            result_selector = {
              "agentid": sfn.JsonPath.string_at("$.Payload.agent_id"),
              "agentstatus": sfn.JsonPath.string_at("$.Payload.agent_status"),
              "full_payload": sfn.JsonPath.string_at("$")},
            result_path = sfn.JsonPath.string_at("$.status_output_1")
            )
            
            
        agent_role = iam.Role(
            self,
            "AgentRole",
            assumed_by=iam.ServicePrincipal("bedrock.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess")
            ])
        
        update_agent_function = _lambda.Function(
            self,
            "UpdateAgentFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "update_bedrock_agent",
                )
            ),
            layers=[powertools_layer.layer_version]
        )
        
        
        
        update_agent_function.add_environment("AGENT_ROLE",agent_role.role_arn)

        update_agent_step = tasks.LambdaInvoke(
            self,
            "Update Agent",
            lambda_function = update_agent_function,
            payload=sfn.TaskInput.from_json_path_at("$"),
            result_path = "$.update_output",
            result_selector = {
            "agentid": sfn.JsonPath.string_at("$.Payload.agentid")
            }
            )
            
        first_choice = sfn.Choice(self, "UpdateChoice1")
        
        condition1 = sfn.Condition.or_(
        sfn.Condition.string_equals("$.status_output_1.agentstatus", "UPDATING"),
        sfn.Condition.string_equals("$.status_output_1.agentstatus", "VERSIONING")
        )
        
        wait_step= sfn.Wait(
            self,
            "Wait1",
            time=sfn.WaitTime.duration(Duration.seconds(30))
            )
        
        
        create_alias_function = _lambda.Function(
            self,
            "CreateAliasFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "create_alias",
                )
            ),
            layers=[powertools_layer.layer_version]
        )

        create_alias_step = tasks.LambdaInvoke(
            self,
            "Create Alias",
            lambda_function = create_alias_function,
            payload=sfn.TaskInput.from_json_path_at("$"),
            output_path = sfn.JsonPath.string_at("$.Payload"),
            
            )
      
        get_status_function_2 = _lambda.Function(
            self,
            "GetStatusFunction2",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "check_agent_status_2",
                )
            ),
            layers=[powertools_layer.layer_version]
        )
            
        get_status_step_2 = tasks.LambdaInvoke(
            self,
            "Get Status 2",
            lambda_function=get_status_function_2,
            payload=sfn.TaskInput.from_json_path_at("$"),
            result_selector = {
              "agentid": sfn.JsonPath.string_at("$.Payload.agent_id"),
              "agentstatus": sfn.JsonPath.string_at("$.Payload.agent_status"),
              "full_payload": sfn.JsonPath.string_at("$")},
            result_path = "$.status_output_2")
            
            
        
        second_choice = sfn.Choice(self, "UpdateChoice2")
        condition2 = sfn.Condition.not_(
        sfn.Condition.string_equals("$.status_output_2.agentstatus", "PREPARED"),
        )
        wait_step_2= sfn.Wait(
            self,
            "Wait2",
            time=sfn.WaitTime.duration(Duration.seconds(30))
            )
        
        
        agent_alias_map = sfn.Map(
            self,
            "Agent Alias Map",
            max_concurrency=1,
            items_path = sfn.JsonPath.string_at("$.body"),
            item_selector={
                "agent_id": sfn.JsonPath.string_at("$.agent_id"),
                "agent_name": sfn.JsonPath.string_at("$.agent_name"),
                "prompt": sfn.JsonPath.string_at("$$.Map.Item.Value.prompt"),
                "scenarios": sfn.JsonPath.string_at("$$.Map.Item.Value.scenarios")
            }
            #you can only update an agent one at a time
            #
            )
        
        pass_step = sfn.Pass(self, 
                             "Pass State"
                             )
        
        run_test_function = _lambda.Function(
            self,
            "RunTestFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(10),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "run_test",
                )
            ),
            layers=[powertools_layer.layer_version, agenteval_layer.layer_version],
             environment={
                "EVALUATION_BUCKET": evaluation_bucket.bucket_name,
            },
        )
        run_test_step = tasks.LambdaInvoke(
            self,
            "Run Test",
            lambda_function=run_test_function,
            payload=sfn.TaskInput.from_json_path_at("$"),
            result_path="$.run_test"
            )
        
        error_pass = sfn.Pass(self, "handle failure")
            
        run_test_step.add_catch(error_pass,
                                result_path="$.error")
        test_map= sfn.Map(
            self,
            "Evaluation Map",
            items_path = sfn.JsonPath.string_at("$.scenarios"),
            item_selector={
                "prompt": sfn.JsonPath.string_at("$.prompt"),
                "agent_id": sfn.JsonPath.string_at("$.agent_id"),
                "agent_alias_id": sfn.JsonPath.string_at("$.agent_alias_id"),
                "agent_alias_name": sfn.JsonPath.string_at("$.agent_alias_name"),
                "scenario": sfn.JsonPath.string_at("$$.Map.Item.Value")
            },
            result_path="$.map_output"
            )
        delete_alias_function = _lambda.Function(
            self,
            "DeleteAliasFunction",
            runtime=runtime,
            architecture=architecture,
            timeout=cdk.Duration.minutes(5),
            handler="index.handler",
            code=_lambda.Code.from_asset(
                os.path.join(
                    pathlib.Path(__file__).resolve().parent,
                    "functions",
                    "delete_alias",
                )
            ),
            layers=[powertools_layer.layer_version]
        )
        
        delete_alias_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*"],
                resources=["*"],
            )
        )
        
        delete_alias_step = tasks.LambdaInvoke(
            self,
            "Delete Alias",
            lambda_function = delete_alias_function,
            payload=sfn.TaskInput.from_json_path_at("$"),
            result_path = "$.Payload",

            )
        
        map_definition_2= run_test_step.next(pass_step)
        
        test_map.item_processor(map_definition_2)
       
        
        map_definition =   get_status_step_1.next(
            first_choice.when(condition1, wait_step.next(get_status_step_1)).otherwise(update_agent_step
            .next(
                get_status_step_2.next(
                    second_choice.when(condition2,wait_step_2.next(get_status_step_2)).otherwise(create_alias_step.next(
                        test_map
                        ).next(
                            delete_alias_step
                        )
                    )
                    )
                )
            )
            )
            
       
        
        agent_alias_map.item_processor(map_definition)
        
     
        
        chain = generate_map_step.next(agent_alias_map)
        
        evaluator_state_machine = sfn.StateMachine(
            self,
            "EvaluatorState",
            definition_body = sfn.DefinitionBody.from_chainable(chain))
        
        
        
        evaluator_state_machine.role.attach_inline_policy(
            iam.Policy(
                self,
                "BedrockPolicy",
                statements=[
                    iam.PolicyStatement(
                        actions=["bedrock:*"],
                        resources=["*"],
                    )
                ],
            )
        )
            
      
        
        on_put_rule = events.Rule(
            self,
            "InvokeState",
            event_pattern=events.EventPattern(
                source=["aws.s3"],
                detail_type=[
                    "Object Created"
                ],
                detail={
                    "bucket": {
                        "name": [evaluation_bucket.bucket_name]
                    },
                    "object": {
                        "key": [{"prefix": "evaluation_prompts"}]},
                },
            ),
        )

        on_put_rule.add_target(targets.SfnStateMachine(evaluator_state_machine))
        
        get_status_function_1.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*"],
                resources=["*"],
            )
        )
        get_status_function_2.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*"],
                resources=["*"],
            )
        )
        
        create_alias_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*"],
                resources=["*"],
            )
        )
        
        generate_map_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:*"],
                resources=["*"],
            )
        )
         
        run_test_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:*","bedrock:*"],
                resources=["*"],
            )  
        )
        
        update_agent_function.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*","iam:PassRole","iam:ListRoles"],
                resources=["*"],
            )  
        )