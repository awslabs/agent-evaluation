# Bedrock Agent Evaluation Framework

This project implements an automated evaluation framework for Amazon Bedrock Agents using AWS CDK, Step Functions, and Lambda.

## Overview

The framework automates the process of updating Bedrock Agents with new prompts, creating aliases, running evaluation scenarios, and cleaning up resources. It uses AWS Step Functions to orchestrate the workflow and AWS Lambda functions to perform individual tasks.

The example provided is for an energy chatbot usecase

## Components

1. **CDK Stack (StepfunctionsStack)**: Defines the infrastructure, including Lambda functions, Step Functions state machine, and associated IAM roles.

2. **Lambda Functions**:
   - `generate_map`: Generates evaluation scenarios from S3 input.
   - `check_agent_status_1` and `check_agent_status_2`: Check the status of Bedrock Agents.
   - `update_bedrock_agent`: Updates the Bedrock Agent with new instructions.
   - `create_alias`: Creates an alias for the updated agent.
   - `run_test`: Executes evaluation scenarios using the `agenteval` library.
   - `delete_alias`: Removes the temporary alias after evaluation.

3. **Step Functions State Machine**: Orchestrates the evaluation workflow, including agent updates, status checks, and scenario execution.

4. **S3 Bucket**: Stores evaluation prompts and results.

5. **EventBridge Rule**: Triggers the Step Functions workflow when new evaluation prompts are uploaded to S3.

## Workflow

1. New evaluation prompts are uploaded to the S3 bucket.
2. The EventBridge rule triggers the Step Functions state machine.
3. The state machine updates the Bedrock Agent with new instructions.
4. An alias is created for the updated agent.
5. Evaluation scenarios are executed using the `agenteval` library.
6. Results are stored in the S3 bucket.
7. The temporary alias is deleted.

## Setup and Deployment

1. Ensure you have the AWS CDK installed and configured.
2. Install project dependencies:
   ```
   npm install
   ```
3. Deploy the stack:
   ```
   cdk deploy
   ```

## Usage

To run an evaluation:

1. Prepare an evaluation JSON file with prompts and customer profiles.
2. Upload the file to the S3 bucket in the `evaluation_prompts/` prefix.
3. The evaluation process will start automatically.
4. Results will be available in the S3 bucket under the `results/` prefix.

## Notes

- Ensure proper IAM permissions are set up for accessing Bedrock, S3, and other AWS services.
- The `agenteval` library is assumed to be provided as a custom Lambda layer.


# CDK instructions

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
