import os
import re
import sys
import json
import sentiment

import colorama 
from colorama import Fore, Style
colorama.init()

"""
big_five_whatsapp.py

Interfaz: x 
Funcion: Complemento de whatsapp.py, puntuaciones de los big five por cada mensaje y por cada persona (de tipo usuario y chatbot)
"""

# Puntuaciónes Big Five

big5 = {
    "Apertura a la experiencia": 0,
    "Consciencia" : 0,
    "Extraversion" : 0,
    "Amabilidad" : 0,
    "Neuroticismo" : 0
    }

big5CB = {
    "Apertura a la experiencia": 0,
    "Consciencia" : 0,
    "Extraversion" : 0,
    "Amabilidad" : 0,
    "Neuroticismo" : 0
    }

big5U = {
    "Apertura a la experiencia": 0,
    "Consciencia" : 0,
    "Extraversion" : 0,
    "Amabilidad" : 0,
    "Neuroticismo" : 0
}

# Datos de la persona chatbot

CB_word_count_1 = {}
CB_word_count_2 = {}
CB_word_count_3 = {}
CB_word_count_4 = {}
CB_word_count_5 = {}

CB_sentence_count_1 = {}
CB_sentence_count_2 = {}
CB_sentence_count_3 = {}
CB_sentence_count_4 = {}
CB_sentence_count_5 = {}

# Datos de la persona usuario

U_word_count_1 = {}
U_word_count_2 = {}
U_word_count_3 = {}
U_word_count_4 = {}
U_word_count_5 = {}

U_sentence_count_1 = {}
U_sentence_count_2 = {}
U_sentence_count_3 = {}
U_sentence_count_4 = {}
U_sentence_count_5 = {}

# Funcion para guardar los resultados en un .txt
def saveBigFive(chatbot_name, user_name, total_time):
    # Abre el archivo en modo escritura
    with open(f"./data/personality_profile/profile_{chatbot_name}_{user_name}.txt", "w") as file:
        # Escribe los mensajes en el archivo
        file.write(f"\n---------------------------------------------------\n")
        file.write(f">> Contacto: {chatbot_name} (Chatbot)\n")

        file.write(f"\n>> Puntuacion Big Five:\n")
        file.write(f"   1. Apertura a la experiencia: {percentageBigFive('CB', 1)} >> ({big5CB[getBigFive(1)]}pts)\n")
        file.write(f"   2. Consciencia: {percentageBigFive('CB', 2)} >> ({big5CB[getBigFive(2)]}pts)\n")
        file.write(f"   3. Extraversion: {percentageBigFive('CB', 3)} >> ({big5CB[getBigFive(3)]}pts)\n")
        file.write(f"   4. Amabilidad: {percentageBigFive('CB', 4)} >> ({big5CB[getBigFive(4)]}pts)\n")
        file.write(f"   5. Neuroticismo: {percentageBigFive('CB', 5)} >> ({big5CB[getBigFive(5)]}pts)\n")

        file.write(f"\n>> Lista de palabras:\n")
        file.write(f"   1. Apertura a la experiencia: {CB_word_count_1}\n")
        file.write(f"   2. Consciencia: {CB_word_count_2}\n")
        file.write(f"   3. Extraversion: {CB_word_count_3}\n")
        file.write(f"   4. Amabilidad: {CB_word_count_4}\n")
        file.write(f"   5. Neuroticismo: {CB_word_count_5}\n")

        file.write(f"\n---------------------------------------------------\n")
        file.write(f">> Contacto: {user_name} (User)\n")

        file.write(f"\n>> Puntuacion Big Five:\n")
        file.write(f"   1. Apertura a la experiencia: {percentageBigFive('U', 1)} >> ({big5U[getBigFive(1)]}pts)\n")
        file.write(f"   2. Consciencia: {percentageBigFive('U', 2)} >> ({big5U[getBigFive(2)]}pts)\n")
        file.write(f"   3. Extraversion: {percentageBigFive('U', 3)} >> ({big5U[getBigFive(3)]}pts)\n")
        file.write(f"   4. Amabilidad: {percentageBigFive('U', 4)} >> ({big5U[getBigFive(4)]}pts)\n")
        file.write(f"   5. Neuroticismo: {percentageBigFive('U', 5)} >> ({big5U[getBigFive(5)]}pts)\n")

        file.write(f"\n>> Lista de palabras:\n")
        file.write(f"   1. Apertura a la experiencia: {U_word_count_1}\n")
        file.write(f"   2. Consciencia: {U_word_count_2}\n")
        file.write(f"   3. Extraversion: {U_word_count_3}\n")
        file.write(f"   4. Amabilidad: {U_word_count_4}\n")
        file.write(f"   5. Neuroticismo: {U_word_count_5}\n")

        file.write(f"\n---------------------------------------------------")

        file.write(f"\nTIEMPO DE EJECUCION: " + str(round(total_time, 2)) + "s" )


# Funcion para imprimir en whatsapp.py
def printBigFive(chatbot_name, user_name):

    print(Fore.LIGHTBLACK_EX + "\n---------------------------------------------------\n")
    print(Fore.YELLOW + f">> Contacto: " + Fore.WHITE + f"{chatbot_name}" + Fore.LIGHTBLACK_EX + " (Chatbot)")

    print("\n" + Fore.YELLOW + ">> Puntuacion Big Five:")
    print(Fore.LIGHTBLUE_EX + "   1. Apertura a la experiencia: " + Fore.WHITE + str(percentageBigFive("CB", 1)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5CB[getBigFive(1)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   2. Consciencia: " + Fore.WHITE + str(percentageBigFive("CB", 2)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5CB[getBigFive(2)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   3. Extraversion: " + Fore.WHITE + str(percentageBigFive("CB", 3)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5CB[getBigFive(3)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   4. Amabilidad: " + Fore.WHITE + str(percentageBigFive("CB", 4)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5CB[getBigFive(4)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   5. Neuroticismo: " + Fore.WHITE + str(percentageBigFive("CB", 5)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5CB[getBigFive(5)]) + "pts) ")

    print("\n" + Fore.YELLOW + ">> Lista de palabras:")
    print(Fore.LIGHTBLUE_EX + "   1. Apertura a la experiencia: " + Fore.WHITE + str(CB_word_count_1))
    print(Fore.LIGHTBLUE_EX + "   2. Consciencia: " + Fore.WHITE + str(CB_word_count_2))
    print(Fore.LIGHTBLUE_EX + "   3. Extraversion: " + Fore.WHITE + str(CB_word_count_3))
    print(Fore.LIGHTBLUE_EX + "   4. Amabilidad: " + Fore.WHITE + str(CB_word_count_4))
    print(Fore.LIGHTBLUE_EX + "   5. Neuroticismo: " + Fore.WHITE + str(CB_word_count_5))

    print(Fore.LIGHTBLACK_EX + "\n---------------------------------------------------\n")
    print(Fore.YELLOW + f">> Contacto: " + Fore.WHITE + f"{user_name}" + Fore.LIGHTBLACK_EX + " (User)")

    print("\n" + Fore.YELLOW + ">> Puntuacion Big Five:")
    print(Fore.LIGHTBLUE_EX + "   1. Apertura a la experiencia: " + Fore.WHITE + str(percentageBigFive("U", 1)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5U[getBigFive(1)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   2. Consciencia: " + Fore.WHITE + str(percentageBigFive("U", 2)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5U[getBigFive(2)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   3. Extraversion: " + Fore.WHITE + str(percentageBigFive("U", 3)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5U[getBigFive(3)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   4. Amabilidad: " + Fore.WHITE + str(percentageBigFive("U", 4)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5U[getBigFive(4)]) + "pts) ")
    print(Fore.LIGHTBLUE_EX + "   5. Neuroticismo: " + Fore.WHITE + str(percentageBigFive("U", 5)) + Fore.YELLOW + " >> " + Fore.LIGHTBLACK_EX + "(" + str(big5U[getBigFive(5)]) + "pts) ")

    print("\n" + Fore.YELLOW + ">> Lista de palabras:")
    print(Fore.LIGHTBLUE_EX + "   1. Apertura a la experiencia: " + Fore.WHITE + str(U_word_count_1))
    print(Fore.LIGHTBLUE_EX + "   2. Consciencia: " + Fore.WHITE + str(U_word_count_2))
    print(Fore.LIGHTBLUE_EX + "   3. Extraversion: " + Fore.WHITE + str(U_word_count_3))
    print(Fore.LIGHTBLUE_EX + "   4. Amabilidad: " + Fore.WHITE + str(U_word_count_4))
    print(Fore.LIGHTBLUE_EX + "   5. Neuroticismo: " + Fore.WHITE + str(U_word_count_5))

    print(Fore.LIGHTBLACK_EX + "\n---------------------------------------------------")

# Funcion para calcular el porcentaje de big five
def percentageBigFive(subject, five):

    # Porcentaje Big Five Chatbot
    total = sum(big5CB.values())
    CB_word_count_1P = '{:.0%}'.format(big5CB[getBigFive(1)] / total)
    CB_word_count_2P = '{:.0%}'.format(big5CB[getBigFive(2)] / total)
    CB_word_count_3P = '{:.0%}'.format(big5CB[getBigFive(3)] / total)
    CB_word_count_4P = '{:.0%}'.format(big5CB[getBigFive(4)] / total)
    CB_word_count_5P = '{:.0%}'.format(big5CB[getBigFive(5)] / total)

    # Porcentaje Big Five Usuario
    total = sum(big5U.values())
    U_word_count_1P = '{:.0%}'.format(big5U[getBigFive(1)] / total)
    U_word_count_2P = '{:.0%}'.format(big5U[getBigFive(2)] / total)
    U_word_count_3P = '{:.0%}'.format(big5U[getBigFive(3)] / total)
    U_word_count_4P = '{:.0%}'.format(big5U[getBigFive(4)] / total)
    U_word_count_5P = '{:.0%}'.format(big5U[getBigFive(5)] / total)

    # Return
    if subject == "CB":
        return eval(f"CB_word_count_{five}P")
    if subject == "U":
        return eval(f"U_word_count_{five}P")

# Funcion para realizar las puntuaciones en todos los big5 (general y especifico) con appendBigFive
def addBigFive(line, subject):

    # Big five general
    big5L = {
    "Apertura a la experiencia": 0,
    "Consciencia" : 0,
    "Extraversion" : 0,
    "Amabilidad" : 0,
    "Neuroticismo" : 0
    }

    # Divide y toma solo la seccion que contiene el mensaje de texto
    line = line.split("-")[1].split(":")[1]

    # Funcion para eliminar todos los caracteres que no son letras, números o espacios, y convertir todo el texto en minúsculas
    line = remove_punctuation(line)

    # Openness to experience (Apertura a la experiencia): Refiere a la inclinación de una personas a ser imaginativo, curioso, e intelectualmente abierto.
    appendBigFive(line, subject, 1, big5L)

    # Conscientiousness (Consciencia): Refiere a la tendencia de una persona a ser organizado, responsable y auto-disciplinado.
    appendBigFive(line, subject, 2, big5L)

    # Extraversion (Extraversión): Refiere al nivel de gregarismo, sociabilidad y confianza en sí mismo de una persona.
    appendBigFive(line, subject, 3, big5L)

    # Agreeableness (Amabilidad): Refiere a la tendencia de una persona a ser amable, compasiva y considerada con los demás.
    appendBigFive(line, subject, 4, big5L)

    # Neuroticism (Neuroticismo): Refiere a la tendencia de una persona a experimentar emociones negativas como ansiedad, estrés, y depresión.
    appendBigFive(line, subject, 5, big5L)

    return big5CB, big5U, big5L

# Funcion para agregar un punto si corresponde en la linea especificada (utilizado en addBigFive)
def appendBigFive(line, subject, five, big5L):

    # Si la persona es tipo chatbot
    if subject == "Chatbot":

        # Crea una variable dinamica del big five especificado.
        # Agrega las conjugaciones del big five especificado a la variable dinamica word_bank con read_conjugation
        exec(f"CB_word_bank_{five} = {read_conjugation(f'{getBigFive(five)}.json')}")
        
        # Obtiene el valor de las variables dinamicas creadas
        # Las asigna a una variable fija para trabajarlas
        CB_word_bank = eval(f"CB_word_bank_{five}")
        CB_word_count = eval(f"CB_word_count_{five}")

        # Agrega las puntuaciones, ya sea al big5 general, o al big5 especifico
        word_count, add = words_count(line, CB_word_bank, CB_word_count)
        big5L[f"{getBigFive(five)}"] += add
        big5CB[f"{getBigFive(five)}"] += add
        
    # Si la persona es tipo usuario
    elif subject == "User":

        # Crea una variable dinamica del big five especificado.
        # Agrega las conjugaciones del big five especificado a la variable dinamica word_bank con read_conjugation
        exec(f"U_word_bank_{five} = {read_conjugation(f'{getBigFive(five)}.json')}")

        # Obtiene el valor de las variables dinamicas creadas
        # Las asigna a una variable fija para trabajarlas
        U_word_bank = eval(f"U_word_bank_{five}")
        U_word_count = eval(f"U_word_count_{five}")

        # Agrega las puntuaciones, ya sea al big5 general, o al big5 especifico
        word_count, add = words_count(line, U_word_bank, U_word_count)
        big5L[f"{getBigFive(five)}"] += add
        big5U[f"{getBigFive(five)}"] += add

# Funcion que devuelve el texto basado en el numero
def getBigFive(five):
    if five == 1:
        return 'Apertura a la experiencia'
    if five == 2:
        return 'Consciencia'
    if five == 3:
        return 'Extraversion'
    if five == 4:
        return 'Amabilidad'
    if five == 5:
        return 'Neuroticismo'

# Funcion que devuelve el texto basado en el numero
def getBigFiveDescription(five):
    if five == 1:
        return 'Refiere a la inclinación de una personas a ser imaginativo, curioso, e intelectualmente abierto.'
    if five == 2:
        return 'Refiere a la tendencia de una persona a ser organizado, responsable y auto-disciplinado.'
    if five == 3:
        return 'Refiere al nivel de gregarismo, sociabilidad y confianza en sí mismo de una persona.'
    if five == 4:
        return 'Refiere a la tendencia de una persona a ser amable, compasiva y considerada con los demás.'
    if five == 5:
        return 'Refiere a la tendencia de una persona a experimentar emociones negativas como ansiedad, estrés, y depresión.'
    
# Funcion para eliminar todos los caracteres que no son letras, números o espacios, y convertir todo el texto en minúsculas
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text).lower()

# Funcion para leer todas las conjugaciones del json de big5 especificado
def read_conjugation(filename):

    # Abrir el json y cargar los datos
    with open(f"./data/big_five/{filename}", 'r') as f:
        resultados_existentes = json.load(f)

    # Crear una lista vacía para guardar todas las formas
    formas = []

    # Iterar a través de cada verbo en los resultados existentes
    for verbo, resultados in resultados_existentes.items():

        # Agregar el verbo sin modificar (para utilizar el verbo base en el análisis tambien)
        formas.append(verbo)

        # Iterar a través de cada resultado para un verbo específico
        for resultado in resultados:
            # Verificar si el resultado tiene la clave "forma"
            if "forma" in resultado:
                # Agregar la forma a la lista
                formas.append(resultado["forma"])

    return formas

# Devuelve cuanto agregar a la puntuacion de big5 de una linea indicada, basada en el banco de palabras
def words_count(line, word_bank, word_count):

    # Dividir el mensaje en palabras
    words = line.split()
    
    add = 0

    # Iterar sobre las palabras
    for word in words:
        if word in word_bank:
            if word in word_count:
                # Si ya existe, agregar 1 al resultado existente
                word_count[word] += 1
            else:
                # Si no existe, crear el resultado 1
                word_count[word] = 1
            # Agregar al contador
            add += 1
    return word_count, add
