import pyttsx3

def list_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    for idx, voice in enumerate(voices):
        print(f"Voice {idx + 1}:")
        print(f" - ID: {voice.id}")
        print(f" - Name: {voice.name}")
        print(f" - Languages: {voice.languages}")
        print(f" - Gender: {voice.gender}")
        print()

if __name__ == "__main__":
    list_available_voices()
