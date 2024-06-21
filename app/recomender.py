import random


class RecomenderSystem():
    """
    Recomender system for improve Scratch projects
    """

    def __init__(self, ):
        self.MAGENTA = "\033[95m"
        self.RESET = "\033[0m"
        self.GREEN = "\033[92m"

        print(f"{self.MAGENTA}Welcome to the recomender system engine{self.RESET}")

        self.motivational_phrases = [
            "You are doing a very good job, it's amazing, but my cat-like sense of smell has detected that",
            "You are doing excellent work, it's impressive, but my cat-like sense of smell has detected that someone ate my tuna, or maybe it's that",
            "You're doing a fantastic job, it's wonderful, but my cat skills have detected a mouse nearby, or perhaps it might be that",
            "Your effort is outstanding, it's fascinating, but my feline instincts have identified that someone is keeping secrets in the litter box, or perhaps it might be that",
        ]

        self.farwells = [
            "\nGood luck improving your project, you can do it!! :)",
            "\nKeep going with your project, you’re doing a great job! :)",
            "\nI’m sure your project will be a great success! :)",
            "\nDon’t give up, every effort brings you closer to your goal! :)",
            "\nI trust your abilities, you will improve your project! :)",
        ]

    def recomender_deadcode(self, dict_deadCode) -> dict:
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
        if (len(dict_deadCode.items()) > 3): #Only one sprite with deadCode (maybe multiple blocks)
            message += f" you haven't used a lot of blocks in different sprites, maybe it would be a good idea to remove it, you agree?\nTry removing the following blocks: "

        for sprite, blocks in dict_deadCode.items():
            if sprite not in ("deadCode", "number"):
                if (len(dict_deadCode.items()) <= 3): #Only one sprite with deadCode (maybe multiple blocks)
                    message += f" you haven't used one block in the sprite {self.MAGENTA}{sprite}{self.RESET}, maybe it would be a good idea to remove it, you agree?\nTry removing the block: "
                for block in blocks:
                    blocks_list.append((f"{block}", f"This block is in the sprite {self.MAGENTA}{sprite}{self.RESET}:"))        
        
        # Select one of the explanation phrases of deadCode
        rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
        explanation += explanation_phrases[rand_explanation_index]

        # Select one of the farwell phrases
        rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
        farwell += self.farwells[rand_farwell_index]

        feedback = {
            'message': message,
            'blocks': blocks_list,  
            'explanation': explanation,
            'farwell': farwell,
        }
        return feedback
    
    def recomender_sprite(self, dict_spriteNaming) -> dict:
        message = ""
        explanation = ""
        farwell = ""
        sprite_list = []

        explanation_phrases = [
            "\nEXPLANATION:\nGiving meaningful names to sprites is like labeling items in your toolbox: it helps you quickly find what you need. Clear names make your project easier to understand and navigate.",
            "\nEXPLANATION:\nNaming sprites is like naming characters in a story: it gives them identity and makes interactions clearer. Well-chosen names enhance the readability of your project.",
            "\nEXPLANATION:\nThink of naming sprites like assigning roles in a play: each name should reflect the sprite's purpose. This organization improves the overall structure and comprehension of your project.",
            "\nEXPLANATION:\nNaming sprites is like naming instruments in an orchestra: it ensures each part plays its intended role harmoniously. Clarity in naming enhances project management and development.",
            "\nEXPLANATION:\nConsider sprite naming as labeling ingredients in a recipe: it makes assembling your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
        ]

        # Select one of the motivational phrases to start
        rand_message_index = random.randint(0, len(self.motivational_phrases) - 1)
        message += self.motivational_phrases[rand_message_index]

        # First we have remove the first line
        sprite_list = dict_spriteNaming.splitlines()
        sprite_list = sprite_list[1:]

        # We have to create an message
        if (len(sprite_list) > 1):
            message += f" you have a lot of sprites with the default name, for example in your case you have {self.MAGENTA}{len(sprite_list)} sprites{self.RESET} with the default names. Look, the solution it's simple you have to change the default sprites names for more descriptive names."
        else:
            message += f" you have one sprite with the default name provided by Scratch, try change the sprite {self.MAGENTA}{sprite_list[0]}{self.RESET} name, for a more descriptive name according to the function of the sprite.";  

        # Select one of the explanation phrases of deadCode
        rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
        explanation += explanation_phrases[rand_explanation_index]

        # Select one of the farwell phrases
        rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
        farwell += self.farwells[rand_farwell_index]

        feedback = {
            'message': message,
            'blocks': [],  
            'explanation': explanation,
            'farwell': farwell,
        }
        return feedback   

    def recomender_backdrop(self, dict_backdropNaming) -> dict:
        message = ""
        explanation = ""
        farwell = ""
        backdrop_list = []

        explanation_phrases = [
            "\nEXPLANATION:\nGiving meaningful names to backdrops is like labeling the rooms in a house: it helps you quickly identify each environment. Clear names make your project easier to organize and navigate.",
            "\nEXPLANATION:\nNaming backdrops is like titling the scenes in a movie: it provides context and enhances the understanding of the story's progression. Appropriate names make your project more intuitive.",
            "\nEXPLANATION:\nThink of naming backdrops like designating locations on a map: each name should clearly indicate its purpose. This improves the overall structure and facilitates the comprehension of the project.",
            "\nEXPLANATION:\nNaming backdrops is like putting signs in a theme park: it ensures that each area is well-identified and visitors don't get lost. Clarity in naming enhances project management and user experience.",
            "\nEXPLANATION:\nConsider naming backdrops like labeling the different sections of a magazine: it makes navigating your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
        ]

        # Select one of the motivational phrases to start
        rand_message_index = random.randint(0, len(self.motivational_phrases) - 1)
        message += self.motivational_phrases[rand_message_index]

        # First we have remove the first line
        backdrop_list = dict_backdropNaming.splitlines()
        backdrop_list = backdrop_list[1:]

        # We have to create an message
        if (len(backdrop_list) > 1):
            message += f" you have a lot of backdrops with the default name, for example in your case you have {self.MAGENTA}{len(backdrop_list)} backdrops{self.RESET} with the default names. Look, the solution it's simple you have to change the default backdrop names for more descriptive names."
        else:
            message += f" you have one backdrop with the default name provided by Scratch, try change the sprite {self.MAGENTA}{backdrop_list[0]}{self.RESET} name, for a more descriptive name according to the aspect of the backdrop.";  

        # Select one of the explanation phrases of deadCode
        rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
        explanation += explanation_phrases[rand_explanation_index]

        # Select one of the farwell phrases
        rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
        farwell += self.farwells[rand_farwell_index]

        feedback = {
            'message': message,
            'blocks': [],  
            'explanation': explanation,
            'farwell': farwell,
        }
        return feedback    