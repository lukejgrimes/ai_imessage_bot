from chat import Chat
from bot import Bot
from message import Message
import time

from db import get_db_cursor

cursor = get_db_cursor()

def get_chats():
    chat_query = "SELECT ROWID, guid FROM chat;"
    cursor.execute(chat_query)
    chat_rows = cursor.fetchall()

    chat_info = [chat_row[1] for chat_row in  chat_rows]

    for i, (chat_id, guid) in enumerate(chat_rows):
        participant_query = """
            SELECT handle.id
            FROM chat_handle_join
            JOIN handle ON handle.ROWID = chat_handle_join.handle_id
            WHERE chat_handle_join.chat_id = ?
        """
        cursor.execute(participant_query, (chat_id,))
        participants = [row[0] for row in cursor.fetchall()]

        participants_str = ", ".join(participants) if participants else "Unknown"

        print(f"{i}: Participants: {participants_str}")

    return chat_info

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
    mode = int(input("Input 0 for standard, 1 for RobGPT: "))

    chats = get_chats()

    chat_number = input("Select a chat for which you'd like to start a bot:\n")
    selected_chat = chats[int(chat_number)]

    contacts = set_names(selected_chat)

    print("Great! Let's start a bot with chat: ")
    chat_context = input("Please provide context for the chat:\n")

    chat_context += f"The people in the chat and their corresponding numbers are: {contacts.items()}"

    current_chat = Chat(id=selected_chat, context=chat_context)
    send_first_text = input("Do you want to send the first text?(Y/n): ")
    send_first_text = True if send_first_text == 'Y' or send_first_text == 'y' else False
    start = input("Are you ready to start the bot? (Y/n): ")

    bot = Bot(current_chat, mode)
    if mode == 1:
        print("ROB MODE")

    last_message = current_chat.get_last_message(cursor) if not send_first_text else None
    last_text = last_message.content if last_message else "First text"

    while True:
        if current_chat.get_last_message(cursor).content != last_text:
            last_message = current_chat.get_last_message(cursor)
            last_text = last_message.content
            res = bot.create_response(last_message)
            current_chat.send_text(Message(sender="Me", content=res))
        time.sleep(5)


