from playsound import playsound

try:
    playsound("internal_audio.mp3")  # Replace with the path to your file
    print("Audio played successfully!")
except Exception as e:
    print(f"Error: {e}")
