from langdetect import detect
import moviepy.editor as mp
import speech_recognition as sr
import os
from speech_recognition import UnknownValueError

def detect_language(text):
    detected_language = detect(text)
    return detected_language

def fetch_transcribe(video_path):
    print("video path=-------", video_path)
    # Load the video file
    clip = mp.VideoFileClip(video_path)
    print("clip----", clip)
    # Initialize recognizer
    r = sr.Recognizer()
    print("r==============", r)
    r.energy_threshold = 4000
    # Define output file paths
    english_output_file = "english_textfile.txt"
    hindi_output_file = "hindi_textfile.txt"

    # Extract audio from the entire video
    audio = clip.audio

    # Define duration of audio segments (in seconds)
    segment_duration = 10 # Adjust as needed

    # Split audio into segments and transcribe each segment
    for i, start_time in enumerate(range(0, int(audio.duration), segment_duration)):
        # Define end time for the segment
        end_time = min(start_time + segment_duration, int(audio.duration))

        # Extract the segment of audio
        segment = audio.subclip(start_time, end_time)

        # Save the audio segment as a temporary WAV file
        temp_audio_path = f"temp_audio_{i}.wav"
        segment.write_audiofile(temp_audio_path)

        # Transcribe the audio to text
        try:
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = r.record(source)
        except sr.UnknownValueError:
            print(f"Segment {i + 1}: Unable to recognize speech. Skipping...")
            os.remove(temp_audio_path)
            continue

        # Determine the language of the audio using langdetect library
        try:
            detected_language = detect_language(r.recognize_google(audio_data))
            print("detected language", detected_language)
        except UnknownValueError:
            print(f"Segment {i + 1}: Unable to determine language. Skipping...")
            os.remove(temp_audio_path)
            continue

        # Append transcript to the respective text file
        if detected_language == "hi":
            output_file = hindi_output_file
        elif detected_language == "en":
            output_file = english_output_file
        else:
            # Do not transcribe audio in other languages
            print(f"Segment {i + 1}: Audio language other than English or Hindi. No transcription performed.")
            os.remove(temp_audio_path)
            continue

        with open(output_file, "a", encoding="utf-8") as file:
            audio_text = r.recognize_google(audio_data, language="hi-IN" if detected_language == "hi" else "en-US")
            file.write(audio_text + "\n")
            print(f"Segment {i + 1}: Transcription appended to {output_file}")

        # Clean up temporary audio file
        os.remove(temp_audio_path)
    print("Transcription completed.")

