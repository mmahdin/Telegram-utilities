# Audio Search User Bot (New Feature)

## Overview
This repository contains the code for the new feature of the Audio Search Bot. The previous version can be found in the `python_v1` folder. The bot is written in Python and is currently command-line based, with plans to incorporate a GUI in C++ for Linux and potentially for Android in the future. The repository is actively being developed, with interesting features being added every week.

## Main Features
The main feature of this new version is the ability to search for a word or phrase within audio files in a private chat. Users can initiate a search by sending a specific message format in the chat. Here's how it works:

### Search Format
To search for a word or phrase in the audio files of a private chat, send the following message:

@telegram|30000


### Search Criteria
- **Word or Phrase**: Replace "telegram" with the word or phrase you want to search for within the audio files.
- **File Size Limit**: Specify the maximum size of audio files to be searched in bytes. In this example, the limit is set to 30,000 bytes.

### Search Process
When the bot receives the search message, it scans the 10 most recent audio files in the chat, each with a size less than the specified limit. If any of the audio files contain the specified word or phrase, the bot will reply with the corresponding messages.




# Telegram-ghost (Latest Version)
Python-based GUI for staying hidden in Telegram

## With this application, you can perform the following actions without anyone knowing:
* View messages from personal chats and groups!
* Send messages to personal chats and groups!
* Download and view any files and media from personal chats and groups!
* Send any files and media to personal chats and groups!
* View profile photos and save them!
* Save text messages from personal chats and groups to a .txt file!
* Specify the maximum size of files for downloading!


## Example

	

https://user-images.githubusercontent.com/82968741/211257490-bc0237e2-ecc2-4707-acfd-63d604f8b391.mp4


	
## Setup
```
$ pip install Telethon
$ pip install PySide6
$ pip install functools
$ pip install pygame
$ pip install asyncio
$ pip install moviepy
$ pip install subprocess.run
```
