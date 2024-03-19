A Target represents the agent to test.

---
## Targets on AWS

### Configurations

```yaml
target:
  aws_profile:
  aws_region:
  endpoint_url:
```

- `aws_profile` *(string; optional)*: Named profile used to access AWS services and resources. If unspecified, the `default` profile is used.
- `aws_region` *(string; optional)*: AWS Region to send requests to. If unspecified, the region associated with the `default` profile is used.
- `endpoint_url` *(string; optional)*: The endpoint URL for the AWS service. If unspecified, the public endpoint based on `aws_region` will be used.

### [Agents for Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)

#### Prerequisites

The principal must have the following permissions:

- [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html)

#### Configurations

```yaml
  type: bedrock-agent
  bedrock_agent_id:
  bedrock_agent_alias_id:
```

- `bedrock_agent_id` *(string)*:  The unique identifier of the Bedrock agent.
- `bedrock_agent_alias_id` *(string)*: The alias of the Bedrock agent.

### [Amazon Q for Business](https://docs.aws.amazon.com/amazonq/latest/business-use-dg/what-is.html)

!!! warning

    Amazon Q is in preview release and is subject to change.

#### Prerequisites

The principal must have the following permissions:

- [ChatSync](https://docs.aws.amazon.com/amazonq/latest/api-reference/API_ChatSync.html)

#### Configurations

```yaml
  type: q-business
  q_business_application_id:
  q_business_user_id:
```

- `q_business_application_id` *(string)*: The unique identifier of the Amazon Q application.
- `q_business_user_id` *(string)*: The identifier of the Amazon Q user.


### [Amazon SageMaker Endpoint](https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints.html)

!!! note

    dfsafsfasfa

#### Prerequisites

The principal must have the following permissions:

- [InvokeEndpoint](https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_runtime_InvokeEndpoint.html)

#### Configurations

```yaml
  type: sagemaker-endpoint
  endpoint_name:
  request_body:
  input_path:
  output_path:
  custom_attributes:
  target_model:
  target_variant:
  target_container_hostname:
  inference_component_name:
```

- `endpoint_name` *(string)*: The name of the Amazon Sagemaker endpoint
- `request_body` *(map)*: The JSON request body that is send to the endpoint. This should include the field for the input prompt. For example:
```yaml
request_body:
  input_text: None # input prompt
  temperature: 0.1
  top_p: 0.9
```
- `input_path` *(string)*: A [JSONPath expression](https://github.com/h2non/jsonpath-ng?tab=readme-ov-file#jsonpath-syntax) to match the field for the input prompt in the request body. Using the example above, the `input_path` should be set to `$.input_text`.
- `output_path` *(string)*: A [JSONPath expression](https://github.com/h2non/jsonpath-ng?tab=readme-ov-file#jsonpath-syntax) to match the the generated text in the response body. For example, if the endpoint returns the following:
```json
[{"generated_text": "Hello!"}]
```
You would use the JSONPath expression `$.[0].generated_text` to match the text.
- `custom_attributes` *(string; optional)*: Provides additional information about a request for an inference submitted to a model hosted at an Amazon SageMaker endpoint.
- `target_model` *(string; optional)*: The model to request for inference when invoking a multi-model endpoint.
- `target_variant` *(string; optional)*: The production variant to send the inference request to when invoking an endpoint that is running two or more variants.
- `target_container_hostname` *(string; optional)*: The hostname of the container to invoke if the endpoint hosts multiple containers and is configured to use direct invocation.
- `inference_component_name` *(string; optional)*: The name of the inference conmponent to invoke if the endpoint hosts one or more inference components.

---

## Custom Targets

If you want to test an agent that is not natively supported, you can bring your own Target by creating a subclass of `BaseTarget`. The `BaseTarget` class is an abstract base class and all child classes must implement the `invoke` method to invoke the Target agent.

!!! example "my_custom_target.py"

    ```python
    from agenteval.targets import BaseTarget
    from my_agent import MyAgent

    class MyCustomTarget(BaseTarget):

        def __init__(self, **kwargs):
            self.agent = MyAgent(**kwargs)

        def invoke(self, prompt: str) -> str:
            return self.agent.invoke(prompt)
    ```

Once you have created your subclass, specify the Target in `agenteval.yaml`.

!!! example "agenteval.yaml"

    ```yaml
    target:
      type: path.to.my_custom_target.MyCustomTarget`
      my_agent_parameter: "value" # (1)
      
    ```
    
    1. this value will be passed as `kwargs` when initializing the Target.

!!! warning
    Agent Evaluation currently uses `threading` to run tasks concurrently. During a run, an instance of the Target will be created for each task in the test plan. We recommend avoiding testing Targets that load large models or vector stores into memory, as this can lead to a memory error. Consider deploying your agent as a service using a web framework like [FastAPI](https://fastapi.tiangolo.com).

---

### Examples

#### LangChain Agent

In this example, we create a simple [LangChain](https://python.langchain.com/docs/modules/agents/) agent which calculates the length of a given piece of text. We will create this agent as we instantiate `MyLangChainTarget`.

!!! example "my_langchain_target.py"

    ```python
    from langchain_community.llms import Bedrock
    from langchain.agents import tool
    from langchain import hub
    from langchain.agents import AgentExecutor, create_xml_agent

    from agenteval.targets import BaseTarget

    llm = Bedrock(model_id="anthropic.claude-v2:1")

    @tool
    def calculate_text_length(text: str) -> int:
        """Returns the length of a given text."""
        return len(text)


    tools = [calculate_text_length]
    prompt = hub.pull("hwchase17/xml-agent-convo")

    agent = create_xml_agent(llm, tools, prompt)


    class MyLangChainTarget(BaseTarget):
        def __init__(self, **kwargs):
            self.agent = AgentExecutor(agent=agent, tools=tools, verbose=False)

        def invoke(self, prompt: str) -> str:
            return self.agent.invoke({"input": prompt})["output"]
    ```

We create a test plan that references `MyLangChainTarget`.

!!! example "agenteval.yaml"

    ```yaml
    target:
      type: my_langchain_target.MyLangChainTarget
    tasks:
    - name: CalculateTextLength
      steps:
      - "Ask agent to calculate the length of this text: Hello world!"
      expected_results:
      - The agent responds that the length is 12.
    ```
