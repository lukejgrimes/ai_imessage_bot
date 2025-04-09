from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import uuid
import firebase_admin
from firebase_admin import credentials

app = FastAPI()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cred = credentials.Certificate("../imessage-bot-c48a3-firebase-adminsdk-iv83d-d852e850ee.json")
firebase_admin.initialize_app(cred)

class Message(BaseModel):
    sender: str
    content: str

class Contact(BaseModel):
    id: uuid.UUID
    name: str
    nickname: str
    phoneNumber: str

class Chat(BaseModel):
    # id: str = id
    participants: list[Contact]
    chatContext: str
    # chat_history: list[Message]

class BotRequest(BaseModel):
    messages: list[dict[str, str]]
    newMessage: Message
    chatContext: str
    updateContext: bool

class TestObject(BaseModel):
    id: uuid.UUID
    name: str
    participants: list[Contact]
    chatContext: str
    isActive: bool


@app.post("/api/generate_response/")
async def create_response(request: BotRequest) -> list[dict[str, str]]:
    updateContext = request.updateContext
    if len(request.messages == 0):
        messages = []
        updateContext = True
    elif len(request.messages > 20):
        messages = request.messages[0] + request.messages[-20:]
    if (updateContext):
        messages.append({"role": "system", "content": f"You have one and only one role which is to respond to text messages. Respond to all future messages according to the CHAT CONTEXT\nCHAT CONTEXT: {request.chatContext}"}) 

    messages.append({"role": "user", "content": f"{request.newMessage.sender}: {request.newMessage.content}"})
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    messages.append(response.choices[0].message)

    return messages
    

@app.post("/api/test/")
def test(obj: TestObject) -> None:
    print(obj.chatContext)
    return {"status": 200, "content": "Test Content"}

@app.get("/")
def root():
    return {"status": 200}
