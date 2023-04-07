# Modelo de Personalidad de un Chatbot: Asimilación de los modismos de comunicación y los rasgos de personalidad Big Five de una persona.

## Informacion del Proyecto

El objetivo de este estudio es investigar la viabilidad de integrar características de personalidad en los chatbots y representarlas de manera convincente. Para definir la personalidad, se tomó como referencia los cinco grandes rasgos de personalidad establecidos. Se desarrolló un modelo de redes neuronales para detectar la intención de los mensajes, así como para identificar los rasgos de personalidad en los mensajes de WhatsApp. El modelo GPT fue utilizado para realizar un finetune final de la respuesta seleccionada, lo que resultó en una conversación dinámica y convincente.

## *Clases Principales*

### **0. Menú Principal** >> main.py

Interfaz: ✓

Funcion: El menu del programa, permite seguir paso a paso el entrenamiento, la creacion del modelo y la ejecucion.

### **1. Reconocimiento de mensajes** >> tag_training.py

Interfaz: ✓ 

Funciones:
1. Ayudar a whatsapp.py para identificar el tag del mensaje con findMessage()
2. El resto es dedicado a una interfaz para entrenar la base de datos de tipos de mensaje generada en ./data/intents/tag_training/tags.json

### **2. Añade a la base de datos de Big Five** >> big_five_data.py

Interfaz: ✓ 

Funcion: Permite agregar y conjugar verbos correspondientes en la base de datos de big five (./data/big_five)

### **3. Procesamiento de mensajes WhatsApp** >> whatsapp.py

Interfaz: ✓ 

Funcion: Leer cada mensaje del .txt expecificado, generar resutlados de sentimiento, big_five y tag en: ./data/intents/personality_training/intent_{name}.json

### **4. Entrena el modelo** >> entrenamiento.py

Interfaz: ✓ 

Funcion: Entrena el modelo y genera: 
1. ./data/intents/personality_training/..
2. ./data/intents/model_training/..
3. ./models/..
4. ./data/pickles/..

### **5. Habla con el bot (Asistido por GPT-3 & Big5)** >> interfaz-gpt.py

Interfaz: ✓ 

Funcion: Similar a interfaz.py, interfaz-gpt.py utiliza gpt.py para el uso de la API de OpenAI en el finetune de mensajes predecidos por el modelo entrenado.

## *Clases Complementarias*

### big_five_whatsapp.py

Interfaz: x 

Funcion: Complemento de whatsapp.py, puntuaciones de los big five por cada mensaje y por cada persona (de tipo usuario y chatbot)

### conjugate.py

Interfaz: x 

Funcion: Conjuga los verbos solicitados por big_five_data.py con el propósito de obtener todas las variaciones posibles.

### gpt.py

Interfaz: x 

Funcion: Asiste a interfaz-gpt.py en el uso de la API de OpenAI para el uso del modelo GPT3 en el finetuning de los mensajes predecidos por el modelo entrenado.

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

```
> git clone https://github.com/Pvidal4/Chatbot-Big-Five-GPT-3.git
```

### Pre-requisitos 📋

```
> pip install --upgrade pip
> pip install -r requirements.txt
```

Ingresa tu API Key de OpenAI en **interfaz-gpt.py**
```
# Key (Introduce tu GPT API Key)
key = "[introduce tu api key aquí]"
```

Ingresa tu Export de WhatsApp en la carpeta **/chats**
- **Español** > Chat de WhatsApp con [nombre]
- **Inglés** > WhatsApp Chat with [nombre]

## Despliegue 📦

_Desde el directorio del proyecto_

```
>  python scripts/main.py
```

## Construido con 🛠️

* [Keras](https://keras.io/) 
* [OpenAI API](https://openai.com/blog/openai-api)
* [spanishconjugator](https://pypi.org/project/spanishconjugator/)

## Autor ✒️

* **Pedro Vidal** - [Pvidal4](https://github.com/Pvidal4)
