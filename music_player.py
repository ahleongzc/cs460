import pygame
import threading


def alert():
    file_path = "alarm.mp3"
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    
    for i in range(10):
        # Play the music
        pygame.mixer.music.play()

        # Keep the script running until the music stops
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


def motion():
    file_path = "motion.mp3"
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    # Play the music
    pygame.mixer.music.play()

    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def cancel():
    file_path = "cancel.mp3"
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    # Play the music
    pygame.mixer.music.play()

    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        

def notify():
    file_path = "countdown.mp3"
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    # Play the music
    pygame.mixer.music.play()

    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        