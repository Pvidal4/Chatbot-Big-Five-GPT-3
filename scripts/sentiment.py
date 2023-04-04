from googletrans import Translator

"""
sentiment.py (NO INCORPORADO)

Interfaz: x
Funcion: A partir de un input, calcula el porcentaje de sentimientos encontrados (positivo, negativo y neutral), y los devuelve como su magnitud.
"""

# Funcion para obtener la magnitud de los sentimientos
def getSentiment(input):

    sentiment = ""

    ### TRADUCTOR (es -> en) ### 
    translator = Translator()
    translation = translator.translate(input, src='es', dest='en')

    ### SENTIMIENTO ###
    import nltk
    from nltk.sentiment import SentimentIntensityAnalyzer

    # Comprobar si se ha instalado vader_lexicon (es una herramienta de análisis de sentimientos basada en reglas y léxico con los sentimientos expresados ​​en las redes sociales)
    try:
        # Inicializar el analizador de sentimiento
        sia = SentimentIntensityAnalyzer()
    except:
        nltk.download('vader_lexicon') # Descarga la lista de palabras de sentimiento
        # Inicializar el analizador de sentimiento
        sia = SentimentIntensityAnalyzer()

    # Calcular el sentimiento
    sentiment = sia.polarity_scores(translation.text)

    # Obtener la magnitud
    if sentiment.get("compound") > 0:
        #print("Positive")
        sentiment = "Positivo"
    elif sentiment.get("compound") == 0.0:
        #print("Neutral")
        sentiment = "Neutral"
    else:
        #print("Negative")
        sentiment = "Negativo"

    return sentiment