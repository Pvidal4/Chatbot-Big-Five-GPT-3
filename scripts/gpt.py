import openai
import os
import re

"""
gpt.py

Interfaz: x 
Funcion: Asiste a interfaz-gpt.py en el uso de la API de OpenAI para el uso del modelo GPT3 en el finetuning de los mensajes predecidos por el modelo entrenado.
"""

# Funcion para obtener la respuesta del gpt finetuned (con memoria)
# Mas informacion sobre prompts: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api
def send_message(key, patterns, responses, ultimo_mensaje, secure, big5, me, you, descripcion):

    # Verificar la llave
    openai.api_key = key

    tu = str(ultimo_mensaje).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '')
    yo = str(patterns).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", '').replace(',', '')
    respuestas = str(responses).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", '')

    # Big5 Prompts
    CBPrompt = readBig5(you, me)

    # Prompt a OpenAI (revisar link)

    # Si tiene una respuesta segura
    if secure == True:
        prompt = f"Estamos teniendo una conversacion. Me llamo \"{me}\".\nEres {descripcion}. La conversación inicia:\n Tu: \"" + tu + "\" \n Yo: \"" + yo + "\" \n Respondeme mi mensaje, puedes usar solo una de estas respuestas:\n \"\"\"" + respuestas + "\"\"\""

        # Si se utiliza big5
        if big5 == "True":
            prompt = f"{CBPrompt}\nEstamos teniendo una conversacion. Me llamo \"{me}\".\nEres {descripcion}. La conversación inicia:\n Tu: \"" + tu + "\" \n Yo: \"" + yo + "\" \n Respondeme mi mensaje, puedes usar solo una de estas respuestas:\n \"\"\"" + respuestas + "\"\"\""

    # Si no tiene una respuesta segura
    if secure == False:
        prompt = f"Estamos teniendo una conversacion. Me llamo \"{me}\".\nEres {descripcion}. La conversación inicia:\n Tu: \"" + tu + "\" \n Yo: \"" + yo + "\" \n Respondeme mi mensaje."

        # Si se utiliza big5
        if big5 == "True":
            prompt = f"{CBPrompt}\nEstamos teniendo una conversacion. Me llamo \"{me}\".\nEres {descripcion}. La conversación inicia:\n Tu: \"" + tu + "\" \n Yo: \"" + yo + "\" \n Respondeme mi mensaje."

    # Respuesta generada
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].text.strip()

# Funcion para obtener la respuesta del gpt finetuned (sin memoria)
# Mas informacion sobre prompts: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api
def getGPTResponse(key, patterns, responses, secure):

    # Verificar la llave
    openai.api_key = key

    # Prompt a OpenAI (revisar link)
    if secure == True:

        prompt = "Estamos teniendo una conversacion casual por sms.\nTe escribi esto: " + patterns + "\nEscribe una oracion como respuesta relacionado a lo que te escribí. " + "\nPuedes usar una de estas respuestas: " + str(responses)

    if secure == False:

        prompt = "Estamos teniendo una conversacion casual por sms.\nTe escribi esto: " + patterns + "\nEscribe una oracion como respuesta relacionado a lo que te escribí. "

    print("Patterns: " + patterns)
    print("Responses: " + str(responses))

    # Respuesta generada
    response = openai.Completion.create(
        engine="text-davinci-001",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def readBig5(chatbot, user):
    # Abrir y leer el archivo de texto
    with open(f'./data/personality_profile/profile_{chatbot}_{user}.txt', 'r') as file:
        lineas = file.readlines()

        # Limpiar Terminal
        #os.system('cls' if os.name == 'nt' else 'clear')

        # Chatbot
        Chatbot_name = lineas[2].split("Contacto: ")[1].split(" (Chatbot)")[0]

        # Puntuaciones chatbot
        cb_max_pts = 0
        cb_max_big5 = 0

        for i in range(5, 9):
            # Extraer el número y el valor pts de la línea actual
            big5 = int(lineas[i].split(".")[0])
            pts = int(lineas[i].split("(")[-1].split("pts")[0])
            
            # Comparar el valor actual con el máximo encontrado hasta el momento
            if pts > cb_max_pts:
                cb_max_pts = pts
                cb_max_big5 = big5

        # Imprimir los resultados
        #print("\nChatbot: " + Chatbot_name)
        #print("El pts mayor es:", cb_max_pts)
        #print("El número al que pertenece es:", cb_max_pts)
        #print(getBig5(cb_max_big5))

        # User
        User_name = lineas[19].split("Contacto: ")[1].split(" (User)")[0]

        # Puntuaciones user
        u_max_pts = 0
        u_max_big5 = 0

        for i in range(22, 26):
            # Extraer el número y el valor pts de la línea actual
            big5 = int(lineas[i].split(".")[0])
            pts = int(lineas[i].split("(")[-1].split("pts")[0])
            
            # Comparar el valor actual con el máximo encontrado hasta el momento
            if pts > u_max_pts:
                u_max_pts = pts
                u_max_big5 = big5

        # Imprimir los resultados
        #print("\nUser: " + User_name)
        #print("El pts mayor es:", u_max_pts)
        #print("El número al que pertenece es:", u_max_pts)
        #print(getBig5(u_max_big5))

        return getBig5(cb_max_big5)
        
        
def getBig5(big5):
    if big5 == 1:
        prompt5 = "Eres una persona imaginativa, curiosa, e intelectualmente abierta. "
    if big5 == 2:
        prompt5 = "Eres una persona organizada, responsable y auto-disciplinada. "
    if big5 == 3:
        prompt5 = "Eres una persona sociable y con mucha confianza en ti misma. "
    if big5 == 4:
        prompt5 = "Eres una persona amable, compasiva y considerada con los demás. "
    if big5 == 5:
        prompt5 = "Eres una persona que experimenta emociones negativas. "

    return prompt5