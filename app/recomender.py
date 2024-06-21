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

        self.farwell = [
            "\nGood luck improving your project, you can do it!! :)",
            "\nKeep going with your project, you’re doing a great job! :)",
            "\nI’m sure your project will be a great success! :)",
            "\nDon’t give up, every effort brings you closer to your goal! :)",
            "\nI trust your abilities, you will improve your project! :)",
        ]

    def recomender_deadcode(self) -> dict:
        print(f"{self.MAGENTA}{self.deadCode}")
        message = ""
        explanation = ""
        farwell = ""
        blocks_list = []

        # explanations lists about what is deadCode
        explanation_phrases = [
            "\nEXPLANATION:\nDead code is like having unused blocks scattered on the floor: it makes everything more cluttered and harder to understand. By removing it, your project will be cleaner, easier to understand, and work better.",
            "\nEXPLANATION:\nHaving dead code is like having broken toys in your room: they are useless and just take up space. By removing them, everything will be more organized.",
            "\nEXPLANATION:\nDead code is like having old papers on your desk: they distract you and make it hard to find what you need. By getting rid of them, you will work better.",
            "\nEXPLANATION:\nDead code is like having clothes you no longer wear in your closet: it just takes up space and makes everything look messy. Removing it makes everything easier to manage.",
            "\nEXPLANATION:\nDead code is like having trash in your backpack: it's useless and just gets in the way. By cleaning it out, you find everything faster and it's easier to use.",
        ]

        # Select one of the motivational phrases to start
        rand_message_index = random.randint(0, len(self.motivational_phrases) - 1)
        message += self.motivational_phrases[rand_message_index]


        # Search the deadCode of the dict and make phrase
        if (len(self.deadCode.items()) > 3): #Only one sprite with deadCode (maybe multiple blocks)
            message += f" you haven't used a lot of blocks in different sprites, maybe it would be a good idea to remove it, you agree?\nTry removing the following blocks: "

        for sprite, blocks in self.deadCode.items():
            if sprite not in ("deadCode", "number"):
                if (len(self.deadCode.items()) <= 3): #Only one sprite with deadCode (maybe multiple blocks)
                    message += f" you haven't used one block in the sprite {self.MAGENTA}{sprite}{self.RESET}, maybe it would be a good idea to remove it, you agree?\nTry removing the block: "
                for block in blocks:
                    blocks_list.append((f"{block}", f"This block is in the sprite {self.MAGENTA}{sprite}{self.RESET}:"))        
        
        # Select one of the explanation phrases of deadCode
        rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
        explanation += explanation_phrases[rand_explanation_index]

        # Select one of the farwell phrases
        rand_farwell_index = random.randint(0, len(self.farwell) - 1) 
        farwell += self.farwell[rand_explanation_index]

        feedback = {
            'message': message,
            'blocks': blocks_list,  
            'explanation': explanation,
            'farwell': farwell,
        }
        return feedback
    