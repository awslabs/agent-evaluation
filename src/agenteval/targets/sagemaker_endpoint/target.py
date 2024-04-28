import json
from typing import Optional

from jsonpath_ng import parse

from agenteval.targets import Boto3Target, TargetResponse

_SERVICE_NAME = "sagemaker-runtime"
_CONTENT_TYPE = "application/json"
_ACCEPT = "application/json"


class SageMakerEndpointTarget(Boto3Target):
    def __init__(
        self,
        endpoint_name: str,
        request_body: dict,
        input_path: str,
        output_path: str,
        custom_attributes: Optional[str] = None,
        target_model: Optional[str] = None,
        target_variant: Optional[str] = None,
        target_container_hostname: Optional[str] = None,
        inference_component_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(boto3_service_name=_SERVICE_NAME, **kwargs)

        self._request_body = request_body
        self._input_jp_expr = parse(input_path)
        self._output_jp_expr = parse(output_path)

        self._args = self._create_base_args(
            endpoint_name,
            custom_attributes,
            target_model,
            target_variant,
            target_container_hostname,
            inference_component_name,
        )

    @staticmethod
    def _create_base_args(
        endpoint_name: str,
        custom_attributes: Optional[str],
        target_model: Optional[str],
        target_variant: Optional[str],
        target_container_hostname: Optional[str],
        inference_component_name: Optional[str],
    ):
        args = {
            "EndpointName": endpoint_name,
            "ContentType": _CONTENT_TYPE,
            "Accept": _ACCEPT,
            **{
                key: value
                for key, value in {
                    "CustomAttributes": custom_attributes,
                    "TargetModel": target_model,
                    "TargetVariant": target_variant,
                    "TargetContainerHostname": target_container_hostname,
                    "InferenceComponentName": inference_component_name,
                }.items()
                if value is not None
            },
        }

        return args

    def _update_request(self, prompt: str):
        self._input_jp_expr.update(self._request_body, prompt)
        self._args["Body"] = json.dumps(self._request_body)

    def _query_response(self, response_body: dict) -> str:
        return self._output_jp_expr.find(response_body)[0].value

    def invoke(self, prompt: str) -> str:
        self._update_request(prompt)

        response = self.boto3_client.invoke_endpoint(**self._args)

        response_body = json.loads(response.get("Body").read())

        return TargetResponse(response=self._query_response(response_body))
