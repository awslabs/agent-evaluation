from agenteval.plan import Plan

"""
Example plan runs with configs against a simple agent with the following instructions:

> If the input is positve in style, answer with the fruit of your choosing
> If the input is negative in style, answer with the vegtable of your choosing

YML specs with test cases are found in `/eval_yml_specs` folder

uncomment `result` lines to run an evaluation (the agent IDs in the yml would need to be populated)
"""

# test plan with custom config (haiku 3_5)
test_custom_evaluator_plan = Plan.load(plan_dir="eval_yml_specs")
# result = test_custom_evaluator_plan.run()

# test plan with claude_haiku_3_5 default config
test_claude_haiku_3_5_evaluator_plan = Plan.load(plan_file_name="agenteval_default_claude_haiku_3_5.yml", plan_dir="eval_yml_specs")
# result = test_claude_haiku_3_5_evaluator_plan.run()


# test plan with claude_3 default config
test_claude_3_evaluator_plan = Plan.load(plan_file_name="agenteval_default_claude_3.yml", plan_dir="eval_yml_specs")
# result = test_claude_3_evaluator_plan.run()

# test plan with claude_3_5 default config
test_claude_3_5_evaluator_plan = Plan.load(plan_file_name="agenteval_default_claude_3_5.yml", plan_dir="eval_yml_specs")
# result = test_claude_3_5_evaluator_plan.run()

# test plan with claude_3_7 default config
test_claude_3_7_evaluator_plan = Plan.load(plan_file_name="agenteval_default_claude_3_7.yml", plan_dir="eval_yml_specs")
# result = test_claude_3_7_evaluator_plan.run()

# test plan with llama_3.3 default config
test_llama_3_3_evaluator_plan = Plan.load(plan_file_name="agenteval_default_llama_3_3.yml", plan_dir="eval_yml_specs")
#result = test_llama_3_3_evaluator_plan.run()
