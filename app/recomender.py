import random


class RecomenderSystem():
    """
    Recomender system for improve Scratch projects
    """

    def __init__(self, Dictionary):
        self.MAGENTA = "\033[95m"
        self.RESET = "\033[0m"
        self.GREEN = "\033[92m"

        print(f"{self.MAGENTA}Welcome to the recomender system engine{self.RESET}")
        print(Dictionary)
        self.deadCode = Dictionary
        #self.deadCode = Dictionary['deadCode']

        self.motivational_phrases = [
            "You are doing a very good job, it's amazing, but my cat-like sense of smell has detected that",
            "You are doing excellent work, it's impressive, but my cat-like sense of smell has detected that someone ate my tuna, or maybe it's that",
            "You're doing a fantastic job, it's wonderful, but my cat skills have detected a mouse nearby, or perhaps it might be that",
            "Your effort is outstanding, it's fascinating, but my feline instincts have identified that someone is keeping secrets in the litter box, or perhaps it might be that",
        ]

    def recomender_deadcode(self) -> dict:
        feedback = ""
        print(f"{self.MAGENTA}{self.deadCode}")
        
        # Select one of the motivational phrases to start
        rand_index = random.randint(0, len(self.motivational_phrases) - 1)
        feedback += self.motivational_phrases[rand_index]

        # Search the deadCode of the dict and make phrase
        for sprite, blocks in self.deadCode.items():
            if sprite not in ("deadCode", "number"):
                for block in blocks:
                    
                    feedback += f" You haven't used one block in the sprite {self.GREEN}{sprite}{self.RESET}, maybe it would be a good idea to remove it, you agree?\n"
                    feedback += f" Try removing the block: {self.GREEN}{block}{self.RESET}\n"
                    print("INSIDE --------------------------------------------")
                    print(f"{self.MAGENTA}{feedback}")
        return feedback
    