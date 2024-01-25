
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import webbrowser
import datetime
import wikipedia
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('ELEVENLABS_API_KEY')
print(api_key)
#hear the microphone
def transform_audio_into_text():
    r = sr.Recognizer()
    with sr.Microphone(3) as source:
        r.pause_threshold = 0.8
        #report that the recording has begun
        print("You can now speak")

        #save what you hear
        audio = r.listen(source)

        try:
            #search on google
            request = r.recognize_google(audio, language="en-us")
            #test in text
            print("You said "+ request)

            #return request
            return request
        #In case it doesn't accept audio
        except sr.UnknownValueError:
            #show proof that it didn't understand audio
            print("I didn't understand the audio")
            #return error
            return "I am still waiting"
        #In case the request cannot be resolved
        except sr.RequestError:
            print("There is no service")
            return "I am still waiting"
        #Unexpected error
        except:
            # show proof that it didn't understand audio
            print("Something went wrong")
            # return error
            return "I am still waiting"
#function so that the assistant can be heard
def speak(message):
    # start the engine of pyttsx3
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
#inform day of the week
def ask_day():
    #create a variable with todays information
    day = datetime.date.today()
    print(day)

    #create variable for day of the week
    week_day = day.weekday()
    print(week_day)
    #Names of days
    calendar = { 0:"Monday",
                 1:"Tuesday",
                 2:"Wednesday",
                 3:"Thursday",
                 4:"Friday",
                 5:"Saturday",
                 6:"Sunday",}
    #say the day of the week
    speak(f"Today is {calendar[week_day]}")
#inform what time it is
def ask_time():
    #Variable with time information
    time = datetime.datetime.now()
    time = f"At this moment it is {time.hour} hours and {time.minute} minutes"
    print(time)
    #Say the time
    speak(time)
#Create initial greeting
def initial_greeting():
    #say greeting
    speak("Hello I am Batman, Because I'm Batman, How can I help you today?")
#Main function of the assistant
def my_assistant():
    # Activate the initial greeting:
    initial_greeting()
    #cut off variable
    go_on = True
    while go_on:

        #Activating the microphone and save request
        my_request = transform_audio_into_text().lower()
        if "open youtube" in my_request:
            speak("Sure, I'm opening Youtube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "open browser" in my_request:
            speak("Of course, I'll get right to it")
            webbrowser.open("https://www.google.com")
            continue
        elif "what day" in my_request:
            ask_day()
            continue
        elif "what time" in my_request:
            ask_time()
            continue
        elif "do a wikipedia search for" in my_request:
            speak("I am looking for it Batman")
            my_request = my_request.replace("do a wikipedia search for","")
            answer = wikipedia.summary(my_request, sentences = 1)
            speak(f"According to wikipedia: ")
            speak(answer)
            continue
        elif "rap" in my_request:
            with open("skrhaa.txt") as file:
                data = file.readlines()
            for i in range(len(data)):
                speak(data[i])

        elif "tell me" in my_request:
            speak("right away, good sir")
            my_request = my_request.replace("tell me", "")
            pywhatkit.search(my_request)
            speak("this is what i found, Batman")
        elif "play" in my_request:
            speak("Oh, amazing taste indeed Batman! I'll play it for you right away.")
            pywhatkit.playonyt(my_request)
            continue
        elif "joke" in my_request:
            speak(pyjokes.get_joke())
            continue
        elif "bye" in my_request:
            speak("Going to rest, let me know if you need anything")
            break
my_assistant()