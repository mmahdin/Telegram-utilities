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

NTH_LAST_MESSAGE = 10


async def search_word_in_audio(audio_file, word_to_search):
    """
    Asynchronously searches for a specific word in an audio file using speech recognition.

    This function loads an audio file, converts it to text using Google's speech recognition service,
    and checks if the specified word exists in the converted text.

    Args:
    audio_file (str): The path to the audio file.
    word_to_search (str): The word to search for in the audio file.

    Returns:
    int: 1 if the word is found in the audio, 0 otherwise.
    """
    print(
        f"Entering search_word_in_audio with {audio_file} looking for '{word_to_search}'")
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        print('audio recognizer...')
        text = recognizer.recognize_google(audio_data, language='fa-IR')
        if word_to_search.lower() in text.lower():
            print(f"'{word_to_search}' found in audio.")
            return 1
        else:
            print(f"'{word_to_search}' not found in audio.")
            return 0
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return 0
    except sr.RequestError as e:
        print(
            f"Could not request results from Google Speech Recognition service; {e}")
        return 0
    finally:
        print("Exiting search_word_in_audio")


async def convert_ogg_mpeg_to_wav(media_folder, wav_folder):
    """
    Converts audio files from OGG or MPEG format to WAV format.

    This function scans a specified media folder for files with .ogg or .mpeg extensions,
    converts them to .wav format, and saves them in a specified WAV folder.

    Args:
    media_folder (str): The directory path where the original media files are stored.
    wav_folder (str): The directory path where the converted WAV files will be saved.
    """
    print(
        f"Entering convert_ogg_mpeg_to_wav with media_folder={media_folder} and wav_folder={wav_folder}")
    for filename in os.listdir(media_folder):
        if filename.endswith('.ogg') or filename.endswith('.mpeg'):
            original_path = os.path.join(media_folder, filename)
            wav_path = os.path.join(
                wav_folder, filename.rsplit('.', 1)[0] + '.wav')
            sound = AudioSegment.from_file(original_path)
            sound.export(wav_path, format="wav")
    print("Exiting convert_ogg_mpeg_to_wav")


async def process_and_search_audio_files(word_to_search, cht_id):
    """
    Processes and searches for a specified word in audio files within a directory.
    Converts audio files to WAV format, searches each WAV file for the word, and sends a reply in the chat if found.

    Args:
    word_to_search (str): The word to search for in audio files.
    """
    print(
        f"Entering process_and_search_audio_files with word_to_search='{word_to_search}' and cht_id={cht_id}")
    media_folder = './media/'
    wav_folder = './media/wav/'
    os.makedirs(wav_folder, exist_ok=True)
    await convert_ogg_mpeg_to_wav(media_folder, wav_folder)
    for filename in os.listdir(wav_folder):
        if filename.endswith('.wav'):
            wav_path = os.path.join(wav_folder, filename)
            result = await search_word_in_audio(wav_path, word_to_search)
            if result == 1:
                parts = filename.split('_')
                chat_id = parts[0]
                if int(chat_id) == int(cht_id):
                    message_id = parts[1].split('.')[0]
                    reply_message = f"ایناهاش🤝"
                    try:
                        await client.send_message(int(chat_id), reply_message, reply_to=int(message_id))
                    except ValueError as e:
                        print(f"Failed to send message: {str(e)}")
    print("Exiting process_and_search_audio_files")


async def download_audio_by_id(chat_id, data):
    """
    Asynchronously downloads an audio file by its ID from a specified chat.

    Args:
    chat_id (int): The ID of the chat from which the audio is to be downloaded.
    data (list): A list containing the message ID and the file extension of the audio to be downloaded.
    """
    print(
        f"Entering download_audio_by_id with chat_id={chat_id} and data={data}")
    try:
        message = await client.get_messages(entity=chat_id, ids=data[0])
        if message and message.media:
            file_path = f'./media/{chat_id}_{data[0]}.{data[1]}'
            if not os.path.exists(file_path):
                await client.download_media(message, file=file_path)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Exiting download_audio_by_id")


async def search_audio_files_in_chat(chat_id, size=50000):
    """
    Asynchronously searches for audio files in a chat that are smaller than a specified size.
    It collects the IDs of these audio messages and returns them.

    Args:
    chat_id (int): The ID of the chat where the search is performed.
    size (int): The maximum file size (in bytes) to include in the search.

    Returns:
    list: A list of audio message IDs and their respective formats that meet the criteria.
    """
    print(
        f"Entering search_audio_files_in_chat with chat_id={chat_id} and size={size}")
    audio_message_ids = []
    async for message in client.iter_messages(chat_id):
        if message.media:
            try:
                if isinstance(message.media, types.MessageMediaDocument):
                    if message.media.document.mime_type.startswith('audio'):
                        file_size = message.media.document.size
                        if file_size < size:
                            audio_message_ids.append(
                                [message.id, message.media.document.mime_type.split('/')[1]])
                            if len(audio_message_ids) > NTH_LAST_MESSAGE:
                                print("Exiting search_audio_files_in_chat")
                                return audio_message_ids
            except AttributeError:
                continue
    print("Exiting search_audio_files_in_chat")
    return audio_message_ids


async def handle_search_and_download_audio(message_text, chat_id):
    """
    This function processes a message from a given chat_id. It checks if the message matches a specific pattern.
    If the pattern is matched, it retrieves audio IDs from the chat, downloads each audio, and then processes the audios.
    """
    print(
        f"Entering handle_search_and_download_audio with message_text='{message_text}' and chat_id={chat_id}")
    if message_text.startswith("@") and "|" in message_text:
        print('pattern is ok')
        data, size = message_text[1:].split("|", 1)
        size = int(size)
        print('pattern is matched')
        audio_ids = await search_audio_files_in_chat(chat_id, size)
        if audio_ids:
            for audio_id in audio_ids:
                await download_audio_by_id(chat_id, audio_id)
        await process_and_search_audio_files(data, chat_id)
    print("Exiting handle_search_and_download_audio")


@client.on(events.NewMessage(outgoing=True))
async def log_outgoing_messages(event):
    """
    This event handler listens for outgoing messages. If the message is sent in a private chat,
    it extracts the chat ID and the message text, then processes the message to search and download audio files.
    """
    if event.is_private:
        chat_id = event.chat_id
        message_text = event.raw_text
        await handle_search_and_download_audio(message_text, chat_id)

with client:
    client.start()
    client.run_until_disconnected()
