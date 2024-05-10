from telethon import TelegramClient, events
from telethon.tl import types
import asyncio
import re


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


async def search_audio_files_in_chat(chat_id, size):
    audio_message_ids = []
    async for message in client.iter_messages(chat_id):
        if message.media:
            try:
                if isinstance(message.media, types.MessageMediaDocument):
                    if message.media.document.mime_type.startswith('audio'):
                        file_size = message.media.document.size
                        print(message.media.document.mime_type, file_size)
                        if file_size < size:
                            audio_message_ids.append(message.id)
            except AttributeError:
                continue
    return audio_message_ids


async def download_audio_by_id(chat_id, message_id):
    try:
        message = await client.get_messages(entity=chat_id, ids=message_id)
        if message and message.media:
            await client.download_media(message, file=f'./media/{chat_id}_{message_id}.mp3')
    except Exception as e:
        print(f"An error occurred: {str(e)}")


@client.on(events.NewMessage(outgoing=True))
async def log_outgoing_messages(event):
    if event.is_private:
        chat_id = event.chat_id
        message_text = event.raw_text
        await handle_search_and_download_audio(message_text, chat_id)


async def handle_search_and_download_audio(message_text, chat_id):
    if message_text.startswith("search4{") and message_text.endswith("}"):
        print('pattern is ok')
        extracted_text = message_text[8:-1]
        match = re.match(r"(.+)\((\d+)\)", extracted_text)
        if match:
            print('pattern is mached')
            data = match.group(1)
            size = int(match.group(2))
            audio_ids = await search_audio_files_in_chat(chat_id, size)
            if audio_ids:
                for audio_id in audio_ids:
                    await download_audio_by_id(chat_id, audio_id)


with client:
    client.start()
    client.run_until_disconnected()
