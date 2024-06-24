from google.cloud import speech_v1p1beta1 as speech
import io

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
