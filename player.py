from machine import Pin, PWM
import time

# Define buzzers on GPIO pins
buzzer1 = PWM(Pin(21))  # First buzzer
buzzer2 = PWM(Pin(10))  # Second buzzer

# Define notes (frequencies in Hz)
NOTES = {
    "C0": 16, "C#0": 17, "D0": 18, "D#0": 19, "E0": 21, "F0": 22, "F#0": 23, "G0": 25, "G#0": 26, "A0": 28, "A#0": 29, "B0": 31,
    "C1": 33, "C#1": 35, "D1": 37, "D#1": 39, "E1": 41, "F1": 44, "F#1": 46, "G1": 49, "G#1": 52, "A1": 55, "A#1": 58, "B1": 62,
    "C2": 65, "C#2": 69, "D2": 73, "D#2": 78, "E2": 82, "F2": 87, "F#2": 92, "G2": 98, "G#2": 104, "A2": 110, "A#2": 117, "B2": 123,
    "C3": 131, "C#3": 139, "D3": 147, "D#3": 156, "E3": 165, "F3": 175, "F#3": 185, "G3": 196, "G#3": 208, "A3": 220, "A#3": 233, "B3": 247,
    "C4": 262, "C#4": 277, "D4": 294, "D#4": 311, "E4": 330, "F4": 349, "F#4": 370, "G4": 392, "G#4": 415, "A4": 440, "A#4": 466, "B4": 494,
    "C5": 523, "C#5": 554, "D5": 587, "D#5": 622, "E5": 659, "F5": 698, "F#5": 740, "G5": 784, "G#5": 831, "A5": 880, "A#5": 932, "B5": 988,
    "C6": 1047, "C#6": 1109, "D6": 1175, "D#6": 1245, "E6": 1319, "F6": 1397, "F#6": 1480, "G6": 1568, "G#6": 1661, "A6": 1760, "A#6": 1865, "B6": 1976,
    "C7": 2093, "C#7": 2217, "D7": 2349, "D#7": 2489, "E7": 2637, "F7": 2794, "F#7": 2960, "G7": 3136, "G#7": 3322, "A7": 3520, "A#7": 3729, "B7": 3951,
    "REST": 0
}

# Mario Theme
mario_theme = [
    ("E5", 125), ("E5", 125), ("REST", 125), ("E5", 125),
    ("REST", 125), ("C5", 125), ("E5", 125), ("G5", 250),
    ("REST", 125), ("G4", 250)
]

# Imperial March melody
imperial_march = [
    ("A4", 500), ("A4", 500), ("F4", 350), ("C5", 150),
    ("A4", 500), ("F4", 350), ("C5", 150), ("A4", 1000),
    ("E5", 500), ("E5", 500), ("E5", 500), ("F5", 350), ("C5", 150),
    ("G#4", 500), ("F4", 350), ("C5", 150), ("A4", 1000)
]

# Function to play a note
def play_note(note, duration):
    freq = NOTES[note]
    
    if freq > 0:
        buzzer1.freq(freq)
        buzzer2.freq(freq // 2)  # Second buzzer plays at half frequency
        buzzer1.duty_u16(20000)  # Activate buzzers
        buzzer2.duty_u16(15000)
    else:
        buzzer1.duty_u16(0)  # Silence for rests
        buzzer2.duty_u16(0)

    time.sleep_ms(duration)
    buzzer1.duty_u16(0)
    buzzer2.duty_u16(0)
    time.sleep_ms(50)  # Small pause between notes

# Play the Mario Theme
def play_song(song):
    for note, duration in song:
        play_note(note, duration)

# Run the song once
play_song(mario_theme)
play_song(imperial_march)
