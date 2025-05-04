# detection.py
import time
import audio
import head_pose
import matplotlib.pyplot as plt
import numpy as np

PLOT_LENGTH = 200

# Placeholders
GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.6
XDATA = list(range(PLOT_LENGTH))
YDATA = [0] * PLOT_LENGTH

AUDIO_IMPACT_FACTOR = 0.5  # Increased impact of audio

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return previous * 0.9 + current * 0.1  # Slightly reduced smoothing

def process():
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT
    audio_cheat_value = 0
    if audio.AUDIO_CHEAT == 1:
        audio_cheat_value = AUDIO_IMPACT_FACTOR
        audio.AUDIO_CHEAT = 0  # Reset the audio cheat flag immediately

    head_x_cheat_value = 0
    if head_pose.X_AXIS_CHEAT == 1:
        head_x_cheat_value = 0.3
    head_y_cheat_value = 0
    if head_pose.Y_AXIS_CHEAT == 1:
        head_y_cheat_value = 0.3

    total_cheat_contribution = head_x_cheat_value + head_y_cheat_value + audio_cheat_value
    PERCENTAGE_CHEAT = avg(total_cheat_contribution, PERCENTAGE_CHEAT)

    if PERCENTAGE_CHEAT > CHEAT_THRESH:
        GLOBAL_CHEAT = 1
        print("CHEATING")
    else:
        GLOBAL_CHEAT = 0
    print(f"Cheat percent: {PERCENTAGE_CHEAT:.2f}, GLOBAL_CHEAT: {GLOBAL_CHEAT}")

def run_detection():
    global XDATA, YDATA, PERCENTAGE_CHEAT
    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    ax.set_xlim(0, PLOT_LENGTH)
    ax.set_ylim(0, 1)
    line, = ax.plot(XDATA, YDATA, 'r-')
    plt.title("Suspicious Behaviour Detection")
    plt.xlabel("Time")
    plt.ylabel("Cheat Probability")

    while True:
        YDATA.pop(0)
        YDATA.append(PERCENTAGE_CHEAT)
        line.set_xdata(XDATA)
        line.set_ydata(YDATA)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(1 / 5)
        process()
if __name__ == "__main__":
    print("[DETECTION] Running detection.py for testing...")
    # You would typically run this via run.py
    # For direct testing, you might need to simulate head_pose and audio flags
    run_detection()
