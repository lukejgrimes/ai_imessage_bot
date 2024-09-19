from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Message(BaseModel):
    sender: str
    content: str

class Contact(BaseModel):
    name: str
    phone_number: str
    notes: list[str]

class Chat(BaseModel):
    # id: str = id
    participants: list[Contact]
    chat_context: str
    # chat_history: list[Message]

class BotRequest(BaseModel):
    chat: Chat
    message: Message


@app.post("/api/generate_response/")
async def create_response(self, request: BotRequest) -> Message:
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[  {"role": "system", "content": f"You have one and only one role which is to respond to text messages. Respond to all future messages according to the CHAT CONTEXT\nCHAT CONTEXT: {request.chat.chat_context}"},
                    {"role": "user", "content": f"{request.message.sender}: {request.message.content}"}         
        ]
    )

    return Message(sender="Me", content=response.choices[0].message.content)
    