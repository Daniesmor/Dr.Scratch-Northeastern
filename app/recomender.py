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
        print(f"{self.MAGENTA}{self.deadCode}")
        message = ""
        blocks_list = []
        # Select one of the motivational phrases to start
        rand_index = random.randint(0, len(self.motivational_phrases) - 1)
        message += self.motivational_phrases[rand_index]

        # Search the deadCode of the dict and make phrase
        
        if (len(self.deadCode.items()) > 3): #Only one sprite with deadCode (maybe multiple blocks)
            message += f" you haven't used a lot of blocks in different sprites, maybe it would be a good idea to remove it, you agree?\nTry removing the following blocks: "

        for sprite, blocks in self.deadCode.items():
            if sprite not in ("deadCode", "number"):
                if (len(self.deadCode.items()) <= 3): #Only one sprite with deadCode (maybe multiple blocks)
                    message += f" you haven't used one block in the sprite {self.MAGENTA}{sprite}{self.RESET}, maybe it would be a good idea to remove it, you agree?\nTry removing the block: "
                for block in blocks:
                    print("longiutd: ", len(self.deadCode.items()))


                    blocks_list.append((f"{block}", f"This block is in the sprite {self.MAGENTA}{sprite}{self.RESET}:"))

                    
        feedback = {
            'message': message,
            'blocks': blocks_list,  
        }
        print("FEEDBACK --------------------------------------------")
        print(f"{self.MAGENTA}{feedback}")
        return feedback
    