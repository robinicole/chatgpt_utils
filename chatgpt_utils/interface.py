import openai

ROLE_ASSISTANT: str = "assistant"
ROLE_USER: str = "user"
ROLE_SYSTEM: str = "system"


class ChatGPTBot:
    """An interface to the OpenAi chatgpt API."""

    def __init__(self, api_key, model="gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def generate_response(self):
        completion = openai.ChatCompletion.create(
            model=self.model, messages=self.messages
        )
        response = completion.choices[0].message.content
        self.add_message(ChatGPTBot.ASSISTANT, response)
        return response

    def add_message_and_generate_response(self, role, content):
        self.add_message(role, content)
        return self.generate_response()

    def reset_conversation(self):
        self.messages = []
