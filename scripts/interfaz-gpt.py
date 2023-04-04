from main import exit_main
from gpt import getGPTResponse, send_message

import os
import re
import sys
import json 
import pickle
import random
import sentiment

import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder

import colorama 
from colorama import Fore, Style
colorama.init()

"""
interfaz-gpt.py

Interfaz: ✓ 
Funcion: Similar a interfaz.py, interfaz-gpt.py utiliza gpt.py para el uso de la API de OpenAI en el finetune de mensajes predecidos por el modelo entrenado.
"""

# Key (Introduce tu GPT API Key)
key = ""

# [Arg] Asistido por Big5
big5 = sys.argv[1]

# Limpiar Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Introduccion
if big5 == "False":
    print(Fore.GREEN + "\n>> Habla con el bot (Asistido por GPT-3) <<" + Style.RESET_ALL)
if big5 == "True":
    print(Fore.GREEN + "\n>> Habla con el bot (Asistido por GPT-3 & Big5) <<" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nAsegurate de haber realizado:\n(4) Entrena el modelo" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)

# Si no se ha introducido una key arriba
while(True):

    # Solicitar API KEY
    if key == "":
        key = input(Fore.YELLOW + "\nPor favor, ingresa tu GPT Key\n" + Fore.LIGHTBLACK_EX + "También puedes ingresarla en el python interfaz-gpt.py\n" + Style.RESET_ALL)

    # Solicitar Nombre
    name = input(Fore.YELLOW + "\n¿Cual es el nombre del contacto?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(name, "interfaz-gpt.py", big5) == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(name, "interfaz-gpt.py") 

    # Solicitar Nombre
    yo = input(Fore.YELLOW + "\n¿Cual es tu nombre?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(yo, "interfaz-gpt.py", big5) == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(yo, "interfaz-gpt.py") 

    # Solicitar Descripcion
    descripcion = input(Fore.YELLOW + f"\n¿Quien es {name}?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(yo, "interfaz-gpt.py", big5) == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(yo, "interfaz-gpt.py") 

    try:
        # Abrir el JSON
        with open(f"data/intents/model_training/intent_{name}.json", encoding="utf8") as file:
            print(Fore.LIGHTBLACK_EX +f"\nUtilizando: intent_{name}.json" + Style.RESET_ALL)
            data = json.load(file)
            break
    except:
        print(Fore.RED +f"\nERROR: No existe entrenamiento de: {name}" + Style.RESET_ALL)

# Limpiar Terminal
os.system('cls' if os.name == 'nt' else 'clear')

### INTERFAZ DEL CHATBOT ###
def chat(big5):

    # Abrir modelo entrenado
    model = keras.models.load_model(f'./models/modelo_chatbot_{name}')

    # Abrir objeto tokenizer
    with open(f'./data/pickles/tokenizer_{name}.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # Abrir label encoder object
    with open(f'./data/pickles/label_encoder_{name}.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    # Longitud máxima
    max_len = 20
    
    # Limpiar Terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # Mensaje inicial
    print(Fore.YELLOW + f"\n{name}: " + Style.RESET_ALL + "¡Hola! Habla conmigo\n")

    # Memoria del ultimo mensaje
    ultimo_mensaje = "Hola!"

    while True:

        # Prompt del usuario
        print(Fore.LIGHTBLUE_EX + f"{yo}: " + Style.RESET_ALL, end="")
        inp = input()

        # Opcion de salir
        if inp.lower() == "exit":
            break

        # Finaliza este subproceso
        if(exit_main(inp, "interfaz-gpt.py", big5) == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(inp, "interfaz-gpt.py", big5) 

        # Obtener sentimiento
        sentiment.getSentiment(inp)

        # Calcula la similitud entre la secuencia de texto recibida y los datos de entrenamiento. 
        # Teniendo en cuenta las puntuaciones de confianza obtenidas para cada categoría, clasifica el mensaje del usuario en una intención con la puntuación de confianza más alta.
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))

        # Revisar si el mensaje generado es apropiado al prompt del usuario
        pred_class = np.argmax(result)
        accuracy = result[0][pred_class]
        print("Accuracy: " + str(accuracy))
        secure = True
        

        # Utilizamos la función para deconvertir las etiquetas comprensible del modelo a las originales.
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        # Selecciona una de las 'respuestas' asociadas con el 'tipo' predicto
        for i in data['intents']:
            if i['tag'] == tag:

                if accuracy < 0.9:
                    secure = False
                    print("Tag no reconocido del entrenamiento...")
                else:
                    # Imprimir el tag del mensaje predecido
                    print("Tag entrenado: " + i['tag'])

                # Mensaje finetuned sin memoria
                #print(Fore.YELLOW + f"{name}: " + Style.RESET_ALL + getGPTResponse(key, inp, i['responses'], secure))
 
                # Mensaje finetuned con memoria
                respuesta = send_message(key, inp, i['responses'], ultimo_mensaje, secure, str(big5), yo, name, descripcion)
                print(Fore.YELLOW + f"{name}: " + Style.RESET_ALL + str(respuesta))

                # Asignar la memoria
                ultimo_mensaje = respuesta
                
# Ejecutar interfaz
chat(big5)