from telethon import TelegramClient, events
from telethon.tl import types
import speech_recognition as sr
import re
import os
from pydub import AudioSegment


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


async def search_word_in_audio(audio_file, word_to_search):
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Convert audio to text
    try:
        # Specify the language as Persian (Farsi)
        text = recognizer.recognize_google(audio_data, language='fa-IR')
        print("Audio converted to text: ", text)

        # Search for the word in text
        if word_to_search.lower() in text.lower():
            print(f"'{word_to_search}' found in audio.\n")
            return 1
        else:
            print(f"'{word_to_search}' not found in audio.\n")
            return 0
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio\n")
        return 0
    except sr.RequestError as e:
        print(
            f"Could not request results from Google Speech Recognition service; {e}\n")
        return 0


async def search_audio_files_in_chat(chat_id, size):
    audio_message_ids = []
    async for message in client.iter_messages(chat_id):
        if message.media:
            try:
                if isinstance(message.media, types.MessageMediaDocument):
                    if message.media.document.mime_type.startswith('audio'):
                        file_size = message.media.document.size
                        print(message.media.document.mime_type)
                        if file_size < size:
                            audio_message_ids.append(
                                [message.id, message.media.document.mime_type.split('/')[1]])
                            if len(audio_message_ids) > 10:
                                return audio_message_ids
            except AttributeError:
                continue
    return audio_message_ids


async def download_audio_by_id(chat_id, data):
    # TODO: if there exist
    try:
        message = await client.get_messages(entity=chat_id, ids=data[0])
        if message and message.media:
            await client.download_media(message, file=f'./media/{chat_id}_{data[0]}.{data[1]}')
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
            await process_and_search_audio_files(data)


async def process_and_search_audio_files(word_to_search):
    media_folder = './media/'
    wav_folder = './media/wav/'
    os.makedirs(wav_folder, exist_ok=True)
    await convert_ogg_mpeg_to_wav(media_folder, wav_folder)

    # Search for the specified word in each wav file
    for filename in os.listdir(wav_folder):
        if filename.endswith('.wav'):
            wav_path = os.path.join(wav_folder, filename)
            result = await search_word_in_audio(wav_path, word_to_search)
            if result == 1:
                parts = filename.split('_')
                chat_id = parts[0]
                message_id = parts[1].split('.')[0]

                # Replying to the message in the chat
                reply_message = f"Found the word '{word_to_search}' in your audio message."
                try:
                    await client.send_message(int(chat_id), reply_message, reply_to=int(message_id))
                except ValueError as e:
                    print(f"Failed to send message: {str(e)}")


async def convert_ogg_mpeg_to_wav(media_folder, wav_folder):
    for filename in os.listdir(media_folder):
        if filename.endswith('.ogg') or filename.endswith('.mpeg'):
            original_path = os.path.join(media_folder, filename)
            wav_path = os.path.join(
                wav_folder, filename.rsplit('.', 1)[0] + '.wav')
            sound = AudioSegment.from_file(original_path)
            sound.export(wav_path, format="wav")


with client:
    client.start()
    client.run_until_disconnected()
