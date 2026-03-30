# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
from typing import Any, Optional

from autogen import AssistantAgent, LLMConfig, UserProxyAgent

from agenteval.targets import BaseTarget, TargetResponse

logger = logging.getLogger(__name__)


class AG2Target(BaseTarget):
    """A target encapsulating an AG2 (formerly AutoGen) agent.

    AG2 is an open-source multi-agent framework. This target enables
    evaluation of AG2-based agents through the agent-evaluation framework.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_type: str = "openai",
        api_key: Optional[str] = None,
        system_message: str = "You are a helpful AI assistant.",
        max_turns: int = 3,
        **kwargs: Any,
    ):
        """Initialize the target.

        Args:
            model (str): The LLM model to use.
            api_type (str): The API type (e.g. "openai", "bedrock").
            api_key (Optional[str]): The API key. Reads from
                OPENAI_API_KEY env var if not provided.
            system_message (str): The system message for the assistant agent.
            max_turns (int): Maximum number of consecutive auto replies.
        """
        self._model = model
        self._api_type = api_type
        self._api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self._system_message = system_message
        self._max_turns = max_turns

        self._llm_config = LLMConfig(
            {
                "model": self._model,
                "api_key": self._api_key,
                "api_type": self._api_type,
            }
        )

        self._assistant = AssistantAgent(
            name="assistant",
            system_message=self._system_message,
            llm_config=self._llm_config,
        )

        self._user_proxy = UserProxyAgent(
            name="evaluator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=self._max_turns,
            code_execution_config=False,
        )

    def invoke(self, prompt: str) -> TargetResponse:
        """Invoke the target with a prompt.

        Args:
            prompt (str): The prompt as a string.

        Returns:
            TargetResponse
        """
        self._assistant.reset()
        self._user_proxy.reset()

        result = self._user_proxy.run(
            self._assistant,
            message=prompt,
        ).process()

        response_text = ""
        if result:
            response_text = result.summary or ""

        return TargetResponse(response=response_text)
