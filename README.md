# AI Video Audio Replacement

This project is an AI-powered tool that allows users to replace the audio in a video by transcribing the original audio, correcting it, and generating new audio using Azure OpenAI. The application is built using Python, Streamlit for the UI, and integrates Azure OpenAI's Whisper, GPT, and TTS models.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Approach](#approach)
- [License](#license)

## Features
- Extract audio from a video.
- Transcribe audio using Azure OpenAI Whisper API.
- Correct transcription by removing filler words and fixing grammar.
- Generate new audio using Azure TTS (Text-to-Speech).
- Replace the original audio in the video with the new synthesized audio.
- Simple and interactive web interface using Streamlit.

## Requirements
The project requires the following Python packages:
- `streamlit`
- `openai`
- `moviepy`
- `python-dotenv`
- `azure-cognitiveservices-speech`

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Majesty404/ai-video-audio-replacement-streamlit.git
    cd ai-video-audio-replacement
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the project root directory and add your Azure API keys:
    ```plaintext
    azure_api_key=your_azure_api_key_here
    azure_whisper_endpoint=https://your_whisper_endpoint
    azure_openai_api_key=your_openai_key_here
    azure_openai_endpoint=https://your_openai_endpoint
    azure_speech_service_endpoint=https://your_speech_service_endpoint
    ```

## Environment Variables
Make sure your `.env` file contains the correct environment variables:
- `azure_api_key`: Your Azure API key for authentication.
- `azure_whisper_endpoint`: Endpoint URL for Azure OpenAI Whisper API.
- `azure_openai_api_key`: API key for Azure OpenAI to correct transcription.
- `azure_openai_endpoint`: Endpoint URL for Azure OpenAI services.
- `azure_speech_service_endpoint`: Endpoint URL for Azure Speech Services.

## Usage
1. Run the application:
    ```bash
    streamlit run app.py
    ```

2. Upload a video file (`.mp4`, `.mov`) through the web interface.
3. The application will process the video by transcribing the audio, correcting it, generating new audio, and replacing the original audio with the new one.
4. Download the final video with the updated audio.

## Approach

The process follows several key steps:

1. **Extract Audio**: The video file's audio is extracted and saved as a temporary `.wav` file using `moviepy`.
2. **Transcription**: The audio file is sent to the Azure OpenAI Whisper API to transcribe the spoken content into text.
3. **Text Correction**: The transcribed text may contain filler words or grammatical issues. It is processed through Azure OpenAI's GPT model to correct these issues and improve readability.
4. **Generate New Audio**: The corrected text is converted into a new audio file using Azure Cognitive Services' Text-to-Speech (TTS) feature. The new audio is saved as an `.mp3` file.
5. **Replace Original Audio**: Using `moviepy`, the original video file's audio is replaced with the newly generated audio. This final video is then saved as an output file.
6. **User Interface**: The application uses Streamlit for a user-friendly web interface, allowing users to upload videos, monitor the process, and download the final output.

### Code Flow:
- **Streamlit UI**: The user uploads a video file, which triggers the processing workflow.
- **Extract Audio**: `transcribe_audio_from_video(video_path)` extracts the audio.
- **Transcription**: `transcribe_with_openai_whisper(audio_path)` calls the Azure Whisper API to convert the audio into text.
- **Correction**: `correct_grammar(text)` uses Azure GPT to clean and correct the transcription.
- **Generate Audio**: `generate_audio(text)` creates new audio from the corrected text using Azure TTS.
- **Replace Audio**: `replace_audio_in_video(video_path, new_audio_path, output_path)` integrates the new audio into the original video.

## License
Currently, there is no license file available for this project.

---

Feel free to customize the README as needed, especially under sections like "Features" and "Usage," depending on how the project is meant to be used.