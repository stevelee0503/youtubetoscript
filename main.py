from pytube import YouTube
from moviepy.editor import *
import openai
import os

API_KEY = 'YOUR_API_KEY '


def extract_audio(url, output_file):
    # Download the YouTube video
    video = YouTube(url)
    audio_stream = video.streams.filter(only_audio=True).first()
    audio_stream.download(output_path='./')

    # Convert the audio file to MP3
    input_file = './' + audio_stream.default_filename
    audio_clip = AudioFileClip(input_file)
    audio_clip.write_audiofile(output_file)

    # Remove the original audio file
    os.remove(input_file)


def youtube_to_script(url, output_file):
    # First, set your OpenAI API key as an environment variable
    os.environ["OPENAI_API_KEY"] = API_KEY

    # Create the OpenAI API client
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Extract the audio from the YouTube video
    extract_audio(url, 'audio.mp3')

    # Open the audio file
    file = open("audio.mp3", "rb")

    # Transcribe the audio file
    transcription = openai.Audio.transcribe("whisper-1", file)

    # Write the transcription to a file
    with open(output_file, "w") as file:
        file.write(transcription['text'])


def main():
    url = input('Enter the URL of the YouTube video: ')
    youtube_to_script(url, 'script.txt')

    with open('script.txt', "r") as file:
        content = file.read()
        print(f"The extracted script is : {content}")


if __name__ == '__main__':
    main()
