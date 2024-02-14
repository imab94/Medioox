import pyttsx3
import re
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub import AudioSegment
from pydub.utils import mediainfo

# Set the path to ffprobe executable
os.environ["PATH"] += os.pathsep + r"\ffmpeg-master-latest-win64-gpl-shared\ffmpeg-master-latest-win64-gpl-shared\bin"

def merge_audio_files(audio_files, output_file):
    # Load each audio file
    segments = [AudioSegment.from_file(file) for file in audio_files]

    # Add a brief silence between segments (adjust duration as needed)
    silence = AudioSegment.silent(duration=1000)  # 1 second silence
    combined = silence

    # Concatenate audio segments with silence in between
    for segment in segments:
        combined += segment + silence
    # Export the combined audio to the output file
    combined.export(output_file, format="mp3")

def text_to_speech(text, file_path, voice_gender):
    engine = pyttsx3.init()

    # Set voice properties based on gender
    if voice_gender == 'female':
        engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Index 1 corresponds to a female voice
    else:
        engine.setProperty('voice', engine.getProperty('voices')[0].id)  # Use the default (male) voice

    engine.setProperty('rate', 190)  # You can experiment with different values
    engine.setProperty('volume', 0.9)  # Adjust volume (0.0 to 1.0)
    engine.save_to_file(text, file_path)
    engine.runAndWait()

def process_conversation(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    conversation = []
    current_speaker = None
    current_message = ""

    for line in lines:
        #match = re.match(r'\(\s*\d+h?\s*\d+m\s*\d+s\s*\)\s*([\w\s]+):\s*(.*)', line)
        match = re.match(r'\(\s*(?:(\d+h?)\s*)?(?:(\d+m)\s*)?(\d+s)\s*\)\s*([\w\s]+):\s*(.*)', line)

        # print("match------",match)
        if match:
            groups = match.groups()
            speaker = groups[-2]
            message = groups[-1]
            if current_speaker:
                conversation.append((current_speaker, current_message))
            current_speaker = speaker
            current_message = message
        else:
            current_message += line.strip()


    if current_speaker:
        conversation.append((current_speaker, current_message))

    return conversation

def main(uploaded_file):
    conversation_file = uploaded_file
    output_folder = 'audio_files'
    final_audio_folder = 'final_audio'
    merged_output_file = 'merged_audio.mp3'
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(final_audio_folder,exist_ok=True)
    conversation = process_conversation(conversation_file)
    for index, (speaker, message) in enumerate(conversation, start=1):
        # Determine voice gender based on the speaker
        voice_gender = 'female' if speaker.lower() == 'robin j' else 'male'
        # Generate output file path
        output_file = os.path.join(output_folder, f'{index}_{speaker.lower()}.mp3')
        # Convert text to speech
        text_to_speech(message, output_file, voice_gender)
        # Get a list of all generated audio files
    audio_files = [os.path.join(output_folder, f'{index}_{speaker.lower()}.mp3') for index, (speaker, _) in enumerate(conversation, start=1)]
    # Merge the audio files
    merge_audio_files(audio_files, os.path.join(final_audio_folder, merged_output_file))
        
if __name__ == "__main__":
    main()
