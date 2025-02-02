from machine import Pin, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
import time

# Initialize Screen
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Initialize Buzzers
buzzer1 = PWM(Pin(21))  # Main melody
buzzer2 = PWM(Pin(10))  # Harmonic support

# Initialize Buttons
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Define notes (frequencies in Hz)
NOTES = {
    "C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392,
    "A4": 440, "B4": 494, "C5": 523, "D5": 587, "E5": 659,
    "F5": 698, "G5": 784, "A5": 880, "B5": 988, "REST": 0
}

# Mario Theme melody
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
    ("G4", 500), ("F4", 350), ("C5", 150), ("A4", 1000)
]

# List of available songs
songs = [mario_theme, imperial_march]

# Global state variables
running = False
next_song = False

# Interrupt Handlers
def toggle_pause(pin):
    time.sleep_ms(300)
    global running
    running = not running  # Toggle play/pause

def skip_song(pin):
    time.sleep_ms(300)
    global next_song
    next_song = True  # Signal to skip song

# Attach interrupts to buttons
button_a.irq(trigger=Pin.IRQ_FALLING, handler=toggle_pause)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=skip_song)

# Function to play a note with improved sound
def play_note(note, duration):
    freq = NOTES[note]

    if freq > 0:
        buzzer1.freq(freq)
        buzzer2.freq(freq // 2)  # Adds a harmonic undertone
        buzzer1.duty_u16(20000)  # Softer duty cycle
        buzzer2.duty_u16(10000)

    time.sleep_ms(duration)

    # Brief silence for better staccato effect
    buzzer1.duty_u16(0)
    buzzer2.duty_u16(0)
    time.sleep_ms(40)

# Play song with interrupt-based pausing and skipping
def play_song(song):
    global running, next_song

    for note, duration in song:
        if next_song:  # Skip song immediately
            return

        while not running:  # Pause handling
            if next_song:
                return
            time.sleep(0.2)

        play_note(note, duration)

# Stop sound
def pause_song():
    buzzer1.duty_u16(0)
    buzzer2.duty_u16(0)

# Display song menu
def display_menu():
    oled.fill(0)
    oled.text("MUSIC PLAYER", 15, 10)
    oled.text("A: Play/Pause", 10, 30)
    oled.text("B: Next Song", 10, 40)
    oled.show()

# Main Player Loop
def music_player():
    global running, next_song
    current_song_index = 0

    display_menu()

    while True:
        if running:
            play_song(songs[current_song_index])

        if next_song:
            current_song_index = (current_song_index + 1) % len(songs)
            running = True
            next_song = False

        pause_song()  # Ensure sound stops if paused

        time.sleep(0.2)

music_player()
