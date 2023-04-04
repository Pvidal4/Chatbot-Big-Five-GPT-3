from main import exit_main
import time
import os
import re
import sys
import json 

import colorama 
from colorama import Fore, Style
colorama.init()

import numpy as np 
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Embedding, GlobalAveragePooling1D
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.preprocessing import LabelEncoder

"""
entrenamiento.py

Interfaz: ✓ 
Funcion: Entrena el modelo y genera: 
        1. ./data/intents/personality_training/..
        2. ./data/intents/model_training/..
        3. ./models/..
        4. ./data/pickles/..
"""

# Limpiar Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Introduccion
print(Fore.GREEN + "\n>> Entrena el modelo <<" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nEntrena el modelo del chatbot a partir de los mensajes WhatsApp" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nAsegurate de haber realizado:\n(3) Procesamiento de mensajes WhatsApp" + Style.RESET_ALL)
print(Fore.LIGHTBLACK_EX + "\nEscribe 'exit' para salir" + Style.RESET_ALL)

while(True):

    # Solicitar Nombre
    name = input(Fore.YELLOW + "\n¿Cual es el nombre del contacto?\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(name, "entrenamiento.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(name, "entrenamiento.py") 

    try:
        # Abrir el JSON
        with open(f"data/intents/personality_training/intent_{name}.json", "r", encoding="utf8") as file:
            data = json.load(file)
            
        print(Fore.LIGHTBLACK_EX +f"\nUtilizando: intent_{name}.json" + Style.RESET_ALL)
        break
    except:
        print(Fore.RED +f"\nERROR: No existe intent_{name}.json" + Style.RESET_ALL)
        print(Fore.LIGHTBLACK_EX +f"Para generarlo: (3) Procesamiento de mensajes WhatsApp " + Style.RESET_ALL)

while(True):
    # Solicitar Nombre
    epochs = input(Fore.YELLOW + "\n¿Con cuantos ciclos se desea entrenar?" + Fore.LIGHTBLACK_EX + "\nRecomendado mínimo 500 epochs\n" + Style.RESET_ALL)

    # Finaliza este subproceso
    if(exit_main(name, "entrenamiento.py") == True):
        sys.exit()
    
    # Devuelve al Menú
    exit_main(name, "entrenamiento.py") 

    try:
        int(epochs)
        break
    except:
        print(Fore.RED +f"ERROR: Debe ser un número entero" + Style.RESET_ALL)
        
# Inicializar contador de tiempo de ejecución
start_time = time.time() 

# La variable "training_sentences" contiene todos los datos de entrenamiento (que son los mensajes de muestra en cada categoría de intención) 
# La variable "training_labels" contiene todas las etiquetas objetivo correspondientes a cada dato de entrenamiento.

training_sentences = []
training_labels = []
labels = []
responses = []

known_tag = []

for intent in data['intents']:

    if intent['tag'] not in known_tag:
        known_tag.append(intent['tag'])

print("\nTAGS: " + str(known_tag) + "\n")

## Patterns = User
## Responses = Chatbot

intnts ={"intents":[]}

for tag in known_tag:
    
    new_patterns = []
    new_responses = []
    
    if tag != 'NOT FOUND':


        for intent in data['intents']:
            if intent['tag'] == tag:

                if intent['subject'] == 'User':

                    training_sentences.append(intent['mensaje'])
                    training_labels.append(intent['tag'])

                    new_patterns.append(intent['mensaje'])
                    
                elif intent['subject'] == 'Chatbot':
                    responses.append(intent['mensaje'])

                    new_responses.append(intent['mensaje'])

                if intent['tag'] not in labels:
                    labels.append(intent['tag'])

    new_intent ={
        "tag": tag,
        "patterns": new_patterns,
        "responses": new_responses
    }
    intnts["intents"].append(new_intent)

with open(f"data/intents/model_training/intent_{name}.json", 'w', encoding='utf8') as file:
    json.dump(intnts, file)

num_classes = len(labels)
# La función "LabelEncoder()" proporcionada por scikit-learn sirve para convertir las etiquetas de destino en una forma comprensible del modelo.

lbl_encoder = LabelEncoder()
lbl_encoder.fit(training_labels)
training_labels = lbl_encoder.transform(training_labels)

# Limitar el tamaño de nuestro vocabulario hasta un número definido.

vocab_size = 1000

# La Embedding layer nos permite convertir cada palabra en un vector de longitud fija de tamaño definido. El vector resultante es denso y tiene valores reales en lugar de solo 0 y 1.
embedding_dim = 16
max_len = 20

# También podemos agregar "oov_token", que es un valor para "out of token" para tratar con palabras fuera de vocabulario (tokens) en el momento de la inferencia.
oov_token = "<OOV>"

# Se vectoriza nuestro corpus de datos de texto utilizando la clase "Tokenizer" para el preprocesamiento de texto.
tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(training_sentences)

# El método "pad_sequences" se utiliza para hacer que todas las secuencias de texto de entrenamiento tengan el mismo tamaño.
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

### ENTRENAMIENTO DEL MODELO ###
# Red neuronal para el modelo se utiliza la clase de modelo "secuencial" de Keras.

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(GlobalAveragePooling1D())
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

# ENTRENAMIENTO. 

#epochs = 500
history = model.fit(padded_sequences, np.array(training_labels), epochs=int(epochs))

# Después del entrenamiento, es mejor guardar todos los archivos necesarios para usarlos en el momento de la inferencia. Para que guardemos el modelo entrenado, el objeto tokenizador ajustado y el objeto codificador de etiqueta ajustado.

# Guardar el modelo entrenado
model.save(f"./models/modelo_chatbot_{name}")

import pickle

# Guardar el tokenizer
with open(f'./data/pickles/tokenizer_{name}.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
# Guardar el label encoder
with open(f'./data/pickles/label_encoder_{name}.pickle', 'wb') as ecn_file:
    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)

# Tiempo Final
end_time = time.time()
total_time = end_time - start_time
print(Fore.YELLOW + f"\nTIEMPO DE EJECUCION: " + Fore.WHITE + str(round(total_time, 2)) + "s" + Style.RESET_ALL)

exit_main("exit", "entrenamiento.py") 