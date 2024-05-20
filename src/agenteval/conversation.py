# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

_USER = "USER"
_AGENT = "AGENT"
_START_TURN_COUNT = 0


class Conversation:
    """Captures the interaction between a user and an agent.

    Attributes:
        messages (list): A list of tuples of the form (role, message).
        turns (int): The number of turns in the conversation.
    """

    def __init__(self):
        """
        Initialize the conversation.
        """
        self.messages = []
        self.turns = _START_TURN_COUNT

    def __iter__(self):
        return iter(self.messages)

    def add_turn(self, user_message: str, agent_response: str):
        """Record a turn in the conversation.

        Args:
            user_message (str): The users's message
            agent_response (str): The agent's response to the user's message

        Increments the `turn` counter by `1`.
        """
        self.messages.extend([(_USER, user_message), (_AGENT, agent_response)])
        self.turns += 1
