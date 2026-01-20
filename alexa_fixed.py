import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import random
import sys

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 170)

def speak(text):
    print(f"🤖 Alexa: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening... Say 'Alexa' then command")
        while True:
            try:
                listener.adjust_for_ambient_noise(source, duration=0.3)
                audio = listener.listen(source, timeout=10, phrase_time_limit=5)
                command = listener.recognize_google(audio).lower()
                print(f"👤 You: {command}")
                
                if 'alexa' in command:
                    return command.replace('alexa', '').strip()
            except (sr.UnknownValueError, sr.WaitTimeoutError):
                continue
            except sr.RequestError:
                print("⚠️ Check internet connection")
                continue

def handle_command(cmd):
    if 'play' in cmd:
        song = cmd.replace('play', '').strip()
        speak(f'Playing {song}')
        pywhatkit.playonyt(song)
        
    elif 'time' in cmd:
        speak(f"It's {datetime.datetime.now().strftime('%I:%M %p')}")
        
    elif 'who is' in cmd or 'what is' in cmd:
        try:
            speak(wikipedia.summary(cmd, sentences=2))
        except:
            speak(f"Searching for {cmd}")
            webbrowser.open(f"https://en.wikipedia.org/wiki/{cmd.replace(' ', '_')}")
            
    elif 'joke' in cmd:
        speak(pyjokes.get_joke())
        
    elif any(word in cmd for word in ['stop', 'exit', 'quit']):
        speak("Goodbye!")
        sys.exit()
        
    elif 'open' in cmd:
        site = cmd.replace('open', '').strip()
        sites = {'youtube':'youtube.com', 'google':'google.com', 'github':'github.com'}
        url = sites.get(site, f'{site}.com')
        webbrowser.open(f'https://{url}')
        
    else:
        speak("Try: 'play song', 'time', 'joke', or 'open website'")

def main():
    speak("Hello! Say 'Alexa' then your command")
    while True:
        try:
            cmd = listen()
            if cmd:
                handle_command(cmd)
                print("\n✅ Ready...\n")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()