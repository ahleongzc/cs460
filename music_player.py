import pygame
import threading

def alert():
    file_path = "alarm.mp3"
    # Initialize the mixer
    pygame.mixer.init()
    # Load the MP3 file
    pygame.mixer.music.load(file_path)
    # Play the music
    pygame.mixer.music.play()
    
    # Keep the script running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
