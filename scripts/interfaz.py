from main import exit_main

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
interfaz.py (NO INCORPORADO)

Interfaz: ✓ 
Funcion: Utiliza prediccion de keras para determinar el tipo de mensaje dicho por el usuario, y escojer una de las respuestas con el modelo entrenado.
"""

# Limpiar Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Introduccion
print(Fore.GREEN + "\n>> Habla con el bot <<" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nAsegurate de haber realizado:\n(4) Entrena el modelo" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)

while(True):

    # Solicitar Nombre
    name = input(Fore.YELLOW + "\n¿Cual es el nombre del contacto?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(name, "interfaz.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(name, "interfaz.py") 

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
def chat():
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

    while True:

        # Prompt del usuario
        print(Fore.LIGHTBLUE_EX + "Yo: " + Style.RESET_ALL, end="")
        inp = input()

        # Opcion de salir
        if inp.lower() == "exit":
            break

        # Finaliza este subproceso
        if(exit_main(inp, "interfaz.py") == True):
            sys.exit()
        
        # Devuelve al Menú
        exit_main(inp, "interfaz.py") 

        # Obtener sentimiento
        sentiment.getSentiment(inp)

        # Calcula la similitud entre la secuencia de texto recibida y los datos de entrenamiento. 
        # Teniendo en cuenta las puntuaciones de confianza obtenidas para cada categoría, clasifica el mensaje del usuario en una intención con la puntuación de confianza más alta.
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len))

        # Revisar si el mensaje generado es apropiado al prompt del usuario
        pred_class = np.argmax(result)
        accuracy = result[0][pred_class]
        print(accuracy)
        if accuracy < 0.998:
            print("La predicción no es segura")

        # Utilizamos la función para deconvertir las etiquetas comprensible del modelo a las originales.
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        # Selecciona una de las 'respuestas' asociadas con el 'tipo' predicto
        for i in data['intents']:
            if i['tag'] == tag:
                # Respuesta al prompt
                print(Fore.YELLOW + f"{name}:" + Style.RESET_ALL , np.random.choice(i['responses']) + "\n")

# Ejecutar interfaz
chat()