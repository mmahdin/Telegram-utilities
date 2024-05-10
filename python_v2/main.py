from telethon import TelegramClient, events
import asyncio


# Define your API ID and Hash from Telegram
# Read API ID and Hash from a configuration file
config_file_path = 'config'
with open(config_file_path, 'r') as file:
    lines = file.readlines()
    api_id = lines[0].split()[1].strip()
    api_hash = lines[1].split()[1].strip()

# Create the client and connect to Telegram
client = TelegramClient('anon', api_id, api_hash,
                        proxy=("http", '172.19.0.1', 8080))


@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):
    if event.is_private:  # Check if the message is from a private chat
        sender = await event.get_sender()
        sender_id = sender.id

        # Auto-reply to the sender
        response_message = "Hello! I received your message."
        await client.send_message(sender_id, response_message)

with client:
    client.start()
    client.run_until_disconnected()
