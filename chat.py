from message import Message
from contact import Contact
import subprocess
import sqlite3


class Chat:
    def __init__(self, id=None, participants=None, context=None) -> None:
        self.id: str = id
        self.participants: list[Contact] = participants
        self.chat_context: str = context
        self.chat_history: list[Message]

    def create_new_context(self, new_context: str) -> None:
        self.chat_context = new_context

    def add_to_chat_context(self, new_context: str) -> None:
        self.chat_context += new_context

    def add_participant(self, new_participant: Contact) -> None:
        self.participants.append(new_participant)

    def add_message_to_history(self, new_message: Message) -> None:
        self.chat_history.append(new_message)

    def get_last_message(self, cursor) -> Message:
        query = f"""
            SELECT message.text, handle.id
            FROM message
            LEFT JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
            LEFT JOIN chat ON chat_message_join.chat_id = chat.ROWID
            LEFT JOIN handle ON message.handle_id = handle.ROWID
            WHERE chat.guid = '{self.id}'
            AND message.is_from_me = 0
            ORDER BY message.date DESC
            LIMIT 1;
            """
        cursor.execute(query)
        res = cursor.fetchone()
        try: 
            text_message = res[0]
            sender = res[1]
        except Exception:
            text_message = ""
            sender = ""
        return Message(sender=sender, content=text_message)

    
    def send_text(self, new_message: Message) -> None:
        safe_content = new_message.content.replace('"', '\\"')
        applescript = f'''
        tell application "Messages"
            set targetChat to chat id "{self.id}"
            send "{safe_content}" to targetChat
        end tell'''

        subprocess.run(["osascript", "-e", applescript])

    

