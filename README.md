# Pico W Game Emulator  

## Introduction  

This project runs on BitDogLab, an educational STEM device equipped with a Raspberry Pi Pico W and various peripherals. The goal is to play songs in an embedded environment using MicroPython, allowing real-time interaction through buttons for play/pause and song selection.

### Hardware Components
- RP2040 microcontroller (Raspberry Pi Pico W)
- SSD1306 OLED display (128x64, I2C)
- Two passive buzzers (for dual-tone playback)
- Two buttons (for controlling playback and song selection)

## Demonstration
<!-- Place images and videos -->

## Code Overview

### Interruption Handlers
```python
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
```

### Play Song funtion
```python
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
```

### Main Player Loop
```python
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
```

## How to Run the Project  
1. Flash MicroPython firmware onto the Raspberry Pi Pico W  
2. Run `player.py` file in Pico W using VS Code  
