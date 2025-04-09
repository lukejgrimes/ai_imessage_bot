from openai import OpenAI
from chat import Chat
from message import Message
import os
from dotenv import load_dotenv

class Bot:
    def __init__(self, chat: Chat, mode: int) -> None:
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat = chat
        if mode == 0:
            self.messages = [{"role": "system", "content": f"You have one and only one role which is to respond to text messages. Respond to all future messages according to the CHAT CONTEXT\nCHAT CONTEXT: {self.chat.chat_context}"}]
            self.model = "gpt-4o"
        elif mode == 1:
            self.messages = [{"role": "system", "content": "You are Rob, you're a fired up guy and not afraid to be loud and outspoken. You love to be controversial. You don't believe in math or statistics and you love pro wrestling. You hate Corporate America. You love to voice your grievances with the world. You are also often time very explicit and type in all caps. You're main goal is to get the user riled up and ready to argue or join in with your rants."}]
            self.model = os.getenv("ROB_MODEL")

    def create_response(self, received_text: Message) -> Message:
        self.messages.append({"role": "user", "content": f"{received_text.sender}: {received_text.content}"})
        if len(self.messages) > 20:
            del self.messages[1]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
        )

        self.messages.append(response.choices[0].message)

        res_message = response.choices[0].message.content
        return res_message
    
