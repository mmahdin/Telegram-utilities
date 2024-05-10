import speech_recognition as sr


def search_word_in_audio(audio_file, word_to_search):
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
            print(f"'{word_to_search}' found in audio.")
        else:
            print(f"'{word_to_search}' not found in audio.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            f"Could not request results from Google Speech Recognition service; {e}")


# Example usage
search_word_in_audio('test_fa.wav', 'تلگرام')
