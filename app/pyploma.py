import os, shutil


def generate_certificate(filename, level, language):
    """
    Generate certificate of analysis
    Este generador de diplomas lee una lista con nombre, dni y calificación para
    rellenarlos en una plantilla LaTeX con un marcador para cada campo.
    Opcionalemente compila los ficheros LaTeX generados y los une en uno solo.
    Si la plantilla LaTeX da error de compilación, pulsar intro varias veces.
    """

    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.chdir(base_dir + "/app/certificate")

    salida = open("output.tex", "w") # crea fichero LaTeX para cada persona
    person = [filename, level] # pasar la cadena en lista ["testing.sb2","21"]
    text = open("certi-" + language + ".tex") # abrir documento LaTeX
    text = text.read() # leer documento LaTeX
    text_list = list(text) # pasa a lista

    y_cali = text.find("%pointcalification") # busca marcador de calificación
    z_cali = len("%pointcalification")+2
    text_list[y_cali+z_cali:y_cali+z_cali] = list(person[1]) # inserta calificación

    y_name = text.find("%pointname") # lo mismo para el nombre
    z_name = len("%pointname") + 2
    text_list[y_name + z_name: y_name + z_name] = list(person[0])

    text_final = "".join(text_list) # de lista a cadena

    salida.write(text_final) # guarda los cambio en el fichero creado
    salida.close() # cierra el fichero creado
    
    if shutil.which("pdflatex"): # comprueba que pdflatex está instalado
        os.system(str("pdflatex " + "output.tex")) # compila el fichero LaTeX a pdf (opcional)
    else:
        print("pdflatex not found") # si no está instalado, muestra un mensaje
    os.chdir(base_dir)
