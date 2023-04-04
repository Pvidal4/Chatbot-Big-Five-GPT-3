import os
import re
import sys

import time
import subprocess
import msvcrt

import colorama 
from colorama import Fore, Style
colorama.init()

"""
main.py

Interfaz: ✓ 
Funcion: El menu del programa, permite seguir paso a paso el entrenamiento, la creacion del modelo y la ejecucion.
"""

# Funcion para devolver al usuaio al main.py cuando haya escrito 'exit' en cualquier input del resto de las interfaces
def exit_main(input, python, arg=None):
    if input == 'exit':
        print(Fore.LIGHTBLUE_EX + "\nPresione ESC para ir al menu principal")
        print("Presione ENTER para repetir\n" + Style.RESET_ALL)
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if ord(key) == 27: # 27 es el código ASCII de la tecla Esc
                    # Cierra el subproceso para volver al main
                    sys.exit()
                else:
                    # Vuelve a ejecutar el script
                    if arg == None:
                        subprocess.call(["python", f"./scripts/{python}"])
                    else:
                        subprocess.call(["python", f"./scripts/{python}", arg])
                    
                    return True

# Inicializacion de subprocesos desde el main
def ejecutar_script_1():
    subprocess.call(["python", "./scripts/tag_training.py"])
    main()

def ejecutar_script_2():
    subprocess.call(["python", "./scripts/big_five_data.py"])
    main()

def ejecutar_script_3():
    subprocess.call(["python", "./scripts/whatsapp.py"])
    main()

def ejecutar_script_4():
    subprocess.call(["python", "./scripts/entrenamiento.py"])
    main()

def ejecutar_script_5():
    subprocess.call(["python", "./scripts/interfaz.py"])
    main()

def ejecutar_script_6(big5):
    subprocess.call(["python", "./scripts/interfaz-gpt.py", str(big5)])
    main()
        
# Interfaz del main
def main():

    while(True):
        while(True):

            os.system('cls' if os.name == 'nt' else 'clear')

            print(Fore.GREEN + ">> Main Menu <<" + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "\nSelecciona 'I' para más información" + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir\n" + Style.RESET_ALL)
            print(Fore.GREEN + ">> Datos & Entrenamiento <<\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "1. Reconocimiento de mensajes" + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(tag_training.py)" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "2. Añade a la base de datos de Big Five" + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(big_five_data.py)" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "3. Procesamiento de mensajes WhatsApp" + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(whatsapp.py)" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "4. Entrena el modelo" + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(entrenamiento.py)" + Style.RESET_ALL)
            print(Fore.GREEN + "\n>> Chatbot <<\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "5. Habla con el bot (Asistido por GPT-3 & Big5)" + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(interfaz-gpt.py)" + Style.RESET_ALL)

            opcion = input(Fore.YELLOW + "\nSeleccione una opción: " + Style.RESET_ALL)

            if opcion == 'I' or opcion == "i":
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            if opcion == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_1()
                break
            elif opcion == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_2()
                break
            elif opcion == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_3()
                break
            elif opcion == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_4()
                break
            elif opcion == '5':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(True)
                break
            elif opcion == '6':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(False)
                break
            elif opcion == '7':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(True)
                break
            elif opcion == 'exit':
                sys.exit()
                break
            else:
                print(Fore.RED + "\nERROR: Opción no válida" + Style.RESET_ALL)
                time.sleep(1.5)

        while(True):

            os.system('cls' if os.name == 'nt' else 'clear')

            print(Fore.GREEN + ">> Más información <<\n" + Style.RESET_ALL)
            print(Fore.GREEN + ">> ¿Cómo utilizar? <<" + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "\nEn cualquier paso del programa, puedes utilizar 'back' para volver un paso atrás." + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "También puedes utilizar 'exit' para volver al menú principal." + Style.RESET_ALL)
            print(Fore.LIGHTBLACK_EX + "Aquí tienes una breve explicación de cada una de las funcionalidades...\n" + Style.RESET_ALL)
            print(Fore.GREEN + ">> Datos & Entrenamiento <<\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "1. Reconocimiento de mensajes" + Fore.YELLOW + "\n\n>> " + Fore.LIGHTBLACK_EX + "Aquí tienes que clasificar palabras por su 'tipo'." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "Es decir, podemos crear un tipo de mensaje como 'juego' y asignarle palabras que indiquen este 'tipo' de mensaje como: 'monopolio, futbol, jenga'." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "En este ejemplo, mensajes que contengan las palabras: 'monopolio, futbol o jenga', se clasificarán como mensajes de tipo 'juego'.\n"+ Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "2. Añade a la base de datos de Big Five" + Fore.YELLOW + "\n\n>> " + Fore.LIGHTBLACK_EX + "Aquí se encuentran clasificados los verbos para identificar mensajes que posean ciertas características de personalidad big five." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "Los verbos se conjugarán automáticamente para detectar todas las variaciones posibles en cada mensaje." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "No es necesario agregar. Se encuentran clasificados los verbos estudiados que corresponen a cada rasgo de personalidad.\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "3. Procesamiento de mensajes WhatsApp" + Fore.YELLOW + "\n\n>> " + Fore.LIGHTBLACK_EX + "Aquí es donde se utilizan los dos pasos anteriores para clasificar mensajes por su 'tipo' en el chat y detectar verbos conjugados big five." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "Para ello, es necesario que hayas extraido el chat WhatsApp de tu celular o computadora con la funcion \"Exportar Chat\" (Omite multimedia)" + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "El export debes colocarlo en la ruta /chats del programa\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "4. Entrena el modelo" + Fore.YELLOW + "\n\n>> " + Fore.LIGHTBLACK_EX + "Antes de comenzar la siguiente sección, debes entrenar un modelo de redes neuronales." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "Este modelo es lo que permite al chatbot hablar como el contacto que has seleccionado." + Fore.YELLOW + "\n>> " + Fore.LIGHTBLACK_EX + "En caso de obtener resultados no deseados, se debe reentrenar el modelo con más parámetros en '1. Reconocimiento de mensajes'."+ Style.RESET_ALL)
            print(Fore.GREEN + "\n>> Chatbot <<\n" + Style.RESET_ALL)
            print(Fore.LIGHTBLUE_EX + "5. Habla con el bot (Asistido por GPT-3 & Big5)" + Fore.YELLOW + "\n\n>> " + Fore.LIGHTBLACK_EX + "Este chatbot reconoce intents, utiliza un fintune de GPT-3 y realiza un reconocimiento de los rasgos de personalidad Big Five.\n" + Style.RESET_ALL)
            
            opcion = input(Fore.YELLOW + "Seleccione una opción: " + Style.RESET_ALL)

            if opcion == 'back' or opcion == "exit":
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            if opcion == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_1()
                break
            elif opcion == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_2()
                break
            elif opcion == '3':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_3()
                break
            elif opcion == '4':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_4()
                break
            elif opcion == '5':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(True)
                break
            elif opcion == '6':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(False)
                break
            elif opcion == '7':
                os.system('cls' if os.name == 'nt' else 'clear')
                ejecutar_script_6(True)
                break
            elif opcion == 'exit':
                sys.exit()
                break
            else:
                print(Fore.RED + "\nERROR: Opción no válida" + Style.RESET_ALL)
                time.sleep(1.5)

if __name__ == "__main__":
    main()
    