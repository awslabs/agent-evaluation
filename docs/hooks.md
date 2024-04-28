You can specify hooks that run before and/or after evaluating a test. This is useful for performing integration testing, as well as any setup or cleanup tasks required.

To create your hooks, define a Python module containing a subclass of [Hook](reference/hook.md#src.agenteval.hook.Hook). The name of this module must contain the suffix `_hook` (e.g. `my_evaluation_hook`).

- Implement the `pre_evaluate` method for a hook that runs *before* evaluation. In this method, you have access to the [Test](reference/test.md#src.agenteval.test.Test) and [Trace](reference/trace.md#src.agenteval.trace.Trace) via the `test` and `trace` arguments, respectively.

- Implement the `post_evaluate` method for a hook that runs *after* evaluation,. Similar to the `pre_evaluate` method, you have access to the [Test](reference/test.md#src.agenteval.test.Test) and [Trace](reference/trace.md#src.agenteval.trace.Trace). You also have access to the [TestResult](reference/test_result.md#src.agenteval.test_result.TestResult) via the `test_result` argument. You may override the attributes of the `TestResult` if you plan to use this hook to perform additional testing, such as integration testing.


```python title="my_evaluation_hook.py"
from agenteval import Hook
# import dependencies here

class MyEvaluationHook(Hook):

    def pre_evaluate(test, trace):
    # implement logic here

    def post_evaluate(test, test_result, trace):
    # implement logic here
```

Once you have created your subclass, specify the module path to the hook.

```yaml title="agenteval.yml"
tests:
  make_reservation:
    hook: my_evaluation_hook.MyEvaluationHook
```

## Examples

### Integration testing using `post_evaluate`

In this example, we will test an agent that can make dinner reservations. In addition to evaluating the conversation, we want to test that the reservation is written to the backend database. To do this, we will create a post evaluation hook that queries a PostgreSQL database for the reservation record. If the record is not found, we will override the `TestResult`.

!!! example "test_record_insert_hook.py"

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

    class TestRecordInsertHook(Hook):

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
      make_reservation:
        steps:
        - Ask agent to make a reservation under the name Bob for 7 PM.
        expected_results:
        - The agent confirms that a reservation has been made.
        hook: test_record_insert_hook.TestRecordInsert
    ```