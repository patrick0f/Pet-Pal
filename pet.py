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
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 10)

    def sleep(self):
        self.energy = min(100, self.energy + 25)

    def update(self):
        # Stats decay over time
        self.hunger = min(100, self.hunger + 0.01)
        self.energy = max(0, self.energy - 0.005)
        self.happiness = max(0, self.happiness - 0.007)
        
        # Check for mood changes and show speech bubble
        new_mood = self.get_mood()
        if new_mood != self.current_mood:
            self.current_mood = new_mood
            self.show_speech_bubble(new_mood)
        
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
    
    def show_speech_bubble(self, mood):
        # Dictionary of mood-specific messages
        mood_messages = {
            "hungry": "I'm so hungry! :(",
            "tired": "I need a nap...",
            "sad": "I'm feeling lonely... :'(",
            "excited": "This is amazing!",
            "happy": "I'm feeling great! :DDD"
        }
        
        self.speech_bubble_text = mood_messages.get(mood, "Hello!")
        self.speech_bubble_timer = 180  # Show for 3 seconds at 60 FPS