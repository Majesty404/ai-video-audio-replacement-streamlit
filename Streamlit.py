import streamlit as st
from openai import AzureOpenAI
from moviepy.editor import VideoFileClip, AudioFileClip
import os
from dotenv import load_dotenv
import warnings

load_dotenv('Api_Key.env')

client = AzureOpenAI(api_key = os.getenv('azure_api_key'),
                     azure_endpoint = os.getenv('azure_whisper_endpoint'),
                     api_version="2024-09-01-preview" )

def transcribe_audio_from_video(video_path):
    # Extract audio from the video
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)

    # Use OpenAI Whisper API for transcription
    transcription = transcribe_with_openai_whisper(audio_path)
    return transcription

def transcribe_with_openai_whisper(audio_path):
    # Open the audio file for transcription
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file,
        response_format='text'
    )
    return response

def correct_grammar(text):
    client = AzureOpenAI(
    api_key = os.getenv('azure_openai_api_key'),  
    api_version = "2024-02-01",
    azure_endpoint = os.getenv("azure_openai_endpoint")
    )

    prompt=f"Correct the following transcription and remove any filler words:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user",
             "content": [
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        max_tokens=2000,
        temperature=0.7,
    )
    return response.choices[0].message.content

def generate_audio(text):
    client = AzureOpenAI(api_key = os.getenv('azure_api_key'),
                     azure_endpoint =  os.getenv('azure_speech_service_endpoint'),
                     api_version="2024-09-01-preview" )
    response = client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input= text,
                response_format='mp3'
            )
    # Ignore DeprecationWarning
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    response.stream_to_file("new_audio.mp3")

def replace_audio_in_video(video_path, new_audio_path, output_path):
    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)
    final_video = video.set_audio(new_audio)
    final_video.write_videofile(output_path)

# Streamlit UI
st.title("AI Video Audio Replacement")
uploaded_video = st.file_uploader("Upload a video", type=["mp4", "mov"])

if uploaded_video is not None:
    st.info("Processing video...")
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_video.getbuffer())

    with st.status("Transcription in progress....."):
        transcription = transcribe_audio_from_video("input_video.mp4")
    st.write(f"Transcription: {transcription}")

    with st.status("Correction in progress....."):
        st.write("Removing filler words.......")
        st.write("Correcting Grammar....")
        corrected_text = correct_grammar(transcription)
    st.write(f"Corrected Text: {corrected_text}")

    bar = st.progress(0,text="Generating Video.....")
    generate_audio(corrected_text)
    bar.progress(25,text="Generating Video.....")

    new_audio_path = 'new_audio.mp3'
    bar.progress(50,text="Generating Video.....")
    bar.progress(75,text="Generating Video.....")

    replace_audio_in_video("input_video.mp4", new_audio_path, "final_output.mp4")
    bar.progress(100,text="Generating Video.....")
    bar.empty()

    st.info("Final Video")
    st.video("final_output.mp4")
    st.success("Audio replacement complete!")