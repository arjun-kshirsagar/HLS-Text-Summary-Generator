import time
from pydub import AudioSegment
import speech_recognition as sr

def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

def recognize_audio(wav_file):
    r = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        r.adjust_for_ambient_noise(source)
        print("Converting Audio File To Text...")
        audio = r.record(source)  # read the entire audio file
    return r.recognize_google(audio)

def main():
    mp3_file = "test.mp3"
    wav_file = "test.wav"

    # Convert MP3 to WAV
    convert_mp3_to_wav(mp3_file, wav_file)

    max_attempts = 3
    attempt = 1
    while attempt <= max_attempts:
        try:
            result = recognize_audio(wav_file)
            print("Converted Audio Is: \n" + result)
            break  # Break out of the retry loop if successful
        except sr.RequestError as e:
            print(f"Attempt {attempt}: Could not request results from Google Web Speech API; {e}")
        except sr.UnknownValueError:
            print(f"Attempt {attempt}: Google Web Speech API could not understand the audio")
        except Exception as e:
            print(f"Attempt {attempt}: An unexpected error occurred: {e}")
        
        attempt += 1
        time.sleep(2)  # Wait for 2 seconds before retrying

    if attempt > max_attempts:
        print(f"Failed to recognize audio after {max_attempts} attempts.")

if __name__ == "__main__":
    main()
