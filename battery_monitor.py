import psutil
import time
import pygame
import threading
from plyer import notification
import logging
import os
import sys

# Path for the .wav file, whether in the current directory or extracted by PyInstaller
def get_wav_path():
    if getattr(sys, 'frozen', False):  # Check if the script is running as an executable
        # Get the path to the temporary folder where PyInstaller extracts files
        return os.path.join(sys._MEIPASS, 'warning.wav')
    else:
        # Return the path for non-bundled versions of the script
        return os.path.join(os.path.dirname(__file__), 'warning.wav')

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Global flags to control sound and notifications
sound_playing = False
stop_sound = False
show_notification = True

# Set up logging for debugging
logging.basicConfig(
    filename="battery_monitor.log",
    level=logging.DEBUG,  # Use DEBUG to capture more details
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to clear the log file
def clear_log_file():
    try:
        with open("battery_monitor.log", "w"):  # Opens the file in write mode to clear its contents
            pass
        logging.info("Log file cleared.")
    except Exception as e:
        logging.error("Error clearing log file: %s", e)

# Function to play sound repeatedly
def play_sound_repeatedly():
    global stop_sound
    try:
        sound = pygame.mixer.Sound(get_wav_path())  # Load the sound from the correct path
        while not stop_sound:
            logging.debug("Playing warning sound.")
            sound.play()
            time.sleep(1)  # Wait 1 second before playing the sound again
    except Exception as e:
        logging.error("Error in play_sound_repeatedly: %s", e)

# Function to show notifications repeatedly
def show_persistent_notification():
    global show_notification
    try:
        while show_notification:
            logging.debug("Showing persistent notification.")
            notification.notify(
                title="Battery Warning",
                message="Battery is almost full. Please unplug the charger!",
                app_name="Battery Monitor",
                timeout=10  # Notification duration in seconds
            )
            time.sleep(7)  # Repeat notification every 7 seconds
    except Exception as e:
        logging.error("Error in show_persistent_notification: %s", e)

# Function to monitor battery status
def monitor_battery():
    global sound_playing, stop_sound, show_notification
    last_log_clear_time = time.time()

    try:
        while True:
            logging.debug("Checking battery status...")
            battery = psutil.sensors_battery()
            if not battery:
                logging.error("Battery information is not available.")
                print("Battery information not available. Exiting.")
                break

            plugged = battery.power_plugged  # True if charging, False otherwise
            percent = battery.percent
            logging.debug(f"Battery: {percent}% | Plugged: {plugged}")
            print(f"Battery: {percent}% | Plugged: {plugged}")  # Debug output

            # Clear the log file every 60 seconds
            if time.time() - last_log_clear_time >= 60:
                clear_log_file()
                last_log_clear_time = time.time()

            # Check conditions for alerts
            if percent >= 97 and plugged:
                if not sound_playing:
                    sound_playing = True
                    stop_sound = False
                    show_notification = True

                    logging.info("Battery almost full and still charging. Starting alerts.")
                    sound_thread = threading.Thread(target=play_sound_repeatedly, daemon=True)
                    notification_thread = threading.Thread(target=show_persistent_notification, daemon=True)
                    sound_thread.start()
                    notification_thread.start()

            elif not plugged:
                if sound_playing:
                    logging.info("Charger unplugged. Stopping alerts.")
                    sound_playing = False
                    stop_sound = True
                    show_notification = False

            time.sleep(1)  # Check battery status every second

    except Exception as e:
        logging.error("Error in monitor_battery: %s", e)

if __name__ == "__main__":
    try:
        logging.info("Starting Battery Monitor.")
        monitor_battery()
    except Exception as e:
        logging.error("Unexpected error in main: %s", e)
