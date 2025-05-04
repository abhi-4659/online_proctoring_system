# audio.py
import sounddevice as sd
import numpy as np

# Constants and thresholds
CALLBACKS_PER_SECOND = 38               # Callbacks per second (system dependent)
SUS_FINDING_FREQUENCY = 5               # Increased frequency to calculate "suspicious" sound
SOUND_AMPLITUDE_THRESHOLD = 10          # Lowered amplitude threshold
FRAMES_COUNT = int(CALLBACKS_PER_SECOND / SUS_FINDING_FREQUENCY)  # Number of frames to consider

# Placeholders and global variables
AMPLITUDE_LIST = [0] * FRAMES_COUNT
SUS_COUNT = 0
count = 0
AUDIO_CHEAT = 0

def print_sound(indata, outdata, frames, time, status):
    """
    Callback function to process the sound data.
    """
    global SUS_COUNT, count, AUDIO_CHEAT, AMPLITUDE_LIST

    # Calculate the norm of the input sound data to determine its amplitude
    vnorm = int(np.linalg.norm(indata) * 10)

    # Update the amplitude list
    AMPLITUDE_LIST.append(vnorm)
    count += 1
    AMPLITUDE_LIST.pop(0)

    if count == FRAMES_COUNT:
        # Calculate the average amplitude
        avg_amp = sum(AMPLITUDE_LIST) / FRAMES_COUNT
        print(f"[AUDIO] vnorm: {vnorm}, avg_amp: {avg_amp}, SUS_COUNT: {SUS_COUNT}, AUDIO_CHEAT: {AUDIO_CHEAT}")

        if SUS_COUNT >= 1:  # Reduced consecutive SUS count
            AUDIO_CHEAT = 1
            SUS_COUNT = 0
        elif avg_amp > SOUND_AMPLITUDE_THRESHOLD:
            # Increment the SUS count if the average amplitude is above the threshold
            SUS_COUNT += 1
        else:
            # Reset the SUS count and cheat flag if amplitude is below the threshold
            SUS_COUNT = 0
            AUDIO_CHEAT = 0

        # Reset the frame count
        count = 0

def sound():
    """
    Start the sound stream and analyze the incoming sound.
    """
    with sd.Stream(callback=print_sound):
        sd.sleep(-1)  # Keep the stream open indefinitely
if __name__ == "__main__":
    print("[AUDIO] Running audio.py for testing...")
    sound()
