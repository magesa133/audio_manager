import time
import os
from pycaw.pycaw import AudioUtilities, IMMNotificationClient
from ctypes import POINTER
from comtypes import CLSCTX_ALL
import pygame
import threading

class AudioDeviceManager(IMMNotificationClient):
    def __init__(self, internal_audio, external_audio):
        self.internal_audio = internal_audio
        self.external_audio = external_audio
        self.device_count = len(AudioUtilities.GetAllDevices())
        self.running = True

    def OnDefaultDeviceChanged(self, flow, role, default_device_id):
        """Triggered when the default device changes."""
        devices = AudioUtilities.GetAllDevices()
        new_device_count = len(devices)

        if new_device_count > self.device_count:
            print("Headset connected!")
            threading.Thread(target=self.play_audio, args=(self.external_audio,)).start()
        elif new_device_count < self.device_count:
            print("Headset disconnected!")
            threading.Thread(target=self.play_audio, args=(self.internal_audio,)).start()

        self.device_count = new_device_count

    def play_audio(self, file_path):
        """Plays the given audio file."""
        print(f"Playing: {file_path}")
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def monitor_devices(self):
        """Continuously monitors device changes."""
        print("Monitoring audio devices...")
        while self.running:
            time.sleep(1)

    def stop_monitoring(self):
        """Stops the monitoring loop."""
        self.running = False


def main():
    # Paths to audio files
    internal_audio = "internal_audio.mp3"
    external_audio = "external_audio.mp3"

    if not os.path.exists(internal_audio) or not os.path.exists(external_audio):
        print("Error: Audio files not found.")
        return

    audio_manager = AudioDeviceManager(internal_audio, external_audio)

    try:
        audio_manager.monitor_devices()
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        audio_manager.stop_monitoring()


if __name__ == "__main__":
    main()
