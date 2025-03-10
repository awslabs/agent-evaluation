import json
from agenteval.evaluators.bedrock_request.bedrock_request_handler import BedrockRequestHandler
from agenteval.evaluators.model_config.bedrock_model_config import BedrockModelConfig, ModelProvider
import pytest
from unittest.mock import MagicMock

TEST_SYSTEM_PROMPT = "You are a helpful assistant."
TEST_PROMPT = "Why do we want to use an LLM to evaluate an LLM?"

@pytest.fixture
def model_config_meta():
    return BedrockModelConfig(model_id="meta.llama-v0", request_body={})

@pytest.fixture
def model_config_anthropic():
    return BedrockModelConfig(model_id="anthropic.claude-v0", request_body={})

def test_build_request_body_meta(model_config_meta):
    request_body = {}
    
    result = BedrockRequestHandler.build_request_body(request_body, model_config_meta, TEST_SYSTEM_PROMPT, TEST_PROMPT)
    
    assert "prompt" in result
    assert result["prompt"] == f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>{TEST_SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>{TEST_PROMPT}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"


def test_build_request_body_anthropic(model_config_anthropic):
    request_body = {"messages": [{"content": [{"text": ""}]}]}
    
    result = BedrockRequestHandler.build_request_body(request_body, model_config_anthropic, TEST_SYSTEM_PROMPT, TEST_PROMPT)
    
    assert "system" in result
    assert result["system"] == TEST_SYSTEM_PROMPT
    assert result["messages"][0]["content"][0]["text"] == TEST_PROMPT


def test_parse_completion_from_response_meta(model_config_meta):
    response_mock = MagicMock()
    response_mock.get.return_value.read.return_value = json.dumps({"generation": "test completion"}).encode()
    
    result = BedrockRequestHandler.parse_completion_from_response(response_mock, model_config_meta)
    
    assert result == "test completion"


def test_parse_completion_from_response_anthropic(model_config_anthropic):
    response_mock = MagicMock()
    response_mock.get.return_value.read.return_value = json.dumps({"content": [{"text": "test completion"}]}).encode()
    
    result = BedrockRequestHandler.parse_completion_from_response(response_mock, model_config_anthropic)
    
    assert result == "test completion"

def test_unsupported_model_throws():
    with pytest.raises(ValueError, match="Unsupported model ID: stability.ai-v0"):
        BedrockRequestHandler.build_request_body({}, BedrockModelConfig(model_id="stability.ai-v0", request_body={}), "", "")

