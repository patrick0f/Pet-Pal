# pet.py
class Pet:
    def __init__(self, name="Fluffy"):
        self.name = name
        self.hunger = 50
        self.energy = 50
        self.happiness = 50
        self.current_mood = "happy"
        self.speech_bubble_text = ""
        self.speech_bubble_timer = 0
        self.max_friendship_achieved = False
        self.congrats_popup_timer = 0

    def feed(self):
        self.hunger = max(0, self.hunger - 20)

    def play(self):
        self.happiness = min(101, self.happiness + 20)  # Max happiness now 101
        self.energy = max(0, self.energy - 10)

    def sleep(self):
        self.energy = min(100, self.energy + 25)

    def update(self, ai_message_func=None):
        # Stats decay over time
        self.hunger = min(100, self.hunger + 0.01)
        self.energy = max(0, self.energy - 0.005)
        self.happiness = max(0, self.happiness - 0.007)
        
        # Check for mood changes and show speech bubble
        new_mood = self.get_mood()
        if new_mood != self.current_mood:
            self.current_mood = new_mood
            self.show_speech_bubble(new_mood, ai_message_func)
        
        # Decrease speech bubble timer
        if self.speech_bubble_timer > 0:
            self.speech_bubble_timer -= 1
        
        # Check for max friendship achievement
        if self.happiness >= 100 and not self.max_friendship_achieved:
            self.max_friendship_achieved = True
            self.congrats_popup_timer = 300  # Show for 5 seconds at 60 FPS
        
        # Decrease congratulations popup timer
        if self.congrats_popup_timer > 0:
            self.congrats_popup_timer -= 1

    def get_mood(self):
        # Priority-based mood system using all stats
        
        # Critical needs first
        if self.hunger > 75:
            return "hungry"
        elif self.energy < 20:
            return "tired"
        
        # Emotional states based on overall wellbeing
        elif self.happiness < 30:
            return "sad"
        elif self.happiness > 80 and self.energy > 70 and self.hunger < 40:
            return "excited"
        else:
            return "happy"
    
    def show_speech_bubble(self, mood, ai_message_func=None):
        if ai_message_func:
            # Use AI-generated message
            self.speech_bubble_text = ai_message_func(mood, self.hunger, self.energy, self.happiness)
        else:
            # Fallback to static messages
            mood_messages = {
                "hungry": "I'm so hungry! :(",
                "tired": "I need a nap...",
                "sad": "I'm feeling lonely... :'(",
                "excited": "This is amazing!",
                "happy": "I'm feeling great! :DDD"
            }
            self.speech_bubble_text = mood_messages.get(mood, "Hello!")
        
        self.speech_bubble_timer = 180  # Show for 3 seconds at 60 FPS
    
    def show_action_response(self, action, ai_message_func=None):
        """Show a response to a specific action like feeding, playing, or sleeping"""
        if ai_message_func:
            self.speech_bubble_text = ai_message_func(self.get_mood(), self.hunger, self.energy, self.happiness, action)
        else:
            action_messages = {
                "fed": "Yum! Thanks for the food! :)",
                "played": "That was so fun! :D",
                "slept": "I feel so much better now! Zzz..."
            }
            self.speech_bubble_text = action_messages.get(action, "Thanks!")
        
        self.speech_bubble_timer = 180