print("Starting...")
# Autostart https://learn.sparkfun.com/tutorials/how-to-run-a-raspberry-pi-program-on-startup#method-2-autostart

from pathlib import Path
import RPi.GPIO as GPIO
from pygame import mixer
from numpy import random
from time import sleep
import subprocess
import time

MUSIC_DIR = '/home/pi/Music/'
mp3_path = Path(MUSIC_DIR)
mp3s = list(mp3_path.glob('*.mp3'))
print("mp3s")
print(mp3s)

assert len(mp3s) > 0, 'There were no mp3 files found in {}'.format(MUSIC_DIR)
amount_song=1
def skip_backwards():
    skip_state=GPIO.input(16)
    while skip_state == 1:
        time.sleep(0.02)
        skip_state=GPIO.input(16)
    start_time=time.time()
    while True:
        skip_state=GPIO.input(16)
        current_time=time.time()
        if current_time>start_time+1:
            return 1
        if skip_state == 1:
            return 2

        time.sleep(0.1)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


mixer.init()

song_index = 0


while True:
    for song in mp3s:
        mixer.music.load(str(song))
        mixer.music.play(0,0)
        is_paused = False
        print('Now playing {}'.format(song))
        while mixer.music.get_busy():
            pause_state = GPIO.input(10)
            skip_state=GPIO.input(16)
            change_state=GPIO.input(18)
            shuffle_state=GPIO.input(12)
            if pause_state==1:
                if is_paused:
                    print('Unpausing...')
                    mixer.music.unpause()
                    is_paused = False
                else:
                    print('Pausing...')
                    mixer.music.pause()
                    is_paused = True
                sleep(1)
            if change_state==1:
                mixer.music.rewind()
                print("Repeat")
                print("Now playing {}".format(song))
                sleep(1)
            if skip_state==1:
                skip = skip_backwards()
                if skip == 1:
                    song_index += 1
                    print("skipping...")
                    mixer.music.load(str(song))
                elif skip == 2:
                    song_index -= 1
                    print("skipping backward...")
                    mixer.music.load(str(song))
            if shuffle_state==1:
                print("List shuffle...")
                random.shuffle(mp3s)
                sleep(0.2)
            sleep(0.1)
        
