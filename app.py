import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyttsx3
from characterai import PyCAI
from pydub import AudioSegment
from pydub.playback import play
import argparse
import json

# Installing FFmpeg: https://phoenixnap.com/kb/ffmpeg-windows

def initVar():
    global CAI
    global CAI_client
    global EL

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
    except:
        print("Unable to open JSON file.")
        exit()

    class CAI:
        token = data["CAI_data"][0]["token"]
        character = data["CAI_data"][0]["character"]

    if CAI.token:
        CAI_client = PyCAI(CAI.token)

    class EL:
        key = data["EL_data"][0]["EL_key"]
        voice = data["EL_data"][0]["voice"]



def speech_to_text():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Recording voice...")
        audio_text = r.listen(source)
        print("------------------------------------------------------")
        
        try:
            user_statement = r.recognize_google(audio_text)
            print("User: " + user_statement)
            print("")
            return user_statement
        except:
            print("Sorry, I did not get that")
            return "..."



def text_to_personality_text_GPT(user_statement):
    class ChromeDriverSingleton:
        _instance = None

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                cls._instance = cls._create_instance()
            return cls._instance

        @classmethod
        def _create_instance(cls):
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # Run Chrome in headless mode
            #options.add_argument('--disable-gpu')  # Disable GPU acceleration
            options.add_argument('--no-sandbox')  # Bypass OS security model
            options.add_argument('--disable-dev-shm-usage')  # Disable "DevShmUsage" flag
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            return webdriver.Chrome(options=options)

    driver = ChromeDriverSingleton.get_instance()
    driver.get("https://chat.chatgptdemo.net/")
    time.sleep(2) 
    textarea = driver.find_element(By.ID, "input-chat")
    personality_AJ = "(You have the personality of a skeptical conspiracy theorist, akin to Alex Jones. Respond to the following statement in 50 words or less.)"
    personality_IM = "(You have a personality of someone who believes that the ends always justify the means. As such, you are pragmatic and utterly ruthless. You are also incredibly stubborn and dogmatic, always convinced that you're right and never considering for a second that there's anything wrong with your methods. Respond to the following statement by responding in 50 words or less.)"
    textarea.send_keys(personality_AJ + " " + user_statement) 
    time.sleep(1.5)
    textarea.send_keys(Keys.RETURN)
    time.sleep(4)

    try:
        response = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        print("Response: " + response.text)
        print("")
        return response.text
    finally:
        driver.quit()



def text_to_personality_text_CAI(user_statement):
    chat = CAI_client.chat.get_chat(CAI.character)

    history_id = chat['external_id']
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']
    
    data = CAI_client.chat.send_message(
        CAI.character,
        user_statement,
        history_external_id=history_id,
        tgt=tgt
    )

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    print(f"{name}: {text}")
    print("")

    return text
        


def text_to_speech_EL(text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{EL.voice}'
    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': EL.key,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'voice_settings': {
            'stability': 0.75,
            'similarity_boost': 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data, stream=True)
    audio_content = AudioSegment.from_file(io.BytesIO(response.content), format="mp3")
    play(audio_content)



def text_to_speech_PYTTS(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id) # voices[1].id for female, voices[0].id for male

    engine.say(text)
    engine.runAndWait()


def main(args):
    text_to_text_method = args.ttt
    text_to_speech_method = args.tts
    
    user_statement = speech_to_text()
    character_response = "..."

    if text_to_text_method == 'gpt':
        character_response = text_to_personality_text_GPT(user_statement)
    else:
        character_response = text_to_personality_text_CAI(user_statement)
    
    if text_to_speech_method == 'pyttsx3':
        text_to_speech_PYTTS(character_response)
    else:
        text_to_speech_EL(character_response)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()  

    # pipeline methods
    parser.add_argument("--ttt", default="gpt", choices=['gpt', 'cai'], help="text-to-text method, [gpt, cai]")
    parser.add_argument("--tts", default="pyttsx3", choices=['pyttsx3', 'el'], help="text-to-speech method, [pytts, el]")
    parser.add_argument("--repeat", action="store_true", help="the app only terminates on command")

    args = parser.parse_args()

    initVar()
    
    if args.repeat:
        while True:
            main(args)
    else:
        main(args)
