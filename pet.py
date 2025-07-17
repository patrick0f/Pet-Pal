# pet.py
class Pet:
    def __init__(self, name="Fluffy"):
        self.name = name
        self.hunger = 50
        self.energy = 50
        self.happiness = 50

    def feed(self):
        self.hunger = max(0, self.hunger - 20)

    def play(self):
        self.happiness = min(100, self.happiness + 15)
        self.energy = max(0, self.energy - 10)

    def sleep(self):
        self.energy = min(100, self.energy + 25)

    def update(self):
        # Stats decay over time
        self.hunger = min(100, self.hunger + 0.05)
        self.energy = max(0, self.energy - 0.02)
        self.happiness = max(0, self.happiness - 0.03)

    def get_mood(self):
        if self.hunger > 80:
            return "hungry"
        elif self.energy < 20:
            return "tired"
        elif self.happiness < 30:
            return "sad"
        else:
            return "happy"