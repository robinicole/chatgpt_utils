"""
A class represent a discussion between two chatgpt bots.
"""

from chatgpt_utils.interface import ChatGPTBot, ROLE_SYSTEM


def generate_iam_initial_prompt(role: str):
    return f"I am {role}."


class ChatGPTDiscussion:
    """A class represent a discussion between two chatgpt bots."""

    def __init__(self, bot1: ChatGPTBot, bot2: ChatGPTBot):
        self.bot1 = bot1
        self.bot2 = bot2

    def set_role(self, bot1_role: str, bot2_role: str):
        """Set the role of each bot."""
        self.bot1.add_message_and_generate_response(
            ROLE_SYSTEM, generate_iam_initial_prompt(bot1_role)
        )
        self.bot2.add_message_and_generate_response(
            ROLE_SYSTEM, generate_iam_initial_prompt(bot2_role)
        )

    def kickoff_discussion(self):
        """TODO: implement this method."""
