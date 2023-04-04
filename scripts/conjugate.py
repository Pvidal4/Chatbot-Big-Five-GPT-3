from spanishconjugator import Conjugator

"""
conjugate.py

Interfaz: x 
Funcion: Conjuga los verbos solicitados por big_five_data.py con el propósito de obtener todas las variaciones posibles.
"""

def conjugar(verbo):

    # Estructura de datos para almacenar los resultados
    resultados = {}

    # Todos los tipos de datos
    pronombres = ['yo', 'tu', 'usted', 'nosotros', 'vosotros', 'ustedes']
    modo_condicional = ['indicative', 'conditional']
    tiempo = ['present', 'imperfect', 'preterite', 'future', 'present_perfect', 'past_anterior', 'future_perfect', 'conditional_simple']

    # Conjugar verbos con cada opcion posible
    for p in pronombres:
        for m in modo_condicional:
            for t in tiempo:

                # Conjugacion del verbo
                result = Conjugator().conjugate(verbo,t,m,p)

                # En caso que no exista conjugacion
                if result != None:
                    #print(result)

                    # Crear un diccionario con los resultados de cada verbo
                    resultados_verbo = {"tiempo": t, "modo_condicional": m, "pronombre": p, "forma": result}

                    # Verificar que no contenga un espacio (para evitar conjugaciones repetidas ej: has guardado y hubiste guardado; solo queremos obtener un guardado)
                    if " " not in result:
                        # Verificar si el verbo ya existe en los resultados
                        if verbo in resultados:
                            resultados[verbo].append(resultados_verbo)
                        else:
                            resultados[verbo] = [resultados_verbo]
    return resultados