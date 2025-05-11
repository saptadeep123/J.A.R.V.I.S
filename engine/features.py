import os
import re
from shlex import quote
import sqlite3
import subprocess
import webbrowser
from playsound import playsound
import eel
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
from hugchat import hugchat

from engine.helper import extract_yt_term, removewords

conn = sqlite3.connect("jarvisnew.db")
cursor = conn.cursor()

#playing assistent sound function
@eel.expose
def playassistentsound():
    music_dir ="frontend\\assets\\vendors\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

#making the hotword feature...
import struct
import time
import pvporcupine
import pyaudio


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

#finding contacts
def findcontacts(querry):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    querry = removewords(querry,words_to_remove)
    try:
        querry =querry.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE? OR LOWER(name) LIKE?",('%' +querry+ '%',querry+ '%'))
        result = cursor.fetchall()

        print(result[0][0])
        mobile_no_str = str(result[0][0])
        if not mobile_no_str.startswith('+91'):
            mobile_no_str = '+91' + mobile_no_str

        return mobile_no_str,querry
    except:
        speak('not exist in contacts')
        return 0,0
    
#whatsapp function main
import subprocess
import time

import pyautogui



def whatsapp(mobile_no, message, flag, name):
    # Button Coordinates (adjust if needed)
    SEND_BUTTON = (1871, 1044)  # (x,y) of send button
    CALL_BUTTON = (1804, 1104)  # (x,y) of call button
    VIDEO_BUTTON = (1732, 1074) # (x,y) of video button

    # 1. Open WhatsApp with contact
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={quote(message)}"
    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
    time.sleep(8)  # Increased wait for slow systems

    # 2. Force focus on WhatsApp (critical!)
    try:
        win = pyautogui.getWindowsWithTitle("WhatsApp")[0]
        win.activate()
        win.maximize()  # Ensures buttons are visible
        time.sleep(2)
    except Exception as e:
        print(f"Window focus error: {e}")

    # 3. Navigate to contact
    pyautogui.hotkey('ctrl', 'f')  # Open search
    time.sleep(1)
    pyautogui.write(name)          # Type name
    time.sleep(1)
    pyautogui.press('enter')       # Select contact
    time.sleep(3)  # Wait for chat to fully load

    # 4. CLICK THE BUTTON (with failsafe)
    try:
        if flag == 'message':
            pyautogui.click(SEND_BUTTON[0], SEND_BUTTON[1], clicks=2, interval=0.5)
            jarvis_message = f"Message sent to {name}"
        elif flag == 'call':
            pyautogui.click(CALL_BUTTON[0], CALL_BUTTON[1], clicks=2, interval=0.5)
            jarvis_message = f"Calling {name}"
        elif flag == 'video call':
            pyautogui.click(VIDEO_BUTTON[0], VIDEO_BUTTON[1], clicks=2, interval=0.5)
            jarvis_message = f"Video calling {name}"
        
        speak(jarvis_message)
    except Exception as e:
        speak(f"Failed to click button. Error: {str(e)}")
        print(f"Debug: Current mouse position: {pyautogui.position()}")


#chatbot
def chatbot(querry):
    input = querry.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(input)
    print(response)
    speak(response)
    return response










    
    

