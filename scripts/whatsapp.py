from main import exit_main

import os
import re
import sys
import json
import time

from datetime import datetime
from unidecode import unidecode

import colorama 
from colorama import Fore, Style
colorama.init()

import sentiment
import big_five_whatsapp as big_five
from tag_training import findMessage

"""
whatsapp.py

Interfaz: ✓ 
Funcion: Leer cada mensaje del .txt expecificado, generar resutlados de sentimiento, big_five y tag en: ./data/intents/personality_training/intent_{name}.json
"""

# Limpiar Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Introduccion
print(Fore.GREEN + "\n>> Procesamiento de mensajes WhatsApp <<" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nPara un mejor resultado, asegurate de haber hecho:\n(1) Reconocimiento de mensajes\n(2) Añade a la base de datos de Big Five" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)

########################
### INFO & CHECKING ####
########################

"""
El siguiente código solicita información del usuario:
1. Nombre del contacto
2. Desde que año se entrenan los datos
3. Si la información fue extraída de WhatsApp en inglés o español.

También realiza verificación de errores:
1. Si ./chats se encuentra vacío. Debe haber por lo menos un .txt para funcionar el programa
2. Si el año ingresado:
    a. Es un número
    b. Es menor al actual (datetime)
    c. Es mayor o igual al 2009 (lanzamiento de WhatsApp)
3. Si el idioma solicitado es Español o Inglés
"""

# Revisar si hay archivos .txt en './chats'
# (RECORDAR QUE EL EXPORT DEBE SER "sin archivos")
folder = "./chats"
if not os.listdir(folder):
    print(Fore.RED +"\nERROR: El directorio './chats' se encuentra vacío" + Fore.LIGHTBLACK_EX + "\nPor favor, colocar al menos un export de WhatsApp (.txt)" + Style.RESET_ALL)
    sys.exit()

# Solicitar Nombre
name = input(Fore.YELLOW + "\n¿Cual es el nombre del contacto?\n" + Style.RESET_ALL)

# Finaliza este subproceso
if(exit_main(name, "whatsapp.py") == True):
    sys.exit()

# Devuelve al Menú
exit_main(name, "whatsapp.py") 

# Solicitar Año
year = input(Fore.YELLOW + "\n¿Desde que año desea entrenar?\n" + Style.RESET_ALL)

# Finaliza este subproceso
if(exit_main(year, "whatsapp.py") == True):
    sys.exit()

# Devuelve al Menú
exit_main(year, "whatsapp.py") 

# Obtener el Año actual
current_year = datetime.now().year

# Validar el Año ingresado
while not year.isdigit() or int(year) > current_year or int(year) < 2009:
    print(Fore.RED +"ERROR: Por favor ingresa un año válido" + Fore.LIGHTBLACK_EX + "\nEl año seleccionado no puede ser mayor al año actual ni menor al año 2009." + Style.RESET_ALL)
    year = input(Fore.YELLOW + "\n¿Desde que año desea entrenar?\n" + Style.RESET_ALL)
    # Finaliza este subproceso
    if(exit_main(year, "whatsapp.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(year, "whatsapp.py") 

# Solicitar Idioma
lan = input(Fore.YELLOW + "\n¿El idioma del archivo WhatsApp esta en ESPAÑOL (es) o INGLES (en)?\n" + Style.RESET_ALL)

# Finaliza este subproceso
if(exit_main(lan, "whatsapp.py") == True):
    sys.exit()

# Devuelve al Menú
exit_main(lan, "whatsapp.py") 

# Validar el idioma ingresado
while lan.lower() not in ["es", "en"]:
    print(Fore.RED +"ERROR: Por favor ingresa un idioma del archivo WhatsApp válido" + Fore.LIGHTBLACK_EX + "\nEl idioma del archivo WhatsApp puede estar en ESPAÑOL (es) o INGLÉS (en)" + Style.RESET_ALL)
    lan = input(Fore.YELLOW + "\n¿El idioma del archivo WhatsApp esta en ESPAÑOL (es) o INGLÉS (en)?\n" + Style.RESET_ALL)
    # Finaliza este subproceso
    if(exit_main(lan, "whatsapp.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(lan, "whatsapp.py")  

# Convertir el idioma a minúsculas y prepararlo para mostrar
lan = lan.lower()
if lan == 'en':
    language = "INGLÉS (en)"
if lan == 'es':
    language = "ESPAÑOL (es)"

#####################
### INTENTS.JSON ####
#####################

"""
Este bloque detecta si existe un archivo de intents.json antes de iniciar el programa, 
te avisa si hay uno existente para asegurar que lo quieras guardar antes de sobrescribirlo, 
en tal caso te da la opción de borrarlo y empezar de cero, o continuar con el existente (no recomendado)
"""

# Ruta
route = f"./data/intents/personality_training/intent_{name}.json"

# Inicializar un diccionario vacío para guardar los intents
intents = {"intents": []}
    
# Verificación intents.json

try: # Si es que existe json o Si no esta vacio
    
    # Para verificar si existe un archivo intents.json, intenta abrirlo para lectura/escritura
    with open(route, "r+") as json_file:
        intents = json.load(json_file)

    # Si no existe -> except

    # Mensaje al usuario sobre borrar el existente
    print(Fore.RED +f"ERROR: Ya existe un archivo intent_{name}.json" + Fore.LIGHTBLACK_EX + "\nPor favor, utilice el archivo generado para entrenar el chatbot" + Style.RESET_ALL)
    delete = input(Fore.YELLOW + "\n¿Desesas eliminarlo y crear uno vacío? (y/n)\n" + Style.RESET_ALL)
    delete = delete.lower()

    # Finaliza este subproceso
    if(exit_main(delete, "whatsapp.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(delete, "whatsapp.py") 

    while delete.lower() not in ["y", "n"]:
        print(Fore.LIGHTBLACK_EX +"Por favor ingresa sólamente (y/n)" + Style.RESET_ALL)
        delete = input(Fore.YELLOW + "\n¿Desesas eliminarlo y crear uno vacío? (y/n)\n" + Style.RESET_ALL)
        delete = delete.lower()

        # Finaliza este subproceso
        if(exit_main(delete, "whatsapp.py") == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(delete, "whatsapp.py") 

    # Desea eliminarlo? Si
    if delete == "y" and os.path.exists(route):

        # Eliminado
        os.remove(route)
        time.sleep(0.5)
        print(Fore.LIGHTBLACK_EX +f"\nArchivo 'intent_{name}.json' eliminado" + Style.RESET_ALL)

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
        print(Fore.LIGHTBLACK_EX +f"\nArchivo vacío 'intent_{name}.json' creado" + Style.RESET_ALL)
    
    # Desea eliminarlo? No
    else: 
        # Creado
        time.sleep(0.5)
        print(Fore.LIGHTBLACK_EX +f"\nContinuando sin eliminar 'intent_{name}.json' (No Recomendado)" + Style.RESET_ALL)

except: # Si es que no existe json o Si está vacio

    # Abrir el archivo json para escritura
    with open(route, "w") as json_file:
        json.dump(intents, json_file)

    # Abrir el archivo json para lectura/escritura
    with open(route, "r+") as json_file:
        # Cargar los datos existentes en el archivo json
        intents = json.load(json_file)

    # Creado
    time.sleep(0.5)
    print(Fore.LIGHTBLACK_EX +f"\nArchivo vacío 'intent_{name}.json' creado" + Style.RESET_ALL)

# Limpiar Terminal
time.sleep(2)
os.system('cls' if os.name == 'nt' else 'clear')


# Mostrar Datos
time.sleep(0.5)
print(Fore.LIGHTBLACK_EX + f"\nBuscando chat de: '{name}'...\nRango: {year}-2023\nIdioma del archivo Whatsapp: {language}\n" + Style.RESET_ALL)

# Inicializar Subjects
subjects = {
    "Chatbot":"",
    "User":""
}

# Inicializar contador de tiempo de ejecución
start_time = time.time()

###############################
###<<<<<<<<<<<<>>>>>>>>>>>>>###
###<<< PROGRAMA WHATSAPP >>>###
###<<<<<<<<<<<<>>>>>>>>>>>>>###
###############################

"""
Este es el programa.

El programa funciona de esta manera:

1. Dependiendo del lenguaje, se utiliza formato (es) o (en)
2. Búsqueda del export.txt
    a. Inicializa el nombre del archivo a buscar (predefinido) y le incrusta el nombre
        i. file_name = f"Chat de WhatsApp con {name}"
        ii. file_name = f"WhatsApp Chat with {name}"
    b. Verifica si existe un archivo en el idioma dado y con ese nombre.
    c. Verifica si existe un archivo descargado más reciente
        i. El nombre del archivo puede terminar con (1) o (2) después de varias descargas
        ii. Utiliza el del número más alto
        iii. Si no existe tal archivo, se muestra un mensaje de error
3. Abre el archivo más reciente
4. Truncación de datos
    a. Se eliminan líneas vacías
    b. Se eliminan líneas que no empiecen con una fecha
    c. Se eliminan líneas de mensajes generadas por las distintas funcionalidades de WhatsApp
        i. Eliminaste este mensaje.
        ii. Se eliminó este mensaje.
        iii. Llamada perdida
        iv. Videollamada perdida
        v. <Multimedia omitido>
        vi. (archivo adjunto)
        vii. ENCUESTA:
        viii. OPCIÓN:
        ix. ubicación en tiempo real compartida
        x. ubicación:
        xi. links
    d. Se elimina un carácter especial que aparece con los emojis: "🏻"
5. Formateo de datos
    a. Se toma en cuenta la estructura de la línea para el patrón
        i. dd/mm/AAAA HH:MM - {nombre}: {mensaje}
        ii. dd/mm/yy, HH:MM AM/PM - {nombre}: {mensaje}
    b. Se ajusta la fecha datetime
        i. '%d/%m/%Y' -> Formato Español -> "dd/mm/YYYY"
        ii. '%m/%d/%y' -> Formato USA -> "dd/mm/yy"
6. Se crea un diccionario con el formato requerido y se agrega al intents.json
    
"""
############################################
###<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>###
###<<< PROGRAMA WHATSAPP ESPAÑOL (es) >>>###
###<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>###
############################################

"""
La versión en español tiene las siguientes diferencias:

1. Cada línea tiene esta estructura:

    dd/mm/AAAA HH:MM - {nombre}: {mensaje}

2. Datetime utiliza este formato: '%d/%m/%Y' 

3. El nombre del archivo .txt tiene la siguiente estructura:

    Chat de WhatsApp con {name}.txt

"""

# Si el idioma es español
if lan == "es":
    
    # Nombre del archivo que se esta buscando
    file_name = f"Chat de WhatsApp con {name}"

    # Inicializar el numero mas alto encontrado
    max_number = 0

    # Inicializar el nombre del archivo mas reciente
    latest_file = None
    
    try:
        # Verifica si existe un archivo .txt con el idioma y nombre especificado
        if os.path.exists(folder + '/' + file_name + '.txt'):
            latest_file = file_name + '.txt'
            time.sleep(0.5)
            print(Fore.LIGHTBLACK_EX + "Archivo encontrado: " + latest_file + Style.RESET_ALL)
        
        # Revisa si hay uno más reciente -> (1)
        for file in os.listdir(folder):
            # Buscar el nombre del archivo seguido de un parentesis y un numero
            match = re.search(f"{file_name}.*\((\d+)\).txt", file)
            if match:
                # Si se encuentra una coincidencia, obtener el numero del parentesis
                number = int(match.group(1))
                # Si el numero es mayor al numero maximo encontrado, actualizar el maximo y el nombre del archivo
                if number > max_number:
                    max_number = number
                    latest_file = file
                    time.sleep(0.5)
                    print(Fore.LIGHTBLACK_EX + "Se ha encontrado un archivo más reciente: " + latest_file + Style.RESET_ALL)

        try:
            print(Fore.LIGHTBLACK_EX + "\nProcesando datos de: " + latest_file + " (esto puede tardar varios minutos)" + Style.RESET_ALL)
        except:
            print(Fore.RED + "ERROR: No existe chat en espanol de: " + name)
            os.remove(f"./intents/personality_training/intent_{name}.json")
            # Devuelve al Menú
            exit_main('exit', "whatsapp.py")  

        # Si encontró algun archivo .txt con el idioma y nombre especificado
        if latest_file:
            # Abrir el archivo mas reciente (con el numero mas alto)
            with open(os.path.join(folder, latest_file), "r", encoding="utf-8") as f:
                    for line in f:
                        # Evita leer líneas vacías y las que no empiezan con fechas
                        if line.strip() != "" and line[0].isnumeric() and line.find("/")==1 or line.find("/")==2: 
                            # Truncar los datos de mensajes generados por funcionalidades de WhatsApp
                            if line.find("Eliminaste este mensaje.") == -1 and line.find("Se eliminó este mensaje.") == -1 and line.find("Los mensajes y las llamadas están cifrados de extremo a extremo.") == -1\
                            and line.find("Llamada perdida") == -1 and line.find("Videollamada perdida") == -1 \
                            and line.find("<Multimedia omitido>") == -1 and line.find("(archivo adjunto)") == -1 and line.find("ENCUESTA:") == -1 and line.find("OPCIÓN:") == -1 \
                            and line.find("ubicación en tiempo real compartida") == -1 and line.find("ubicación:") == -1 \
                            and line.find("https://") == -1 and line.find("www.") == -1 and line.find(".com") == -1 and line.find(".net") == -1 and line.find(".ec") == -1 and line.find(".edu") == -1:

                                # Quitar caracter adicional cuando se ingresan emojis
                                line = line.replace("🏻", "") 

                                # Separar la fecha para procesar los años que se van a entrenar (no hay coma en el formato español)
                                line_date = line.split(' ')[0] 

                                try:
                                    date_object = datetime.strptime(line_date, '%d/%m/%Y') #'%d/%m/%Y' -> Formato Español -> "dd/mm/YYYY"
                                except:
                                    date_object = datetime.strptime(line_date, '%d/%m/%y') #'%d/%m/%y' -> Formato Español -> "dd/mm/yy"

                                # Si el año del mensaje es mayor o igual al año mínimo especificado
                                if str(date_object.year) >= year:
                                    try:
                                        # Obtener person y message
                                        line_message = line.split("-", 1)[1].strip()
                                        
                                        parts = line_message.split(":")
                                        person = parts[0]
                                        message = parts[1].strip()

                                        if message is not "":

                                            # Identificar si es Chatbot o User (ignorando tildes y mayusculas en nombre)
                                            if unidecode(person).lower() == unidecode(name).lower():
                                                subjects["Chatbot"] = person
                                                subject = "Chatbot"
                                            else:
                                                subjects["User"] = person
                                                subject = "User"
                                            
                                            # Decidir tag del mensaje
                                            tag = findMessage(message)

                                            # Obtener Big Five del mensaje
                                            big5CB, big5U, big5M = big_five.addBigFive(line, subject)

                                            # Obtener sentimiento del mensaje
                                            #sentiment_tag = sentiment.getSentiment(message)

                                            # Crear un diccionario con la información que se quiere almacenar de la línea
                                            #intent = {"tag": tag, "big_five": big5M, "sentiment": sentiment_tag, "subject": subject, "nombre": person, "mensaje": message}
                                            intent = {"tag": tag, "big_five": big5M, "subject": subject, "nombre": person, "mensaje": message}

                                            # Agregar un nuevo elemento (intent) al final de la lista (intents) con la clave (intents)         
                                            intents["intents"].append(intent)
                                    except:
                                        pass

                    try:
                        # Tiempo Final
                        end_time = time.time()
                        total_time = end_time - start_time

                        # Print Big Five
                        big_five.printBigFive(subjects["Chatbot"], subjects["User"])
                        # Save Big Five Profile
                        big_five.saveBigFive(subjects["Chatbot"], subjects["User"], total_time)
                    except:
                        print(Fore.RED + f"\nERROR: Hubo una discrepancia con el nombre dado y el chat de WhatsApp" + Style.RESET_ALL)
                        # Devuelve al Menú
                        exit_main('exit', "whatsapp.py")  

                    # Abrir el archivo json para escritura
                    with open(route, "w") as json_file:
                        # Escribir los datos actualizados en el archivo json
                        json.dump(intents, json_file)           

                    # Finalizado                 
                    print(Fore.YELLOW + "\nHECHO!")
        
        # No encontró algun archivo .txt con el idioma y nombre especificado
        else:
            try:
                # Eliminar intent_{name}.json
                os.remove(route)
                print(Fore.LIGHTBLACK_EX +f"Archivo 'intent_{name}.json' eliminado\n" + Style.RESET_ALL)
                raise FileNotFoundError(Fore.RED + f"ERROR: No se ha encontrado el archivo \"Chat de WhatsApp con {name}.txt\" en el directorio './chats'" + Style.RESET_ALL)
            except:
                raise FileNotFoundError(Fore.RED + f"ERROR: No se ha encontrado el archivo \"Chat de WhatsApp con {name}.txt\" en el directorio './chats'" + Style.RESET_ALL)
    except FileNotFoundError as e:
        try:
            # Eliminar intent_{name}.json
            os.remove(route)
            print(Fore.LIGHTBLACK_EX +f"\nArchivo 'intent_{name}.json' eliminado\n" + Style.RESET_ALL)
            print(e)
        except:
            print(e)

###########################################
###<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>###
###<<< PROGRAMA WHATSAPP INGLÉS (en) >>>###
###<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>###
###########################################

"""
La versión en inglés tiene las siguientes diferencias:

1. Cada línea tiene esta estructura:

    mm/dd/yy, HH:MM AM/PM - {nombre}: {mensaje}

2. Datetime utiliza este formato: '%m/%d/%y' 

3. El nombre del archivo .txt tiene la siguiente estructura:

    WhatsApp Chat with {name}.txt

"""

# Si el idioma es inglés
if lan == "en":

    # Nombre del archivo que se esta buscando
    file_name = f"WhatsApp Chat with {name}"

    # Inicializar el numero mas alto encontrado
    max_number = 0

    # Inicializar el nombre del archivo mas reciente
    latest_file = None

    try:
        # Verifica si existe un archivo .txt con el idioma y nombre especificado
        if os.path.exists(folder + '/' + file_name + '.txt'):
            latest_file = file_name + '.txt'
            time.sleep(0.5)
            print(Fore.LIGHTBLACK_EX + "Archivo encontrado: " + latest_file + Style.RESET_ALL)

        # Revisa si hay uno más reciente -> (1)
        for file in os.listdir(folder):
            # Buscar el nombre del archivo seguido de un parentesis y un numero
            match = re.search(f"{file_name}.*\((\d+)\).txt", file)
            if match:
                # Si se encuentra una coincidencia, obtener el numero del parentesis
                number = int(match.group(1))
                # Si el numero es mayor al numero maximo encontrado, actualizar el maximo y el nombre del archivo
                if number > max_number:
                    max_number = number
                    latest_file = file
                    time.sleep(0.5)
                    print(Fore.LIGHTBLACK_EX + "Se ha encontrado un archivo más reciente: " + latest_file + Style.RESET_ALL)

        try:
            print(Fore.LIGHTBLACK_EX + "\nProcesando datos de: " + latest_file + " (esto puede tardar varios minutos)" + Style.RESET_ALL)
        except:
            print(Fore.RED + "ERROR: No existe chat en ingles de: " + name)
            os.remove(f"./intents/personality_training/intent_{name}.json")
            # Devuelve al Menú
            exit_main('exit', "whatsapp.py")  

        # Si encontró algun archivo .txt con el idioma y nombre especificado
        if latest_file:
            # Abrir el archivo mas reciente (con el numero mas alto)
            with open(os.path.join(folder, latest_file), "r", encoding="utf-8") as f:
                for line in f:
                    # Evita leer líneas vacías y las que no empiezan con fechas
                    if line.strip() != "" and line[0].isnumeric() and line.find("/")==1 or line.find("/")==2:
                        # Truncar los datos de mensajes generados por funcionalidades de WhatsApp 
                        if line.find("You deleted this message") == -1 and line.find("This message was deleted") == -1 and line.find("Messages and calls are end-to-end encrypted.") == -1\
                        and line.find("Missed voice call") == -1 and line.find("Missed video call") == -1 \
                        and line.find("<Media omitted>") == -1 and line.find("(file attached)") == -1 and line.find("POLL:") == -1 and line.find("OPTION:") == -1 \
                        and line.find("live location shared") == -1 and line.find("location:") == -1 \
                        and line.find("https://") == -1 and line.find("www.") == -1 and line.find(".com") == -1 and line.find(".net") == -1 and line.find(".ec") == -1 and line.find(".edu") == -1:

                            # Quitar caracter adicional cuando se ingresan emojis
                            line = line.replace("🏻", "")

                            # Separar la fecha para procesar los años que se van a entrenar (hay coma en el formato ingés)
                            line_date = line.split(' ')[0].rstrip(",") # Quitar coma "mm/dd/yy," -> "mm/dd/yy"
                            date_object = datetime.strptime(line_date, '%m/%d/%y') # '%m/%d/%y' -> Formato USA -> "mm/dd/yy"

                            # Si el año del mensaje es mayor o igual al año mínimo especificado
                            if str(date_object.year) >= year:
                                try:
                                    # Obtener person y message
                                    line_message = line.split("-", 1)[1].strip()

                                    parts = line_message.split(":")
                                    person = parts[0]
                                    message = parts[1].strip()

                                    if message is not "":

                                        # Identificar si es Chatbot o User
                                        if unidecode(person).lower() == unidecode(name).lower():
                                            subjects["Chatbot"] = person
                                            subject = "Chatbot"
                                        else:
                                            subjects["User"] = person
                                            subject = "User"

                                        # Decidir tag del mensaje
                                        tag = findMessage(message)

                                        # Big Five
                                        big5CB, big5U, big5M = big_five.addBigFive(line, subject)

                                        # Obtener sentimiento del mensaje
                                        #sentiment_tag = sentiment.getSentiment(message)

                                        # Crear un diccionario con la información que se quiere almacenar de la línea
                                        #intent = {"tag": tag, "big_five": big5M, "sentiment": sentiment_tag, "subject": subject, "nombre": person, "mensaje": message}
                                        intent = {"tag": tag, "big_five": big5M, "subject": subject, "nombre": person, "mensaje": message}

                                        # Agregar un nuevo elemento (intent) al final de la lista (intents) con la clave (intents)
                                        intents["intents"].append(intent)
                                except:
                                    pass
                try:
                    # Tiempo Final
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    # Big Five
                    big_five.printBigFive(subjects["Chatbot"], subjects["User"])
                    # Save Big Five Profile
                    big_five.saveBigFive(subjects["Chatbot"], subjects["User"], total_time)
                except:
                    print(Fore.RED + f"\nERROR: Hubo una discrepancia con el nombre dado y el chat de WhatsApp" + Style.RESET_ALL)
                    # Devuelve al Menú
                    exit_main('exit', "whatsapp.py") 

                # Abrir el archivo json para escritura
                with open(route, "w") as json_file:
                    # Escribir los datos actualizados en el archivo json
                    json.dump(intents, json_file)      

                # Finalizado               
                print(Fore.YELLOW + "\nHECHO!")
        
        # No encontró algun archivo .txt con el idioma y nombre especificado
        else:
            try:
                # Eliminar intent_{name}.json
                os.remove(route)
                print(Fore.LIGHTBLACK_EX +f"Archivo 'intent_{name}.json' eliminado\n" + Style.RESET_ALL)
                raise FileNotFoundError(Fore.RED + f"ERROR: No se ha encontrado el archivo \"Chat de WhatsApp con {name}.txt\" en el directorio './chats'" + Style.RESET_ALL)
            except:
                raise FileNotFoundError(Fore.RED + f"ERROR: No se ha encontrado el archivo \"Chat de WhatsApp con {name}.txt\" en el directorio './chats'" + Style.RESET_ALL)
    except FileNotFoundError as e:
        try:
            # Eliminar intent_{name}.json
            os.remove(route)
            print(Fore.LIGHTBLACK_EX +f"\nArchivo 'intent_{name}.json' eliminado\n" + Style.RESET_ALL)
            print(e)
        except:
            print(e)

# Finaliza este subproceso
#if(exit_main(True, "whatsapp.py") == True):
#sys.exit()

# Print tiempo total
print(Fore.YELLOW + f"\nTIEMPO DE EJECUCION: " + Fore.WHITE + str(round(total_time, 2)) + "s" + Style.RESET_ALL)

# Devuelve al Menú
exit_main('exit', "whatsapp.py")  