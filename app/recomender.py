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
    
    def recomender_longScripts(self, dict_long) -> dict:
        type = "longScripts"
        message = ""
        explanation = ""
        farwell = ""
        total_long_blocks = dict_long.get('result').get('total_long_blocks')
        blocks_list = []
        long_scripts_list = dict_long.get('result').get('list_long_blocks')

        if (total_long_blocks != 0):

            message += self.upgrade_feedback(type)

            if (total_long_blocks > 1):
                if self.curr_lan == 'en':
                    message += f" you have more than one long script in your project, maybe it would be a good idea to remove them, do you agree?\nTry refactoring the following long scripts: "
                elif self.curr_lan == 'es':
                    message += f" tienes más de un script largo en tu proyectto, quizás sería una buena idea eliminarlos, ¿estás de acuerdo?\nIntenta modificar los siguientes scripts largos: "
            else:
                if self.curr_lan == 'en':
                    message += f" you have one long script in the sprite {self.MAGENTA}{dict_long.get('result').get('list_long_blocks')[0].get('sprite')}{self.RESET}, maybe it would be a good idea to remove it, do you agree?\nTry refactoring the script: "
                elif self.curr_lan == 'es':
                    message += f" tienes un script largo en el sprite {self.MAGENTA}{dict_long.get('result').get('list_long_blocks')[0].get('sprite')}{self.RESET}, quizás sería una buena idea eliminarlo, ¿estás de acuerdo?\nIntenta modificar el script: "

            if self.curr_lan == 'en':
                blocks_list.append((f"{long_scripts_list[0].get('script_text')}", f"You have this {self.MAGENTA}long script{self.RESET} with a size of {long_scripts_list[0].get('script_length')} blocks in the sprite {self.MAGENTA}{long_scripts_list[0].get('sprite')}{self.RESET}."))
            elif self.curr_lan == 'es':
                blocks_list.append((f"{long_scripts_list[0].get('script_text')}", f"Tienes este {self.MAGENTA}script largo{self.RESET} con un tamaño de {long_scripts_list[0].get('script_length')} bloques en el sprite {self.MAGENTA}{long_scripts_list[0].get('sprite')}{self.RESET}."))            
            
            explanation += self.language_manager.longScripts_explanation_phrases[random.randint(0, len(self.language_manager.longScripts_explanation_phrases) - 1) ]

            farwell += self.farwells[random.randint(0, len(self.farwells) - 1)]

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
    
    def recommender_message(self, dict_messageNaming):
        type = "Messages"
        message = ""
        explanation = ""
        farwell = ""
        message_list = [line.strip() for line in dict_messageNaming.splitlines()[1:]]

        if (len(message_list) != 0):
            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # We have to create an message
            if (len(message_list) > 1):
                messages = ", ".join(message_list)
                if self.curr_lan == 'en':
                    message += f" you have a lot of broadcasts with the default name, for example in your case you have {self.MAGENTA}{len(message_list)} broadcasts{self.RESET} with the default names. To solve it, you have to change the names of {messages} for more descriptive names."
                elif self.curr_lan == 'es':
                    message += f" tienes muchos mensajes con el nombre por defecto, por ejemplo en tu caso tienes {self.MAGENTA}{len(message_list)} mensajes{self.RESET} con nombres por defecto. Mira, para solucionarlo, debes cambiar los nombres de {messages} por nombres más descriptivos."
            else:
                if self.curr_lan == 'en':
                    message += f" you have one broadcast with the default name provided by Scratch, try changing the broadcast {self.MAGENTA}{message_list[0]}{self.RESET} name, for a more descriptive name."
                elif self.curr_lan == 'es':
                    message += f" tienes un mensaje con el nombre por defecto proporcionado por Scratch, intenta cambiar el nombre del mensaje {self.MAGENTA}{message_list[0]}{self.RESET} por un nombre más descriptivo."


            explanation += self.language_manager.messages_explanation_phrases[random.randint(0, len(self.language_manager.messages_explanation_phrases) - 1) ]
            farwell += self.farwells[random.randint(0, len(self.farwells) - 1)]

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
    
    def recommender_variables(self, dict_variablesNaming):
        type = "Variables"
        message = ""
        explanation = ""
        farwell = ""
        variables_list = [line.strip() for line in dict_variablesNaming.splitlines()[1:]]

        if (len(variables_list) != 0):
            # Select one of the motivational phrases to start
            message += self.upgrade_feedback(type)

            # We have to create an message
            if (len(variables_list) > 1):
                variables = ", ".join(variables_list)
                if self.curr_lan == 'en':
                    message += f" you have a lot of variables with the default name, for example in your case you have {self.MAGENTA}{len(variables_list)} variables{self.RESET} with the default names. To solve it, you have to change the names of {variables} for more descriptive names."
                elif self.curr_lan == 'es':
                    message += f" tienes muchas variables con el nombre por defecto, por ejemplo en tu caso tienes {self.MAGENTA}{len(variables_list)} variables{self.RESET} con nombres por defecto. Mira, para solucionarlo, debes cambiar los nombres de {variables} por nombres más descriptivos."
            else:
                if self.curr_lan == 'en':
                    message += f" you have one variable with the default name provided by Scratch, try changing the variable {self.MAGENTA}{variables_list[0]}{self.RESET} name, for a more descriptive name."
                elif self.curr_lan == 'es':
                    message += f" tienes una variable con el nombre por defecto proporcionado por Scratch, intenta cambiar el nombre de la variable {self.MAGENTA}{variables_list[0]}{self.RESET} por un nombre más descriptivo."


            explanation += self.language_manager.variables_explanation_phrases[random.randint(0, len(self.language_manager.variables_explanation_phrases) - 1) ]
            farwell += self.farwells[random.randint(0, len(self.farwells) - 1)]

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
        sequentialBlocks = original_dict.get('result', {}).get('total_sequential', 0)
        
        if sequentialBlocks == 0:
            return None

        seq_original = [{
            'sprite': entry['sprite'], 
            'code': entry['original'], 
            'repetitions': entry['repetitions'], 
            'same_inputs': entry['same_inputs']
        } for entry in refactor_dict]
        
        seq_refactor = [{
            'sprite': entry['sprite'], 
            'code': entry['refactored']
        } for entry in refactor_dict]

        message = self.upgrade_feedback(type)

        same_inputs = seq_original[0]['same_inputs']
        
        # Diccionario con las palabras clave por idioma
        key_phrases_by_lang = {
            'en': ("loop", "loops", "function", "functions"),
            'es': ("bucle", "bucles", "función", "funciones"),
            'eu': ("begizta", "begiztak", "funtzio", "funtzioak"),
            'gl': ("bucle", "bucles", "función", "funcións"),
            'el': ("βρόχος", "βρόχοι", "συνάρτηση", "συναρτήσεις"),
            'pt': ("laço", "laços", "função", "funções"),
            'it': ("ciclo", "cicli", "funzione", "funzioni"),
            'ru': ("цикл", "циклы", "функция", "функции"),
            'ca': ("bucle", "bucles", "funció", "funcions"),
            'tr': ("döngü", "döngüler", "fonksiyon", "fonksiyonlar"),
        }

        # Obtener la palabra correcta según el idioma y si se usan loops o funciones
        key_phrase, key_phrase_plural, alt_phrase, alt_phrase_plural = key_phrases_by_lang.get(self.curr_lan, key_phrases_by_lang['en'])
        chosen_phrase = key_phrase if same_inputs else alt_phrase
        chosen_phrase_plural = key_phrase_plural if same_inputs else alt_phrase_plural

        messages = {
            'en': (
                f" you have {self.MAGENTA}{sequentialBlocks} sequence{'s' if sequentialBlocks > 1 else ''} of blocks{self.RESET} in your code, "
                f"which means you have the same actions repeated multiple times. Instead of repeating the same blocks, you can use a {chosen_phrase} to simplify your code.\n\n"
                "But don't worry, let's fix that. To solve it: below this text, you have a selector with arrows. "
                f"In tab {self.MAGENTA}1{self.RESET}, you can see your sequence of blocks, and in tab {self.MAGENTA}2{self.RESET}, "
                f"you can see the refactored version with {chosen_phrase_plural}. You just need to replace the sequence of blocks with the refactored version in your project."
            ),
            'es': (
                f" tienes {self.MAGENTA}{sequentialBlocks} secuencia{'s' if sequentialBlocks > 1 else ''} de bloques{self.RESET} en tu código, "
                f"lo que significa que tienes las mismas acciones repetidas múltiples veces. En lugar de repetir los mismos bloques, puedes usar un(a) {chosen_phrase} para simplificar tu código.\n\n"
                "Pero no te preocupes, vamos a solucionarlo. Para solucionarlo: debajo de este texto, tienes un selector con flechas. "
                f"En la pestaña {self.MAGENTA}1{self.RESET}, puedes ver tu secuencia de bloques, y en la pestaña {self.MAGENTA}2{self.RESET}, "
                f"puedes ver la versión refactorizada con {chosen_phrase_plural}. Solo necesitas reemplazar la secuencia de bloques con la versión refactorizada en tu proyecto."
            )
        }

        message += messages.get(self.curr_lan, messages['en'])

        blocks = [
            (
                seq_original[0]['code'], 
                f"Tienes esta {self.MAGENTA}secuencia de bloques{self.RESET} repetida {seq_original[0]['repetitions']} veces seguidas en el sprite {self.MAGENTA}{seq_original[0]['sprite']}{self.RESET}."
            ),
            (
                seq_refactor[0]['code'], 
                f"Este es el {self.MAGENTA}código refactorizado{self.RESET} para evitar secuencias de bloques largas en tu proyecto."
            )
        ] if self.curr_lan == 'es' else [
            (
                seq_original[0]['code'], 
                f"You have this {self.MAGENTA}sequence of blocks{self.RESET} repeated {seq_original[0]['repetitions']} times in a row in the sprite {self.MAGENTA}{seq_original[0]['sprite']}{self.RESET}."
            ),
            (
                seq_refactor[0]['code'], 
                f"This is the {self.MAGENTA}refactored code{self.RESET} to avoid sequential blocks in your project."
            )
        ]

        # Elegir una explicación aleatoria
        explanation_template = random.choice(self.language_manager.sequential_explanation_phrases)

        # Reemplazar todas las palabras clave en todos los idiomas
        for lang, (loop_sing, loop_plur, func_sing, func_plur) in key_phrases_by_lang.items():
            explanation_template = explanation_template.replace(loop_sing, chosen_phrase).replace(loop_plur, chosen_phrase_plural) \
                                                    .replace(func_sing, chosen_phrase).replace(func_plur, chosen_phrase_plural)

        explanation = explanation_template

        farwell = random.choice(self.farwells)

        return {
            'type': type,
            'message': message,
            'blocks': blocks,  
            'explanation': explanation,
            'farwell': farwell,
        }




    def upgrade_feedback(self, new_type: str) -> str:
        """
        This function see what was the last type of bad smell analyzed for see
        if the user has solved it. And if not uses the default messages.
        """
        new_message = ""

        if (self.curr_type != ""):
            fail_message = self.language_manager.upgrade_feedback_phrases.get(self.curr_type).get('fail')
            success_message = self.language_manager.upgrade_feedback_phrases.get(self.curr_type).get('success')
        
            # Current Order: Backdrop, Sprites, Messages, Variables, DeadCode, Duplicates, Sequential, LongScripts
            bad_smells_order = ['Backdrops','Sprites','Messages','Variables','deadCode','Duplicates','Sequential','longScripts']
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