import time
import os
from pycaw.pycaw import AudioUtilities, IMMNotificationClient
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.interfaces import IAudioEndpointVolume
from playsound import playsound
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

    def OnDeviceAdded(self, pwstrDeviceId):
        pass

    def OnDeviceRemoved(self, pwstrDeviceId):
        pass

    def OnDeviceStateChanged(self, pwstrDeviceId, dwNewState):
        pass

    def OnPropertyValueChanged(self, pwstrDeviceId, key):
        pass

    def play_audio(self, file_path):
        """Plays the given audio file."""
        print(f"Playing: {file_path}")
        playsound(file_path)

    def monitor_devices(self):
        """Continuously monitors device changes."""
        print("Monitoring audio devices...")
        while self.running:
            time.sleep(1)  # Keep the loop running

    def stop_monitoring(self):
        """Stops the monitoring loop."""
        self.running = False


def main():
    # Paths to audio files
    internal_audio = "internal_audio.mp3"  # Path to internal audio file
    external_audio = "external_audio.mp3"  # Path to external audio file

    # Ensure audio files exist
    if not os.path.exists(internal_audio) or not os.path.exists(external_audio):
        print("Error: Audio files not found. Ensure 'internal_audio.mp3' and 'external_audio.mp3' are in the same directory.")
        return

    # Initialize the audio manager
    audio_manager = AudioDeviceManager(internal_audio, external_audio)

    # Start monitoring devices
    try:
        audio_manager.monitor_devices()
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        audio_manager.stop_monitoring()


if __name__ == "__main__":
    main()
