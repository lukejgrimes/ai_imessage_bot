from openai import OpenAI
from chat import Chat
from message import Message
import os
from dotenv import load_dotenv

class Bot:
    def __init__(self, chat: Chat) -> None:
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat = chat

    def create_response(self, recieved_text: Message) -> Message:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[  {"role": "system", "content": f"You have one and only one role which is to respond to text messages. Respond to all future messages according to the CHAT CONTEXT\nCHAT CONTEXT: {self.chat.chat_context}"},
                        {"role": "user", "content": f"{recieved_text.sender}: {recieved_text.content}"}         
            ]
        )

        return response.choices[0].message.content
    