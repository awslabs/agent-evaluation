# Custom Targets

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
      my_agent_parameter: "value" # will be passed as `kwargs` when initializing the Target.
      
    ```

!!! warning
    During a run, an instance of the Target will be created for each task in the test plan. We recommend avoiding testing Targets that load large models or vector stores into memory, as this can lead to a memory error. Consider deploying your agent and exposing it as a RESTful API.

---

## Examples

### Testing an agent exposed as a REST API

Example coming soon. 


### Testing a LangChain agent

We will create a simple [LangChain](https://python.langchain.com/docs/modules/agents/) agent which calculates the length of a given piece of text.

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

Create a test plan that references `MyLangChainTarget`.

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
