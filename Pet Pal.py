import pygame
import os
import sys
from pet import Pet  # Make sure pet.py exists with a Pet class

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet Pal")

# Font
font = pygame.font.Font(None, 36)

# Asset path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets")

# Load and scale background image to fit the screen
background_path = os.path.join(ASSET_PATH, "background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load and scale pet image to a reasonable size
pet_img_path = os.path.join(ASSET_PATH, "pet_happy.png")
pet_img = pygame.image.load(pet_img_path)
pet_img = pygame.transform.scale(pet_img, (200, 200))  # Adjust size as needed

# Pet instance
pet = Pet()

# Clock
clock = pygame.time.Clock()

# Draw pet stats on screen
def draw_stat(label, value, y_pos):
    text = font.render(f"{label}: {int(value)}", True, (0, 0, 0))
    screen.blit(text, (20, y_pos))

# Game loop
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(pet_img, (300, 200))  # Pet image position

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pet.feed()
            elif event.key == pygame.K_p:
                pet.play()
            elif event.key == pygame.K_s:
                pet.sleep()

    pet.update()
    draw_stat("Hunger", pet.hunger, 20)
    draw_stat("Energy", pet.energy, 60)
    draw_stat("Happiness", pet.happiness, 100)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
