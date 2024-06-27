import random


class RecomenderSystem():
    """
    Recomender system for improve Scratch projects
    """

    # The variable below, indicates the last type of bad smell analyzed
    

    def __init__(self, curr_type=""):
        self.MAGENTA = "\033[95m"
        self.RESET = "\033[0m"
        self.GREEN = "\033[92m"

        self.curr_type = curr_type

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
        type = "deadCode"
        message = ""
        explanation = ""
        farwell = ""
        blocks_list = []
        deadCode_list = []

        is_dead_code = dict_deadCode['result'].get('total_dead_code_scripts', 1)
        if (is_dead_code != 0):
            # explanations lists about what is deadCode
            explanation_phrases = [
                "\nEXPLANATION:\nDead code is like having unused blocks scattered on the floor: it makes everything more cluttered and harder to understand. By removing it, your project will be cleaner, easier to understand, and work better.",
                "\nEXPLANATION:\nHaving dead code is like having broken toys in your room: they are useless and just take up space. By removing them, everything will be more organized.",
                "\nEXPLANATION:\nDead code is like having old papers on your desk: they distract you and make it hard to find what you need. By getting rid of them, you will work better.",
                "\nEXPLANATION:\nDead code is like having clothes you no longer wear in your closet: it just takes up space and makes everything look messy. Removing it makes everything easier to manage.",
                "\nEXPLANATION:\nDead code is like having trash in your backpack: it's useless and just gets in the way. By cleaning it out, you find everything faster and it's easier to use.",
            ]

            message += self.upgrade_feedback(type)

            # Calc total deadCode
            tot_deadCode = 0
            for sprite in dict_deadCode["result"]["list_dead_code_scripts"][0]:
                print("sprite-----------------------------------------")
                print(sprite)
                tot_deadCode += len(dict_deadCode["result"]["list_dead_code_scripts"][0][sprite])

            # Search the deadCode of the dict and make phrase
            deadCode_list = dict_deadCode["result"]["list_dead_code_scripts"][0]
            if (tot_deadCode > 1): #Only one sprite with deadCode (maybe multiple blocks)
                message += f" you haven't used a lot of blocks in different sprites, maybe it would be a good idea to remove it, you agree?\nTry removing the following blocks: "

            for sprite, blocks in deadCode_list.items():
                if sprite not in ("deadCode", "number"):
                    if (tot_deadCode == 1): #Only one sprite with deadCode (maybe multiple blocks)
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
                'type': type,
                'message': message,
                'blocks': blocks_list,  
                'explanation': explanation,
                'farwell': farwell,
            }
        else:
            feedback = None
        return feedback
    
    def recomender_sprite(self, dict_spriteNaming) -> dict:
        type = "Sprites"
        message = ""
        explanation = ""
        farwell = ""
        sprite_list = []

        # First we have remove the first line
        sprite_list = dict_spriteNaming.splitlines()
        sprite_list = sprite_list[1:]

        if (len(sprite_list) !=  0):
            explanation_phrases = [
                "\nEXPLANATION:\nGiving meaningful names to sprites is like labeling items in your toolbox: it helps you quickly find what you need. Clear names make your project easier to understand and navigate.",
                "\nEXPLANATION:\nNaming sprites is like naming characters in a story: it gives them identity and makes interactions clearer. Well-chosen names enhance the readability of your project.",
                "\nEXPLANATION:\nThink of naming sprites like assigning roles in a play: each name should reflect the sprite's purpose. This organization improves the overall structure and comprehension of your project.",
                "\nEXPLANATION:\nNaming sprites is like naming instruments in an orchestra: it ensures each part plays its intended role harmoniously. Clarity in naming enhances project management and development.",
                "\nEXPLANATION:\nConsider sprite naming as labeling ingredients in a recipe: it makes assembling your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
            ]

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # We have to create an message
            if (len(sprite_list) > 1):
                sprites = ", ".join(sprite_list)
                message += f" you have a lot of sprites with the default name, for example in your case you have {self.MAGENTA}{len(sprite_list)} sprites{self.RESET} with the default names. Look, the solution it's simple, try to change the names of {self.MAGENTA}{sprites}{self.RESET} for a more descriptive names according to their functionalities."
            else:
                message += f" you have one sprite with the default name provided by Scratch, try change the sprite {self.MAGENTA}{sprite_list[0]}{self.RESET} name, for a more descriptive name according to the function of the sprite.";  

            # Select one of the explanation phrases of deadCode
            rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
            explanation += explanation_phrases[rand_explanation_index]

            # Select one of the farwell phrases
            rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
            farwell += self.farwells[rand_farwell_index]

            feedback = {
                'type': type,
                'message': message,
                'blocks': [],  
                'explanation': explanation,
                'farwell': farwell,
            }
        else:
            feedback = None
        return feedback   

    def recomender_backdrop(self, dict_backdropNaming) -> dict:
        type = "Backdrops"
        message = ""
        explanation = ""
        farwell = ""
        backdrop_list = []

        # First we have remove the first line
        backdrop_list = dict_backdropNaming.splitlines()
        backdrop_list = backdrop_list[1:]

        if (len(backdrop_list) != 0):
            explanation_phrases = [
                "\nEXPLANATION:\nGiving meaningful names to backdrops is like labeling the rooms in a house: it helps you quickly identify each environment. Clear names make your project easier to organize and navigate.",
                "\nEXPLANATION:\nNaming backdrops is like titling the scenes in a movie: it provides context and enhances the understanding of the story's progression. Appropriate names make your project more intuitive.",
                "\nEXPLANATION:\nThink of naming backdrops like designating locations on a map: each name should clearly indicate its purpose. This improves the overall structure and facilitates the comprehension of the project.",
                "\nEXPLANATION:\nNaming backdrops is like putting signs in a theme park: it ensures that each area is well-identified and visitors don't get lost. Clarity in naming enhances project management and user experience.",
                "\nEXPLANATION:\nConsider naming backdrops like labeling the different sections of a magazine: it makes navigating your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
            ]

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)
            
            # We have to create an message
            if (len(backdrop_list) > 1):
                backdrops = ", ".join(backdrop_list)
                message += f" you have a lot of backdrops with the default name, for example in your case you have {self.MAGENTA}{len(backdrop_list)} backdrops{self.RESET} with the default names. Look, the solution it's simple you have to change the names of {backdrops} for a more descriptive names according to their aspect."
            else:
                message += f" you have one backdrop with the default name provided by Scratch, try change the backdrop {self.MAGENTA}{backdrop_list[0]}{self.RESET} name, for a more descriptive name according to the aspect of the backdrop.";  

            # Select one of the explanation phrases of deadCode
            rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
            explanation += explanation_phrases[rand_explanation_index]

            # Select one of the farwell phrases
            rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
            farwell += self.farwells[rand_farwell_index]

            feedback = {
                'type': type,
                'message': message,
                'blocks': [],  
                'explanation': explanation,
                'farwell': farwell,
            }
        else:
            feedback = None
        return feedback    
    
    def recomender_duplicatedScripts(self, dict_duplicatedScripts, dict_refactoredDups) ->dict:
        type = "Duplicates"
        message = ""
        explanation = ""
        farwell = ""
        blocks = []
        duplicatedScripts = 0
        dup_list = []

        # Calc the number of duplicatedScripts
        for scripts in dict_refactoredDups: # scripts has all the duplicatedScripts in a individual sprite
            dup_list = scripts['original'].split("\nend\n\n\n")
            duplicatedScripts += len(dup_list)

        if (duplicatedScripts != 0):
            # Explanation phrases for duplicated scripts
            explanation_phrases = [
                "\nEXPLANATION:\nImagine that in a project we have two scripts composed of the same blocks but with different parameters or values. What happens if we need to make a small change? We would have to modify both scripts, complicating code maintenance. In such situations, it is more appropriate for the programmer to create a custom block that defines this behavior and use this new block wherever needed.",
                "\nEXPLANATION:\nDuplicated scripts are like having multiple copies of the same recipe with slight ingredient variations. If you change one ingredient, you have to update all copies, which is cumbersome. Instead, create a master recipe and refer to it wherever needed.",
                "\nEXPLANATION:\nHaving duplicated scripts is like having several identical tools in your toolbox with minor differences. If one breaks or needs adjustment, you must fix each one individually. A better approach is to have a single tool with adjustable settings.",
                "\nEXPLANATION:\nThink of duplicated scripts like writing the same instructions for different tasks. If you need to update the instructions, you must rewrite them for each task, which is inefficient. Instead, write a single set of instructions and refer to them as needed.",
                "\nEXPLANATION:\nDuplicated scripts are like painting multiple walls the same color but with different brands of paint. If you decide to change the color, you need to repaint each wall separately. Using a consistent paint allows for easier changes and maintenance.",
            ]

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # Create a message for duplicatedScripts
            message += f" you have {self.MAGENTA}{duplicatedScripts} scripts duplicated{self.RESET} in your code, this is that you have the sames blocks repeated, you can use one of those instead of duplicate it.\n \nBut don't worry let's solve that, for now we are going to try to solve only a few. Look this is so simple, down this text you have a selector with arrows, in the tab {self.MAGENTA}1{self.RESET} you can see your duplicated code, and in the tab {self.MAGENTA}2{self.RESET} you can see the code refactorized, you only have to replace the duplicated code with the code refactorized in your project."

            # First we have remove the first line
            dup_script = dict_refactoredDups[0]['original']
            dup_script_sprite = dict_refactoredDups[0]['sprite']
            blocks.append((f"{dup_script}", f"This is the {self.MAGENTA}duplicated code{self.RESET} that you have in your project and it's located in the sprite {self.MAGENTA}{dup_script_sprite}{self.RESET}."))

            refactor_script = dict_refactoredDups[0]['refactored']
            blocks.append((f"{refactor_script}", f"This is the {self.MAGENTA}refactorized code{self.RESET} to avoid the duplicated code in your project."))

            # Select one of the explanation phrases of deadCode
            rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
            explanation += explanation_phrases[rand_explanation_index]

            # Select one of the farwell phrases
            rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
            farwell += self.farwells[rand_farwell_index]

            feedback = {
                'type': type,
                'message': message,
                'blocks': blocks,  
                'explanation': explanation,
                'farwell': farwell,
            }
        else:
            feedback = None
        return feedback   
    
    def upgrade_feedback(self, new_type: str) -> str:
        """
        This function see what was the last type of bad smell analyzed for see
        if the user has solved it. And if not uses the default messages.
        """
        new_message = ""

        if (self.curr_type != ""):
            if (self.curr_type == "Backdrops"):
                fail_message = "Oooops, it's seem's that you havent solved the problem with the backdrop naming, but don't worry, we are going to review again how we could solve it,"
                success_message = "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE BACKDROP NAMING, thats is very great news! Does it seem good to you if we keep improving the project?"
            if (self.curr_type == "Sprites"):
                fail_message = "Oooops, it's seem's that you havent solved the problem with the sprite naming, but don't worry, we are going to review again how we could solve it,"
                success_message = "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE SPRITE NAMING, thats is very great news! Does it seem good to you if we keep improving the project?"
            if (self.curr_type == "deadCode"):
                fail_message = "Oooops, it's seem's that you havent solved the problem with the dead code, but don't worry, we are going to review again how we could solve it,"
                success_message = "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DEAD CODE, thats is very great news! Does it seem good to you if we keep improving the project?"
            if (self.curr_type == "Duplicates"):
                fail_message = "Oooops, it's seem's that you havent solved the problem with the duplicated code already, but don't worry, we are going to review again how we could solve it,"
                success_message = "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DUPLICATED CODE, thats is very great news! Does it seem good to you if we keep improving the project?"
            
            # Current Order: Backdrop, Sprites, DeadCode, Duplicates
            bad_smells_order = ['Backdrops','Sprites','deadCode','Duplicates']
            currIndex = bad_smells_order.index(self.curr_type)
            newIndex = bad_smells_order.index(new_type)
            if (currIndex == newIndex):
                #new_message = "{}\n{}".format(fail_message, curr_message)
                new_message = fail_message
            else:
                #new_message = "{}\n{}".format(success_message, curr_message)
                new_message = success_message
        else: 
            # Select one of the motivational phrases to start
            rand_message_index = random.randint(0, len(self.motivational_phrases) - 1)
            new_message += self.motivational_phrases[rand_message_index]    
        return new_message