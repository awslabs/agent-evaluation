import json
import logging
import os
import re
from typing import Literal, Tuple

from agenteval import jinja_env
from agenteval.evaluators.aws.bedrock import BedrockEvaluator
from agenteval.evaluators.aws.bedrock.claude import model_configs
from agenteval.test_result import TestResult

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE_ROOT = "evaluators/claude"
_SYSTEM_PROMPT_DIR = "system"
_PROMPT_TEMPLATE_NAMES = [
    "generate_initial_prompt",
    "generate_user_response",
    "generate_test_status",
    "generate_evaluation",
]

_TEST_STATUS_ALL_STEPS_ATTEMPTED_CAT = "A"
_TEST_STATUS_NOT_ALL_STEPS_ATTEMPTED_CAT = "B"
_EVALUATION_ALL_EXPECTED_OBSERVED_CAT = "A"
_EVALUATION_NOT_ALL_EXPECTED_OBSERVED_CAT = "B"

_MAX_TURNS_REACHED_RESULT = "Maximum turns reached."
_EVALUATION_ALL_EXPECTED_OBSERVED_RESULT = (
    "All of the expected results can be observed in the conversation."
)
_EVALUATION_NOT_ALL_EXPECTED_OBSERVED_RESULT = (
    "Not all of the expected results can be observed in the conversation."
)


class ClaudeEvaluator(BedrockEvaluator):
    def __init__(
        self,
        model: Literal[
            "claude-sonnet", "claude", "claude-instant"
        ] = model_configs.DEFAULT_MODEL,
        **kwargs,
    ):
        super().__init__(model_id=model_configs.CLAUDE_MODEL_ID_MAP[model], **kwargs)

        self._prompt_template_map = {
            name: {
                "system": jinja_env.get_template(
                    os.path.join(
                        _PROMPT_TEMPLATE_ROOT, _SYSTEM_PROMPT_DIR, f"{name}.j2"
                    )
                ),
                "prompt": jinja_env.get_template(
                    os.path.join(_PROMPT_TEMPLATE_ROOT, f"{name}.j2")
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
        request_body = model_configs.REQUEST_BODY
        request_body["system"] = system_prompt
        request_body["messages"][0]["content"][0]["text"] = prompt

        response = self.invoke_model(request_body=request_body)
        response_body = response.get("body").read()
        completion = json.loads(response_body)["content"][0]["text"]

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
        success = False
        result = _MAX_TURNS_REACHED_RESULT
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
            if test_status == _TEST_STATUS_ALL_STEPS_ATTEMPTED_CAT:
                # evaluate conversation
                eval_category, reasoning = self._generate_evaluation()
                if eval_category == _EVALUATION_NOT_ALL_EXPECTED_OBSERVED_CAT:
                    result = _EVALUATION_NOT_ALL_EXPECTED_OBSERVED_RESULT
                elif eval_category == _EVALUATION_ALL_EXPECTED_OBSERVED_CAT:
                    result = _EVALUATION_ALL_EXPECTED_OBSERVED_RESULT
                    success = True

                break

        return TestResult(
            test_name=self.test.name,
            success=success,
            result=result,
            reasoning=reasoning,
            conversation_handler=self.conversation,
        )
