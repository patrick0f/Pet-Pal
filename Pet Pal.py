import pygame
import os
import sys
from pet import Pet  # Make sure pet.py exists with a Pet class
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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

# Load star image for congratulations popup
star_img_path = os.path.join(ASSET_PATH, "star.png")
star_img = pygame.image.load(star_img_path)
star_img = pygame.transform.scale(star_img, (40, 40))  # Scale to appropriate size

# AI Message Generation
def generate_ai_message(mood, hunger, energy, happiness, recent_action=None):
    try:
        # Create context for the AI
        context = f"You are a cute virtual pet. Your current stats are: Hunger: {hunger:.1f}, Energy: {energy:.1f}, Happiness: {happiness:.1f}. Your mood is: {mood}."
        
        if recent_action:
            context += f" Your owner just {recent_action}."
        
        prompt = f"{context} Respond with a short, cute message (max 7 words) that reflects how you're feeling. Use simple, friendly language and text based emojis, like :D."
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a cute virtual pet who speaks in short, adorable messages with text based emojis (e.g. :D)."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI message generation failed: {e}")
        # Fallback to static messages
        fallback_messages = {
            "hungry": "I'm so hungry! :(",
            "tired": "I need a nap...",
            "sad": "I'm feeling lonely... :'(",
            "excited": "This is amazing!",
            "happy": "I'm feeling great! :DDD"
        }
        return fallback_messages.get(mood, "Hello! :)")

# Game restart function
def restart_game():
    global pet, current_state
    pet = Pet()  # Create new pet with fresh stats
    current_state = LANDING  # Go back to landing page

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
        # Calculate bubble position (above the pet) - Made bigger for AI messages
        bubble_width = 400  # Increased from 250
        bubble_height = 120  # Increased from 80
        bubble_x = pet_x + 150 - bubble_width // 2  # Center above pet
        bubble_y = pet_y - 140  # Moved up more to accommodate larger bubble
        
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
        
        # Draw text inside bubble (with better text handling)
        text_lines = []
        words = pet.speech_bubble_text.split(' ')
        current_line = ""
        
        # Simple word wrapping for longer AI messages
        for word in words:
            test_line = current_line + word + " "
            test_surface = tutorial_font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() > bubble_width - 20:  # Leave 20px padding
                if current_line:
                    text_lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    text_lines.append(word)
                    current_line = ""
            else:
                current_line = test_line
        
        if current_line:
            text_lines.append(current_line.strip())
        
        # Draw each line of text
        line_height = 25
        start_y = bubble_y + bubble_height // 2 - (len(text_lines) * line_height) // 2
        
        for i, line in enumerate(text_lines):
            line_surface = tutorial_font.render(line, True, (0, 0, 0))
            line_rect = line_surface.get_rect(center=(bubble_x + bubble_width // 2, start_y + i * line_height))
            screen.blit(line_surface, line_rect)

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
            star_rect = star_img.get_rect(center=(star_x, star_y))
            screen.blit(star_img, star_rect)
        
        # Draw Play Again button
        pygame.draw.rect(screen, (100, 200, 100), play_again_button_rect)  # Green button
        pygame.draw.rect(screen, (255, 255, 255), play_again_button_rect, 3)  # White border
        
        play_again_text = button_font.render("PLAY AGAIN", True, (255, 255, 255))
        play_again_text_rect = play_again_text.get_rect(center=play_again_button_rect.center)
        screen.blit(play_again_text, play_again_text_rect)

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

# Play Again button for congratulations popup
play_again_button_width = 280  # Increased from 200
play_again_button_height = 80  # Increased from 60
play_again_button_x = (WIDTH - play_again_button_width) // 2
play_again_button_y = (HEIGHT // 2) + 160  # Moved down from +120 to +160
play_again_button_rect = pygame.Rect(play_again_button_x, play_again_button_y, play_again_button_width, play_again_button_height)

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
                # Check for Play Again button click (during congratulations popup)
                if pet.congrats_popup_timer > 0 and play_again_button_rect.collidepoint(event.pos):
                    restart_game()
                # Check action button clicks (only if no popup is showing)
                elif pet.congrats_popup_timer == 0:
                    if feed_button_rect.collidepoint(event.pos):
                        pet.feed()
                        pet.show_action_response("fed", generate_ai_message)
                    elif action_play_button_rect.collidepoint(event.pos):
                        pet.play()
                        pet.show_action_response("played", generate_ai_message)
                    elif sleep_button_rect.collidepoint(event.pos):
                        pet.sleep()
                        pet.show_action_response("slept", generate_ai_message)
        
        elif event.type == pygame.KEYDOWN and current_state == GAME and pet.congrats_popup_timer == 0:
            # Only allow keyboard controls when popup is not showing
            if event.key == pygame.K_f:
                pet.feed()
                pet.show_action_response("fed", generate_ai_message)
            elif event.key == pygame.K_p:
                pet.play()
                pet.show_action_response("played", generate_ai_message)
            elif event.key == pygame.K_s:
                pet.sleep()
                pet.show_action_response("slept", generate_ai_message)
    
    if current_state == LANDING:
        draw_landing_page()
    elif current_state == TUTORIAL:
        draw_tutorial()
    elif current_state == GAME:
        # Pass AI function to pet update
        pet.update(generate_ai_message)
        draw_game()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
