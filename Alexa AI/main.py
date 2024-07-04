import speech_recognition as sr
import webbrowser 
import pyttsx3
import musicLibrary
from openai import OpenAI

recognizer = sr.Recognizer()
engine= pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Choose a female voice (if available)
engine.setProperty('voice', voices[1].id) 

def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
    client = OpenAI(api_key="sk-proj-LuRD262Iv82Dv4PTQVl1T3BlbkFJoi3XnpqFUI7Jn53mAA8W",
)


    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant, skilled as alexa , google cloud"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


    
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    
    else:
        #let openAI handle this case
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Alexa.....")
    while True:
        r = sr.Recognizer()
        
        print("recognizing.....")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source , timeout=2 , phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "alexa"):
                speak("Yes sir")

                #listen for command
                with sr.Microphone() as source:
                    print("Alexa active....")
                    audio = r.listen(source , timeout=2 , phrase_time_limit=1)
                    command = r.recognize_google(audio)

                    processCommand(command)
        

        except Exception as e:
            print("Error ;{0}".format(e))