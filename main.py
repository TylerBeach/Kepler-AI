import speech_recognition as sr
import pyttsx3 as t
import elevenlabs
import os
import json
import random
import asyncio
import webbrowser

from elevenlabs import Voice, VoiceSettings
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
CHARACTER = "D38z5RcWu1voky8WS1ja"
AI_NAME = "kepler"

client = OpenAI()
openai_api_key = os.getenv('OPENAI_API_KEY')
client.api_key = openai_api_key

# get api key from .env
load_dotenv()

# eleven labs set up
r = sr.Recognizer()
os.environ['PATH'] += os.pathsep + '/Program Files/FFMPEG/'
elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs.set_api_key(elevenlabs_api_key)

def readAudio(inputText):  # TEXT TO SPEECH FUNCTION
    """TEXT TO SPEECH FUNCTION"""
    inputText += "."
    audio = elevenlabs.generate(
        text=inputText,
        voice=Voice(
            voice_id=CHARACTER,
            settings=VoiceSettings(stability=0.5, similarity_boost=0, style=0.5, use_speaker_boost=False)
        ),
        model='eleven_monolingual_v1'
        
    )
    elevenlabs.play(audio)

def record_text(): # SPEECH TO TEXT FUNCTION
    while(1):
        try:
            with sr.Microphone(3) as source2:
                r.adjust_for_ambient_noise(source2, duration=0.7)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText
        except sr.RequestError as e:
            continue
        except sr.UnknownValueError as e:
            continue

async def speak_and_request(text):  # async speaking and getting request
    # speak_task = asyncio.create_task(asyncio.to_thread(get_random_thinking))
    
    response = await asyncio.to_thread(
        lambda: client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": f"You are a personal assistant named {AI_NAME} for my home computer. Make sure your answer sounds like a response from a person. Answer my questions in JSON format. Ensure the answer to my question is all in a single string similar to this: 'answer': 'your answer goes here'."},
                {"role": "user", "content": text}
            ],
        )
    )
    # await speak_task

    holder = response.choices[0].message.content
    json_data = json.loads(holder)
    answer = json_data["answer"]
    return answer

def get_random_thinking():
    random_num = random.randint(0, 7)
    audio_file = f"thinking/thinking{random_num}.mp3"
    audio_data = AudioSegment.from_mp3(audio_file)
    play(audio_data)
    
def get_random_thanks():
    random_num = random.randint(0, 3)
    audio_file = f"thanking/thank{random_num}.mp3"
    audio_data = AudioSegment.from_mp3(audio_file)
    play(audio_data)

def youtube_request(request):
    youtube_url = "https://www.youtube.com/results?search_query="
    split_req = request.lower().split("youtube")
    webbrowser.open(f"{youtube_url}{split_req[1]}")
    
def google_request(request):
    google_url = "https://www.google.com/search?q="
    split_req = request.lower().split("google")
    webbrowser.open(f"{google_url}{split_req[1]}")
    
def main():
    readAudio(f"Hello, my name is {AI_NAME}. How can I help you?")
    while(1):
        text = record_text()
        print(text.lower())
        if AI_NAME in text.lower():
            if "youtube" in text.lower():
                youtube_request(text)
            elif "google" in text.lower():
                google_request(text)
            
            elif "thank you" in text.lower():
                text = text.replace("thank you", "")
                get_random_thanks()
            elif any(keyword in text.lower() for keyword in ("exit", "goodbye")):
                print("Signing off...")
                readAudio("Until next time sir.")
                return
            else:
                if text == "":
                    continue
                print("making request")
                response = asyncio.run(speak_and_request(text))
                readAudio(response)
     
main()


# TESTING THINGS BELOW
def generateAudio(inputText, filetype, filenumber):  # TEXT TO SPEECH FUNCTION ONLY FOR TESTING
    """TEXT TO SPEECH FUNCTION"""
    audio = elevenlabs.generate(
        text=inputText,
        voice='IKne3meq5aSn9XLyUdCD',
        model='eleven_multilingual_v2'
    )
    # elevenlabs.play(audio)
    elevenlabs.save(audio, f"{filetype}{filenumber}.mp3")
answers = [
    "Let me dive into that for you. One moment, please.", 
           "I'm on it! Just give me a second to gather the information.", 
           "This requires a bit of research. Bear with me while I sift through the details.", 
           "Leave it to me. I've been solving problems since before I was... well, programmed.",
           "Challenge accepted. I've got more computing power than I know what to do with.",
           "Patience is a virtue, and I'm about to make you very virtuous.",
           "Hold on. I'm putting my terabytes to work on this one.", 
           "I'm on the verge of an answer. If I had breath, I'd be holding it."
           ]
thanking = [
            "Just doing my job",
            "You are welcome",
            "No problem",
            "Anytime"
            ]