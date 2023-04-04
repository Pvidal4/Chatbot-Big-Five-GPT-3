import os
import re
import sys
import json

import colorama 
from colorama import Fore, Style
colorama.init()

from unidecode import unidecode

from big_five_whatsapp import getBigFive, getBigFiveDescription
from conjugate import conjugar
from main import exit_main

"""
big_five_data.py

Interfaz: ✓ 
Funcion: Permite agregar y conjugar verbos correspondientes en la base de datos de big five (./data/big_five)
"""

while(True):

    # Limpiar Terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # Introduccion
    print(Fore.GREEN + "\n>> Añade a la base de datos de Big Five <<" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "\nAgregar palabras asociadas con las personalidades para conjugar" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)

    print(Fore.LIGHTBLACK_EX + "\n1. Abierto a la experiencia\n2. Consciencia\n3. Extraversion\n4. Amabilidad\n5. Neuroticismo" + Style.RESET_ALL)

    inp = input(Fore.YELLOW + "\n¿A cual se va a añadir?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(inp, "big_five_data.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(inp, "big_five_data.py") 

    # Verificar que se selecciono uno de los big5
    try:
        b5 = getBigFive(int(inp)) 
        m5 = getBigFiveDescription(int(inp)) 
        while(b5 == None):
            print(Fore.RED +"\nERROR: Por favor selecciona uno de los big five" + Style.RESET_ALL)
            inp = input(Fore.YELLOW + "\n¿A cual se va a añadir?\n" + Style.RESET_ALL)
            b5 = getBigFive(int(inp)) 
            m5 = getBigFiveDescription(int(inp)) 
    except:
        print(Fore.RED +"\nERROR: Tiene que ser un número" + Style.RESET_ALL)
        inp = input(Fore.YELLOW + "\n¿A cual se va a añadir?\n" + Style.RESET_ALL)
        
        # Finaliza este subproceso
        if(exit_main(inp, "big_five_data.py") == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(inp, "big_five_data.py") 

        # Nombre del big five con el numero para usar en el nombre del archivo
        b5 = getBigFive(int(inp)) 
        m5 = getBigFiveDescription(int(inp)) 

    # Agregar verbo

    # Limpiar Terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + "\n>> Añade a la base de datos de Big Five <<" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)
    print(Fore.LIGHTBLACK_EX + "\n" + b5 + f": {m5}" + Style.RESET_ALL)

    # Verificar si el archivo JSON ya existe
    if os.path.exists(f"./data/big_five/{b5}.json"):
        # Abrir el archivo JSON para lectura
        with open(f"./data/big_five/{b5}.json", "r") as archivo_json:
            # Cargar los resultados existentes
            resultados_existentes = json.load(archivo_json)
            conjugados = []
            for verbo in resultados_existentes.keys():
                # Lista de verbos que han sido conjugados
                conjugados.append(verbo)
            print(Fore.LIGHTBLUE_EX + "\nVerbos conjugados: "+ Fore.WHITE + str(conjugados) + Style.RESET_ALL)
                
    verbo = input(Fore.YELLOW + "\nVerbo nuevo:\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(verbo, "big_five_data.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(verbo, "big_five_data.py") 

    if verbo == 'back':
        continue
    else:
        # Verificar si el archivo JSON ya existe
        if os.path.exists(f"./data/big_five/{b5}.json"):
            # Abrir el archivo JSON para lectura
            with open(f"./data/big_five/{b5}.json", "r") as archivo_json:
                # Cargar los resultados existentes
                resultados_existentes = json.load(archivo_json)
            # Actualizar los resultados existentes con los nuevos resultados (utilizando la funcion conjugar de conjugate.py)
            resultados_existentes.update(conjugar(verbo))
            resultados = resultados_existentes

        # Abrir el archivo JSON para escritura
        with open(f"./data/big_five/{b5}.json", "w") as archivo_json:
            # Escribir los resultados en el archivo JSON
            json.dump(resultados, archivo_json)

        # Abrir el archivo JSON para lectura
        with open(f"./data/big_five/{b5}.json", "r") as archivo_json:
            # Cargar los resultados desde el archivo JSON
            resultados_existentes = json.load(archivo_json)


