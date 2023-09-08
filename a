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
assert len(mp3s) > 0, 'There were no mp3 files found in {}'.format(MUSIC_DIR)
random.shuffle(mp3s)
amount_song=1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

mixer.init()

for song in mp3s:
    state = 1
    mixer.music.load(str(song))
    mixer.music.play()
    is_paused = False
    print('Now playing {}'.format(song))
    while mixer.music.get_busy():
        pause_state = GPIO.input(10)
        skip_state=GPIO.input(16)
        change_state=GPIO.input(18)
        if skip_state==1:
            print('Skipping to next song...')
            mixer.music.stop()
            sleep(1)

            amount_song+=1
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
        
