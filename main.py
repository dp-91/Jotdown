import pyaudio
import wave
import speech_recognition as sr

def record_audio(output_filename, duration, sample_rate=44100, channels=1, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=channels,
                        rate=sample_rate, input=True,
                        frames_per_buffer=chunk)
    frames = []

    print("Recording...")
    for _ in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording finished")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

def audio_to_text(audio_filename, language="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from Speech Recognition service; {e}"

def main():
    output_filename = './Recordings/output.wav'
    duration = 0
    try:
        duration = float(input("Enter the duration in second(s) less than 30: "))
        print(f"Duration entered: {duration} second(s)")
    except ValueError:
        print("Invalid input. Please enter a valid number for the duration.")
    if (duration > 30):
        print("Invalid Length x > 30s, canceling application")
        return
    
    record_audio(output_filename, duration)

    # I mean might as well prompt both unless there's a specific use case to do one or the other?

    print("Transcribing to English...")
    text_en = audio_to_text(output_filename, language="en-US")
    print("Transcribed English Text:")
    print(text_en)

    print("Transcribing to Russian...")
    text_ru = audio_to_text(output_filename, language="ru-RU")
    print("Transcribed Russian Text:")
    print(text_ru)

if __name__ == "__main__":
    main()