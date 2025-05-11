import speech_recognition as sr

# List all audio input devices and their indices
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Device Index {index}: {name}")


try:
    with sr.Microphone(device_index=27) as source:
        print("Microphone initialized successfully.")
except Exception as e:
    print(f"Error initializing microphone: {e}")
