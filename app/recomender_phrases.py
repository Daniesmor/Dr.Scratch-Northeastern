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
        self.messages_explanation_phrases = self.get_messages_explanation_phrases()
        self.variables_explanation_phrases = self.get_variable_naming_explanations()
        self.sequential_explanation_phrases = self.get_sequential_explanation_phrases()
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
        elif self.curr_lan == 'pt':
            return [
                "Você está fazendo um trabalho muito bom, é incrível, mas meu sentido felino de olfato detectou que",
                "Você está fazendo um trabalho excelente, é impressionante, mas meu sentido felino de olfato detectou que alguém comeu meu atum, ou talvez seja que",
                "Você está fazendo um trabalho fantástico, é maravilhoso, mas minhas habilidades de gato detectaram um rato por perto, ou talvez seja que",
                "Seu esforço é excepcional, é fascinante, mas meus instintos felinos identificaram que alguém está guardando segredos na caixa de areia, ou talvez seja que",
            ]
        elif self.curr_lan == 'eu':
            return [
                "Oso lan ona egiten ari zara, zoragarria da, baina nire katu-usaina detektatu du",
                "Oso ona lan egiten ari zara, oso harro, baina nire katu-usaina detektatu du norbait nire atuna jaten duela, edo agian",
                "Lan bikaina egiten ari zara, zoragarria da, baina nire katu-gaitasunek sagu bat hurbildu dutela detektatu dute, edo agian",
                "Zure ahalegina bikaina da, zaigetsua da, baina nire katu-garunek sekretuak gordetzen ari direla identifikatu dute, edo agian",
            ]
        elif self.curr_lan == 'gl':
            return [
                "Estás a facer un traballo moi bo, é incrible, pero o meu sentido do olfato felino detectou que",
                "Estás a facer un traballo excelente, é impresionante, pero o meu sentido do olfato felino detectou que alguén comeu o meu atún, ou talvez sexa que",
                "Estás a facer un traballo fantástico, é marabilloso, pero as miñas habilidades de gato detectaron un rato moi preto, ou talvez sexa que",
                "O teu esforzo é sobresaínte, é fascinante, pero os meus instintos felinos identificaron que alguén está a gardar segredos na caixa de area, ou talvez sexa que",
            ]
        elif self.curr_lan == 'el':
            return [
                "Κάνεις εξαιρετική δουλειά, είναι εντυπωσιακό, αλλά ο γατίσιος μου ένστικτος μύρισε ότι",
                "Κάνεις εξαιρετική δουλειά, είναι καταπληκτικό, αλλά ο γατίσιος μου ένστικτος μύρισε ότι κάποιος έφαγε το τόνο μου, ή ίσως",
                "Κάνεις φανταστική δουλειά, είναι υπέροχο, αλλά οι γατίσιες μου ικανότητες εντόπισαν ένα ποντίκι κοντά, ή ίσως",
                "Η προσπάθειά σου είναι εξαιρετική, είναι συναρπαστικό, αλλά οι γατίσιες μου αντιδράσεις ανιχνεύουν ότι κάποιος κρύβει μυστικά στο κατσικούδι, ή ίσως"
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
        elif self.curr_lan == 'tr':
            return [
                "Çok iyi bir iş çıkarıyorsunuz, bu harika, ama kedi gibi koku alma duyum şunu tespit etti",
                "Mükemmel bir iş çıkarıyorsunuz, bu etkileyici, ama kedi gibi koku alma duyum birisinin ton balığımı yediğini tespit etti, ya da belki",
                "Harika bir iş çıkarıyorsunuz, bu muhteşem, ama kedi becerilerim yakınlarda bir fare tespit etti, ya da belki",
                "Çabanız olağanüstü, bu büyüleyici, ama kedisel içgüdülerim birisinin kum kutusunda sırlar sakladığını tespit etti, ya da belki",
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
        elif self.curr_lan == 'eu':
            return [
                "\nZorte ona zure proiektua hobetzean, lortu dezakezu! :)",
                "\nJarraitu zure proiektuarekin, oso ona lan egiten ari zara! :)",
                "\nZiur nago zure proiektua arrakasta handia izango dela! :)",
                "\nEz utzi, erabat esfortzu guztiak helburua hurbiltzen zaituzte! :)",
                "\nZure gaitasunetan sinetsi, zure proiektua hobetuko duzu! :)",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nBoa sorte mellorando o teu proxecto, podes facelo! :)",
                "\nAdiante co teu proxecto, estás a facer un gran traballo! :)",
                "\nEstou seguro de que o teu proxecto será un gran éxito! :)",
                "\nNon te rendas, cada esforzo achégache máis ao teu obxectivo! :)",
                "\nConfío nas túas habilidades, mellorarás o teu proxecto! :)",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΚαλή τύχη στη βελτίωση του έργου σου, μπορείς να τα καταφέρεις! :)",
                "\nΣυνέχισε με το έργο σου, κάνεις εξαιρετική δουλειά! :)",
                "\nΕίμαι σίγουρος ότι το έργο σου θα είναι μεγάλη επιτυχία! :)",
                "\nΜην τα παρατάς, κάθε προσπάθεια σε φέρνει πιο κοντά στον στόχο σου! :)",
                "\nΈχω εμπιστοσύνη στις ικανότητές σου, θα βελτιώσεις το έργο σου! :)",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nBoa sorte melhorando seu projeto, você consegue! :)",
                "\nContinue com seu projeto, você está fazendo um ótimo trabalho! :)",
                "\nEstou certo de que seu projeto será um grande sucesso! :)",
                "\nNão desista, cada esforço te aproxima mais do seu objetivo! :)",
                "\nConfio em suas habilidades, você vai melhorar seu projeto! :)",
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
        elif self.curr_lan == 'tr':
            return [
                "\nProjenizi geliştirirken iyi şanslar, yapabilirsiniz!! :)",
                "\nProjenize devam edin, harika bir iş çıkarıyorsunuz! :)",
                "\nEminim projeniz büyük bir başarı olacak! :)",
                "\nPes etmeyin, her çaba sizi hedefinize daha da yaklaştırıyor! :)",
                "\nYeteneklerinize güveniyorum, projenizi geliştireceksiniz! :)",
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
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nIruditu zaizu proiektu batean bi script izatea, bloke berdinak baina parametro edo balio ezberdinez osatuak. Zer gertatuko litzateke aldaketa txiki bat egin behar badugu? Bi script horiek aldatu beharko genituzke, eta kodearen mantentzea konplikatzen du hori. Horrelako egoeretan, programatzaileak modu egokiena da bloke pertsonalizatu bat sortzea, hau da, jatorrizko jarrera definitzen duena, eta beharrezkoa denean bloke berri hori erabili.",
                "\nAZALPENA:\nScript bikoitza izateak errezeta bera hainbat kopia izatearen antzekoa da, ingredienteen txikiko aldaerak badaude. Ingrediente bat aldatzen baduzu, kopi guztiak eguneratu behar dituzu, eta hori nahiko galtzailea da. Badago, sortu errezepta nagusia eta erreferentzia egin behar duzu beharrezkoa den lekuan.",
                "\nAZALPENA:\nScript bikoitzak izateak besteak beste, bitxikeria askorekin eguneratzeko premia dagoen tresna bera duzula ikusten da. Batzuk apurtzen badira edo egokitzeko behar izango dituzu bakoitzeko. Harreman onena, tresna bakarra izan behar da ezarpen egokitagarriekin.",
                "\nAZALPENA:\nPentsatu script bikoitzak tresnetan erabiltzea eta horien legeak eta tarea ezberdinetarako berbera. Aginduak eguneratu behar badituzu, bakoitza berriro idatzi behar duzu, eta hori ez da eraginkorra. Horren ordez, idatzi agindu bakarra eta erreferentziatu behar duzu beharrezkoa den moduan.",
                "\nAZALPENA:\nScript bikoitzak paretak berdin kolorez margotzea da, baina kolore ezberdinak erabili. Kolorea aldatzea erabakitzen baduzu, paretak banan banan margotu behar dituzu. Kolore konstantea erabiltzeak eguneraketa eta mantentze errazagoak egiten ditu.",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nImaxina que nun proxecto temos dous scripts compostos polos mesmos bloques pero con diferentes parámetros ou valores. Que pasa se precisamos facer un pequeno cambio? Teríamos que modificar ambos scripts, o que complica o mantemento do código. Nestas situacións, é máis apropiado que o programador cree un bloque personalizado que defina este comportamento e use este novo bloque onde sexa necesario.",
                "\nEXPLICACIÓN:\nOs scripts duplicados son como ter múltiples copias da mesma receita con pequenas variacións nos ingredientes. Se cambias un ingrediente, tes que actualizar todas as copias, o que é engorroso. En lugar diso, crea unha receita mestra e refírete a ela onde sexa necesario.",
                "\nEXPLICACIÓN:\nTer scripts duplicados é como ter varias ferramentas idénticas na túa caixa de ferramentas con pequenas diferenzas. Se unha se rompe ou necesita axuste, debes arranxar cada unha individualmente. Unha mellor aproximación é ter unha única ferramenta con configuracións axustables.",
                "\nEXPLICACIÓN:\nPensa nos scripts duplicados como escribir as mesmas instrucións para diferentes tarefas. Se necesitas actualizar as instrucións, debes reescribilas para cada tarefa, o que é ineficiente. En lugar diso, escribe un único conxunto de instrucións e refírete a elas segundo sexa necesario.",
                "\nEXPLICACIÓN:\nOs scripts duplicados son como pintar varias paredes da mesma cor pero con diferentes marcas de pintura. Se decides cambiar a cor, necesitas repintar cada parede por separado. Usar unha pintura consistente permite cambios e mantemento máis sinxelos.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΦαντάσου ότι σε ένα έργο έχουμε δύο σενάρια που αποτελούνται από τα ίδια τμήματα αλλά με διαφορετικές παραμέτρους ή τιμές. Τι συμβαίνει αν χρειαστεί να κάνουμε ένα μικρό αλλαγή; Θα έπρεπε να τροποποιήσουμε και τα δύο σενάρια, κάτι που δυσκολεύει τη συντήρηση του κώδικα. Σε τέτοιες καταστάσεις, είναι πιο κατάλληλο για τον προγραμματιστή να δημιουργήσει έναν προσαρμοσμένο τεμαχισμό που να ορίζει αυτή τη συμπεριφορά και να χρησιμοποιεί αυτόν τον νέο τεμαχισμό όπου απαιτείται.",
                "\nΕΡΜΗΝΕΙΑ:\nΤα διπλασιασμένα σενάρια είναι σαν να έχεις πολλαπλές αντίγραφα της ίδιας συνταγής με μικρές παραλλαγές στα συστατικά. Αν αλλάξεις ένα συστατικό, πρέπει να ενημερώσεις όλα τα αντίγραφα, που είναι ενοχλητικό. Αντί γι' αυτό, δημιούργησε μια μητρική συνταγή και αναφέρσου σε αυτήν όπου χρειάζεται.",
                "\nΕΡΜΗΝΕΙΑ:\nΝα έχεις διπλασιασμένα σενάρια είναι σαν να έχεις διάφορα αντίγραφα του ίδιου εργαλείου στο εργαλειοθήκη σου με μικρές διαφορές. Αν ένα χαλάσει ή χρειαστεί προσαρμογή, πρέπει να επιδιορθώσεις κάθε ένα ξεχωριστά. Ένα καλύτερο προσέγγιση είναι να έχεις ένα μοναδικό εργαλείο με ρυθμίσεις που μπορούν να προσαρμοστούν.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου τα διπλασιασμένα σενάρια ως το να γράφεις τις ίδιες οδηγίες για διαφορετικές εργασίες. Αν χρειαστεί να ενημερώσεις τις οδηγίες, πρέπει να τις ξαναγράψεις για κάθε εργασία, που είναι ανεπιτυχές. Αντί γι' αυτό, γράψε ένα μοναδικό σύνολο οδηγιών και αναφέρσου σε αυτές όπως χρειάζεται.",
                "\nΕΡΜΗΝΕΙΑ:\nΤα διπλασιασμένα σενάρια είναι σαν να βάφεις πολλούς τοίχους με το ίδιο χρώμα αλλά με διαφορετικές μάρκες χρώματος. Αν αποφασίσεις να αλλάξεις το χρώμα, πρέπει να ξαναβάψεις κάθε τοίχο ξεχωριστά. Χρησιμοποίησε ένα συνεπές χρώμα επιτρέπει ευκολότερες αλλαγές και συντήρηση.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nImagine que em um projeto temos dois scripts compostos pelos mesmos blocos, mas com diferentes parâmetros ou valores. E se precisarmos fazer uma pequena alteração? Teríamos que modificar ambos os scripts, o que complica a manutenção do código. Nessas situações, é mais apropriado para o programador criar um bloco personalizado que defina esse comportamento e utilizar esse novo bloco onde for necessário.",
                "\nEXPLICAÇÃO:\nScripts duplicados são como ter várias cópias da mesma receita com pequenas variações nos ingredientes. Se você altera um ingrediente, precisa atualizar todas as cópias, o que é trabalhoso. Em vez disso, crie uma receita mestra e refira-se a ela onde for necessário.",
                "\nEXPLICAÇÃO:\nTer scripts duplicados é como ter várias ferramentas idênticas em sua caixa de ferramentas com pequenas diferenças. Se uma quebra ou precisa de ajuste, você precisa consertar cada uma individualmente. Uma abordagem melhor é ter uma única ferramenta com configurações ajustáveis.",
                "\nEXPLICAÇÃO:\nPense em scripts duplicados como escrever as mesmas instruções para diferentes tarefas. Se precisar atualizar as instruções, você deve reescrevê-las para cada tarefa, o que é ineficiente. Em vez disso, escreva um único conjunto de instruções e faça referência a elas conforme necessário.",
                "\nEXPLICAÇÃO:\nScripts duplicados são como pintar várias paredes da mesma cor, mas com marcas de tinta diferentes. Se decidir mudar a cor, precisará repintar cada parede separadamente. Usar uma tinta consistente facilita alterações e manutenção.",
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
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nBir projede aynı bloklardan oluşan ancak farklı parametreler veya değerlerle iki betiğimiz olduğunu hayal edin. Küçük bir değişiklik yapmamız gerekirse ne olur? Her iki betiği de değiştirmemiz gerekecek, bu da kod bakımını zorlaştırır. Böyle durumlarda, programcının bu davranışı tanımlayan özel bir blok oluşturması ve bu yeni bloğu gerektiği yerde kullanması daha uygundur.",
                "\nAÇIKLAMA:\nYinelenen betikler, hafif malzeme varyasyonlarıyla aynı tarifin birden fazla kopyasına sahip olmak gibidir. Bir malzemeyi değiştirirseniz, tüm kopyaları güncellemeniz gerekir, bu da zahmetlidir. Bunun yerine, bir ana tarif oluşturun ve gerektiğinde ona başvurun.",
                "\nAÇIKLAMA:\nYinelenen betiklere sahip olmak, alet kutunuzda küçük farklarla birden fazla aynı araca sahip olmak gibidir. Bir tanesi bozulur veya ayar gerektirirse, her birini ayrı ayrı tamir etmeniz gerekir. Daha iyi bir yaklaşım, ayarlanabilir ayarları olan tek bir araca sahip olmaktır.",
                "\nAÇIKLAMA:\nYinelenen betikleri, farklı görevler için aynı talimatları yazmak gibi düşünün. Talimatları güncellemeniz gerekirse, her görev için yeniden yazmanız gerekir, bu verimsizdir. Bunun yerine, tek bir talimat seti yazın ve gerektiğinde ona başvurun.",
                "\nAÇIKLAMA:\nYinelenen betikler, aynı rengi boyayan ancak farklı boya markaları kullanan birden fazla duvarı boyamak gibidir. Rengi değiştirmeye karar verirseniz, her duvarı ayrı ayrı yeniden boyamanız gerekir. Tutarlı bir boya kullanmak, değişiklikleri ve bakımı kolaylaştırır.",
            ]
        else:
            return []
    
    def get_sequential_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nImagine you have to pick up your toys one by one and put them in the box. Wouldn't it be faster if someone said, 'Put 5 toys in the box'? That's what a loop does—it helps you repeat actions quickly and easily.",
                "\nEXPLANATION:\nRepeating blocks is like writing your name on a piece of paper over and over again. Wouldn't it be easier to just say, 'Write your name 10 times'? A loop lets you do the same thing without getting so tired.",
                "\nEXPLANATION:\nThink about eating a big bowl of cereal. If you only eat one piece of cereal at a time, it would take forever! A loop is like using a spoon to scoop up many pieces at once—it makes everything faster and easier.",
                "\nEXPLANATION:\nImagine building a sandcastle by carrying one handful of sand at a time. A loop is like using a bucket to carry many handfuls all at once. It helps you finish your castle faster so you can play more!",
                "\nEXPLANATION:\nSequential blocks are like carrying apples one at a time to a basket. If you had a cart, you could carry all the apples in one trip! A loop is like that cart—it makes things easier and faster."
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nImagina que tienes que recoger tus juguetes uno por uno y ponerlos en la caja. ¿No sería más rápido si alguien dijera: 'Pon 5 juguetes en la caja'? Eso es lo que hace un bucle: te ayuda a repetir acciones de manera rápida y fácil.",
                "\nEXPLICACIÓN:\nRepetir bloques es como escribir tu nombre en una hoja de papel una y otra vez. ¿No sería más fácil decir: 'Escribe tu nombre 10 veces'? Un bucle te permite hacer lo mismo sin cansarte tanto.",
                "\nEXPLICACIÓN:\nPiensa en comer un gran tazón de cereales. Si comes un grano de cereal a la vez, ¡te tardarás una eternidad! Un bucle es como usar una cuchara para tomar muchos cereales a la vez: hace todo más rápido y fácil.",
                "\nEXPLICACIÓN:\nImagina que estás construyendo un castillo de arena llevando un puñado de arena a la vez. Un bucle es como usar un cubo para llevar muchos puñados de una sola vez. Te ayuda a terminar tu castillo más rápido para que puedas jugar más.",
                "\nEXPLICACIÓN:\nLos bloques secuenciales son como llevar manzanas una a una a una cesta. Si tuvieras un carrito, podrías llevar todas las manzanas de un solo viaje. Un bucle es como ese carrito: hace las cosas más fáciles y rápidas."
            ]
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nImajinatu zure jostailuak banan-banan hartu eta kutxan sartu behar dituzula. Ez al izango litzateke azkarrago norbaitek esango balizu, 'Sartu 5 jostailu kutxan'? Hori da buelta batek egiten duena: ekintzak azkar eta erraz errepikatzen laguntzen dizu.",
                "\nAZALPENA:\nBlokeak errepikatzea zure izena paper batean behin eta berriz idaztea bezala da. Ez al litzateke errazago esatea besterik gabe, 'Idatzi zure izena 10 aldiz'? Buelta batek gauza bera egiten uzten dizu, nekatuta geratu gabe.",
                "\nAZALPENA:\nPentsa zereal-ontzi handi bat jaten. Zereal pieza bakarra aldi bakoitzean jaten baduzu, betirako beharko duzu! Buelta bat koilara erabiltzea bezala da, aldi berean pieza asko hartzeko. Denak azkarrago eta errazago egiten ditu.",
                "\nAZALPENA:\nImajinatu hondar gaztelu bat eraikitzen, hondar esku bete bakarra aldi bakoitzean eramanez. Buelta bat ontzi bat erabiltzea bezala da, aldi berean esku bete asko eramateko. Zure gaztelua azkarrago amaitzen laguntzen dizu, gehiago jolastu ahal izateko!",
                "\nAZALPENA:\nBloke sekuentzialak sagarrak banan-banan saskira eramatea bezalakoa da. Gurdi bat izango bazenu, sagar guztiak bidaia bakarrean eraman ahal izango zenituzke! Buelta hori gurdi hori bezalakoa da: gauzak errazago eta azkarrago egiten ditu."
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nImaxina que tes que coller os teus xoguetes un por un e metelos na caixa. Non sería máis rápido se alguén che dixese: 'Mete 5 xoguetes na caixa'? Iso é o que fai un bucle: axúdache a repetir accións de forma rápida e sinxela.",
                "\nEXPLICACIÓN:\nRepetir bloques é como escribir o teu nome nun anaco de papel unha e outra vez. Non sería máis doado dicir simplemente: 'Escribe o teu nome 10 veces'? Un bucle permíteche facer o mesmo sen cansarte tanto.",
                "\nEXPLICACIÓN:\nPensa en comer unha gran cunca de cereais. Se comes só un anaco de cereal cada vez, levaríache unha eternidade! Un bucle é como usar unha culler para coller moitos anacos á vez: fai todo máis rápido e sinxelo.",
                "\nEXPLICACIÓN:\nImaxina que estás a construír un castelo de area levando un puñado de area cada vez. Un bucle é como usar un balde para levar moitos puñados de area á vez. Axúdache a rematar o castelo máis rápido para que poidas xogar máis!",
                "\nEXPLICACIÓN:\nOs bloques secuenciais son como levar mazás unha a unha ata unha cesta. Se tiveses un carro, poderías levar todas as mazás nun só traxecto! Un bucle é como ese carro: fai as cousas máis doadas e rápidas."
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΦαντάσου ότι πρέπει να μαζέψεις τα παιχνίδια σου ένα-ένα και να τα βάλεις στο κουτί. Δεν θα ήταν πιο γρήγορο αν κάποιος σου έλεγε: 'Βάλε 5 παιχνίδια στο κουτί'; Αυτό κάνει ένας βρόχος: σε βοηθά να επαναλαμβάνεις ενέργειες γρήγορα και εύκολα.",
                "\nΕΡΜΗΝΕΙΑ:\nΗ επανάληψη μπλοκ είναι σαν να γράφεις το όνομά σου σε ένα χαρτί ξανά και ξανά. Δεν θα ήταν πιο εύκολο να πεις απλώς: 'Γράψε το όνομά σου 10 φορές'; Ένας βρόχος σου επιτρέπει να κάνεις το ίδιο χωρίς να κουράζεσαι.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου να τρως ένα μεγάλο μπολ με δημητριακά. Αν φας μόνο ένα κομμάτι δημητριακών κάθε φορά, θα σου πάρει για πάντα! Ένας βρόχος είναι σαν να χρησιμοποιείς κουτάλι για να πάρεις πολλά κομμάτια ταυτόχρονα: κάνει τα πάντα πιο γρήγορα και εύκολα.",
                "\nΕΡΜΗΝΕΙΑ:\nΦαντάσου να χτίζεις ένα κάστρο στην άμμο μεταφέροντας μια χούφτα άμμο κάθε φορά. Ένας βρόχος είναι σαν να χρησιμοποιείς κουβά για να μεταφέρεις πολλές χούφτες άμμου ταυτόχρονα. Σε βοηθά να τελειώσεις το κάστρο πιο γρήγορα, ώστε να παίξεις περισσότερο!",
                "\nΕΡΜΗΝΕΙΑ:\nΤα διαδοχικά μπλοκ είναι σαν να μεταφέρεις μήλα ένα-ένα σε ένα καλάθι. Αν είχες ένα καρότσι, θα μπορούσες να μεταφέρεις όλα τα μήλα σε ένα μόνο ταξίδι! Ένας βρόχος είναι σαν αυτό το καρότσι: κάνει τα πράγματα πιο εύκολα και γρήγορα."
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nImagine que você tem que pegar seus brinquedos um por um e colocá-los na caixa. Não seria mais rápido se alguém dissesse: 'Coloque 5 brinquedos na caixa'? Isso é o que um loop faz—ele ajuda você a repetir ações de forma rápida e fácil.",
                "\nEXPLICAÇÃO:\nRepetir blocos é como escrever seu nome em um pedaço de papel várias vezes. Não seria mais fácil apenas dizer: 'Escreva seu nome 10 vezes'? Um loop permite que você faça a mesma coisa sem se cansar tanto.",
                "\nEXPLICAÇÃO:\nPense em comer uma grande tigela de cereal. Se você comer uma peça de cereal por vez, levaria uma eternidade! Um loop é como usar uma colher para pegar várias peças de uma vez—torna tudo mais rápido e fácil.",
                "\nEXPLICAÇÃO:\nImagine construir um castelo de areia carregando um punhado de areia por vez. Um loop é como usar um balde para carregar vários punhados de uma vez. Ele ajuda você a terminar seu castelo mais rápido para poder brincar mais!",
                "\nEXPLICAÇÃO:\nBlocos sequenciais são como carregar maçãs uma por uma para uma cesta. Se você tivesse um carrinho, poderia carregar todas as maçãs em uma viagem! Um loop é como esse carrinho—ele torna as coisas mais fáceis e rápidas."
            ]
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nImmagina di dover raccogliere i tuoi giocattoli uno per uno e metterli nella scatola. Non sarebbe più veloce se qualcuno ti dicesse: 'Metti 5 giocattoli nella scatola'? Questo è quello che fa un ciclo: ti aiuta a ripetere azioni rapidamente e facilmente.",
                "\nSPIEGAZIONE:\nRipetere i blocchi è come scrivere il tuo nome su un foglio più e più volte. Non sarebbe più facile dire semplicemente: 'Scrivi il tuo nome 10 volte'? Un ciclo ti permette di fare la stessa cosa senza stancarti.",
                "\nSPIEGAZIONE:\nPensa a mangiare una grande ciotola di cereali. Se mangi un chicco alla volta, ci metteresti una vita! Un ciclo è come usare un cucchiaio per raccogliere molti chicchi insieme: rende tutto più veloce e semplice.",
                "\nSPIEGAZIONE:\nImmagina di costruire un castello di sabbia portando una manciata di sabbia alla volta. Un ciclo è come usare un secchio per trasportare molte manciate in una volta sola. Ti aiuta a finire il castello più velocemente, così puoi giocare di più!",
                "\nSPIEGAZIONE:\nI blocchi sequenziali sono come trasportare mele una alla volta in un cestino. Se avessi un carrello, potresti portare tutte le mele in un solo viaggio! Un ciclo è come quel carrello: rende le cose più facili e veloci."
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nПредставь, что тебе нужно собирать свои игрушки одну за другой и класть их в коробку. Разве не было бы быстрее, если бы кто-то сказал: 'Положи 5 игрушек в коробку'? Вот что делает цикл: он помогает быстро и легко повторять действия.",
                "\nОБЪЯСНЕНИЕ:\nПовторение блоков похоже на то, как если бы ты писал свое имя на листе бумаги снова и снова. Разве не было бы проще просто сказать: 'Напиши свое имя 10 раз'? Цикл позволяет сделать то же самое, не уставая.",
                "\nОБЪЯСНЕНИЕ:\nПодумай о том, как есть большую миску хлопьев. Если ты будешь есть по одному кусочку за раз, это займет вечность! Цикл — это как использовать ложку, чтобы зачерпнуть много кусочков сразу: всё становится быстрее и проще.",
                "\nОБЪЯСНЕНИЕ:\nПредставь, что ты строишь песочный замок, перенося по одной горсти песка за раз. Цикл — это как использовать ведро, чтобы перенести много горстей сразу. Это помогает быстрее закончить замок, чтобы ты мог больше играть!",
                "\nОБЪЯСНЕНИЕ:\nПоследовательные блоки — это как переносить яблоки по одному в корзину. Если бы у тебя была тележка, ты мог бы перенести все яблоки за один раз! Цикл похож на эту тележку: он делает всё проще и быстрее."
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nImagina que has de recollir les teves joguines una a una i posar-les a la caixa. No seria més ràpid si algú et digués: 'Posa 5 joguines a la caixa'? Això és el que fa un bucle: t'ajuda a repetir accions de manera ràpida i fàcil.",
                "\nEXPLICACIÓ:\nRepetir blocs és com escriure el teu nom en un paper una vegada i una altra. No seria més fàcil dir simplement: 'Escriu el teu nom 10 vegades'? Un bucle et permet fer el mateix sense cansar-te tant.",
                "\nEXPLICACIÓ:\nPensa en menjar un gran bol de cereals. Si menges un gra de cereal cada vegada, trigaries una eternitat! Un bucle és com utilitzar una cullera per agafar molts grans alhora: fa que tot sigui més ràpid i fàcil.",
                "\nEXPLICACIÓ:\nImagina que estàs construint un castell de sorra portant una grapada de sorra cada vegada. Un bucle és com utilitzar un cubell per portar moltes grapades alhora. T'ajuda a acabar el castell més ràpidament, de manera que puguis jugar més!",
                "\nEXPLICACIÓ:\nEls blocs seqüencials són com portar pomes una a una a una cistella. Si tinguessis un carro, podries portar totes les pomes en un sol viatge! Un bucle és com aquest carro: fa que les coses siguin més fàcils i ràpides."
            ]
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nHayal et ki oyuncaklarını teker teker alıp kutuya koyman gerekiyor. Birisi sana '5 oyuncak koy' dese daha hızlı olmaz mıydı? İşte döngü bunu yapar: eylemleri hızlı ve kolay bir şekilde tekrarlamana yardımcı olur.",
                "\nAÇIKLAMA:\nBlokları tekrarlamak, adını bir kağıda defalarca yazmak gibidir. 'Adını 10 kez yaz' demek daha kolay olmaz mıydı? Bir döngü, aynı şeyi daha az yorularak yapmanı sağlar.",
                "\nAÇIKLAMA:\nBüyük bir kase mısır gevreği yediğini düşün. Her seferinde bir parça yersen, bu çok uzun sürebilir! Bir döngü, bir kaşık kullanarak birden fazla parça alman gibidir: her şeyi daha hızlı ve kolay yapar.",
                "\nAÇIKLAMA:\nHayal et ki bir kumdan kale yapıyorsun ve her seferinde bir avuç kum taşıyorsun. Bir döngü, bir kova kullanarak birden fazla avuç kum taşıman gibidir. Kalenin daha hızlı bitmesine yardımcı olur, böylece daha fazla oynayabilirsin!",
                "\nAÇIKLAMA:\nSıralı bloklar, elmaları birer birer sepete taşımak gibidir. Bir araban olsa, tüm elmaları tek seferde taşıyabilirdin! Bir döngü, bu araba gibidir: işleri daha kolay ve hızlı hale getirir."
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
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nKodea hildako kodea dela esan daiteke, erabiltzen ez diren blokeak lurpean balean dituzula: guztia zikinagoa eta ulertzeko zailagoa egiten du. Kode hau kenduz gero, zure proiektua garbiagoa izango da, ulertzeko eta ondo funtzionatzeko errazagoa.",
                "\nAZALPENA:\nHildako kodea izateak zure gela jostailu hondakinak izatea da: gauza gabekoak dira eta espazioa bakarrik hartzen dute. Haiek kenduz gero, guztia antolatuta egongo da.",
                "\nAZALPENA:\nHildako kodea izateak zure idazmahai zaharrez hitz egitea da: zure arreta desbideratzen eta beharrezkoa dena aurkitzea zailtzen du. Hauekin amaituz gero, hobe lana egingo duzu.",
                "\nAZALPENA:\nKode hildakoa izateak zure armarian ez duzun arropa izatea da: espazioa hartzen du eta guztia zikinagoa ikusten du. Hauek kentzen badituzu, guztia kudeatzeko errazagoa da.",
                "\nAZALPENA:\nKode hildakoa zure poltsan zabor izatea da: erabili ezin daiteke eta soilik oztopatzen du. Garbi egiten baduzu, azkar aurkitzen duzu eta erabiltzea errazten da.",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nO código morto é como ter bloques non utilizados esparexidos polo chan: fai que todo sexa máis desordenado e difícil de entender. Ao eliminarlo, o teu proxecto estará máis limpo, será máis doado de entender e funcionará mellor.",
                "\nEXPLICACIÓN:\nTer código morto é como ter xoguetes rotos na túa habitación: son inútiles e só ocupan espazo. Ao eliminálos, todo estará máis organizado.",
                "\nEXPLICACIÓN:\nO código morto é como ter papeis vellos no teu escritorio: distraenche e fan que sexa difícil atopar o que necesitas. Ao desfacerte deles, traballarás mellor.",
                "\nEXPLICACIÓN:\nO código morto é como ter roupa que xa non usas no teu armario: só ocupa espazo e fai que todo pareza desordenado. Ao eliminála, todo é máis doado de manexar.",
                "\nEXPLICACIÓN:\nO código morto é como ter lixo na túa mochila: é inútil e só molesta. Ao limparla, atopas todo máis rápido e é máis doado de usar.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΟ νεκρός κώδικας είναι σαν να έχεις αχρησιμοποίητα τμήματα διάσπαρτα στο πάτωμα: κάνει τα πράγματα πιο ατακτοποίητα και δυσκολότερα στην κατανόηση. Απομακρύνοντάς το, το έργο σου θα είναι πιο καθαρό, ευκολότερο να κατανοηθεί και να λειτουργήσει καλύτερα.",
                "\nΕΡΜΗΝΕΙΑ:\nΟ νεκρός κώδικας είναι σαν να έχεις σπασμένα παιχνίδια στο δωμάτιό σου: είναι άχρηστα και απλώς πιάνουν χώρο. Με την αφαίρεσή τους, όλα γίνονται πιο οργανωμένα.",
                "\nΕΡΜΗΝΕΙΑ:\nΟ νεκρός κώδικας είναι σαν να έχεις παλιά χαρτιά στο γραφείο σου: σε αποσπούν την προσοχή και κάνουν δύσκολο το να βρεις αυτό που χρειάζεσαι. Με την απομάκρυνσή τους, εργάζεσαι καλύτερα.",
                "\nΕΡΜΗΝΕΙΑ:\nΟ νεκρός κώδικας είναι σαν να έχεις ρούχα που δεν φοράς πια στη ντουλάπα σου: απλώς πιάνουν χώρο και κάνουν όλα να φαίνονται ατακτοποίητα. Με την απομάκρυνσή τους, όλα είναι πιο εύκολα στη διαχείριση.",
                "\nΕΡΜΗΝΕΙΑ:\nΟ νεκρός κώδικας είναι σαν να έχεις σκουπίδια στο σακίδιό σου: είναι άχρηστα και απλώς εμποδίζουν. Καθαρίζοντάς το, βρίσκεις όλα πιο γρήγορα και τα χρησιμοποιείς ευκολότερα.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nCódigo morto é como ter blocos não utilizados espalhados pelo chão: torna tudo mais bagunçado e difícil de entender. Ao removê-lo, seu projeto ficará mais limpo, será mais fácil de entender e funcionará melhor.",
                "\nEXPLICAÇÃO:\nTer código morto é como ter brinquedos quebrados no seu quarto: são inúteis e ocupam apenas espaço. Ao removê-los, tudo ficará mais organizado.",
                "\nEXPLICAÇÃO:\nCódigo morto é como ter papéis velhos na sua mesa: eles distraem e dificultam encontrar o que você precisa. Ao se livrar deles, você trabalha melhor.",
                "\nEXPLICAÇÃO:\nCódigo morto é como ter roupas que você não usa mais no seu armário: apenas ocupam espaço e deixam tudo bagunçado. Ao removê-las, tudo fica mais fácil de gerenciar.",
                "\nEXPLICAÇÃO:\nCódigo morto é como ter lixo na sua mochila: é inútil e só atrapalha. Ao limpá-lo, você encontra tudo mais rápido e torna o uso mais fácil.",
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
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nÖlü kod, yerde dağınık halde duran kullanılmayan bloklara benzer: her şeyi daha dağınık ve anlaşılması zor hale getirir. Onu kaldırarak, projeniz daha temiz, anlaşılması daha kolay ve daha iyi çalışır hale gelecektir.",
                "\nAÇIKLAMA:\nÖlü kodlara sahip olmak, odanızda kırık oyuncaklar bulundurmak gibidir: işe yaramazlar ve sadece yer kaplarlar. Onları kaldırarak, her şey daha düzenli olacaktır.",
                "\nAÇIKLAMA:\nÖlü kod, masanızda eski kağıtların bulunması gibidir: dikkatinizi dağıtır ve ihtiyacınız olanı bulmayı zorlaştırır. Onlardan kurtularak, daha iyi çalışırsınız.",
                "\nAÇIKLAMA:\nÖlü kod, dolabınızda artık giymediğiniz kıyafetler bulundurmak gibidir: sadece yer kaplar ve her şeyin dağınık görünmesine neden olur. Onları kaldırmak, her şeyi yönetmeyi kolaylaştırır.",
                "\nAÇIKLAMA:\nÖlü kod, sırt çantanızda çöp bulundurmak gibidir: işe yaramaz ve sadece engel olur. Onu temizleyerek, her şeyi daha hızlı bulur ve kullanımı kolaylaştırırsınız.",
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
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nSprite-ek izen garrantzitsuak ematea tresnak etiketatzea bezala da: beharrezkoa dena azkar aurkitzean laguntzen du. Izen argiak egiten dute zure proiektua ulertzeko eta nabigatzeko errazagoa.",
                "\nAZALPENA:\nSprite-ak izendatzea ipuin batean pertsonaiak izendatzea bezala da: identitatea ematen die eta interakzioak argiagoak egiten ditu. Izen onak hobetzen dute zure proiektuaren irakurketa.",
                "\nAZALPENA:\nSprite-ak izendatzea antzezlan batean rolen banaketa bezala da: izena bakoitzak spritearen helburua adierazi behar du. Antolaketa hau proiektuaren egitura eta ulermena hobetzen du.",
                "\nAZALPENA:\nSprite-ak izendatzea orkestrako tresnak izendatzea bezala da: partea bakoitza bere papera armonikoki jokatzea bermatzen du. Izenetan argitasuna proiektuaren kudeaketa eta garapena hobetzen du.",
                "\nAZALPENA:\nSprite-en izendatzea errezeta batean ingredienteen etiketatzea bezala da: proiektua muntatzea eraginkorragoa eta ez-konplexua egiten du. Izen argiak lankidetza eta arazoen ebazpena arindu egiten du.",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nDar nomes significativos aos sprites é como etiquetar os obxectos na túa caixa de ferramentas: axúdate a atopar rapidamente o que necesitas. Nomes claros fan que o teu proxecto sexa máis doado de entender e navegar.",
                "\nEXPLICACIÓN:\nNomear sprites é como nomear personaxes nunha historia: dálles identidade e fai que as interaccións sexan máis claras. Nomes ben elixidos melloran a legibilidade do teu proxecto.",
                "\nEXPLICACIÓN:\nPensa en nomear sprites como asignar roles nunha obra de teatro: cada nome debe reflectir o propósito do sprite. Esta organización mellora a estrutura xeral e a comprensión do teu proxecto.",
                "\nEXPLICACIÓN:\nNomear sprites é como nomear instrumentos nunha orquestra: asegura que cada parte xogue o seu papel previsto de maneira harmoniosa. A claridade nos nomes mellora a xestión e o desenvolvemento do proxecto.",
                "\nEXPLICACIÓN:\nConsidera o nomeamento de sprites como etiquetar ingredientes nunha receita: fai que ensamblar o teu proxecto sexa máis eficiente e menos confuso. Nomes claros axilizan a colaboración e a resolución de problemas.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΤο να δίνεις σημαντικά ονόματα στα sprites είναι σαν να ετικετάρεις τα αντικείμενα στο εργαλειοθήκη σου: σε βοηθά να βρίσκεις γρήγορα αυτό που χρειάζεσαι. Καθαρά ονόματα κάνουν το έργο σου πιο εύκολο στην κατανόηση και την πλοήγηση.",
                "\nΕΡΜΗΝΕΙΑ:\nΤο να ονομάζεις τα sprites είναι σαν να ονομάζεις χαρακτήρες σε μια ιστορία: τους δίνει ταυτότητα και καθιστά τις αλληλεπιδράσεις πιο σαφείς. Καλώς επιλεγμένα ονόματα βελτιώνουν την αναγνωσιμότητα του έργου σου.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου το να ονομάζεις τα sprites ως την ανάθεση ρόλων σε μια θεατρική παράσταση: κάθε όνομα πρέπει να αντικατοπτρίζει τον σκοπό του sprite. Αυτή η οργάνωση βελτιώνει την συνολική δομή και κατανόηση του έργου σου.",
                "\nΕΡΜΗΝΕΙΑ:\nΤο να ονομάζεις τα sprites είναι σαν να ονομάζεις μουσικά όργανα σε ένα ορχηστρικό σύνολο: εξασφαλίζει ότι κάθε μέρος παίζει τον προβλεπόμενο ρόλο του με αρμονία. Η σαφήνεια στα ονόματα βελτιώνει τη διαχείριση και την ανάπτυξη του έργου.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου το να ονομάζεις τα sprites ως το να ετικετάρεις τα συστατικά σε μια συνταγή: κάνει τη συναρμολόγηση του έργου σου πιο αποδοτική και λιγότερο μπερδεμένη. Καθαρά ονόματα επιταχύνουν τη συνεργασία και την επίλυση προβλημάτων.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nDar nomes significativos aos sprites é como etiquetar os objetos na sua caixa de ferramentas: ajuda a encontrar rapidamente o que você precisa. Nomes claros tornam seu projeto mais fácil de entender e navegar.",
                "\nEXPLICAÇÃO:\nNomear sprites é como nomear personagens em uma história: dá-lhes identidade e torna as interações mais claras. Nomes bem escolhidos melhoram a legibilidade do seu projeto.",
                "\nEXPLICAÇÃO:\nPense em nomear sprites como atribuir papéis em uma peça de teatro: cada nome deve refletir o propósito do sprite. Esta organização melhora a estrutura geral e a compreensão do seu projeto.",
                "\nEXPLICAÇÃO:\nNomear sprites é como nomear instrumentos em uma orquestra: garante que cada parte desempenhe seu papel de forma harmoniosa. A clareza nos nomes melhora a gestão e o desenvolvimento do projeto.",
                "\nEXPLICAÇÃO:\nConsidere o nomear dos sprites como etiquetar ingredientes em uma receita: torna a montagem do seu projeto mais eficiente e menos confusa. Nomes claros agilizam a colaboração e a resolução de problemas.",
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
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nKuklalara anlamlı isimler vermek, alet kutunuzdaki öğeleri etiketlemek gibidir: ihtiyacınız olanı hızlıca bulmanıza yardımcı olur. Net isimler, projenizin anlaşılmasını ve gezinilmesini kolaylaştırır.",
                "\nAÇIKLAMA:\nKuklalara isim vermek, bir hikayedeki karakterlere isim vermek gibidir: onlara kimlik kazandırır ve etkileşimleri daha net hale getirir. İyi seçilmiş isimler, projenizin okunabilirliğini artırır.",
                "\nAÇIKLAMA:\nKuklalara isim vermeyi, bir oyundaki rolleri atamak gibi düşünün: her isim, kuklanın amacını yansıtmalıdır. Bu organizasyon, projenizin genel yapısını ve anlaşılmasını geliştirir.",
                "\nAÇIKLAMA:\nKuklalara isim vermek, bir orkestrada enstrümanlara isim vermek gibidir: her parçanın uyum içinde kendi rolünü oynamasını sağlar. İsimlendirmede netlik, proje yönetimini ve geliştirmeyi iyileştirir.",
                "\nAÇIKLAMA:\nKukla isimlendirmeyi, bir tarifteki malzemeleri etiketlemek olarak düşünün: projenizi birleştirmenizi daha verimli ve daha az kafa karıştırıcı hale getirir. Net isimler, işbirliğini ve sorun gidermeyi kolaylaştırır.",
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
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nFondoak izen garrantzitsuak ematea etxea oinarrizko atez ate etiketatzea bezala da: laguntzen dizu ambiente bakoitzari azkar identifikatzeko. Izen argiak egiten dute zure proiektua antolatzeko eta nabigatzeko errazagoa.",
                "\nAZALPENA:\nFondoak izendatzea film baten zenaletasunak izendatzea bezala da: testuinguru ematen du eta ipuinaren aurrerapenaren ulermena hobetzen du. Izen egokiak zure proiektua nahiagoa egiten du.",
                "\nAZALPENA:\nPentsatu fondoen izendatzea mapan kokapenak izendatzea bezala: izen bakoitza bere helburua argi adierazi behar du. Hau proiektuaren egitura orokorra hobetzen du eta ulermena errazten du.",
                "\nAZALPENA:\nFondoak izendatzea parke tematiko baten seinaleak jartzea bezala da: edozein eremua ondo identifikatuta egon behar du eta bisitalariak ez galdu. Izenetan argitasuna proiektuaren kudeaketa eta erabiltzaileen esperientzia hobetzen du.",
                "\nAZALPENA:\nFondoak izendatzea aldizkari baten atalak etiketatzea bezala da: zure proiektuan nabigatzea eraginkorragoa eta ez-konplexua egiten du. Izen argiak lankidetza eta arazoen ebazpena arindu egiten du.",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nDar nomes significativos aos fondos é como etiquetar as habitacións dunha casa: axúdate a identificar rapidamente cada entorno. Nomes claros fan que o teu proxecto sexa máis doado de organizar e navegar.",
                "\nEXPLICACIÓN:\nNomear fondos é como titular as escenas dunha película: proporciona contexto e mellora a comprensión da progresión da historia. Nomes apropiados fan que o teu proxecto sexa máis intuitivo.",
                "\nEXPLICACIÓN:\nPensa en nomear fondos como designar ubicacións nun mapa: cada nome debe indicar claramente o seu propósito. Isto mellora a estrutura xeral e facilita a comprensión do proxecto.",
                "\nEXPLICACIÓN:\nNomear fondos é como poñer carteis nun parque temático: asegura que cada área estea ben identificada e que os visitantes non se perdan. A claridade nos nomes mellora a xestión do proxecto e a experiencia do usuario.",
                "\nEXPLICACIÓN:\nConsidera nomear fondos como etiquetar as diferentes seccións dunha revista: fai que navegar polo teu proxecto sexa máis eficiente e menos confuso. Nomes claros axilizan a colaboración e a resolución de problemas.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΤο να δίνεις σημαντικά ονόματα στα φόντα είναι σαν να ετικετάρεις τα δωμάτια σε ένα σπίτι: σε βοηθά να αναγνωρίζεις γρήγορα κάθε περιβάλλον. Καθαρά ονόματα κάνουν το έργο σου πιο εύκολο να οργανωθεί και να πλοηγηθεί.",
                "\nΕΡΜΗΝΕΙΑ:\nΤο να ονομάζεις τα φόντα είναι σαν να δίνεις τίτλους στις σκηνές ενός φιλμ: παρέχει πλαίσιο και βελτιώνει την κατανόηση της προόδου της ιστορίας. Κατάλληλα ονόματα κάνουν το έργο σου πιο εύχρηστο.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου το να ονομάζεις τα φόντα ως την ανάθεση τοποθεσιών σε ένα χάρτη: κάθε όνομα πρέπει να δείχνει καθαρά τον σκοπό του. Αυτό βελτιώνει τη συνολική δομή και διευκολύνει την κατανόηση του έργου.",
                "\nΕΡΜΗΝΕΙΑ:\nΤο να ονομάζεις τα φόντα είναι σαν να βάζεις πινακίδες σε ένα θεματικό πάρκο: εξασφαλίζει ότι κάθε περιοχή είναι καλά αναγνωρισμένη και οι επισκέπτες δεν χάνονται. Η σαφήνεια στα ονόματα βελτιώνει τη διαχείριση του έργου και την εμπειρία του χρήστη.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου το να ονομάζεις τα φόντα ως το να ετικετάρεις τις διαφορετικές ενότητες ενός περιοδικού: κάνει την πλοήγηση στο έργο σου πιο αποδοτική και λιγότερο μπερδεμένη. Καθαρά ονόματα επιταχύνουν τη συνεργασία και την επίλυση προβλημάτων.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nDar nomes significativos aos fundos é como etiquetar os cômodos de uma casa: ajuda a identificar rapidamente cada ambiente. Nomes claros tornam seu projeto mais fácil de organizar e navegar.",
                "\nEXPLICAÇÃO:\nNomear fundos é como nomear as cenas de um filme: fornece contexto e melhora a compreensão da progressão da história. Nomes apropriados tornam seu projeto mais intuitivo.",
                "\nEXPLICAÇÃO:\nPense em nomear fundos como designar locais em um mapa: cada nome deve indicar claramente seu propósito. Isso melhora a estrutura geral e facilita a compreensão do projeto.",
                "\nEXPLICAÇÃO:\nNomear fundos é como colocar placas em um parque temático: garante que cada área esteja bem identificada e que os visitantes não se percam. A clareza nos nomes melhora a gestão do projeto e a experiência do usuário.",
                "\nEXPLICAÇÃO:\nConsidere nomear fundos como etiquetar as diferentes seções de uma revista: torna a navegação pelo seu projeto mais eficiente e menos confusa. Nomes claros agilizam a colaboração e a resolução de problemas.",
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
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nDekorlara anlamlı isimler vermek, bir evdeki odaları etiketlemek gibidir: her ortamı hızlıca tanımanıza yardımcı olur. Net isimler, projenizin organize edilmesini ve gezinilmesini kolaylaştırır.",
                "\nAÇIKLAMA:\nDekorlara isim vermek, bir filmdeki sahnelere başlık vermek gibidir: bağlam sağlar ve hikayenin ilerleyişinin anlaşılmasını artırır. Uygun isimler, projenizin daha sezgisel olmasını sağlar.",
                "\nAÇIKLAMA:\nDekorlara isim vermeyi, bir haritada konumları belirlemek gibi düşünün: her isim amacını açıkça belirtmelidir. Bu, genel yapıyı geliştirir ve projenin anlaşılmasını kolaylaştırır.",
                "\nAÇIKLAMA:\nDekorlara isim vermek, bir tema parkında tabelalar koymak gibidir: her alanın iyi tanımlanmasını sağlar ve ziyaretçilerin kaybolmamasını sağlar. İsimlendirmede netlik, proje yönetimini ve kullanıcı deneyimini artırır.",
                "\nAÇIKLAMA:\nDekor isimlendirmeyi, bir derginin farklı bölümlerini etiketlemek olarak düşünün: projenizde gezinmeyi daha verimli ve daha az kafa karıştırıcı hale getirir. Net isimler, işbirliğini ve sorun gidermeyi kolaylaştırır.",
            ]
        else:
            return []

    def get_messages_explanation_phrases(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nGiving meaningful names to broadcasts is like labeling the buttons on a control panel: it helps you understand their purpose at a glance. Clear names make debugging and collaboration more efficient.",
                "\nEXPLANATION:\nNaming broadcasts is like naming the chapters of a book: it provides clarity and context, making it easier to follow the logic of your project. This avoids confusion and ensures smooth navigation.",
                "\nEXPLANATION:\nThink of naming broadcasts like labeling containers in a kitchen: each label should reflect its contents to prevent mistakes. Descriptive names improve organization and streamline the development process.",
                "\nEXPLANATION:\nNaming broadcasts is like assigning meaningful filenames to your documents: it saves time and reduces the risk of misinterpretation. Proper names enhance communication and maintain project clarity.",
                "\nEXPLANATION:\nConsider naming broadcasts like giving clear directions on a map: it ensures everyone understands the purpose of each element, leading to better collaboration and project management.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nDar nombres significativos a los broadcasts es como etiquetar los botones de un panel de control: te ayuda a entender su propósito de un vistazo. Los nombres claros hacen que la depuración y la colaboración sean más eficientes.",
                "\nEXPLICACIÓN:\nNombrar los broadcasts es como nombrar los capítulos de un libro: proporciona claridad y contexto, facilitando el seguimiento de la lógica de tu proyecto. Esto evita confusiones y asegura una navegación fluida.",
                "\nEXPLICACIÓN:\nPiensa en nombrar los broadcasts como etiquetar los contenedores en una cocina: cada etiqueta debe reflejar su contenido para evitar errores. Los nombres descriptivos mejoran la organización y agilizan el proceso de desarrollo.",
                "\nEXPLICACIÓN:\nNombrar los broadcasts es como asignar nombres significativos a tus documentos: ahorra tiempo y reduce el riesgo de malentendidos. Los nombres adecuados mejoran la comunicación y mantienen la claridad del proyecto.",
                "\nEXPLICACIÓN:\nConsidera nombrar los broadcasts como dar indicaciones claras en un mapa: asegura que todos entiendan el propósito de cada elemento, lo que lleva a una mejor colaboración y gestión del proyecto.",
            ]
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nEmandako izen esanguratsuek broadcast-ak izendatzea kontrol-panelean botoiak etiketatzea bezala da: zure helburua ikusteko laguntzen dizu. Izen argiek deskargatzea eta lankidetza eraginkorragoak bihurtzen dituzte.",
                "\nAZALPENA:\nBroadcast-ak izendatzea liburu baten kapituloak izendatzea bezala da: argitasuna eta testuingurua eskaintzen du, proiektuko logika jarraitzea errazten du. Honek nahasteak saihesten ditu eta nabigazio leuna ziurtatzen du.",
                "\nAZALPENA:\nBroadcast-ak izendatzea sukaldeko ontziak etiketatzea bezala pentsa dezakezu: etiketak bere edukiaren arabera egon behar dira, akatsak saihesteko. Izen deskribatzaileek antolakuntza hobetzen dute eta garapen prozesua bizkortzen dute.",
                "\nAZALPENA:\nBroadcast-ak izendatzea zure dokumentuei izen esanguratsuak ematea bezala da: denbora aurrezten du eta gaizki ulertuak murrizten ditu. Izen egokiak komunikazioa hobetzen dute eta proiektuaren argitasuna mantentzen dute.",
                "\nAZALPENA:\nPentsa broadcast-ak izendatzea mapa batean adierazpen argiak ematea bezala: guztiek elementu bakoitzaren helburua ulertzea ziurtatzen du, eta honek lankidetza eta proiektuaren kudeaketa hobetzen ditu.",
            ]

        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nDar nomes significativos aos broadcasts é coma etiquetar os botóns dun panel de control: axúdache a entender o seu propósito dun vistazo. Os nomes claros fan que a depuración e a colaboración sexan máis eficientes.",
                "\nEXPLICACIÓN:\nNomear os broadcasts é coma nomear os capítulos dun libro: proporciona clareza e contexto, facilitando o seguimento da lóxica do teu proxecto. Isto evita confusións e asegura unha navegación fluída.",
                "\nEXPLICACIÓN:\nPensa en nomear os broadcasts coma etiquetar os contedores nunha cociña: cada etiqueta debe reflectir o seu contido para evitar erros. Os nomes descritivos melloran a organización e agilizan o proceso de desenvolvemento.",
                "\nEXPLICACIÓN:\nNomear os broadcasts é coma asignar nomes significativos aos teus documentos: aforra tempo e reduce o risco de malentendidos. Os nomes axeitados melloran a comunicación e manteñen a clareza do proxecto.",
                "\nEXPLICACIÓN:\nConsidera nomear os broadcasts coma dar indicacións claras nun mapa: asegura que todos entendan o propósito de cada elemento, o que leva a unha mellor colaboración e xestión do proxecto.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΡΜΗΝΕΙΑ:\nΤο να δίνεις σημασιολογικά ονόματα στις μεταδόσεις είναι σαν να ετικετάρεις τα κουμπιά ενός πίνακα ελέγχου: σε βοηθά να κατανοήσεις τον σκοπό τους με μια ματιά. Τα καθαρά ονόματα κάνουν τον εντοπισμό σφαλμάτων και τη συνεργασία πιο αποδοτικά.",
                "\nΕΡΜΗΝΕΙΑ:\nΗ ονομασία των μεταδόσεων είναι σαν να ονομάζεις τα κεφάλαια ενός βιβλίου: προσφέρει σαφήνεια και συμφραζόμενα, διευκολύνοντας την παρακολούθηση της λογικής του έργου σου. Αυτό αποτρέπει τις συγχύσεις και εξασφαλίζει ομαλή πλοήγηση.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου την ονομασία των μεταδόσεων σαν να ετικετάρεις τα δοχεία σε μια κουζίνα: κάθε ετικέτα πρέπει να αντικατοπτρίζει το περιεχόμενό της για να αποφεύγονται τα λάθη. Τα περιγραφικά ονόματα βελτιώνουν την οργάνωση και επιταχύνουν τη διαδικασία ανάπτυξης.",
                "\nΕΡΜΗΝΕΙΑ:\nΗ ονομασία των μεταδόσεων είναι σαν να δίνεις σημασιολογικά ονόματα στα έγγραφά σου: εξοικονομεί χρόνο και μειώνει τον κίνδυνο παρερμηνειών. Τα κατάλληλα ονόματα βελτιώνουν την επικοινωνία και διατηρούν τη σαφήνεια του έργου.",
                "\nΕΡΜΗΝΕΙΑ:\nΣκέψου την ονομασία των μεταδόσεων σαν να δίνεις σαφείς οδηγίες σε έναν χάρτη: διασφαλίζει ότι όλοι καταλαβαίνουν τον σκοπό κάθε στοιχείου, κάτι που οδηγεί σε καλύτερη συνεργασία και διαχείριση του έργου.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nDar nomes significativos aos broadcasts é como etiquetar os botões de um painel de controle: ajuda a entender seu propósito com um só olhar. Nomes claros tornam a depuração e a colaboração mais eficientes.",
                "\nEXPLICAÇÃO:\nNomear os broadcasts é como nomear os capítulos de um livro: fornece clareza e contexto, facilitando o acompanhamento da lógica do seu projeto. Isso evita confusões e garante uma navegação fluida.",
                "\nEXPLICAÇÃO:\nPense em nomear os broadcasts como etiquetar os recipientes em uma cozinha: cada etiqueta deve refletir seu conteúdo para evitar erros. Nomes descritivos melhoram a organização e aceleram o processo de desenvolvimento.",
                "\nEXPLICAÇÃO:\nNomear os broadcasts é como dar nomes significativos aos seus documentos: economiza tempo e reduz o risco de mal-entendidos. Nomes adequados melhoram a comunicação e mantêm a clareza do projeto.",
                "\nEXPLICAÇÃO:\nConsidere nomear os broadcasts como dar instruções claras em um mapa: garante que todos entendam o propósito de cada elemento, o que leva a uma melhor colaboração e gestão do projeto.",
            ]
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nDare nomi significativi ai broadcast è come etichettare i pulsanti di un pannello di controllo: ti aiuta a capire il loro scopo con uno sguardo. Nomi chiari rendono il debug e la collaborazione più efficienti.",
                "\nSPIEGAZIONE:\nNomina dei broadcast è come nominare i capitoli di un libro: fornisce chiarezza e contesto, facilitando il seguito della logica del tuo progetto. Questo evita confusioni e garantisce una navigazione fluida.",
                "\nSPIEGAZIONE:\nPensa alla nomina dei broadcast come all'etichettatura dei contenitori in una cucina: ogni etichetta dovrebbe riflettere il suo contenuto per evitare errori. I nomi descrittivi migliorano l'organizzazione e accelerano il processo di sviluppo.",
                "\nSPIEGAZIONE:\nNomina dei broadcast è come dare nomi significativi ai tuoi documenti: risparmia tempo e riduce il rischio di fraintendimenti. I nomi giusti migliorano la comunicazione e mantengono la chiarezza del progetto.",
                "\nSPIEGAZIONE:\nConsidera la nomina dei broadcast come dare indicazioni chiare su una mappa: assicura che tutti capiscano lo scopo di ogni elemento, il che porta a una migliore collaborazione e gestione del progetto.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nДавать значимые имена вещаниям — это как подписывать кнопки на панели управления: это помогает понять их назначение с первого взгляда. Ясные имена делают отладку и сотрудничество более эффективными.",
                "\nОБЪЯСНЕНИЕ:\nНазначение имен вещаниям похоже на именование глав книги: это дает ясность и контекст, облегчая отслеживание логики вашего проекта. Это предотвращает путаницу и обеспечивает плавную навигацию.",
                "\nОБЪЯСНЕНИЕ:\nПредставьте, что назначение имен вещаниям — это как подписывать контейнеры на кухне: каждая этикетка должна отражать содержание, чтобы избежать ошибок. Описательные имена улучшают организацию и ускоряют процесс разработки.",
                "\nОБЪЯСНЕНИЕ:\nНазначение имен вещаниям — это как давать значимые имена вашим документам: экономит время и снижает риск недоразумений. Подобающие имена улучшают коммуникацию и сохраняют ясность проекта.",
                "\nОБЪЯСНЕНИЕ:\nПредставьте назначение имен вещаниям как дачу четких указаний на карте: это гарантирует, что все понимают назначение каждого элемента, что приводит к лучшему сотрудничеству и управлению проектом.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nDonar noms significatius als broadcasts és com etiquetar els botons d'un panell de control: t'ajuda a entendre el seu propòsit d'una ullada. Els noms clars fan que la depuració i la col·laboració siguin més eficients.",
                "\nEXPLICACIÓ:\nAnomenar els broadcasts és com anomenar els capítols d'un llibre: proporciona claredat i context, facilitant el seguiment de la lògica del teu projecte. Això evita confusions i garanteix una navegació fluida.",
                "\nEXPLICACIÓ:\nPensa en anomenar els broadcasts com etiquetar els contenidors a la cuina: cada etiqueta ha de reflectir el seu contingut per evitar errors. Els noms descriptius milloren l'organització i acceleren el procés de desenvolupament.",
                "\nEXPLICACIÓ:\nAnomenar els broadcasts és com donar noms significatius als teus documents: estalvia temps i redueix el risc de malentesos. Els noms adequats milloren la comunicació i mantenen la claredat del projecte.",
                "\nEXPLICACIÓ:\nConsidera anomenar els broadcasts com donar instruccions clares a un mapa: assegura't que tothom entengui el propòsit de cada element, cosa que porta a una millor col·laboració i gestió del projecte.",
            ]
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nBroadcast'lere anlamlı isimler vermek, bir kontrol panelindeki düğmeleri etiketlemeye benzer: Amacını bir bakışta anlamana yardımcı olur. Açık isimler, hata ayıklamayı ve işbirliğini daha verimli hale getirir.",
                "\nAÇIKLAMA:\nBroadcast'leri adlandırmak, bir kitabın bölümlerini adlandırmaya benzer: Projendeki mantığı takip etmeyi kolaylaştıran netlik ve bağlam sağlar. Bu, kafa karışıklıklarını önler ve düzgün bir gezinmeyi garanti eder.",
                "\nAÇIKLAMA:\nBroadcast'leri adlandırmayı, bir mutfakta kapları etiketlemeye benzetebilirsin: Her etiket içeriğini yansıtmalı, böylece hatalardan kaçınılır. Tanımlayıcı isimler, organizasyonu geliştirir ve geliştirme sürecini hızlandırır.",
                "\nAÇIKLAMA:\nBroadcast'lere anlamlı isimler vermek, belgelerine anlamlı isimler vermek gibidir: Zaman kazandırır ve yanlış anlamaların riskini azaltır. Uygun isimler, iletişimi geliştirir ve projenin netliğini korur.",
                "\nAÇIKLAMA:\nBroadcast'leri adlandırmayı bir haritaya açık talimatlar vermek gibi düşün: Her öğenin amacını herkesin anlamasını sağlar, bu da daha iyi işbirliği ve proje yönetimi sağlar.",
            ]
        else:
            return []
        
    def get_variable_naming_explanations(self):
        if self.curr_lan == 'en':
            return [
                "\nEXPLANATION:\nUsing default variable names is like labeling every button on a control panel as 'button': it creates confusion and makes debugging a nightmare. Clear, specific names improve code readability and maintenance.",
                "\nEXPLANATION:\nDefault variable names are like calling every folder on your computer 'new folder': it becomes impossible to find what you need. Descriptive names help organize your code and avoid errors.",
                "\nEXPLANATION:\nKeeping default variable names is like using placeholders in a recipe: without clarity, the end result can be disastrous. Meaningful names guide both you and collaborators.",
                "\nEXPLANATION:\nDefault names for variables are like having identical keys without labels: finding the right one is frustrating and time-consuming. Specific names save time and reduce confusion.",
                "\nEXPLANATION:\nUsing default variable names is like writing a book where every character is named 'person': it’s impossible to follow the story. Unique, descriptive names make your code logical and understandable.",
            ]
        elif self.curr_lan == 'es':
            return [
                "\nEXPLICACIÓN:\nUsar nombres de variables por defecto es como etiquetar todos los botones de un panel de control como 'botón': genera confusión y hace que la depuración sea una pesadilla. Los nombres claros y específicos mejoran la legibilidad y el mantenimiento del código.",
                "\nEXPLICACIÓN:\nLos nombres de variables por defecto son como llamar a todas las carpetas de tu ordenador 'nueva carpeta': se vuelve imposible encontrar lo que necesitas. Los nombres descriptivos ayudan a organizar tu código y evitan errores.",
                "\nEXPLICACIÓN:\nMantener nombres de variables por defecto es como usar marcadores de posición en una receta: sin claridad, el resultado final puede ser desastroso. Los nombres significativos guían tanto a ti como a tus colaboradores.",
                "\nEXPLICACIÓN:\nLos nombres por defecto en las variables son como tener llaves idénticas sin etiquetas: encontrar la correcta es frustrante y lleva tiempo. Los nombres específicos ahorran tiempo y reducen la confusión.",
                "\nEXPLICACIÓN:\nUsar nombres de variables por defecto es como escribir un libro donde todos los personajes se llaman 'persona': es imposible seguir la historia. Los nombres únicos y descriptivos hacen que tu código sea lógico y comprensible.",
            ]
        elif self.curr_lan == 'eu':
            return [
                "\nAZALPENA:\nAldagai izen lehenetsiak erabiltzea kontrol-paneleko botoi guztiak 'botoi' bezala etiketatzea bezalakoa da: nahasmena sortzen du eta arazketa amesgaizto bihurtzen du. Izen argi eta zehatzek kodearen irakurgarritasuna eta mantentzea hobetzen dute.",
                "\nAZALPENA:\nAldagai izen lehenetsiak erabiltzea zure ordenagailuko karpeta guztiak 'karpeta berria' deitzea bezalakoa da: behar duzuna aurkitzea ezinezkoa bihurtzen da. Izen deskriptiboek zure kodea antolatzen laguntzen dute eta erroreak saihesten dituzte.",
                "\nAZALPENA:\nAldagai izen lehenetsiak mantentzea errezeta batean leku-markatzaileak erabiltzea bezalakoa da: argitasunik gabe, emaitza katastrofikoa izan daiteke. Izen esanguratsuek bai zu bai zure lankideak gidatzen zaituztete.",
                "\nAZALPENA:\nAldagaietan lehenetsitako izenak edukitzea etiketarik gabeko giltza berdinak izatea bezalakoa da: egokia aurkitzea neketsua eta denbora-galtzea da. Izen zehatzenek denbora aurrezten dute eta nahasmena murrizten dute.",
                "\nAZALPENA:\nAldagai izen lehenetsiak erabiltzea pertsonaia guztiak 'pertsona' deitzen diren liburu bat idaztea bezalakoa da: istorioa jarraitzea ezinezkoa da. Izen bakar eta deskriptiboek zure kodea logiko eta ulergarria bihurtzen dute.",
            ]
        elif self.curr_lan == 'gl':
            return [
                "\nEXPLICACIÓN:\nUsar nomes de variábeis por defecto é coma etiquetar todos os botóns dun panel de control como 'botón': xera confusión e fai que a depuración sexa un pesadelo. Os nomes claros e específicos melloran a lexibilidade e o mantemento do código.",
                "\nEXPLICACIÓN:\nOs nomes de variábeis por defecto son coma chamar a todas as carpetas do teu ordenador 'nova carpeta': faise imposible atopar o que necesitas. Os nomes descritivos axudan a organizar o teu código e evitan erros.",
                "\nEXPLICACIÓN:\nManter nomes de variábeis por defecto é coma usar marcadores de posición nunha receita: sen claridade, o resultado final pode ser desastroso. Os nomes significativos guían tanto a ti coma aos teus colaboradores.",
                "\nEXPLICACIÓN:\nOs nomes por defecto nas variábeis son coma ter chaves idénticas sen etiquetas: atopar a correcta é frustrante e leva tempo. Os nomes específicos aforran tempo e reducen a confusión.",
                "\nEXPLICACIÓN:\nUsar nomes de variábeis por defecto é coma escribir un libro onde todos os personaxes se chaman 'persoa': é imposible seguir a historia. Os nomes únicos e descritivos fan que o teu código sexa lóxico e comprensible.",
            ]
        elif self.curr_lan == 'el':
            return [
                "\nΕΞΗΓΗΣΗ:\nΗ χρήση προεπιλεγμένων ονομάτων μεταβλητών είναι σαν να χαρακτηρίζετε όλα τα κουμπιά σε έναν πίνακα ελέγχου ως 'κουμπί': προκαλεί σύγχυση και καθιστά την αποσφαλμάτωση εφιάλτη. Τα σαφή και συγκεκριμένα ονόματα βελτιώνουν την αναγνωσιμότητα και τη συντήρηση του κώδικα.",
                "\nΕΞΗΓΗΣΗ:\nΤα προεπιλεγμένα ονόματα μεταβλητών είναι σαν να ονομάζετε όλους τους φακέλους στον υπολογιστή σας 'νέος φάκελος': γίνεται αδύνατο να βρείτε αυτό που χρειάζεστε. Τα περιγραφικά ονόματα βοηθούν στην οργάνωση του κώδικα και αποτρέπουν σφάλματα.",
                "\nΕΞΗΓΗΣΗ:\nΗ διατήρηση προεπιλεγμένων ονομάτων μεταβλητών είναι σαν να χρησιμοποιείτε σύμβολα κράτησης θέσης σε μια συνταγή: χωρίς σαφήνεια, το τελικό αποτέλεσμα μπορεί να είναι καταστροφικό. Τα σημασιολογικά ονόματα καθοδηγούν τόσο εσάς όσο και τους συνεργάτες σας.",
                "\nΕΞΗΓΗΣΗ:\nΤα προεπιλεγμένα ονόματα για μεταβλητές είναι σαν να έχετε πανομοιότυπα κλειδιά χωρίς ετικέτες: η εύρεση του σωστού είναι απογοητευτική και χρονοβόρα. Τα συγκεκριμένα ονόματα εξοικονομούν χρόνο και μειώνουν τη σύγχυση.",
                "\nΕΞΗΓΗΣΗ:\nΗ χρήση προεπιλεγμένων ονομάτων μεταβλητών είναι σαν να γράφετε ένα βιβλίο όπου όλοι οι χαρακτήρες ονομάζονται 'πρόσωπο': είναι αδύνατο να παρακολουθήσετε την ιστορία. Τα μοναδικά και περιγραφικά ονόματα καθιστούν τον κώδικά σας λογικό και κατανοητό.",
            ]
        elif self.curr_lan == 'pt':
            return [
                "\nEXPLICAÇÃO:\nUsar nomes padrão para variáveis é como etiquetar todos os botões de um painel de controle como 'botão': cria confusão e torna a depuração um pesadelo. Nomes claros e específicos melhoram a legibilidade e manutenção do código.",
                "\nEXPLICAÇÃO:\nNomes padrão para variáveis são como chamar todas as pastas do seu computador de 'nova pasta': torna-se impossível encontrar o que você precisa. Nomes descritivos ajudam a organizar o código e evitam erros.",
                "\nEXPLICAÇÃO:\nManter nomes padrão para variáveis é como usar espaços reservados em uma receita: sem clareza, o resultado final pode ser desastroso. Nomes significativos guiam você e seus colaboradores.",
                "\nEXPLICAÇÃO:\nNomes padrão para variáveis são como ter chaves idênticas sem rótulos: encontrar a correta é frustrante e demorado. Nomes específicos economizam tempo e reduzem a confusão.",
                "\nEXPLICAÇÃO:\nUsar nomes padrão para variáveis é como escrever um livro onde todos os personagens se chamam 'pessoa': é impossível seguir a história. Nomes únicos e descritivos tornam seu código lógico e compreensível.",
            ]
        elif self.curr_lan == 'it':
            return [
                "\nSPIEGAZIONE:\nUtilizzare nomi predefiniti per le variabili è come etichettare tutti i pulsanti di un pannello di controllo come 'pulsante': crea confusione e rende il debugging un incubo. Nomi chiari e specifici migliorano la leggibilità e la manutenzione del codice.",
                "\nSPIEGAZIONE:\nI nomi predefiniti per le variabili sono come chiamare tutte le cartelle del tuo computer 'nuova cartella': diventa impossibile trovare ciò che ti serve. Nomi descrittivi aiutano a organizzare il codice e a evitare errori.",
                "\nSPIEGAZIONE:\nMantenere nomi predefiniti per le variabili è come usare segnaposto in una ricetta: senza chiarezza, il risultato finale può essere disastroso. Nomi significativi guidano te e i tuoi collaboratori.",
                "\nSPIEGAZIONE:\nI nomi predefiniti per le variabili sono come avere chiavi identiche senza etichette: trovare quella giusta è frustrante e richiede tempo. Nomi specifici fanno risparmiare tempo e riducono la confusione.",
                "\nSPIEGAZIONE:\nUsare nomi predefiniti per le variabili è come scrivere un libro in cui tutti i personaggi si chiamano 'persona': è impossibile seguire la storia. Nomi unici e descrittivi rendono il tuo codice logico e comprensibile.",
            ]
        elif self.curr_lan == 'ru':
            return [
                "\nОБЪЯСНЕНИЕ:\nИспользование имен переменных по умолчанию похоже на то, как если все кнопки на пульте управления назвать 'button': это создает путаницу и превращает отладку в кошмар. Четкие и конкретные имена улучшают читаемость и обслуживание кода.",
                "\nОБЪЯСНЕНИЕ:\nИмена переменных по умолчанию — это как называть все папки на компьютере 'новая папка': становится невозможно найти то, что нужно. Описательные имена помогают организовать код и избежать ошибок.",
                "\nОБЪЯСНЕНИЕ:\nСохранение имен переменных по умолчанию похоже на использование заполнителей в рецепте: без ясности конечный результат может быть катастрофическим. Осмысленные имена помогают вам и вашим коллегам.",
                "\nОБЪЯСНЕНИЕ:\nИмена переменных по умолчанию похожи на одинаковые ключи без этикеток: найти нужный становится сложно и затратно по времени. Конкретные имена экономят время и уменьшают путаницу.",
                "\nОБЪЯСНЕНИЕ:\nИспользование имен переменных по умолчанию похоже на написание книги, где всех персонажей зовут 'человек': следить за историей невозможно. Уникальные и описательные имена делают ваш код логичным и понятным.",
            ]
        elif self.curr_lan == 'ca':
            return [
                "\nEXPLICACIÓ:\nUtilitzar noms de variables per defecte és com etiquetar tots els botons d'un panell de control com a 'botó': genera confusió i fa que la depuració sigui un malson. Els noms clars i específics milloren la llegibilitat i el manteniment del codi.",
                "\nEXPLICACIÓ:\nEls noms de variables per defecte són com anomenar totes les carpetes del teu ordinador 'nova carpeta': esdevé impossible trobar el que necessites. Els noms descriptius ajuden a organitzar el teu codi i eviten errors.",
                "\nEXPLICACIÓ:\nMantenir noms de variables per defecte és com utilitzar marcadors de posició en una recepta: sense claredat, el resultat final pot ser desastrós. Els noms significatius guien tant a tu com als teus col·laboradors.",
                "\nEXPLICACIÓ:\nEls noms per defecte a les variables són com tenir claus idèntiques sense etiquetes: trobar la correcta és frustrant i requereix molt de temps. Els noms específics estalvien temps i redueixen la confusió.",
                "\nEXPLICACIÓ:\nUtilitzar noms de variables per defecte és com escriure un llibre on tots els personatges es diuen 'persona': és impossible seguir la història. Els noms únics i descriptius fan que el teu codi sigui lògic i comprensible.",
            ]
        elif self.curr_lan == 'tr':
            return [
                "\nAÇIKLAMA:\nVarsayılan değişken adlarını kullanmak, bir kontrol panelindeki tüm düğmeleri 'düğme' olarak etiketlemek gibidir: kafa karışıklığı yaratır ve hata ayıklamayı kâbusa çevirir. Açık ve spesifik adlar, kodun okunabilirliğini ve bakımını iyileştirir.",
                "\nAÇIKLAMA:\nVarsayılan değişken adları, bilgisayarınızdaki tüm klasörlere 'yeni klasör' adını vermek gibidir: ihtiyacınız olanı bulmayı imkânsız hale getirir. Açıklayıcı adlar kodunuzu düzenlemeye yardımcı olur ve hataları önler.",
                "\nAÇIKLAMA:\nVarsayılan değişken adlarını korumak, bir tarifte yer tutucular kullanmak gibidir: netlik olmadan, sonuç felaket olabilir. Anlamlı adlar, hem sizi hem de iş arkadaşlarınızı yönlendirir.",
                "\nAÇIKLAMA:\nVarsayılan değişken adları, etiketsiz aynı anahtarlara sahip olmak gibidir: doğru olanı bulmak sinir bozucu ve zaman alıcıdır. Belirli adlar zaman kazandırır ve kafa karışıklığını azaltır.",
                "\nAÇIKLAMA:\nVarsayılan değişken adlarını kullanmak, tüm karakterlerin 'kişi' olarak adlandırıldığı bir kitap yazmak gibidir: hikayeyi takip etmek imkânsızdır. Benzersiz ve açıklayıcı adlar, kodunuzu mantıklı ve anlaşılır hale getirir.",
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
                'Messages': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the message naming, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE MESSAGE NAMING, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'Variables': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the variables naming, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE VARIABLES NAMING, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'deadCode': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the dead code, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DEAD CODE, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'Duplicates': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the duplicated code already, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE DUPLICATED CODE, that's very great news! Does it seem good to you if we keep improving the project?",
                },
                'Sequential': {
                    'fail': "Oooops, it's seem's that you haven't solved the problem with the sequential blocks already, but don't worry, we are going to review again how we could solve it,",
                    'success': "YEAAHH, YOU HAVE SOLVED THE PROBLEM WITH THE SEQUENTIAL BLOCKS, that's very great news! Does it seem good to you if we keep improving the project?",
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
                'Messages': {
                    'fail': "Oooops, parece que no has resuelto el problema con el nombramiento de los mensajes, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL NOMBRAMIENTO DE LOS MENSAJES, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'Variables': {
                    'fail': "Oooops, parece que no has resuelto el problema con el nombramiento de las variables, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL NOMBRAMIENTO DE LOS VARIABLES, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'deadCode': {
                    'fail': "Oooops, parece que no has resuelto el problema con el código muerto, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL CÓDIGO MUERTO, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'Duplicates': {
                    'fail': "Oooops, parece que no has resuelto el problema con el código duplicado, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON EL CÓDIGO DUPLICADO, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                },
                'Sequential': {
                    'fail': "Oooops, parece que no has resuelto el problema con los bloques secuenciales, pero no te preocupes, vamos a revisar cómo podríamos resolverlo de nuevo,",
                    'success': "¡YEAHH, HAS RESUELTO EL PROBLEMA CON LOS BLOQUES SECUENCIALES, esa es una noticia genial! ¿Te parece bien si seguimos mejorando el proyecto?",
                }
            }
        elif self.curr_lan == 'eu':
            return {
                'Backdrops': {
                    'fail': "Oooops, dirudienez ez duzu fondoen izendapen arazoa konpondu, baina ez kezkatu, berriro konpon dezakegu,",
                    'success': "¡YEAHH, FONDOEN IZENDAPEN ARAZOA KONPONDU DUZU, berri ona da hau! Segitzen ari garen proiektua hobetzen jarraitzea ondo dago?",
                },
                'Sprites': {
                    'fail': "Oooops, dirudienez ez duzu sprite-en izendapen arazoa konpondu, baina ez kezkatu, berriro konpon dezakegu,",
                    'success': "¡YEAHH, SPRITE-EN IZENDAPEN ARAZOA KONPONDU DUZU, berri ona da hau! Segitzen ari garen proiektua hobetzen jarraitzea ondo dago?",
                },
                'deadCode': {
                    'fail': "Oooops, dirudienez ez duzu kode hil arazoa konpondu, baina ez kezkatu, berriro konpon dezakegu,",
                    'success': "¡YEAHH, KODE HIL ARAZOA KONPONDU DUZU, berri ona da hau! Segitzen ari garen proiektua hobetzen jarraitzea ondo dago?",
                },
                'Duplicates': {
                    'fail': "Oooops, dirudienez ez duzu kode bikoitza arazoa konpondu, baina ez kezkatu, berriro konpon dezakegu,",
                    'success': "¡YEAHH, KODE BIKOITZA ARAZOA KONPONDU DUZU, berri ona da hau! Segitzen ari garen proiektua hobetzen jarraitzea ondo dago?",
                }
            }
        elif self.curr_lan == 'gl':
            return {
                'Backdrops': {
                    'fail': "Oooops, parece que non resolviches o problema co nomeamento dos fondos, pero non te preocupes, imos revisar como poderiamos resolvelo de novo,",
                    'success': "¡YEAHH, RESOLVESTES O PROBLEMA CO NOMEAMENTO DOS FONDOS, esa é unha gran nova! Pareceche ben se seguimos mellorando o proxecto?",
                },
                'Sprites': {
                    'fail': "Oooops, parece que non resolviches o problema co nomeamento dos sprites, pero non te preocupes, imos revisar como poderiamos resolvelo de novo,",
                    'success': "¡YEAHH, RESOLVESTES O PROBLEMA CO NOMEAMENTO DOS SPRITES, esa é unha gran nova! Pareceche ben se seguimos mellorando o proxecto?",
                },
                'deadCode': {
                    'fail': "Oooops, parece que non resolviches o problema co código morto, pero non te preocupes, imos revisar como poderiamos resolvelo de novo,",
                    'success': "¡YEAHH, RESOLVESTES O PROBLEMA CO CÓDIGO MORTO, esa é unha gran nova! Pareceche ben se seguimos mellorando o proxecto?",
                },
                'Duplicates': {
                    'fail': "Oooops, parece que non resolviches o problema co código duplicado, pero non te preocupes, imos revisar como poderiamos resolvelo de novo,",
                    'success': "¡YEAHH, RESOLVESTES O PROBLEMA CO CÓDIGO DUPLICADO, esa é unha gran nova! Pareceche ben se seguimos mellorando o proxecto?",
                }
            }
        elif self.curr_lan == 'el':
            return {
                'Backdrops': {
                    'fail': "Ούπς, φαίνεται ότι δεν έχεις λύσει το πρόβλημα με την ονομασία των φόντων, αλλά μην ανησυχείς, θα δούμε πώς μπορούμε να το επιλύσουμε ξανά,",
                    'success': "ΝΑΙΙΙΙ, ΕΧΕΙΣ ΛΥΣΕΙ ΤΟ ΠΡΟΒΛΗΜΑ ΜΕ ΤΗΝ ΟΝΟΜΑΣΙΑ ΤΩΝ ΦΟΝΤΩΝ, αυτή είναι μια εξαιρετική είδηση! Θα συνεχίσουμε να βελτιώνουμε το έργο σου;",
                },
                'Sprites': {
                    'fail': "Ούπς, φαίνεται ότι δεν έχεις λύσει το πρόβλημα με την ονομασία των sprites, αλλά μην ανησυχείς, θα δούμε πώς μπορούμε να το επιλύσουμε ξανά,",
                    'success': "ΝΑΙΙΙΙ, ΕΧΕΙΣ ΛΥΣΕΙ ΤΟ ΠΡΟΒΛΗΜΑ ΜΕ ΤΗΝ ΟΝΟΜΑΣΙΑ ΤΩΝ SPRITES, αυτή είναι μια εξαιρετική είδηση! Θα συνεχίσουμε να βελτιώνουμε το έργο σου;",
                },
                'deadCode': {
                    'fail': "Ούπς, φαίνεται ότι δεν έχεις λύσει το πρόβλημα με τον νεκρό κώδικα, αλλά μην ανησυχείς, θα δούμε πώς μπορούμε να το επιλύσουμε ξανά,",
                    'success': "ΝΑΙΙΙΙ, ΕΧΕΙΣ ΛΥΣΕΙ ΤΟ ΠΡΟΒΛΗΜΑ ΜΕ ΤΟΝ ΝΕΚΡΟ ΚΩΔΙΚΑ, αυτή είναι μια εξαιρετική είδηση! Θα συνεχίσουμε να βελτιώνουμε το έργο σου;",
                },
                'Duplicates': {
                    'fail': "Ούπς, φαίνεται ότι δεν έχεις λύσει το πρόβλημα με τον διπλό κώδικα, αλλά μην ανησυχείς, θα δούμε πώς μπορούμε να το επιλύσουμε ξανά,",
                    'success': "ΝΑΙΙΙΙ, ΕΧΕΙΣ ΛΥΣΕΙ ΤΟ ΠΡΟΒΛΗΜΑ ΜΕ ΤΟΝ ΔΙΠΛΟ ΚΩΔΙΚΑ, αυτή είναι μια εξαιρετική είδηση! Θα συνεχίσουμε να βελτιώνουμε το έργο σου;",
                }
            }
        elif self.curr_lan == 'pt':
            return {
                'Backdrops': {
                    'fail': "Oooops, parece que você não resolveu o problema com o nome dos fundos, mas não se preocupe, vamos revisar como podemos resolver isso novamente,",
                    'success': "¡YEAHH, VOCÊ RESOLVEU O PROBLEMA COM O NOME DOS FUNDOS, isso é ótimo! Você gostaria de continuar melhorando o projeto?",
                },
                'Sprites': {
                    'fail': "Oooops, parece que você não resolveu o problema com o nome dos sprites, mas não se preocupe, vamos revisar como podemos resolver isso novamente,",
                    'success': "¡YEAHH, VOCÊ RESOLVEU O PROBLEMA COM O NOME DOS SPRITES, isso é ótimo! Você gostaria de continuar melhorando o projeto?",
                },
                'deadCode': {
                    'fail': "Oooops, parece que você não resolveu o problema com o código morto, mas não se preocupe, vamos revisar como podemos resolver isso novamente,",
                    'success': "¡YEAHH, VOCÊ RESOLVEU O PROBLEMA COM O CÓDIGO MORTO, isso é ótimo! Você gostaria de continuar melhorando o projeto?",
                },
                'Duplicates': {
                    'fail': "Oooops, parece que você não resolveu o problema com o código duplicado, mas não se preocupe, vamos revisar como podemos resolver isso novamente,",
                    'success': "¡YEAHH, VOCÊ RESOLVEU O PROBLEMA COM O CÓDIGO DUPLICADO, isso é ótimo! Você gostaria de continuar melhorando o projeto?",
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
        elif self.curr_lan == 'tr':
            return {
                'Backdrops': {
                    'fail': "Oooops, görünüşe göre dekor isimlendirme sorununu çözemediniz, ama endişelenmeyin, nasıl çözebileceğimizi tekrar gözden geçireceğiz,",
                    'success': "YEAAHH, DEKOR İSİMLENDİRME SORUNUNU ÇÖZDÜNÜZ, bu harika bir haber! Projeyi geliştirmeye devam etsek iyi olur mu?",
                },
                'Sprites': {
                    'fail': "Oooops, görünüşe göre kukla isimlendirme sorununu çözemediniz, ama endişelenmeyin, nasıl çözebileceğimizi tekrar gözden geçireceğiz,",
                    'success': "YEAAHH, KUKLA İSİMLENDİRME SORUNUNU ÇÖZDÜNÜZ, bu harika bir haber! Projeyi geliştirmeye devam etsek iyi olur mu?",
                },
                'deadCode': {
                    'fail': "Oooops, görünüşe göre ölü kod sorununu çözemediniz, ama endişelenmeyin, nasıl çözebileceğimizi tekrar gözden geçireceğiz,",
                    'success': "YEAAHH, ÖLÜ KOD SORUNUNU ÇÖZDÜNÜZ, bu harika bir haber! Projeyi geliştirmeye devam etsek iyi olur mu?",
                },
                'Duplicates': {
                    'fail': "Oooops, görünüşe göre yinelenen kod sorununu henüz çözemediniz, ama endişelenmeyin, nasıl çözebileceğimizi tekrar gözden geçireceğiz,",
                    'success': "YEAAHH, YİNELENEN KOD SORUNUNU ÇÖZDÜNÜZ, bu harika bir haber! Projeyi geliştirmeye devam etsek iyi olur mu?",
                }
            }
        else:
            return {}

            

