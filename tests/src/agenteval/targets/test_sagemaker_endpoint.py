import pytest
from src.agenteval.targets import sagemaker_endpoint
from src.agenteval.targets import target
from io import BytesIO


@pytest.fixture
def sagemaker_endpoint_fixture(mocker):
    mock_session = mocker.patch.object(target.boto3, "Session")
    mocker.patch.object(mock_session.return_value, "client")

    fixture = sagemaker_endpoint.SageMakerEndpointTarget(
        endpoint_name="test-endpoint",
        request_body={"inputs": None, "temperature": 0},
        input_path="$.inputs",
        output_path="$.[0].generated_text",
        custom_attributes=None,
        target_model=None,
        target_variant=None,
        target_container_hostname=None,
        inference_component_name="test-component",
    )

    return fixture


class TestSageMakerEndpointTarget:

    def test_base_args(self, sagemaker_endpoint_fixture):

        assert sagemaker_endpoint_fixture._args == {
            "EndpointName": "test-endpoint",
            "ContentType": sagemaker_endpoint._CONTENT_TYPE,
            "Accept": sagemaker_endpoint._ACCEPT,
            "InferenceComponentName": "test-component",
        }

    @pytest.mark.parametrize(
        "prompt,request_body,input_jp_expr,expected",
        [
            (
                "test prompt 1",
                {"inputs": None},
                sagemaker_endpoint.parse("$.inputs"),
                {"inputs": "test prompt 1"},
            ),
            (
                "test prompt 2",
                {"inputs": {"prompt": None}},
                sagemaker_endpoint.parse("$.inputs.prompt"),
                {"inputs": {"prompt": "test prompt 2"}},
            ),
            (
                "test prompt 3",
                [{"inputs": None}],
                sagemaker_endpoint.parse("$.[0].inputs"),
                [{"inputs": "test prompt 3"}],
            ),
            (
                "test prompt 4",
                {"inputs": [{"prompt": None}]},
                sagemaker_endpoint.parse("$.inputs.[0].prompt"),
                {"inputs": [{"prompt": "test prompt 4"}]},
            ),
        ],
    )
    def test_update_request(
        self, prompt, request_body, input_jp_expr, expected, sagemaker_endpoint_fixture
    ):

        sagemaker_endpoint_fixture._request_body = request_body
        sagemaker_endpoint_fixture._input_jp_expr = input_jp_expr
        sagemaker_endpoint_fixture._update_request(prompt)

        assert sagemaker_endpoint_fixture._args[
            "Body"
        ] == sagemaker_endpoint.json.dumps(expected)

    @pytest.mark.parametrize(
        "response_body,output_jp_expr,expected",
        [
            (
                [{"generated_text": "test completion 1"}],
                sagemaker_endpoint.parse("$.[0].generated_text"),
                "test completion 1",
            ),
            (
                {"output": {"completion": "test completion 2"}},
                sagemaker_endpoint.parse("$.output.completion"),
                "test completion 2",
            ),
            (
                {"output": [{"completion": "test completion 3"}]},
                sagemaker_endpoint.parse("$.output.[0].completion"),
                "test completion 3",
            ),
        ],
    )
    def test_query_response(
        self, response_body, output_jp_expr, expected, sagemaker_endpoint_fixture
    ):

        sagemaker_endpoint_fixture._output_jp_expr = output_jp_expr
        value = sagemaker_endpoint_fixture._query_response(response_body)

        assert value == expected

    def test_invoke(self, mocker, sagemaker_endpoint_fixture):

        mock_update_request = mocker.patch.object(
            sagemaker_endpoint_fixture, "_update_request"
        )

        mock_query_response = mocker.patch.object(
            sagemaker_endpoint_fixture, "_query_response"
        )
        mock_query_response.return_value = "test completion"

        mock_invoke_endpoint = mocker.patch.object(
            sagemaker_endpoint_fixture.boto3_client, "invoke_endpoint"
        )

        mock_invoke_endpoint.return_value = {
            "Body": BytesIO(b'[{"generated_text": "test completion"}]')
        }

        response = sagemaker_endpoint_fixture.invoke("test prompt")

        mock_update_request.assert_called_once_with("test prompt")

        assert mock_invoke_endpoint.call_count == 1
        assert response.response == "test completion"

        mock_query_response.assert_called_once_with(
            [{"generated_text": "test completion"}]
        )
