from google.cloud import speech_v1p1beta1 as speech
import io
from pydub import AudioSegment
from transformers import pipeline

# Function to convert MP3 to WAV
def convert_mp3_to_wav(mp3_file_path, wav_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format="wav")

# Function to transcribe audio to text using Google Cloud Speech-to-Text
def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    
    with io.open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    response = client.recognize(config=config, audio=audio)
    
    captions = ""
    for result in response.results:
        captions += result.alternatives[0].transcript + " "
    
    return captions

# Function to summarize text using Hugging Face's transformers
def summarize_text(text):
    summarizer = pipeline("summarization", model="google/pegasus-xsum")
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

# Main function to process the MP3 file
def process_mp3_file(mp3_file_path):
    wav_file_path = "converted_audio.wav"
    
    # Convert MP3 to WAV
    convert_mp3_to_wav(mp3_file_path, wav_file_path)
    
    # Transcribe audio to text
    transcription = transcribe_audio(wav_file_path)
    print("Transcription:\n", transcription)
    
    # Summarize the transcription
    summary = summarize_text(transcription)
    print("\nSummary:\n", summary)

# Example usage
mp3_file_path = "your_audio_file.mp3"  # Replace with your MP3 file path
process_mp3_file(mp3_file_path)
