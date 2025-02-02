from machine import Pin, PWM
import time

# Define buzzers on GPIO pins
buzzer1 = PWM(Pin(21))  # First buzzer
buzzer2 = PWM(Pin(10))  # Second buzzer

# Define notes (frequencies in Hz)
NOTES = {
    "E5": 659, "C5": 523, "G4": 392, "G5": 784, "A5": 880, "B5": 988,
    "F5": 698, "D5": 587, "C6": 1047, "REST": 0
}

# Define song (note, duration in ms)
mario_theme = [
    ("E5", 200), ("E5", 200), ("REST", 200), ("E5", 200),
    ("REST", 200), ("C5", 200), ("E5", 200), ("G5", 400),
    ("REST", 200), ("G4", 400)
]

# Function to play a note
def play_note(note, duration):
    freq = NOTES[note]
    
    if freq > 0:
        buzzer1.freq(freq)
        buzzer2.freq(freq // 2)  # Second buzzer plays at half frequency
        buzzer1.duty_u16(20000)  # Activate buzzers
        buzzer2.duty_u16(10000)
    else:
        buzzer1.duty_u16(0)  # Silence for rests
        buzzer2.duty_u16(0)

    time.sleep_ms(duration)
    buzzer1.duty_u16(0)
    buzzer2.duty_u16(0)
    time.sleep_ms(50)  # Small pause between notes

# Play the Mario Theme
def play_song():
    for note, duration in mario_theme:
        play_note(note, duration)

# Run the song once
play_song()
