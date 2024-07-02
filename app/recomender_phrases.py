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
        elif self.curr_lan == 'it':
            return [
                "Stai facendo un ottimo lavoro, è incredibile, ma il mio senso dell'olfatto felino ha rilevato che",
                "Stai facendo un lavoro eccellente, è impressionante, ma il mio senso dell'olfatto felino ha rilevato che qualcuno ha mangiato il mio tonno, o forse è",
                "Stai facendo un lavoro fantastico, è meraviglioso, ma le mie abilità da gatto hanno rilevato un topo vicino, o forse è",
                "Il tuo sforzo è eccezionale, è affascinante, ma i miei istinti felini hanno individuato che qualcuno sta nascondendo segreti nella lettiera, o forse è",
            ]
        elif self.curr_lan == 'ru':
            return [
                "Ты делаешь отличную работу, это потрясающе, но мой кошачий обоняния обнаружило, что",
                "Ты делаешь великолепную работу, это впечатляет, но мои кошачьи чутья выявили, что кто-то съел мой тунец, или, может быть, это",
                "Ты делаешь фантастическую работу, это замечательно, но мои кошачьи навыки обнаружили мышь поблизости, или, может быть, это",
                "Твои усилия выдающиеся, это увлекательно, но мои кошачьи инстинкты выявили, что кто-то скрывает секреты в песочнице, или, может быть, это",
            ]
        elif self.curr_lan == 'ca':
            return [
                "Estàs fent una feina molt bona, és increïble, però el meu sentit de l'olfacte felí ha detectat que",
                "Estàs fent una feina excel·lent, és impressionant, però el meu sentit de l'olfacte felí ha detectat que algú s'ha menjat el meu tonyina, o potser és que",
                "Estàs fent una feina fantàstica, és meravellós, però les meves habilitats de gat han detectat un ratolí a prop, o potser és que",
                "El teu esforç és excepcional, és fascinant, però els meus instints felines han identificat que algú guarda secrets a la caixa de sorra, o potser és que",
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
        elif self.curr_lan == 'it':
            return [
                "\nBuona fortuna nel migliorare il tuo progetto, ce la puoi fare! :)",
                "\nContinua con il tuo progetto, stai facendo un ottimo lavoro! :)",
                "\nSono sicuro che il tuo progetto sarà un grande successo! :)",
                "\nNon arrenderti, ogni sforzo ti avvicina sempre di più al tuo obiettivo! :)",
                "\nConfido nelle tue capacità, migliorerai il tuo progetto! :)",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nУдачи вам в улучшении вашего проекта, вы справитесь! :)",
                "\nПродолжайте двигаться вперед с вашим проектом, вы делаете отличную работу! :)",
                "\nЯ уверен, что ваш проект будет большим успехом! :)",
                "\nНе сдавайтесь, каждое усилие приближает вас к вашей цели! :)",
                "\nЯ верю в ваши способности, вы улучшите ваш проект! :)",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nSort amb la millora del teu projecte, pots fer-ho! :)",
                "\nSegueix endavant amb el teu projecte, estàs fent una gran feina! :)",
                "\nEstic segur que el teu projecte serà un gran èxit! :)",
                "\nNo et rendeixis, cada esforç t'acosta més al teu objectiu! :)",
                "\nConfio en les teves habilitats, milloraràs el teu projecte! :)",
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
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nImmagina di avere un progetto con due script composti dagli stessi blocchi ma con parametri o valori diversi. Cosa succede se devi fare una piccola modifica? Dovresti modificare entrambi gli script, complicando la manutenzione del codice. In queste situazioni, è più appropriato che il programmatore crei un blocco personalizzato che definisca questo comportamento e utilizzi questo nuovo blocco dove necessario.",
                "\nSPIEGAZIONE:\nGli script duplicati sono come avere multiple copie della stessa ricetta con lievi variazioni negli ingredienti. Se cambi un ingrediente, devi aggiornare tutte le copie, il che è laborioso. Invece, crea una ricetta principale e fai riferimento ad essa dove necessario.",
                "\nSPIEGAZIONE:\nAvere script duplicati è come avere diverse attrezzature identiche nel tuo set di strumenti con piccole differenze. Se una si rompe o ha bisogno di essere regolata, devi sistemare ciascuna individualmente. Un approccio migliore è avere un'unica attrezzatura con configurazioni regolabili.",
                "\nSPIEGAZIONE:\nPensa agli script duplicati come scrivere le stesse istruzioni per diverse attività. Se devi aggiornare le istruzioni, devi riscriverle per ogni attività, il che è inefficiente. Invece, scrivi un'unica serie di istruzioni e fai riferimento ad esse secondo necessità.",
                "\nSPIEGAZIONE:\nGli script duplicati sono come dipingere pareti multiple dello stesso colore ma con diverse marche di vernice. Se decidi di cambiare il colore, devi ridipingere ogni parete separatamente. Utilizzare una vernice consistente consente modifiche e manutenzione più semplici.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nПредставьте, что у нас есть два скрипта, состоящих из одинаковых блоков, но с разными параметрами или значениями. Что если нам нужно внести небольшие изменения? Нам придется изменить оба скрипта, что усложняет поддержку кода. В таких ситуациях более целесообразно, чтобы программист создал пользовательский блок, который определяет это поведение, и использовал этот новый блок там, где это необходимо.",
                "\nОБЪЯСНЕНИЕ:\nДублированные скрипты — это как иметь несколько копий одного и того же рецепта с небольшими изменениями в ингредиентах. Если вы меняете один ингредиент, вам придется обновить все копии, что неудобно. Вместо этого создайте мастер-рецепт и используйте его по необходимости.",
                "\nОБЪЯСНЕНИЕ:\nИметь дублированные скрипты — это как иметь несколько идентичных инструментов в вашем ящике с инструментами с небольшими различиями. Если один из них сломается или потребует настройки, вам придется исправлять каждый индивидуально. Более эффективный подход — иметь единственный инструмент с настраиваемыми параметрами.",
                "\nОБЪЯСНЕНИЕ:\nДублированные скрипты — это как написание одинаковых инструкций для различных задач. Если вам нужно обновить инструкции, вам придется переписать их для каждой задачи, что неэффективно. Вместо этого напишите единственный набор инструкций и ссылайтесь на них по мере необходимости.",
                "\nОБЪЯСНЕНИЕ:\nДублированные скрипты — это как покраска нескольких стен одним цветом, но с разными марками краски. Если вы решите изменить цвет, вам нужно будет перекрасить каждую стену отдельно. Использование одного и того же типа краски упрощает изменения и обслуживание.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nImagina que en un projecte tenim dos scripts compostos pels mateixos blocs però amb diferents paràmetres o valors. Què passa si necessitem fer un petit canvi? Hauríem de modificar tots dos scripts, cosa que complica el manteniment del codi. En aquestes situacions, és més apropiat que el programador creï un bloc personalitzat que defineixi aquest comportament i utilitzi aquest nou bloc on sigui necessari.",
                "\nEXPLICACIÓ:\nEls scripts duplicats són com tenir múltiples còpies de la mateixa recepta amb petites variacions en els ingredients. Si canviem un ingredient, cal actualitzar totes les còpies, la qual cosa és engorrosa. En lloc d'això, crea una recepta mestra i refèreix-t'hi on sigui necessari.",
                "\nEXPLICACIÓ:\nTenir scripts duplicats és com tenir diverses eines idèntiques a la teva caixa d'eines amb petites diferències. Si una es trenca o necessita ajust, has de reparar cada una individualment. Un millor enfocament és tenir una única eina amb configuracions ajustables.",
                "\nEXPLICACIÓ:\nPensa en els scripts duplicats com escriure les mateixes instruccions per a diferents tasques. Si necessites actualitzar les instruccions, has de reescriure-les per a cada tasca, la qual cosa és ineficient. En lloc d'això, escriu un únic conjunt d'instruccions i refèreix-t'hi segons sigui necessari.",
                "\nEXPLICACIÓ:\nEls scripts duplicats són com pintar diverses parets del mateix color però amb diferents marques de pintura. Si decides canviar el color, necessites repintar cada paret per separat. Utilitzar una pintura consistent permet canvis i manteniment més fàcils.",
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
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nIl codice morto è come avere blocchi non utilizzati sparsi per terra: rende tutto più disordinato e difficile da capire. Eliminandolo, il tuo progetto sarà più pulito, più facile da comprendere e funzionerà meglio.",
                "\nSPIEGAZIONE:\nAvere codice morto è come avere giocattoli rotti nella tua stanza: sono inutili e occupano solo spazio. Eliminandoli, tutto sarà più organizzato.",
                "\nSPIEGAZIONE:\nIl codice morto è come avere vecchi fogli sulla tua scrivania: ti distraggono e rendono difficile trovare ciò di cui hai bisogno. Eliminandoli, lavorerai meglio.",
                "\nSPIEGAZIONE:\nIl codice morto è come avere vestiti che non indossi più nel tuo armadio: occupano solo spazio e rendono tutto più disordinato. Eliminandoli, tutto diventa più gestibile.",
                "\nSPIEGAZIONE:\nIl codice morto è come avere spazzatura nello zaino: è inutile e solo ingombra. Pulendolo, troverai tutto più velocemente e sarà più facile da usare.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nМертвый код — это как иметь неиспользуемые блоки, разбросанные по полу: он делает все более беспорядочным и трудным для понимания. Удаление мертвого кода сделает ваш проект более чистым, понятным и эффективным.",
                "\nОБЪЯСНЕНИЕ:\nИметь мертвый код — это как иметь сломанные игрушки в своей комнате: они бесполезны и занимают только место. Избавление от них сделает все более организованным.",
                "\nОБЪЯСНЕНИЕ:\nМертвый код — это как иметь старые бумаги на своем рабочем столе: они отвлекают и делают поиск нужного сложным. Избавление от них поможет вам лучше работать.",
                "\nОБЪЯСНЕНИЕ:\nМертвый код — это как иметь одежду, которую уже не носишь, в своем шкафу: она только занимает место и создает беспорядок. Удаление ее облегчит управление всем.",
                "\nОБЪЯСНЕНИЕ:\nМертвый код — это как иметь мусор в своем рюкзаке: он бесполезен и только мешает. Убрав его, вы сможете быстрее находить все необходимое и легче его использовать.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nEl codi mort és com tenir blocs no utilitzats escampats pel terra: fa que tot sigui més desordenat i difícil d'entendre. En eliminar-lo, el teu projecte estarà més net, serà més fàcil d'entendre i funcionarà millor.",
                "\nEXPLICACIÓ:\nTenir codi mort és com tenir joguines trencades a la teva habitació: són inútils i només ocupen espai. En eliminar-los, tot estarà més organitzat.",
                "\nEXPLICACIÓ:\nEl codi mort és com tenir papers vells a la teva taula: et distreuen i fan que sigui difícil trobar el que necessites. En desfer-te'n, treballaràs millor.",
                "\nEXPLICACIÓ:\nEl codi mort és com tenir roba que ja no fas servir a l'armari: només ocupa espai i fa que tot sembli desordenat. En eliminar-la, tot és més fàcil de gestionar.",
                "\nEXPLICACIÓ:\nEl codi mort és com tenir escombraries a la teva motxilla: és inútil i només molesta. En netejar-la, trobes tot més ràpidament i és més fàcil d'utilitzar.",
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
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nDare nomi significativi agli sprite è come etichettare gli oggetti nel tuo set di strumenti: ti aiuta a trovare rapidamente ciò di cui hai bisogno. Nomi chiari rendono il tuo progetto più facile da capire e navigare.",
                "\nSPIEGAZIONE:\nDare nomi agli sprite è come dare nomi ai personaggi in una storia: conferisce loro identità e rende le interazioni più chiare. Nomi ben scelti migliorano la leggibilità del tuo progetto.",
                "\nSPIEGAZIONE:\nPensa al nominare gli sprite come assegnare ruoli in un'opera teatrale: ogni nome dovrebbe riflettere lo scopo dello sprite. Questa organizzazione migliora la struttura generale e la comprensione del tuo progetto.",
                "\nSPIEGAZIONE:\nNominare gli sprite è come nominare gli strumenti in un'orchestra: assicura che ogni parte giochi il suo ruolo previsto in modo armonioso. La chiarezza nei nomi migliora la gestione e lo sviluppo del progetto.",
                "\nSPIEGAZIONE:\nConsidera il nominare gli sprite come etichettare gli ingredienti in una ricetta: rende l'assemblaggio del tuo progetto più efficiente e meno confuso. Nomi chiari velocizzano la collaborazione e la risoluzione dei problemi.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nДавать осмысленные имена спрайтам — это как помечать объекты в вашем ящике с инструментами: это помогает быстро найти нужное. Ясные имена делают ваш проект более понятным и удобным для навигации.",
                "\nОБЪЯСНЕНИЕ:\nНазвать спрайты — это как дать имена персонажам в истории: это придает им личность и делает взаимодействия более ясными. Хорошо подобранные имена улучшают читаемость вашего проекта.",
                "\nОБЪЯСНЕНИЕ:\nПодумайте о названии спрайтов, как о назначении ролей в театральном представлении: каждое имя должно отражать цель спрайта. Такая организация улучшает общую структуру и понимание вашего проекта.",
                "\nОБЪЯСНЕНИЕ:\nНазвать спрайты — это как дать имена инструментам в оркестре: это гарантирует, что каждая часть выполняет свою предназначенную роль гармонично. Ясность в именах улучшает управление и развитие проекта.",
                "\nОБЪЯСНЕНИЕ:\nРассмотрите названия спрайтов как маркировку ингредиентов в рецепте: это делает сборку вашего проекта более эффективной и менее запутанной. Ясные имена способствуют более гладкому сотрудничеству и решению проблем.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nDonar noms significatius als sprites és com etiquetar els objectes a la teva caixa d'eines: et ajuda a trobar ràpidament el que necessites. Noms clars fan que el teu projecte sigui més fàcil d'entendre i navegar.",
                "\nEXPLICACIÓ:\nNomenar sprites és com nomenar personatges en una història: els dóna identitat i fa que les interaccions siguin més clares. Noms ben triats milloren la llegibilitat del teu projecte.",
                "\nEXPLICACIÓ:\nPensa en nomenar sprites com assignar rols en una obra de teatre: cada nom ha de reflectir el propòsit del sprite. Aquesta organització millora l'estructura general i la comprensió del teu projecte.",
                "\nEXPLICACIÓ:\nNomenar sprites és com nomenar instruments en una orquestra: assegura que cada part jugui el seu paper previst de manera harmònica. La claredat en els noms millora la gestió i el desenvolupament del projecte.",
                "\nEXPLICACIÓ:\nConsidera el nomenament de sprites com etiquetar ingredients en una recepta: fa que muntar el teu projecte sigui més eficient i menys confús. Noms clars agilitzen la col·laboració i la resolució de problemes.",
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
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nDare nomi significativi ai background è come etichettare le stanze di una casa: ti aiuta a identificare rapidamente ogni ambiente. Nomi chiari rendono il tuo progetto più facile da organizzare e navigare.",
                "\nSPIEGAZIONE:\nNominare i background è come titolare le scene di un film: fornisce contesto e migliora la comprensione della progressione della storia. Nomi appropriati rendono il tuo progetto più intuitivo.",
                "\nSPIEGAZIONE:\nPensa al nominare i background come assegnare posizioni su una mappa: ogni nome dovrebbe indicare chiaramente il suo scopo. Questo migliora la struttura generale e facilita la comprensione del progetto.",
                "\nSPIEGAZIONE:\nNominare i background è come mettere segnaletica in un parco tematico: assicura che ogni area sia ben identificata e che i visitatori non si perdano. La chiarezza nei nomi migliora la gestione del progetto e l'esperienza dell'utente.",
                "\nSPIEGAZIONE:\nConsidera il nominare i background come etichettare le diverse sezioni di una rivista: rende la navigazione nel tuo progetto più efficiente e meno confusa. Nomi chiari velocizzano la collaborazione e la risoluzione dei problemi.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nДавать осмысленные имена фонам — это как помечать комнаты в доме: это помогает быстро опознать каждую обстановку. Ясные названия делают ваш проект более удобным для организации и навигации.",
                "\nОБЪЯСНЕНИЕ:\nНазывать фоны — это как названия сцен в фильме: это добавляет контекст и улучшает понимание хода сюжета. Подходящие названия делают ваш проект более интуитивным.",
                "\nОБЪЯСНЕНИЕ:\nПодумайте о названии фонов, как о указании местоположений на карте: каждое название должно четко указывать на его назначение. Это улучшает общую структуру и облегчает понимание проекта.",
                "\nОБЪЯСНЕНИЕ:\nНазывать фоны — это как размещать указатели в тематическом парке: это гарантирует, что каждая зона хорошо идентифицирована, и посетители не заблудятся. Ясность в названиях улучшает управление проектом и пользовательский опыт.",
                "\nОБЪЯСНЕНИЕ:\nРассмотрите названия фонов, как маркировку различных разделов журнала: это делает навигацию по вашему проекту более эффективной и менее запутанной. Ясные названия способствуют более гладкому сотрудничеству и решению проблем.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nDonar noms significatius als fons és com etiquetar les habitacions d'una casa: t'ajuda a identificar ràpidament cada entorn. Noms clars fan que el teu projecte sigui més fàcil d'organitzar i navegar.",
                "\nEXPLICACIÓ:\nNomenar fons és com titular les escenes d'una pel·lícula: proporciona context i millora la comprensió de la progressió de la història. Noms adequats fan que el teu projecte sigui més intuïtiu.",
                "\nEXPLICACIÓ:\nPensa en nomenar fons com designar ubicacions en un mapa: cada nom ha d'indicar clarament el seu propòsit. Això millora l'estructura general i facilita la comprensió del projecte.",
                "\nEXPLICACIÓ:\nNomenar fons és com posar rètols en un parc temàtic: assegura que cada àrea estigui ben identificada i que els visitants no es perdi. La claredat en els noms millora la gestió del projecte i l'experiència de l'usuari.",
                "\nEXPLICACIÓ:\nConsidera nomenar fons com etiquetar les diferents seccions d'una revista: fa que navegar pel teu projecte sigui més eficient i menys confús. Noms clars agilitzen la col·laboració i la resolució de problemes.",
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
        elif self.curr_lan == 'it':
            return {
                'Backdrops': {
                    'fail': "Oooops, sembra che tu non abbia risolto il problema con il nomina dei fondali, ma non preoccuparti, vediamo come potremmo risolverlo di nuovo,",
                    'success': "YEAHH, HAI RISOLTO IL PROBLEMA CON IL NOMINA DEI FONDALI, questa è una notizia fantastica! Ti va bene se continuiamo a migliorare il progetto?",
                },
                'Sprites': {
                    'fail': "Oooops, sembra che tu non abbia risolto il problema con il nomina degli sprite, ma non preoccuparti, vediamo come potremmo risolverlo di nuovo,",
                    'success': "YEAHH, HAI RISOLTO IL PROBLEMA CON IL NOMINA DEGLI SPRITE, questa è una notizia fantastica! Ti va bene se continuiamo a migliorare il progetto?",
                },
                'deadCode': {
                    'fail': "Oooops, sembra che tu non abbia risolto il problema con il codice morto, ma non preoccuparti, vediamo come potremmo risolverlo di nuovo,",
                    'success': "YEAHH, HAI RISOLTO IL PROBLEMA CON IL CODICE MORTO, questa è una notizia fantastica! Ti va bene se continuiamo a migliorare il progetto?",
                },
                'Duplicates': {
                    'fail': "Oooops, sembra che tu non abbia risolto il problema con il codice duplicato, ma non preoccuparti, vediamo come potremmo risolverlo di nuovo,",
                    'success': "YEAHH, HAI RISOLTO IL PROBLEMA CON IL CODICE DUPLICATO, questa è una notizia fantastica! Ti va bene se continuiamo a migliorare il progetto?",
                }
            }
        elif self.curr_lan == 'ru':
            return {
                'Backdrops': {
                    'fail': "Ой, похоже, вы не решили проблему с названием фонов, но не беспокойтесь, давайте еще раз рассмотрим, как мы можем ее решить,",
                    'success': "УРА, ВЫ РЕШИЛИ ПРОБЛЕМУ С НАЗВАНИЕМ ФОНОВ, это замечательная новость! Можем ли мы продолжить улучшение проекта?",
                },
                'Sprites': {
                    'fail': "Ой, похоже, вы не решили проблему с названием спрайтов, но не беспокойтесь, давайте еще раз рассмотрим, как мы можем ее решить,",
                    'success': "УРА, ВЫ РЕШИЛИ ПРОБЛЕМУ С НАЗВАНИЕМ СПРАЙТОВ, это замечательная новость! Можем ли мы продолжить улучшение проекта?",
                },
                'deadCode': {
                    'fail': "Ой, похоже, вы не решили проблему с мертвым кодом, но не беспокойтесь, давайте еще раз рассмотрим, как мы можем ее решить,",
                    'success': "УРА, ВЫ РЕШИЛИ ПРОБЛЕМУ С МЕРТВЫМ КОДОМ, это замечательная новость! Можем ли мы продолжить улучшение проекта?",
                },
                'Duplicates': {
                    'fail': "Ой, похоже, вы не решили проблему с дублированным кодом, но не беспокойтесь, давайте еще раз рассмотрим, как мы можем ее решить,",
                    'success': "УРА, ВЫ РЕШИЛИ ПРОБЛЕМУ С ДУБЛИРОВАННЫМ КОДОМ, это замечательная новость! Можем ли мы продолжить улучшение проекта?",
                }
            }
        elif self.curr_lan == 'ca':
            return {
                'Backdrops': {
                    'fail': "Oooops, sembla que no has resolt el problema amb el nomenament dels fons, però no et preocupis, revisarem com podríem solucionar-ho de nou,",
                    'success': "¡YEAHH, HAS RESOLT EL PROBLEMA AMB EL NOMENAMENT DELS FONS, aquesta és una notícia genial! ¿Et sembla bé si continuem millorant el projecte?",
                },
                'Sprites': {
                    'fail': "Oooops, sembla que no has resolt el problema amb el nomenament dels sprites, però no et preocupis, revisarem com podríem solucionar-ho de nou,",
                    'success': "¡YEAHH, HAS RESOLT EL PROBLEMA AMB EL NOMENAMENT DELS SPRITES, aquesta és una notícia genial! ¿Et sembla bé si continuem millorant el projecte?",
                },
                'deadCode': {
                    'fail': "Oooops, sembla que no has resolt el problema amb el codi mort, però no et preocupis, revisarem com podríem solucionar-ho de nou,",
                    'success': "¡YEAHH, HAS RESOLT EL PROBLEMA AMB EL CODI MORT, aquesta és una notícia genial! ¿Et sembla bé si continuem millorant el projecte?",
                },
                'Duplicates': {
                    'fail': "Oooops, sembla que no has resolt el problema amb el codi duplicat, però no et preocupis, revisarem com podríem solucionar-ho de nou,",
                    'success': "¡YEAHH, HAS RESOLT EL PROBLEMA AMB EL CODI DUPLICAT, aquesta és una notícia genial! ¿Et sembla bé si continuem millorant el projecte?",
                }
            }
        else:
            return {}

            

