from pydantic import BaseModel

_USER_NAME = "USER"
_AGENT_NAME = "AGENT"


class Session(BaseModel):
    _conversation: list[tuple] = []
    _reasoning: list[str] = []

    def add_user_message(self, message: str) -> None:
        self._conversation.append((_USER_NAME, message))

    def add_agent_message(self, message: str) -> None:
        self._conversation.append((_AGENT_NAME, message))

    def add_reasoning(self, reasoning: str) -> None:
        self._reasoning.append(reasoning)

    @property
    def conversation(self) -> list[tuple]:
        return self._conversation

    @property
    def reasoning(self) -> list[str]:
        return self._reasoning
