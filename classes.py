from pydantic import BaseModel as BM
from pydantic import Field
from typing import Literal
import joblib
import pandas as pd


class InputModelo(BM):
    """
    Clase que define las entradas del modelo según las verá el usuario.
    """

    average_monthly_hours: int = Field(
        ge=96, le=310, description="Horas promedio mensuales trabajadas"
    )
    satisfaction_level: float = Field(ge=0, le=1)
    salary_level: Literal["high", "low", "medium"]

    class Config:
        schema_extra = {
            "example": {
                "average_monthly_hours": 201,
                "satisfaction_level": 0.69,
                "salary_level": "low",
            }
        }


class OutputModelo(BM):
    """
    Clase que define la salida del modelo según la verá el usuario.
    """

    employee_left: float = Field(ge=0, le=1)

    class Config:
        scheme_extra = {
            "example": {
                "employee_left": 0.69,
            }
        }


class APIModelBackEnd:
    def __init__(
        self,
        average_monthly_hours,
        satisfaction_level,
        salary_level,
    ):
        self.satisfaction_level = satisfaction_level
        self.average_monthly_hours = average_monthly_hours
        self.salary_level = salary_level

    def _cargar_modelo(self, model_name:str = "model ex.pkl"):
        self.model = joblib.load(model_name)

    def _preparar_datos(self):
        average_monthly_hours = self.average_monthly_hours
        satisfaction_level = self.satisfaction_level
        salary_level = self.salary_level

        salary_levels = [0] * 3

        # Crea el DataFrame en el mismo orden las columnas del X_train

        data_predict = pd.DataFrame(
            columns=[
                "average_monthly_hours",
                "satisfaction_level",
                "salary_level_high",
                "salary_level_low",
                "salary_level_medium",
            ],
            data=[[average_monthly_hours, satisfaction_level, *salary_levels]],
        )

        # Pone el 1 en la columna que debe ir el 1

        data_predict[
            [
                x
                for x in data_predict.columns
                if ((str(salary_level) in x) and (x.startswith("salary_level_")))
            ]
        ] = 1

        return data_predict

    def predecir(self, y_name="employee_left"):
        self._cargar_modelo()
        x = self._preparar_datos()
        prediction = pd.DataFrame(self.model.predict_proba(x)[:, 1]).rename(
            columns={0: y_name}
        )
        return prediction.to_dict(orient="records")
