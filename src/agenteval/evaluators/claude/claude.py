import json
import logging
import os
import re
from typing import Literal, Tuple

from agenteval import jinja_env
from agenteval.evaluators.claude import model_configs
from agenteval.evaluators.evaluator import BedrockEvaluator
from agenteval.task import TaskResult

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE_ROOT = "evaluator/claude"
_SYSTEM_PROMPT_DIR = "system"
_PROMPT_TEMPLATE_NAMES = [
    "start_session",
    "user_response",
    "task_status",
    "evaluate",
]


_TASK_STATUS_COMPLETED_CATEGORY = "A"
_TASK_STATUS_NOT_COMPLETED_CATEGORY = "B"
_TASK_STATUS_UNABLE_TO_COMPLETE_CATEGORY = "C"
_EVAL_ALL_EXPECTED_RESULT_OBSERVED_CATEGORY = "A"
_EVAL_NOT_ALL_EXPECTED_RESULT_OBSERVED_CATEGORY = "B"


class ClaudeEvaluator(BedrockEvaluator):
    def __init__(
        self, model: Literal["claude-sonnet", "claude", "claude-instant"], **kwargs
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
            f"[{self.task.name}]\n[PROMPT]\n{prompt}\n[COMPLETION]\n{completion}"
        )

        output, reasoning = self._extract_content_from_xml(
            completion, [output_xml_element, "thinking"]
        )

        self.add_to_trace(reasoning)

        return output

    def _generate_initial_prompt(self) -> str:
        return self._generate(
            system_prompt=self._prompt_template_map["start_session"]["system"].render(),
            prompt=self._prompt_template_map["start_session"]["prompt"].render(
                step=self.task.steps[0]
            ),
            output_xml_element="initial_prompt",
        )

    def _generate_task_status(self) -> str:
        return self._generate(
            system_prompt=self._prompt_template_map["task_status"]["system"].render(),
            prompt=self._prompt_template_map["task_status"]["prompt"].render(
                steps=self.task.steps, session=self.session
            ),
            output_xml_element="task_status",
        )

    def _generate_evaluation(self) -> str:
        return self._generate(
            system_prompt=self._prompt_template_map["evaluate"]["system"].render(),
            prompt=self._prompt_template_map["evaluate"]["prompt"].render(
                expected_results=self.task.expected_results,
                session=self.session,
            ),
            output_xml_element="eval",
        )

    def _generate_user_response(self) -> str:
        return self._generate(
            system_prompt=self._prompt_template_map["user_response"]["system"].render(),
            prompt=self._prompt_template_map["user_response"]["prompt"].render(
                steps=self.task.steps, session=self.session
            ),
            output_xml_element="user_response",
        )

    def run(self) -> TaskResult:
        success = False
        description = "Max turns reached."

        while self.turns < self.task.max_turns:
            if self.turns == 0:
                # start convo
                if self.task.initial_prompt:
                    user_input = self.task.initial_prompt
                    self.add_to_trace("Initial prompt provided")
                else:
                    user_input = self._generate_initial_prompt()
            else:
                # generate next user response
                user_input = self._generate_user_response()

            target_response = self.target.invoke(user_input)
            self.add_turn(user_input, target_response)

            # get task status
            task_status_category = self._generate_task_status()
            if task_status_category in (
                _TASK_STATUS_COMPLETED_CATEGORY,
                _TASK_STATUS_UNABLE_TO_COMPLETE_CATEGORY,
            ):
                # evaluate
                eval_category = self._generate_evaluation()
                if eval_category == _EVAL_ALL_EXPECTED_RESULT_OBSERVED_CATEGORY:
                    success = True
                    description = "All expected results observed."
                elif task_status_category == _TASK_STATUS_UNABLE_TO_COMPLETE_CATEGORY:
                    description = "Agent was unable to complete a step."
                else:
                    description = "Not all of the expected results were observed."
                # break since task has been completed
                break
        return TaskResult(
            name=self.task.name,
            success=success,
            description=description,
            session=self.session,
            trace=self.trace,
        )
