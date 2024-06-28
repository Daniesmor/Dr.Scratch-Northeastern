from django.utils.translation import get_language

class LanguageManager:
    def __init__(self):
        self.curr_lan = get_language()

        # Definir las frases según el idioma actual
        self.motivational_phrases = self.get_motivational_phrases()
        self.farwells = self.get_farwells()
        self.duplicated_explanation_phrases = self.get_duplicated_explanation_phrases()
        self.deadcode_explanation_phrases = self.get_deadcode_explanation_phrases()
        self.sprite_explanation_phrases = self.get_sprite_explanation_phrases()
        self.backdrop_explanation_phrases = self.get_backdrop_explanation_phrases()
        self.upgrade_feedback_phrases = self.get_upgrade_feedback_phrases()

    def get_motivational_phrases(self):
        if self.curr_lan == 'en':
            return [
                "You are doing a very good job, it's amazing, but my cat-like sense of smell has detected that",
                "You are doing excellent work, it's impressive, but my cat-like sense of smell has detected that someone ate my tuna, or maybe it's that",
                "You're doing a fantastic job, it's wonderful, but my cat skills have detected a mouse nearby, or perhaps it might be that",
                "Your effort is outstanding, it's fascinating, but my feline instincts have identified that someone is keeping secrets in the litter box, or perhaps it might be that",
            ]
        elif self.curr_lan == 'es':
            return [
                "Estás haciendo un muy buen trabajo, es increíble, pero mi sentido del olfato felino ha detectado que",
                "Estás haciendo un trabajo excelente, es impresionante, pero mi sentido del olfato felino ha detectado que alguien se comió mi atún, o tal vez sea que",
                "Estás haciendo un trabajo fantástico, es maravilloso, pero mis habilidades de gato han detectado un ratón cerca, o tal vez sea que",
                "Tu esfuerzo es sobresaliente, es fascinante, pero mis instintos felinos han identificado que alguien está guardando secretos en la caja de arena, o tal vez sea que",
            ]
        else:
            return []

    def get_farwells(self):
        if self.curr_lan == 'en':
            return [
                "\nGood luck improving your project, you can do it!! :)",
                "\nKeep going with your project, you’re doing a great job! :)",
                "\nI’m sure your project will be a great success! :)",
                "\nDon’t give up, every effort brings you closer to your goal! :)",
                "\nI trust your abilities, you will improve your project! :)",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nBuena suerte mejorando tu proyecto, ¡puedes hacerlo! :)",
                "\nSigue adelante con tu proyecto, ¡estás haciendo un gran trabajo! :)",
                "\n¡Estoy seguro de que tu proyecto será un gran éxito! :)",
                "\nNo te rindas, ¡cada esfuerzo te acerca más a tu objetivo! :)",
                "\nConfío en tus habilidades, ¡mejorarás tu proyecto! :)",
            ]
        else:
            return []

    def get_duplicated_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nImagine that in a project we have two scripts composed of the same blocks but with different parameters or values. What happens if we need to make a small change? We would have to modify both scripts, complicating code maintenance. In such situations, it is more appropriate for the programmer to create a custom block that defines this behavior and use this new block wherever needed.",
                "\nEXPLANATION:\nDuplicated scripts are like having multiple copies of the same recipe with slight ingredient variations. If you change one ingredient, you have to update all copies, which is cumbersome. Instead, create a master recipe and refer to it wherever needed.",
                "\nEXPLANATION:\nHaving duplicated scripts is like having several identical tools in your toolbox with minor differences. If one breaks or needs adjustment, you must fix each one individually. A better approach is to have a single tool with adjustable settings.",
                "\nEXPLANATION:\nThink of duplicated scripts like writing the same instructions for different tasks. If you need to update the instructions, you must rewrite them for each task, which is inefficient. Instead, write a single set of instructions and refer to them as needed.",
                "\nEXPLANATION:\nDuplicated scripts are like painting multiple walls the same color but with different brands of paint. If you decide to change the color, you need to repaint each wall separately. Using a consistent paint allows for easier changes and maintenance.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nImagina que en un proyecto tenemos dos scripts compuestos por los mismos bloques pero con diferentes parámetros o valores. ¿Qué pasa si necesitamos hacer un pequeño cambio? Tendríamos que modificar ambos scripts, lo que complica el mantenimiento del código. En tales situaciones, es más apropiado que el programador cree un bloque personalizado que defina este comportamiento y use este nuevo bloque donde sea necesario.",
                "\nEXPLICACIÓN:\nLos scripts duplicados son como tener múltiples copias de la misma receta con ligeras variaciones en los ingredientes. Si cambias un ingrediente, tienes que actualizar todas las copias, lo cual es engorroso. En su lugar, crea una receta maestra y refiérete a ella donde sea necesario.",
                "\nEXPLICACIÓN:\nTener scripts duplicados es como tener varias herramientas idénticas en tu caja de herramientas con pequeñas diferencias. Si una se rompe o necesita ajuste, debes arreglar cada una individualmente. Un mejor enfoque es tener una única herramienta con configuraciones ajustables.",
                "\nEXPLICACIÓN:\nPiensa en los scripts duplicados como escribir las mismas instrucciones para diferentes tareas. Si necesitas actualizar las instrucciones, debes reescribirlas para cada tarea, lo cual es ineficiente. En su lugar, escribe un único conjunto de instrucciones y refiérete a ellas según sea necesario.",
                "\nEXPLICACIÓN:\nLos scripts duplicados son como pintar varias paredes del mismo color pero con diferentes marcas de pintura. Si decides cambiar el color, necesitas repintar cada pared por separado. Usar una pintura consistente permite cambios y mantenimiento más fáciles.",
            ]
        else:
            return []

    def get_deadcode_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nDead code is like having unused blocks scattered on the floor: it makes everything more cluttered and harder to understand. By removing it, your project will be cleaner, easier to understand, and work better.",
                "\nEXPLANATION:\nHaving dead code is like having broken toys in your room: they are useless and just take up space. By removing them, everything will be more organized.",
                "\nEXPLANATION:\nDead code is like having old papers on your desk: they distract you and make it hard to find what you need. By getting rid of them, you will work better.",
                "\nEXPLANATION:\nDead code is like having clothes you no longer wear in your closet: it just takes up space and makes everything look messy. Removing it makes everything easier to manage.",
                "\nEXPLANATION:\nDead code is like having trash in your backpack: it's useless and just gets in the way. By cleaning it out, you find everything faster and it's easier to use.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nEl código muerto es como tener bloques no utilizados esparcidos por el suelo: hace que todo sea más desordenado y difícil de entender. Al eliminarlo, tu proyecto estará más limpio, será más fácil de entender y funcionará mejor.",
                "\nEXPLICACIÓN:\nTener código muerto es como tener juguetes rotos en tu habitación: son inútiles y solo ocupan espacio. Al eliminarlos, todo estará más organizado.",
                "\nEXPLICACIÓN:\nEl código muerto es como tener papeles viejos en tu escritorio: te distraen y hacen que sea difícil encontrar lo que necesitas. Al deshacerte de ellos, trabajarás mejor.",
                "\nEXPLICACIÓN:\nEl código muerto es como tener ropa que ya no usas en tu armario: solo ocupa espacio y hace que todo se vea desordenado. Al eliminarla, todo es más fácil de manejar.",
                "\nEXPLICACIÓN:\nEl código muerto es como tener basura en tu mochila: es inútil y solo estorba. Al limpiarla, encuentras todo más rápido y es más fácil de usar.",
            ]
        else:
            return []

    def get_sprite_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nGiving meaningful names to sprites is like labeling items in your toolbox: it helps you quickly find what you need. Clear names make your project easier to understand and navigate.",
                "\nEXPLANATION:\nNaming sprites is like naming characters in a story: it gives them identity and makes interactions clearer. Well-chosen names enhance the readability of your project.",
                "\nEXPLANATION:\nThink of naming sprites like assigning roles in a play: each name should reflect the sprite's purpose. This organization improves the overall structure and comprehension of your project.",
                "\nEXPLANATION:\nNaming sprites is like naming instruments in an orchestra: it ensures each part plays its intended role harmoniously. Clarity in naming enhances project management and development.",
                "\nEXPLANATION:\nConsider sprite naming as labeling ingredients in a recipe: it makes assembling your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nDar nombres significativos a los sprites es como etiquetar los objetos en tu caja de herramientas: te ayuda a encontrar rápidamente lo que necesitas. Nombres claros hacen que tu proyecto sea más fácil de entender y navegar.",
                "\nEXPLICACIÓN:\nNombrar sprites es como nombrar personajes en una historia: les da identidad y hace que las interacciones sean más claras. Nombres bien elegidos mejoran la legibilidad de tu proyecto.",
                "\nEXPLICACIÓN:\nPiensa en nombrar sprites como asignar roles en una obra de teatro: cada nombre debe reflejar el propósito del sprite. Esta organización mejora la estructura general y la comprensión de tu proyecto.",
                "\nEXPLICACIÓN:\nNombrar sprites es como nombrar instrumentos en una orquesta: asegura que cada parte juegue su papel previsto de manera armoniosa. La claridad en los nombres mejora la gestión y el desarrollo del proyecto.",
                "\nEXPLICACIÓN:\nConsidera el nombramiento de sprites como etiquetar ingredientes en una receta: hace que ensamblar tu proyecto sea más eficiente y menos confuso. Nombres claros agilizan la colaboración y la resolución de problemas.",
            ]
        else:
            return []

    def get_backdrop_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nGiving meaningful names to backdrops is like labeling the rooms in a house: it helps you quickly identify each environment. Clear names make your project easier to organize and navigate.",
                "\nEXPLANATION:\nNaming backdrops is like titling the scenes in a movie: it provides context and enhances the understanding of the story's progression. Appropriate names make your project more intuitive.",
                "\nEXPLANATION:\nThink of naming backdrops like designating locations on a map: each name should clearly indicate its purpose. This improves the overall structure and facilitates the comprehension of the project.",
                "\nEXPLANATION:\nNaming backdrops is like putting signs in a theme park: it ensures that each area is well-identified and visitors don't get lost. Clarity in naming enhances project management and user experience.",
                "\nEXPLANATION:\nConsider naming backdrops like labeling the different sections of a magazine: it makes navigating your project more efficient and less confusing. Clear names streamline collaboration and troubleshooting.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nDar nombres significativos a los fondos es como etiquetar las habitaciones de una casa: te ayuda a identificar rápidamente cada entorno. Nombres claros hacen que tu proyecto sea más fácil de organizar y navegar.",
                "\nEXPLICACIÓN:\nNombrar fondos es como titular las escenas de una película: proporciona contexto y mejora la comprensión de la progresión de la historia. Nombres apropiados hacen que tu proyecto sea más intuitivo.",
                "\nEXPLICACIÓN:\nPiensa en nombrar fondos como designar ubicaciones en un mapa: cada nombre debe indicar claramente su propósito. Esto mejora la estructura general y facilita la comprensión del proyecto.",
                "\nEXPLICACIÓN:\nNombrar fondos es como poner letreros en un parque temático: asegura que cada área esté bien identificada y que los visitantes no se pierdan. La claridad en los nombres mejora la gestión del proyecto y la experiencia del usuario.",
                "\nEXPLICACIÓN:\nConsidera nombrar fondos como etiquetar las diferentes secciones de una revista: hace que navegar por tu proyecto sea más eficiente y menos confuso. Nombres claros agilizan la colaboración y la resolución de problemas.",
            ]
        else:
            return []

    def get_upgrade_feedback_phrases(self):
        if self.curr_lan == 'en':
            return {
                'Backdrops': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the backdrop naming, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE BACKDROP NAMING, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'Sprites': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the sprite naming, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE SPRITE NAMING, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'deadCode': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the dead code, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DEAD CODE, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'Duplicates': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the duplicated code already, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DUPLICATED CODE, that's very great news! Does it seem good to you if we keep improving the project?",
                }
            }
        elif self.curr_lan == 'es':
            return {
                'Backdrops': {
                    'fail': "Oooops, parece que no has resuelto el problema con el nombramiento de los fondos, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL NOMBRAMIENTO DE LOS FONDOS, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'Sprites': {
                    'fail': "Oooops, parece que no has resuelto el problema con el nombramiento de los sprites, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL NOMBRAMIENTO DE LOS SPRITES, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'deadCode': {
                    'fail': "Oooops, parece que no has resuelto el problema con el código muerto, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL CÓDIGO MUERTO, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'Duplicates': {
                    'fail': "Oooops, parece que no has resuelto el problema con el código duplicado, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL CÓDIGO DUPLICADO, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                }
            }
        else:
            return {}

            

