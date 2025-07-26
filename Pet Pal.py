import pygame
import os
import sys
from pet import Pet  # Make sure pet.py exists with a Pet class

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1500, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet Pal")

# Game state
LANDING = 0
TUTORIAL = 1
GAME = 2
current_state = LANDING

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)
button_font = pygame.font.Font(None, 48)
tutorial_font = pygame.font.Font(None, 32)

# Asset path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets")

# Load and scale background images
landing_bg_path = os.path.join(ASSET_PATH, "landing.jpg")
landing_background = pygame.image.load(landing_bg_path)
landing_background = pygame.transform.scale(landing_background, (WIDTH, HEIGHT))

game_bg_path = os.path.join(ASSET_PATH, "bg.png")
game_background = pygame.image.load(game_bg_path)
game_background = pygame.transform.scale(game_background, (WIDTH, HEIGHT))

# Load and scale pet image to a reasonable size
pet_img_path = os.path.join(ASSET_PATH, "pet_happy-.png")
pet_img = pygame.image.load(pet_img_path)
pet_img = pygame.transform.scale(pet_img, (300, 300))  # Made bigger from (200, 200)

# Load action button images
feed_img_path = os.path.join(ASSET_PATH, "feed.jpg")
play_img_path = os.path.join(ASSET_PATH, "play.jpg")
sleep_img_path = os.path.join(ASSET_PATH, "sleep.jpg")

feed_img = pygame.image.load(feed_img_path)
play_img = pygame.image.load(play_img_path)
sleep_img = pygame.image.load(sleep_img_path)

# Scale action buttons to consistent size
button_size = (100, 100)
feed_img = pygame.transform.scale(feed_img, button_size)
play_img = pygame.transform.scale(play_img, button_size)
sleep_img = pygame.transform.scale(sleep_img, button_size)

# Pet instance
pet = Pet()

# Clock
clock = pygame.time.Clock()

# Draw pet stats on screen
def draw_stat(label, value, y_pos):
    text = font.render(f"{label}: {int(value)}", True, (0, 0, 0))
    screen.blit(text, (20, y_pos))

def draw_speech_bubble(pet_x, pet_y):
    if pet.speech_bubble_timer > 0:
        # Calculate bubble position (above the pet)
        bubble_width = 250
        bubble_height = 80
        bubble_x = pet_x + 150 - bubble_width // 2  # Center above pet
        bubble_y = pet_y - 100  # Position above pet
        
        # Draw bubble background (rounded rectangle effect)
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pygame.draw.ellipse(screen, (255, 255, 255), bubble_rect)
        pygame.draw.ellipse(screen, (0, 0, 0), bubble_rect, 3)
        
        # Draw bubble tail (triangle pointing to pet)
        tail_points = [
            (bubble_x + bubble_width // 2 - 15, bubble_y + bubble_height),
            (bubble_x + bubble_width // 2, bubble_y + bubble_height + 20),
            (bubble_x + bubble_width // 2 + 15, bubble_y + bubble_height)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), tail_points)
        pygame.draw.polygon(screen, (0, 0, 0), tail_points, 3)
        
        # Draw text inside bubble
        bubble_text = tutorial_font.render(pet.speech_bubble_text, True, (0, 0, 0))
        text_rect = bubble_text.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + bubble_height // 2))
        screen.blit(bubble_text, text_rect)

def draw_congratulations_popup():
    if pet.congrats_popup_timer > 0:
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw main popup box
        popup_width = 600
        popup_height = 300
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2
        
        # Popup background with border
        pygame.draw.rect(screen, (255, 215, 0), (popup_x, popup_y, popup_width, popup_height))  # Gold background
        pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height), 5)  # White border
        
        # Main congratulations text
        congrats_text = title_font.render("CONGRATULATIONS!", True, (255, 255, 255))
        congrats_rect = congrats_text.get_rect(center=(WIDTH // 2, popup_y + 80))
        screen.blit(congrats_text, congrats_rect)
        
        # Subtitle text
        subtitle_text = button_font.render("Max Friendship Achieved!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, popup_y + 140))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Additional message
        message_text = tutorial_font.render("Your pet loves you very much!", True, (255, 255, 255))
        message_rect = message_text.get_rect(center=(WIDTH // 2, popup_y + 180))
        screen.blit(message_text, message_rect)
        
        # Stars decoration
        star_positions = [
            (popup_x + 50, popup_y + 50),
            (popup_x + popup_width - 50, popup_y + 50),
            (popup_x + 50, popup_y + popup_height - 50),
            (popup_x + popup_width - 50, popup_y + popup_height - 50),
            (popup_x + popup_width // 2, popup_y + 30),
            (popup_x + popup_width // 2, popup_y + popup_height - 30)
        ]
        
        for star_x, star_y in star_positions:
            star_text = button_font.render("★", True, (255, 255, 255))
            star_rect = star_text.get_rect(center=(star_x, star_y))
            screen.blit(star_text, star_rect)

# Button properties
button_width = 200
button_height = 80
large_button_width = 250
large_button_height = 90
button_x = (WIDTH - button_width) // 2
large_button_x = (WIDTH - large_button_width) // 2
play_button_y = HEIGHT // 2 + 100
start_button_y = HEIGHT - 250  # Moved up from HEIGHT - 150

play_button_rect = pygame.Rect(button_x, play_button_y, button_width, button_height)
start_game_button_rect = pygame.Rect(large_button_x, start_button_y, large_button_width, large_button_height)

# Action button positions (right side of screen, stacked vertically)
action_button_x = WIDTH - 120  # 20 pixels from right edge
action_button_spacing = 120     # 120 pixels between buttons
feed_button_y = HEIGHT // 2 - 120
play_button_y = feed_button_y + action_button_spacing
sleep_button_y = play_button_y + action_button_spacing

feed_button_rect = pygame.Rect(action_button_x, feed_button_y, 100, 100)
action_play_button_rect = pygame.Rect(action_button_x, play_button_y, 100, 100)
sleep_button_rect = pygame.Rect(action_button_x, sleep_button_y, 100, 100)

def draw_landing_page():
    screen.blit(landing_background, (0, 0))
    
    # Semi-transparent background for title
    title_bg = pygame.Surface((400, 120))
    title_bg.set_alpha(100)  # Low opacity
    title_bg.fill((0, 0, 0))
    title_bg_rect = title_bg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_bg, title_bg_rect)
    
    # Draw title
    title_text = title_font.render("Pet Pal", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(title_text, title_rect)
    
    # Draw play button
    pygame.draw.rect(screen, (100, 200, 100), play_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), play_button_rect, 3)
    
    button_text = button_font.render("PLAY", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=play_button_rect.center)
    screen.blit(button_text, button_text_rect)

def draw_tutorial():
    screen.blit(landing_background, (0, 0))
    
    # Semi-transparent background for all tutorial content
    tutorial_bg = pygame.Surface((1000, 650))
    tutorial_bg.set_alpha(120)  # Low opacity
    tutorial_bg.fill((0, 0, 0))
    tutorial_bg_rect = tutorial_bg.get_rect(center=(WIDTH // 2, 400))
    screen.blit(tutorial_bg, tutorial_bg_rect)
    
    # Draw title
    title_text = title_font.render("How to Play", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    
    # Tutorial text
    tutorial_lines = [
        "Welcome to Pet Pal! Your virtual pet needs your care.",
        "Your pet has three important stats:",
        "• HUNGER - Feed your pet when it gets hungry",
        "• ENERGY - Let your pet sleep to restore energy", 
        "• HAPPINESS - Play with your pet to keep it happy",
        "",
        "Controls:",
        "• Press F to FEED your pet",
        "• Press P to PLAY with your pet",
        "• Press S to let your pet SLEEP",
        "",
        "Keep your pet healthy and happy by monitoring its stats!",
        "Stats will slowly decrease over time, so check on your pet regularly."
    ]
    
    # Draw tutorial text
    y_offset = 200
    for line in tutorial_lines:
        if line:  # Skip empty lines
            text = tutorial_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(text, text_rect)
        y_offset += 40
    
    # Draw start game button (now larger)
    pygame.draw.rect(screen, (100, 200, 100), start_game_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), start_game_button_rect, 3)
    
    button_text = button_font.render("START GAME", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=start_game_button_rect.center)
    screen.blit(button_text, button_text_rect)

def draw_game():
    screen.blit(game_background, (0, 0))
    
    # Center pet horizontally and position higher up
    pet_x = (WIDTH - 300) // 2  # Center horizontally (300 is new pet width)
    pet_y = HEIGHT - 450  # Moved up from 300 to 450 pixels from bottom
    screen.blit(pet_img, (pet_x, pet_y))
    
    # Draw stats
    draw_stat("Hunger", pet.hunger, 20)
    draw_stat("Energy", pet.energy, 60)
    draw_stat("Happiness", pet.happiness, 100)
    
    # Draw mood
    mood_text = font.render(f"Mood: {pet.get_mood().title()}", True, (0, 0, 0))
    screen.blit(mood_text, (20, 140))
    
    # Draw action buttons
    screen.blit(feed_img, feed_button_rect)
    screen.blit(play_img, action_play_button_rect)
    screen.blit(sleep_img, sleep_button_rect)
    
    # Draw speech bubble above pet
    draw_speech_bubble(pet_x, pet_y)
    
    # Draw congratulations popup (appears on top of everything)
    draw_congratulations_popup()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == LANDING and play_button_rect.collidepoint(event.pos):
                current_state = TUTORIAL
            elif current_state == TUTORIAL and start_game_button_rect.collidepoint(event.pos):
                current_state = GAME
            elif current_state == GAME:
                # Check action button clicks
                if feed_button_rect.collidepoint(event.pos):
                    pet.feed()
                elif action_play_button_rect.collidepoint(event.pos):
                    pet.play()
                elif sleep_button_rect.collidepoint(event.pos):
                    pet.sleep()
        
        elif event.type == pygame.KEYDOWN and current_state == GAME:
            if event.key == pygame.K_f:
                pet.feed()
            elif event.key == pygame.K_p:
                pet.play()
            elif event.key == pygame.K_s:
                pet.sleep()
    
    if current_state == LANDING:
        draw_landing_page()
    elif current_state == TUTORIAL:
        draw_tutorial()
    elif current_state == GAME:
        pet.update()
        draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
