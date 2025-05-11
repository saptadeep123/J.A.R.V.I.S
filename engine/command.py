import pyttsx3
import speech_recognition as sr
import eel
import time




def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)  
    engine.setProperty('volume', 1)
    eel.DisplayMessage(text) 
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    earbuds_index = 14  # Index of your earbuds
    try:
        with sr.Microphone(device_index=earbuds_index) as source:
            r.adjust_for_ambient_noise(source, duration=2)
            print("Listening...")
            eel.DisplayMessage('Listening...')
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=6)
                print("Recognizing...")
                eel.DisplayMessage('Recognizing...')
                querry = r.recognize_google(audio, language='en-in')
                print(f"User said: {querry}")
                eel.DisplayMessage(querry)
                time.sleep(1)
                return querry.lower()
            except sr.WaitTimeoutError:
                print("Listening timed out. Please try again.")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
    except AssertionError as e:
        print("Microphone initialization failed:", e)
    except AttributeError as e:
        print("Microphone stream issue:", e)
    return ""

@eel.expose
def send_message_content(message, contact_no, name):
    from engine.features import whatsapp
    whatsapp(contact_no, message, "message", name)
    return {"status": "completed"}

@eel.expose
def takeallCommands(message=None):
    try:
        if not message:  # If no message provided, use voice command
            querry = takecommand()
            print("Voice command:", querry)
            eel.senderText(querry)
        else:  # Use the provided text message
            querry = str(message).lower()
            eel.senderText(querry)
            print("Text command:", querry)

        # Process the command
        if "open" in querry:
            from engine.features import openCommand  
            openCommand(querry)
        elif "on youtube" in querry:
            from engine.features import PlayYoutube
            PlayYoutube(querry)
        elif any(cmd in querry for cmd in ["send message", "phone call", "video call"]):
            from engine.features import findcontacts, whatsapp
            contact_no, name = findcontacts(querry)
            if contact_no != 0:
                if "send message" in querry:
                    if message:  # If coming from text input
                        whatsapp(contact_no, querry.replace("send message", "").strip(), "message", name)
                    else:  # If voice command
                        speak("What message to send?")
                        msg = takecommand()
                        whatsapp(contact_no, msg, "message", name)
                        return {"status": "completed"}  # Return immediately after sending
                elif "phone call" in querry:
                    whatsapp(contact_no, querry, "call", name)
                else:
                    whatsapp(contact_no, querry, "video call", name)
        else:
            from engine.features import chatbot
            chatbot(querry)
            
    except Exception as e:
        print(f"Error in takeallCommands: {str(e)}")
        speak("Sorry, I encountered an error")
    
    eel.showHood()
    return {"status": "completed"}  # Return a response to frontend


