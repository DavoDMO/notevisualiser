from threading import Thread
import pygame
from aubioAlgo import q, get_current_note
from datetime import datetime
import threading
import time

current_time = datetime.now()

t = Thread(target=get_current_note)
t.daemon = True
t.start()

pygame.init()
screenWidth, screenHeight = 500, 500
screen = pygame.display.set_mode((screenWidth, screenHeight))
running = True

font = pygame.font.SysFont("comicsansms", 30)
noteText = font.render("C", True, (0, 128, 0))
hzText = font.render("hz", True, (0, 128, 0))
cntText = font.render("cnts", True, (0, 128, 0))

pygame.mixer.init(48000, -16, 2, 1024)
pygame.mixer.music.set_volume(0.8)

# Initialize last detected values
last_note = "C"
last_hz = 250  # Default frequency (middle C ~ 261 Hz)
last_cents = 0

while running:
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((125, 10, 44))

    # If there's a new note in the queue, update values
    if not q.empty():
        b = q.get()
        
        # Ensure the received values are valid
        if 'Note' in b and 'hz' in b and 'Cents' in b:
            last_note = b['Note']
            last_hz = b['hz'] if isinstance(b['hz'], (int, float)) and b['hz'] > 0 else last_hz
            last_cents = b['Cents']

            # Save to file
            with open('notes.txt', 'w') as file:
                file.write(str(last_note))
                file.write(" at time: ")
                file.write(str(current_time))

    # Render text with the last valid values
    noteText = font.render(last_note, True, (0, 128, 0))
    hzText = font.render(str(last_hz), True, (0, 128, 0))
    cntText = font.render(str(last_cents), True, (0, 128, 0))

    # Map frequency to screen height (limit it to prevent errors)
    y = max(0, min(screenHeight - int(last_hz), screenHeight))  

    # Draw circle
    pygame.draw.circle(screen, (100, 100, 255), (20, y), 15, 5)

    # Render text
    screen.blit(noteText, (80, y - 20))
    screen.blit(hzText, (80, y))
    screen.blit(cntText, (80, y + 20))
    
    pygame.display.flip()
