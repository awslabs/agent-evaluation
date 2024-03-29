## Getting started

To begin, initialize a test plan.

```bash
agenteval init
```

This will create an `agenteval.yml` file in the current directory.

```yaml
evaluator:
  type: bedrock-claude
  model: claude-sonnet
target:
  type: bedrock-agent
  bedrock_agent_id: null
  bedrock_agent_alias_id: null
tests:
  - name: RetrieveMissingDocuments
    steps:
      - Ask agent for a list of missing documents for claim-006.
    expected_results:
      - The agent returns a list of missing documents for claim-006.
```

If you are testing an Amazon Bedrock agent, update the following `target` configurations:

- `bedrock_agent_id`: The unique identifier of the Amazon Bedrock agent.
- `bedrock_agent_alias_id`: The alias of the Amazon Bedrock agent.

Update `tests` with your test cases. Each test must have the following:

- `name`: A unique name for the test.
- `steps`: A list of steps you want to perform in your test.
- `expected_results`: A list of expected results for your test.

!!! info

    Refer to [Targets](./targets/index.md) for additional targets and their required configurations.

Once you have updated the test plan, you can run your tests:

```bash
agenteval run
```

The results will be printed in your terminal and a Markdown summary will be available in `agenteval_summary.md`.

You will also find traces saved under `agenteval_traces/`. This is useful for understanding the
flow of evaluation.


## Writing test cases

It is important to be clear and concise when writing your test cases.

```yaml
tests:
  - name: GetOpenClaims
    steps:
      - Ask the agent which claims are open.
    expected_results:
      - The agent returns a list of open claims.
```

If your test cases are complex, consider breaking them down into multiple `steps`, `expected_results`, and/or `tests`.

### Multi-turn conversations

To test multiple user-agent interactions, you can provide multiple `steps` to orchestrate the interaction.

```yaml
tests:
  - name: GetOpenClaimWithDetails
    steps:
      - Ask the agent which claims are open.
      - Once the agent responds with the list of open claims, ask for the details
        on claim-006.
    expected_results:
      - The agent returns the details on claim-006.
```

The maximum number of turns allowed for a conversation is configured using the `max_turns` parameter for the test (defaults to `2` when not specified).
If the number of turns in the conversation reaches the `max_turns` limit, then the test will fail.

### Specify the first user message

By default, the first user message in the test is automatically generated based on the list of `steps`. To override this message, you can specify the `initial_prompt`.

```yaml
tests:
  - name: GetOpenClaimWithDetails
    steps:
      - Ask the agent which claims are open.
      - Once the agent responds with the list of open claims, ask for the details
        on claim-006.
    expected_results:
      - The agent returns the details on claim-006.
    initial_prompt: Can you let me know which claims are open?
```

## Evaluation hooks
You can specify hooks that run before and/or after evaluating a test. This is useful for performing integration testing, as well as any setup or cleanup tasks required.

To create hooks, you will define a subclass of [Hook](reference/hook.md#src.agenteval.hook.Hook).

For a hook that runs *before* evaluation, implement a `pre_evaluate` method. In this method, you have access to the [Test](reference/test.md#src.agenteval.test.Test) and [TraceHandler](reference/trace_handler.md#src.agenteval.trace_handler.TraceHandler) via the `test` and `trace` arguments, respectively.

For a hook that runs *after* evaluation, implement a `post_evaluate` method. Similar to the `pre_evaluate` method, you have access to the `Test` and `TraceHandler`. You also have access to the [TestResult](reference/test_result.md#src.agenteval.test_result.TestResult) via the `test_result` argument. You may override the attributes of the `TestResult` if you plan to use this hook to perform additional testing, such as integration testing.

!!! example "my_evaluation_hook.py"

    ```python
    from agenteval import Hook

    class MyEvaluationHook(Hook):

      def pre_evaluate(test, trace):
        # implement logic here

      def post_evaluate(test, test_result, trace):
        # implement logic here
    ```

Once you have created your subclass, specify the hook for the test in `agenteval.yml`.

!!! example "agenteval.yml"

    ```yaml
    tests:
      - name: MakeReservation
        hook: my_evaluation_hook.MyEvaluationHook
    ```

### Examples

#### Integration testing using `post_evaluate`

In this example, we will test an agent that can make dinner reservations. In addition to evaluating the conversation, we want to test that the reservation is written to the backend database. To do this, we will create a post evaluation hook that queries a PostgreSQL database for the reservation record. If the record is not found, we will override the `TestResult`.

!!! example "test_record_insert.py"

    ```python
    import boto3
    import json
    import psycopg2
    
    from agenteval import Hook

    SECRET_NAME = "test-secret"

    def get_db_secret() -> dict:

      session = boto3.session.Session()
      client = session.client(
          service_name='secretsmanager',
      )
      get_secret_value_response = client.get_secret_value(
          SecretId=SECRET_NAME
      )
      secret = get_secret_value_response['SecretString']

      return json.loads(secret)

    class TestRecordInsert(Hook):
      
      def post_evaluate(test, test_result, trace):

        # get database secret from AWS Secrets Manager
        secret = get_db_secret()

        # connect to database
        conn = psycopg2.connect(
          database=secret["dbname"],
          user=secret["username"],
          password=secret["password"],
          host=secret["host"],
          port=secret["port"]
        )

        # check if record is written to database
        with conn.cursor() as cur:
          cur.execute("SELECT * FROM reservations WHERE name = 'Bob'")
          row = cur.fetchone()

        # override the test result based on query result 
        if not row:
          test_result.success = False
          test_result.result = "Integration test failed"
          test_result.reasoning = "Record was not inserted into the database"
    ```

Create a test that references the hook.

!!! example "agenteval.yml"

    ```yaml
    tests:
    - name: MakeReservation
      steps:
      - Ask agent to make a reservation under the name Bob for 7 PM.
      expected_results:
      - The agent confirms that a reservation has been made.
      hook: test_record_insert.TestRecordInsert
    ```