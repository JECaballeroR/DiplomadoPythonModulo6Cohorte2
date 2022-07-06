"""API para el diplomado de Python de la Universidad de Córdoba"""


from fastapi import FastAPI
from typing import List
from classes import OutputModelo, InputModelo, APIModelBackEnd

# Creamos el objeto app
app = FastAPI(title="API de Machine Learning del Diplomado", version="1.0.0")
"""Objeto FastAPI usado para el deployment de la API :)"""
# Con el decorador, ponemos en el endpoint /predict la funcionalidad de la función predict_proba
# response_model=List[OutputModelo] es que puede responder una lista de instancias válidas de ModelOutput
# En la definición, le decimos que los Inputs son una lista de ModelInput.
# Así, la API recibe para hacer multiples predicciones


@app.post("/predict", response_model=List[OutputModelo])
async def predict_proba(inputs: List[InputModelo]):
    """Endpoint de predicción de la API"""
    # Creamos una lista vacía con las respuestas
    response = list()
    # Iteramos por todas las entradas que damos
    for Input in inputs:
        # Usamos nuestra Clase en el backend para predecir con nuestros inputs.
        # Esta sería la línea que cambiamos en este archivo, podemos los inputs que necesitemos.
        # Esto es, poner Input.Nombre_Atributo
        model = APIModelBackEnd(
            Input.average_monthly_hours, Input.satisfaction_level, Input.salary_level
        )
        response.append(model.predecir()[0])
    # Retorna  la lista con todas las predicciones hechas.
    return response
