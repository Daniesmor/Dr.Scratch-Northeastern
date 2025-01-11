import random
from django.utils.translation import get_language
from .recomender_phrases import LanguageManager

class RecomenderSystem():
    """
    Recomender system for improve Scratch projects
    """    

    def __init__(self, curr_type=""):
        self.MAGENTA = "\033[95m"
        self.RESET = "\033[0m"
        self.GREEN = "\033[92m"

        self.curr_lan = get_language()
        self.curr_type = curr_type
        self.language_manager = LanguageManager()


        print(f"{self.MAGENTA}Welcome to the recomender system engine{self.RESET}")

        self.motivational_phrases = self.language_manager.motivational_phrases
        self.farwells = self.language_manager.farwells

        print(self.motivational_phrases)
        print(self.farwells)

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
            explanation_phrases = self.language_manager.deadcode_explanation_phrases

            message += self.upgrade_feedback(type)

            # Calc total deadCode
            tot_deadCode = 0
            for sprite in dict_deadCode["result"]["list_dead_code_scripts"][0]:
                tot_deadCode += len(dict_deadCode["result"]["list_dead_code_scripts"][0][sprite])

            # Search the deadCode of the dict and make phrase
            deadCode_list = dict_deadCode["result"]["list_dead_code_scripts"][0]
            if (tot_deadCode > 1): #Only one sprite with deadCode (maybe multiple blocks)
                if self.curr_lan == 'en':
                    message += f" you haven't used a lot of blocks in different sprites, maybe it would be a good idea to remove them, do you agree?\nTry removing the following blocks: "
                elif self.curr_lan == 'es':
                    message += f" no has utilizado muchos bloques en diferentes sprites, quizás sería una buena idea eliminarlos, ¿estás de acuerdo?\nIntenta eliminar los siguientes bloques: "

            for sprite, script_dicc in deadCode_list.items():
                for script_name, scripts in script_dicc.items():
                    if tot_deadCode == 1:
                        if self.curr_lan == 'en':
                            message += f" you haven't used one block in the sprite {self.MAGENTA}{sprite}{self.RESET}, maybe it would be a good idea to remove it, do you agree?\nTry removing the block: "
                        elif self.curr_lan == 'es':
                            message += f" no has utilizado un bloque en el sprite {self.MAGENTA}{sprite}{self.RESET}, quizás sería una buena idea eliminarlo, ¿estás de acuerdo?\nIntenta eliminar el bloque: "
                    for block in scripts:
                        if self.curr_lan == 'en':
                            blocks_list.append((f"{block}", f"This block is in the sprite {self.MAGENTA}{sprite}{self.RESET}:"))
                        elif self.curr_lan == 'es':
                            blocks_list.append((f"{block}", f"Este bloque está en el sprite {self.MAGENTA}{sprite}{self.RESET}:"))
            
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
            explanation_phrases = self.language_manager.sprite_explanation_phrases

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # We have to create an message
            if (len(sprite_list) > 1):
                sprites = ", ".join(sprite_list)
                if (self.curr_lan == 'en'):
                    message += f" you have a lot of sprites with the default name, for example in your case you have {self.MAGENTA}{len(sprite_list)} sprites{self.RESET} with the default names. To solve it, try to change the names of {self.MAGENTA}{sprites}{self.RESET} for a more descriptive names according to their functionalities."
                elif (self.curr_lan == 'es'):
                    message += f" tienes muchos sprites con el nombre por defecto, por ejemplo en tu caso tienes {self.MAGENTA}{len(sprite_list)} sprites{self.RESET} con nombres por defecto. Mira, para solucionarlo, intenta cambiar los nombres de {self.MAGENTA}{sprites}{self.RESET} por nombres más descriptivos según sus funcionalidades."
            else:
                if self.curr_lan == 'en':
                    message += f" you have one sprite with the default name provided by Scratch, try to change the sprite {self.MAGENTA}{sprite_list[0]}{self.RESET} name for a more descriptive name according to the function of the sprite."
                elif self.curr_lan == 'es':
                    message += f" tienes un sprite con el nombre por defecto proporcionado por Scratch, intenta cambiar el nombre del sprite {self.MAGENTA}{sprite_list[0]}{self.RESET} por un nombre más descriptivo según la función del sprite."

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
            explanation_phrases = self.language_manager.backdrop_explanation_phrases

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)
            
            # We have to create an message
            if (len(backdrop_list) > 1):
                backdrops = ", ".join(backdrop_list)
                if self.curr_lan == 'en':
                    message += f" you have a lot of backdrops with the default name, for example in your case you have {self.MAGENTA}{len(backdrop_list)} backdrops{self.RESET} with the default names. To solve it, you have to change the names of {backdrops} for more descriptive names."
                elif self.curr_lan == 'es':
                    message += f" tienes muchos fondos con el nombre por defecto, por ejemplo en tu caso tienes {self.MAGENTA}{len(backdrop_list)} fondos{self.RESET} con nombres por defecto. Mira, para solucionarlo, debes cambiar los nombres de {backdrops} por nombres más descriptivos."
            else:
                if self.curr_lan == 'en':
                    message += f" you have one backdrop with the default name provided by Scratch, try changing the backdrop {self.MAGENTA}{backdrop_list[0]}{self.RESET} name, for a more descriptive name."
                elif self.curr_lan == 'es':
                    message += f" tienes un fondo con el nombre por defecto proporcionado por Scratch, intenta cambiar el nombre del fondo {self.MAGENTA}{backdrop_list[0]}{self.RESET} por un nombre más descriptivo."

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
            explanation_phrases = self.language_manager.duplicated_explanation_phrases

            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # Create a message for duplicatedScripts
            if duplicatedScripts > 1:
                if self.curr_lan == 'en':
                    message += f" you have {self.MAGENTA}{duplicatedScripts} scripts duplicated{self.RESET} in your code, this means you have the same blocks repeated. Instead of duplicating code, you can use one instance of it.\n \nBut don't worry, let's solve that. For now, we will try to solve just a few. To solve it: below this text, you have a selector with arrows. In tab {self.MAGENTA}1{self.RESET}, you can see your duplicated code, and in tab {self.MAGENTA}2{self.RESET}, you can see the refactored code. You just need to replace the duplicated code with the refactored code in your project."
                elif self.curr_lan == 'es':
                    message += f" tienes {self.MAGENTA}{duplicatedScripts} scripts duplicados{self.RESET} en tu código, lo que significa que tienes los mismos bloques repetidos. En lugar de duplicar código, puedes usar una sola instancia de él.\n \nPero no te preocupes, vamos a solucionarlo. Por ahora, intentaremos resolver solo unos pocos. Para solucionarlo: debajo de este texto, tienes un selector con flechas. En la pestaña {self.MAGENTA}1{self.RESET}, puedes ver tu código duplicado, y en la pestaña {self.MAGENTA}2{self.RESET}, puedes ver el código refactorizado. Solo necesitas reemplazar el código duplicado con el código refactorizado en tu proyecto."
            elif duplicatedScripts == 1:
                if self.curr_lan == 'en':
                    message += f" you have one script duplicated{self.RESET} in your code, this means you have the same blocks repeated. Instead of duplicating code, you can use one instance of it.\n \nBut don't worry, let's solve that. For now, we will try to solve just a few. To solve it: below this text, you have a selector with arrows. In tab {self.MAGENTA}1{self.RESET}, you can see your duplicated code, and in tab {self.MAGENTA}2{self.RESET}, you can see the refactored code. You just need to replace the duplicated code with the refactored code in your project."
                elif self.curr_lan == 'es':
                    message += f" tienes un script duplicado{self.RESET} en tu código, lo que significa que tienes los mismos bloques repetidos. En lugar de duplicar código, puedes usar una sola instancia de él.\n \nPero no te preocupes, vamos a solucionarlo. Por ahora, intentaremos resolver solo unos pocos. Para solucionarlo: debajo de este texto, tienes un selector con flechas. En la pestaña {self.MAGENTA}1{self.RESET}, puedes ver tu código duplicado, y en la pestaña {self.MAGENTA}2{self.RESET}, puedes ver el código refactorizado. Solo necesitas reemplazar el código duplicado con el código refactorizado en tu proyecto."


            # First we have remove the first line
            dup_script = dict_refactoredDups[0]['original']
            dup_script_sprite = dict_refactoredDups[0]['sprite']
            if self.curr_lan == 'en':
                blocks.append((f"{dup_script}", f"This is the {self.MAGENTA}duplicated code{self.RESET} that you have in your project and it's located in the sprite {self.MAGENTA}{dup_script_sprite}{self.RESET}."))
            elif self.curr_lan == 'es':
                blocks.append((f"{dup_script}", f"Este es el {self.MAGENTA}código duplicado{self.RESET} que tienes en tu proyecto y está ubicado en el sprite {self.MAGENTA}{dup_script_sprite}{self.RESET}."))

            refactor_script = dict_refactoredDups[0]['refactored']
            if self.curr_lan == 'en':
                blocks.append((f"{refactor_script}", f"This is the {self.MAGENTA}refactorized code{self.RESET} to avoid duplicated code in your project."))
            elif self.curr_lan == 'es':
                blocks.append((f"{refactor_script}", f"Este es el {self.MAGENTA}código refactorizado{self.RESET} para evitar código duplicado en tu proyecto."))

            # Select one of the explanation phrases of deadCode
            rand_explanation_index = random.randint(0, len(explanation_phrases) - 1) 
            explanation += explanation_phrases[rand_explanation_index]

            # Select one of the farwell phrases
            rand_farwell_index = random.randint(0, len(self.farwells) - 1) 
            farwell += self.farwells[rand_farwell_index]

            print("mis bloques")
            print(blocks)

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
    
    def recomender_sequentialBlocks(self, original_dict, refactor_dict):
        type = "Sequential"
        message = ""
        explanation = ""
        farwell = ""
        blocks = []
        sequentialBlocks = original_dict.get('result').get('total_sequential')
        seq_original = [{'sprite': entry['sprite'], 'code': entry['original'], 'repetitions': entry['repetitions']} for entry in refactor_dict]
        seq_refactor = [{'sprite': entry['sprite'], 'code': entry['refactored']} for entry in refactor_dict]

        print("PEPE:", seq_original)

        if sequentialBlocks != 0:
            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # Create a message for duplicatedScripts
            if sequentialBlocks > 1:
                if self.curr_lan == 'en':
                    message += f" you have {self.MAGENTA}{sequentialBlocks} sequences of blocks{self.RESET} in your code, which means you have the same actions repeated multiple times. Instead of repeating the same blocks, you can use a loop to simplify your code.\n\nBut don't worry, let's fix that. For now, we will try to solve just a few. To solve it: below this text, you have a selector with arrows. In tab {self.MAGENTA}1{self.RESET}, you can see your sequence of blocks, and in tab {self.MAGENTA}2{self.RESET}, you can see the refactored version with loops. You just need to replace the sequences of blocks with the refactored version in your project."
                elif self.curr_lan == 'es':
                    message += f" tienes {self.MAGENTA}{sequentialBlocks} secuencias de bloques{self.RESET} en tu código, lo que significa que tienes las mismas acciones repetidas múltiples veces. En lugar de repetir los mismos bloques, puedes usar un bucle para simplificar tu código.\n\nPero no te preocupes, vamos a solucionarlo. Por ahora, intentaremos resolver solo unos pocos. Para solucionarlo: debajo de este texto, tienes un selector con flechas. En la pestaña {self.MAGENTA}1{self.RESET}, puedes ver tu secuencia de bloques, y en la pestaña {self.MAGENTA}2{self.RESET}, puedes ver la versión refactorizada con bucles. Solo necesitas reemplazar las secuencias de bloques con la versión refactorizada en tu proyecto."
            elif sequentialBlocks == 1:
                if self.curr_lan == 'en':
                    message += f" you have {self.MAGENTA}{sequentialBlocks} sequence of blocks{self.RESET} in your code, which means you have the same actions repeated multiple times. Instead of repeating the same blocks, you can use a loop to simplify your code.\n\nBut don't worry, let's fix that. To solve it: below this text, you have a selector with arrows. In tab {self.MAGENTA}1{self.RESET}, you can see your sequence of blocks, and in tab {self.MAGENTA}2{self.RESET}, you can see the refactored version with loops. You just need to replace the sequence of blocks with the refactored version in your project."
                elif self.curr_lan == 'es':
                    message += f" tienes {self.MAGENTA}{sequentialBlocks} secuencia de bloques{self.RESET} en tu código, lo que significa que tienes las mismas acciones repetidas múltiples veces. En lugar de repetir los mismos bloques, puedes usar un bucle para simplificar tu código.\n\nPero no te preocupes, vamos a solucionarlo. Para solucionarlo: debajo de este texto, tienes un selector con flechas. En la pestaña {self.MAGENTA}1{self.RESET}, puedes ver tu secuencia de bloques, y en la pestaña {self.MAGENTA}2{self.RESET}, puedes ver la versión refactorizada con bucles. Solo necesitas reemplazar la secuencia de bloques con la versión refactorizada en tu proyecto."
            
            if self.curr_lan == 'en':
                blocks.append((f"{seq_original[0].get('code')}", f"You have this {self.MAGENTA}sequence of blocks{self.RESET} repeated {seq_original[0].get('repetitions')} times in a row in the sprite {self.MAGENTA}{seq_original[0].get('sprite')}{self.RESET}."))
                blocks.append((f"{seq_refactor[0].get('code')}", f"This is the {self.MAGENTA}refactorized code{self.RESET} to avoid sequential blocks in your project."))

            elif self.curr_lan == 'es':
                blocks.append((f"{seq_original[0].get('code')}", f"Tienes esta {self.MAGENTA}secuencia de bloques{self.RESET} repetida {seq_original[0].get('repetitions')} veces seguidas en el sprite {self.MAGENTA}{seq_original[0].get('sprite')}{self.RESET}."))
                blocks.append((f"{seq_refactor[0].get('code')}", f"Este es el {self.MAGENTA}código refactorizado{self.RESET} para evitar secuencias de bloques largas en tu proyecto."))

            explanation += self.language_manager.sequential_explanation_phrases[random.randint(0, len(self.language_manager.sequential_explanation_phrases) - 1) ]

            farwell += self.farwells[random.randint(0, len(self.farwells) - 1)]

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
                fail_message = self.language_manager.upgrade_feedback_phrases['Backdrops']['fail']
                success_message = self.language_manager.upgrade_feedback_phrases['Backdrops']['success']
            if (self.curr_type == "Sprites"):
                fail_message = self.language_manager.upgrade_feedback_phrases['Sprites']['fail']
                success_message = self.language_manager.upgrade_feedback_phrases['Sprites']['success']
            if (self.curr_type == "deadCode"):
                fail_message = self.language_manager.upgrade_feedback_phrases['deadCode']['fail']
                success_message = self.language_manager.upgrade_feedback_phrases['deadCode']['success']
            if (self.curr_type == "Duplicates"):
                fail_message = self.language_manager.upgrade_feedback_phrases['Duplicates']['fail']
                success_message = self.language_manager.upgrade_feedback_phrases['Duplicates']['success']
            if (self.curr_type == "Sequential"):
                fail_message = self.language_manager.upgrade_feedback_phrases['Sequential']['fail']
                success_message = self.language_manager.upgrade_feedback_phrases['Sequential']['success']
            
            # Current Order: Backdrop, Sprites, DeadCode, Duplicates, Sequential
            bad_smells_order = ['Backdrops','Sprites','deadCode','Duplicates', 'Sequential']
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