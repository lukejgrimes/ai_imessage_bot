from chat import Chat
from bot import Bot
from message import Message
import time

from db import get_db_cursor

cursor = get_db_cursor()

def get_chats():
    query = """
        SELECT guid FROM chat;
    """

    cursor.execute(query)
    chat_list = cursor.fetchall()
    for i in range(len(chat_list)):
        print(f"{i}: {chat_list[i][0]}")

    return chat_list

def set_names(chat_id):
    query = f"""
        SELECT handle.id
        FROM handle
        LEFT JOIN chat_handle_join ON handle.ROWID = chat_handle_join.handle_id
        LEFT JOIN chat ON chat_handle_join.chat_id = chat.ROWID
        WHERE chat.guid = '{chat_id}';
    """

    cursor.execute(query)
    numbers = cursor.fetchall()

    contacts = {}

    for i in range(len(numbers)):
        name = input(f"{numbers[i][0]}\nEnter a name for the above number: ")
        contacts[numbers[i][0]] = name

    return contacts

run = True

while(run):
    print("Welcome to AI Text Message Bot!")
    input("Press enter to start")
    chats = get_chats()

    chat_number = input("Select a chat for which you'd like to start a bot:\n")
    selected_chat = chats[int(chat_number)][0]

    contacts = set_names(selected_chat)

    print("Great! Let's start a bot with chat: ")
    chat_context = input("Please provide context for the chat:\n")

    chat_context += f"The people in the chat and their corresponding numbers are: {contacts.items()}"

    current_chat = Chat(id=selected_chat, context=chat_context) # Initialize chat
    send_first_text = input("Do you want to send the first text?(Y/n): ")
    send_first_text = True if send_first_text == 'Y' or send_first_text == 'y' else False
    start = input("Are you ready to start the bot? (Y/n): ")

    bot = Bot(current_chat)

    last_message = current_chat.get_last_message(cursor) if not send_first_text else None
    last_text = last_message.content if last_message else "First text"
    while True:
        if current_chat.get_last_message(cursor).content != last_text:
            last_message = current_chat.get_last_message(cursor)
            last_text = last_message.content
            res = bot.create_response(last_message)
            current_chat.send_text(Message(sender="Me", content=res))
        time.sleep(10)


