from main import exit_main

import os
import re
import sys
import json
import time
import string

from unidecode import unidecode
from datetime import datetime

import colorama 
from colorama import Fore, Style
colorama.init()

"""
tag_training.py

Interfaz: ✓ 
Funcion: Tiene dos:
            1. Ayudar a whatsapp.py para identificar el tag del mensaje con findMessage()
            2. El resto es dedicado a una interfaz para entrenar la base de datos de tipos de mensaje generada en ./data/intents/tag_training/tags.json
"""

# Funcion para whatsapp.py que devuelve el tag del mensaje
def findMessage(message):

    # Borrar las tildes y mayusculas y signos
    message = re.sub(r'[^\w\s]', '', unidecode(message)) 

    try:

        # Separar los mensajes en palabras para colocarlos en words
        words = []
        message = message.split()

        # Por cada palabra en el mensaje, agregar a words
        for word in message:

            # Quitar espacios y signos de puntuacion (para utilizar '==' en if word == intent["mensaje"] que sea exacto)
            # Es necesario hacer lo mismo abajo
            word = word.translate(str.maketrans("", "", string.punctuation))
            word = word.lower()
            word = word.replace(" ", "")
            words.append(word)

        # Abrir el json de tags para comparar
        with open(f"./data/intents/tag_training/tags.json", 'r') as json_file:
            data = json.load(json_file)
            results = []
            messages = []
            for intent in data["intents"]:
                for word in words:

                    # Quitar espacios y signos de puntuacion (para utilizar '==' en if word == intent["mensaje"] que sea exacto)
                    comparar = intent["mensaje"]
                    comparar = comparar.translate(str.maketrans("", "", string.punctuation))
                    comparar = comparar.lower()
                    comparar = comparar.replace(" ", "")
                    
                    if word == comparar:
                        results.append({"tag": intent["tag"], "mensaje": intent["mensaje"]})
                        messages.append({"mensaje": intent["mensaje"]})
 
    except:
        # Error
        tag_catch()
        exit()
    try:
        # Verificar si se encontro tag apropiado
        tag = results[0]["tag"]
    except:
        # Si no se encontro tag apropiado
        tag = "NOT FOUND"
    return tag

# Interfaz tag training
def tag_training():

    while(True): 

        while(True):

            # Prints y catch
            intro()

            if print_tag() != "vacio":
                if tag_catch() == False:
                    break
            else:
                time.sleep(1.5)
                break

        ###################################
        ###<<<<<<<<<<<<<<>>>>>>>>>>>>>>>###
        ###<<< PROGRAMA TAG_TRAINING >>>###
        ###<<<<<<<<<<<<<<>>>>>>>>>>>>>>>###
        ###################################

        # Inicializar un diccionario vacío para guardar los intents
        intents = {"intents": []}

        # Ruta
        route = f"./data/intents/tag_training/tags.json"

        salir = False

        while(salir == False):

            intro()

            # Abrir el archivo json para escritura y escritura (para no sobreescribir)
            with open(route, "r+") as json_file:
                # Cargar los datos actuales en un objeto python
                intents = json.load(json_file)

                # Solicitar Nombre
                tag = input(Fore.YELLOW + "¿Cual es el tag para entrenar?\n" + Style.RESET_ALL)

                # Borrar las tildes y mayusculas y signos
                tag = re.sub(r'[^\w\s]', '', unidecode(tag)) 

                # Finaliza este subproceso
                if(exit_main(tag, "tag_training.py") == True):
                    sys.exit()
                
                # Devuelve al Menú
                exit_main(tag, "tag_training.py") 

                # Back
                salir2 = False
                if tag == 'back':
                    salir = True
                    salir2 = True

                    intro()

                while(salir2 == False):

                    intro()

                    print(Fore.BLUE + f"Tag: " + Fore.WHITE + f"{tag}" + Style.RESET_ALL)

                    mensajes = []

                    for intent in intents["intents"]:
                        if intent["tag"] == tag:
                            mensajes.append(intent["mensaje"])
                    print(Fore.BLUE + "Mensajes: " + Style.RESET_ALL +  str(mensajes))


                    # Solicitar Mensaje
                    message = input(Fore.YELLOW + "\nPalabra:\n" + Style.RESET_ALL)

                    # Borrar las tildes y mayusculas y signos
                    message = re.sub(r'[^\w\s]', '', unidecode(message)) 

                    # Finaliza este subproceso
                    if(exit_main(message, "tag_training.py") == True):
                        sys.exit()
                    
                    # Devuelve al Menú
                    exit_main(message, "tag_training.py") 

                    # Back 2
                    if message == 'back':
                        salir2 = True 
                    else:
                        # Crear un diccionario con la información que se quiere almacenar de la línea
                        intent = {"tag": tag, "mensaje": message}

                        # Agregar un nuevo elemento (intent) al final de la lista (intents) con la clave (intents)         
                        intents["intents"].append(intent)

                        # Mover el puntero al inicio del archivo para sobrescribir los datos actuales
                        json_file.seek(0)
                        # Escribir los datos actualizados en el archivo json
                        json.dump(intents, json_file)
                        # Eliminar los datos adicionales al final del archivo
                        json_file.truncate()

# Funcion para imprimir introduccion
def intro():
    # Limpiar Terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    # Introduccion
    print(Fore.GREEN + "\n>> RECONOCIMIENTO DE MENSAJES <<" + Style.RESET_ALL)
    # Explicacion
    print(Fore.LIGHTBLACK_EX + "\nClasificar palabras con su tipo.\n\n    Tag: saludo\n    Mensajes: hola, hi, buenas" + Style.RESET_ALL)
    # Exit
    print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir o 'back' para ir atras\n" + Style.RESET_ALL)

# Funcion para detectar errores
def tag_catch():
    
    """
    Este bloque detecta si existe un archivo de tag.json antes de iniciar el programa, 
    te avisa si no hay para crear uno, si ya existe te permite entrar en CRUD 
    """

    route = f"./data/intents/tag_training/tags.json"

    # Verificación tag.json

    try: # Si es que existe json o Si no esta vacio
        
        # Para verificar si existe un archivo intents.json, intenta abrirlo para lectura/escritura
        with open(route, "r+") as json_file:
            intents = json.load(json_file)

        if tag_CRUD() == False:
            return False

    except: # Si es que no existe json o Si está vacio
        
        # Mensaje al usuario sobre borrar el existente
        print(Fore.RED +f"WARNING: No hay tags guardados" + Fore.LIGHTBLACK_EX + "\nPor favor, genere tags antes de entrenar intents\n" + Style.RESET_ALL)

        tag_create()
        

    # Limpiar Terminal
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else 'clear')

# Funcion para imprimir los tags existentes
def print_tag():

    route = f"./data/intents/tag_training/tags.json"

    try:
        with open(route, "r") as json_file:
            datos = json.load(json_file)

        if len(datos['intents']) == 0:
            # El diccionario intents está vacío.
            print(Fore.YELLOW + "TAG existentes:\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "[vacio]\n" + Style.RESET_ALL)

            return 'vacio'

        else:
            # El diccionario intents no está vacío.
            print(Fore.YELLOW + "TAG existentes:\n" + Style.RESET_ALL)

            mensajes = {}
            for intent in datos["intents"]:
                tag = intent["tag"]
                mensaje = intent["mensaje"]
                if tag not in mensajes:
                    mensajes[tag] = []
                mensajes[tag].append(mensaje) 

            for tag, mensajes_tag in mensajes.items():
                print(Fore.BLUE + "Tag: " + Fore.WHITE + f"{tag}")
                print(Fore.BLUE + "Mensajes: " + Fore.WHITE + f"{mensajes_tag}\n")

            return 'no vacio'
    
    except:
        print(Fore.YELLOW + "TAG existentes:\n" + Style.RESET_ALL)
        print(Fore.LIGHTBLACK_EX + "[vacio]\n" + Style.RESET_ALL)

# Funcion para crear tags nuevos
def tag_create():

    route = f"./data/intents/tag_training/tags.json"

    # Para trabajar con datos en blanco, volver a inicializar un diccionario vacío
    intents = {"intents": []}

    # Para crear un nuevo json, abrir el archivo json para escritura y meterle el diccionario vacío
    with open(route, "w") as json_file:
        json.dump(intents, json_file)

    # Abrir el archivo json NUEVO para lectura/escritura
    with open(route, "r+") as json_file:
        # Cargar los datos existentes en el archivo json
        intents = json.load(json_file)

    # Creado
    time.sleep(0.5)
    print(Fore.LIGHTBLACK_EX +f"\nArchivo vacío 'tag.json' creado\n" + Style.RESET_ALL)

# Funcion para eliminar tags existentes y todo su contenido
def tag_delete(tag):

    route = f"./data/intents/tag_training/tags.json"

    # Abrir el archivo json NUEVO para lectura/escritura
    with open(route, "r") as json_file:
        # Cargar los datos existentes en el archivo json
        intents = json.load(json_file)

    # crear diccionario de intents copiando todos los datos excepto el tag que se va a 'eliminar'
    intents['intents'] = [intent for intent in intents['intents'] if intent['tag'].strip() != tag.strip()]

    # Abrir el archivo json NUEVO para lectura/escritura
    with open(route, "w") as json_file:
        # Cargar los datos nuevos en el archivo json
        json.dump(intents, json_file)

    # Eliminado
    print(Fore.RED +f"\nTAG ELIMINADO: " + tag + Style.RESET_ALL)

    time.sleep(1)

# Funcion para entrar en tag_delete()
# Hay un error con la funcion exit_main(), se comentaron todos los bloques
def tag_CRUD():

    route = f"./data/intents/tag_training/tags.json"

    # CRUD
    delete = input(Fore.YELLOW + "¿Desea borrar algun tag? (y/n)\n" + Fore.LIGHTBLACK_EX + "(no funciona el exit)\n" + Style.RESET_ALL)
    delete = delete.lower()
    """
    # Finaliza este subproceso
    if(exit_main(delete, "tag_training.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(delete, "tag_training.py") 
    """

    # Verificacion de y/n
    while delete.lower() not in ["y", "n"]:
        print(Fore.LIGHTBLACK_EX +"Por favor ingresa sólamente (y/n)\n" + Style.RESET_ALL)
        delete = input(Fore.YELLOW + "¿Desea borrar algun tag? (y/n)\n" + Fore.LIGHTBLACK_EX + "(no funciona el exit)\n" + Style.RESET_ALL)
        delete = delete.lower()
        """
        # Finaliza este subproceso
        if(exit_main(delete, "tag_training.py") == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(delete, "tag_training.py") 
        """

    # DELETE? Si
    if delete == "y" and os.path.exists(route):

        tag = input(Fore.YELLOW + "\n¿Cual tag desea borrar?\n" + Fore.LIGHTBLACK_EX + "(no funciona el exit)\n" + Style.RESET_ALL)
        tag = tag.lower()
        """
        # Finaliza este subproceso
        if(exit_main(tag, "tag_training.py") == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(tag, "tag_training.py") 
        """

        tag_delete(tag)

        return True

    # DELETE? No
    if delete == "n" and os.path.exists(route):
        return False
        
    time.sleep(0.5)

if __name__ == '__main__':
    tag_training()


 