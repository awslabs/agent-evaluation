# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import re
from typing import Tuple

from agenteval import jinja_env
from agenteval.evaluators import BaseEvaluator
from agenteval.evaluators.bedrock_request.bedrock_request_handler import (
    BedrockRequestHandler,
)
from agenteval.test import TestResult

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE_ROOT = "evaluators/canonical"
_SYSTEM_PROMPT_DIR = "system"
_RUNTIME_PROMPT_DIR = "runtime"
_PROMPT_TEMPLATE_NAMES = [
    "generate_initial_prompt",
    "generate_user_response",
    "generate_test_status",
    "generate_evaluation",
]

# enable backwards-compatible StrEnum
try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class TestStatusCategories(StrEnum):
    ALL_STEPS_ATTEMPTED = "A"
    NOT_ALL_STEPS_ATTEMPTED = "B"


class EvaluationCategories(StrEnum):
    ALL_EXPECTED_RESULTS_OBSERVED = "A"
    NOT_ALL_EXPECTED_RESULTS_OBSERVED = "B"


class Results(StrEnum):
    MAX_TURNS_REACHED = "Maximum turns reached."
    ALL_EXPECTED_RESULTS_OBSERVED = (
        "All of the expected results can be observed in the conversation."
    )
    NOT_ALL_EXPECTED_RESULTS_OBSERVED = (
        "Not all of the expected results can be observed in the conversation."
    )


class CanonicalEvaluator(BaseEvaluator):
    """An evaluator based on the canoncial templates. Compatible with the model providers supported in BedrockModelConfig"""

    def __init__(
        self,
        **kwargs,
    ):
        """Initialize the evaluator."""
        super().__init__(**kwargs)

        self._prompt_template_map = {
            name: {
                "system": jinja_env.get_template(
                    os.path.join(
                        _PROMPT_TEMPLATE_ROOT, _SYSTEM_PROMPT_DIR, f"{name}.jinja"
                    )
                ),
                "prompt": jinja_env.get_template(
                    os.path.join(
                        _PROMPT_TEMPLATE_ROOT, _RUNTIME_PROMPT_DIR, f"{name}.jinja"
                    )
                ),
            }
            for name in _PROMPT_TEMPLATE_NAMES
        }

    @staticmethod
    def _extract_content_from_xml(xml_data: str, element_names: list[str]) -> Tuple:
        content = []
        for e in element_names:
            pattern = rf"<{e}>(.*?)</{e}>"
            match = re.search(pattern, xml_data, re.DOTALL)
            content.append(match.group(1).strip() if match else None)
        return tuple(content)

    def _generate(
        self,
        system_prompt: str,
        prompt: str,
        output_xml_element: str,
    ) -> str:
        request_body = BedrockRequestHandler.build_request_body(
            request_body=self.model_config.request_body,
            model_config=self.model_config,
            system_prompt=system_prompt,
            prompt=prompt,
        )

        response = self.invoke_model(request_body=request_body)

        completion = BedrockRequestHandler.parse_completion_from_response(
            response=response, model_config=self.model_config
        )

        logger.debug(
            f"[{self.test.name}]\n[PROMPT]\n{prompt}\n[COMPLETION]\n{completion}"
        )

        output, reasoning = self._extract_content_from_xml(
            completion, [output_xml_element, "thinking"]
        )

        return output, reasoning

    def _generate_initial_prompt(self) -> str:
        system_prompt = self._prompt_template_map["generate_initial_prompt"][
            "system"
        ].render()
        prompt = self._prompt_template_map["generate_initial_prompt"]["prompt"].render(
            step=self.test.steps[0]
        )

        initial_prompt, reasoning = self._generate(
            system_prompt=system_prompt,
            prompt=prompt,
            output_xml_element="initial_prompt",
        )

        self.trace.add_step(
            system_prompt=system_prompt,
            prompt=prompt,
            initial_prompt=initial_prompt,
            reasoning=reasoning,
        )
        return initial_prompt

    def _generate_test_status(self) -> str:
        system_prompt = self._prompt_template_map["generate_test_status"][
            "system"
        ].render()
        prompt = self._prompt_template_map["generate_test_status"]["prompt"].render(
            steps=self.test.steps, conversation=self.conversation
        )
        test_status, reasoning = self._generate(
            system_prompt=system_prompt,
            prompt=prompt,
            output_xml_element="category",
        )
        self.trace.add_step(
            system_prompt=system_prompt,
            prompt=prompt,
            test_status=test_status,
            reasoning=reasoning,
        )
        return test_status

    def _generate_evaluation(self) -> tuple[str, str]:
        system_prompt = self._prompt_template_map["generate_evaluation"][
            "system"
        ].render()
        prompt = self._prompt_template_map["generate_evaluation"]["prompt"].render(
            expected_results=self.test.expected_results,
            conversation=self.conversation,
        )

        evaluation, reasoning = self._generate(
            system_prompt=system_prompt,
            prompt=prompt,
            output_xml_element="category",
        )
        self.trace.add_step(
            system_prompt=system_prompt,
            prompt=prompt,
            evaluation=evaluation,
            reasoning=reasoning,
        )

        return evaluation, reasoning

    def _generate_user_response(self) -> str:
        system_prompt = self._prompt_template_map["generate_user_response"][
            "system"
        ].render()
        prompt = self._prompt_template_map["generate_user_response"]["prompt"].render(
            steps=self.test.steps, conversation=self.conversation
        )

        user_response, reasoning = self._generate(
            system_prompt=system_prompt,
            prompt=prompt,
            output_xml_element="user_response",
        )

        self.trace.add_step(
            system_prompt=system_prompt,
            prompt=prompt,
            user_response=user_response,
            reasoning=reasoning,
        )
        return user_response

    def _invoke_target(self, user_input) -> str:
        target_response = self.target.invoke(user_input)
        self.trace.add_step(data=target_response.data)

        return target_response.response

    def evaluate(self) -> TestResult:
        """Conduct the test.

        Returns:
            TestResult
        """
        passed = False
        result = Results.MAX_TURNS_REACHED.value
        reasoning = ""

        while self.conversation.turns < self.test.max_turns:
            if self.conversation.turns == 0:
                # start conversation
                if self.test.initial_prompt:
                    user_input = self.test.initial_prompt
                else:
                    user_input = self._generate_initial_prompt()
            else:
                # generate next user response
                user_input = self._generate_user_response()

            # add turn to the conversation
            self.conversation.add_turn(user_input, self._invoke_target(user_input))

            # get test status
            test_status = self._generate_test_status()
            if test_status == TestStatusCategories.ALL_STEPS_ATTEMPTED:
                # evaluate conversation
                eval_category, reasoning = self._generate_evaluation()
                if (
                    eval_category
                    == EvaluationCategories.NOT_ALL_EXPECTED_RESULTS_OBSERVED.value  # noqa: W503
                ):
                    result = Results.NOT_ALL_EXPECTED_RESULTS_OBSERVED.value
                else:
                    result = Results.ALL_EXPECTED_RESULTS_OBSERVED.value
                    passed = True

                break

        return TestResult(
            test_name=self.test.name,
            passed=passed,
            result=result,
            reasoning=reasoning,
            conversation=self.conversation,
        )
