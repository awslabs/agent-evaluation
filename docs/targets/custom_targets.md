# Custom Targets

If you want to test an agent that is not natively supported, you can bring your own Target by defining a Python module containing a subclass of [BaseTarget](../reference/target.md#src.agenteval.targets.target.BaseTarget). The name of this module must contain the suffix `_target` (e.g. `my_custom_target`), and the subclass should implement the `invoke` method to invoke your agent.

```python title="my_custom_target.py"
from agenteval.targets import BaseTarget, TargetResponse
from my_agent import MyAgent

class MyCustomTarget(BaseTarget):

    def __init__(self, **kwargs):
        self.agent = MyAgent(**kwargs)

    def invoke(self, prompt: str) -> TargetResponse:

        response = self.agent.invoke(prompt)

        return TargetResponse(response=response)
```

Once you have created your subclass, specify the module path to the Target.


```yaml title="agenteval.yml"
target:
  type: path.to.my_custom_target.MyCustomTarget`
  my_agent_parameter: "value" # will be passed as `kwargs` when initializing the Target.
```

!!! warning
    During a run, an instance of the Target will be created for each test in the test plan. We recommend avoiding testing Targets that load large models or vector stores into memory, as this can lead to a memory error. Consider deploying your agent and exposing it as a RESTful service.

## Examples

### REST API

We will implement a custom Target that invokes an agent exposed as a REST API.

!!! example "my_api_target.py"

    ```python
    import json

    import requests

    from agenteval.targets import BaseTarget, TargetResponse


    class MyAPITarget(BaseTarget):
        def __init__(self, **kwargs):
            self.url = kwargs.get("url")

        def invoke(self, prompt: str) -> TargetResponse:
            data = {"message": prompt}

            response = requests.post(
                self.url, json=data, headers={"Content-Type": "application/json"}
            )

            return TargetResponse(response=json.loads(response.content)["agentResponse"])
    ```

Create a test plan that references `MyAPITarget`.

!!! example "agenteval.yml"

    ```yaml
    evaluator:
      type: bedrock-claude
      model: claude-sonnet
    target:
      type: my_api_target.MyAPITarget
      url: https://api.example.com/invoke
    tests:
    - name: GetBacklogTickets
      steps:
      - Ask agent how many tickets are left in the backlog
      expected_results:
      - Agent responds with 15 tickets
    ```


### LangChain agent

We will create a simple [LangChain](https://python.langchain.com/docs/modules/agents/) agent which calculates the length of a given piece of text.

!!! example "my_langchain_target.py"

    ```python
    from langchain_community.llms import Bedrock
    from langchain.agents import tool
    from langchain import hub
    from langchain.agents import AgentExecutor, create_xml_agent

    from agenteval.targets import BaseTarget, TargetResponse

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

        def invoke(self, prompt: str) -> TargetResponse:

            response = self.agent.invoke({"input": prompt})["output"]

            return TargetResponse(response=response)
    ```

Create a test plan that references `MyLangChainTarget`.

!!! example "agenteval.yml"

    ```yaml
    evaluator:
      type: bedrock-claude
      model: claude-sonnet
    target:
      type: my_langchain_target.MyLangChainTarget
    tests:
    - name: CalculateTextLength
      steps:
      - "Ask agent to calculate the length of this text: Hello world!"
      expected_results:
      - The agent responds that the length is 12.
    ```
