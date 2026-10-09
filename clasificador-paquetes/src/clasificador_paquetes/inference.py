import csv
from pathlib import Path
import joblib
from .contracts import Entrada, Salida
import pandas as pd
from pydantic import ValidationError


def leer_csv(ruta: Path) -> list[Entrada]:

    # raise NotImplementedError
    with open(ruta, "r") as f:
        data = csv.DictReader(f)
        entradas = []
        for i in data:
            try:
                entrada = Entrada(**i)
                print(entrada)
                entradas.append(entrada)
            except ValidationError:
                raise ValueError(f"Error a la hora de leer")
    return entradas

def preprocesar(entrada: Entrada) -> list[float]:
    
    peso_round = round(float(entrada.peso_kg), 1)

    return [
        peso_round,
        float(entrada.distancia_km)
    ]


def cargar_modelo(ruta: Path):
    modelo = joblib.load(ruta)
    return modelo

def predecir(entrada: Entrada, modelo) -> Salida:
    data = preprocesar(entrada)
    proba_cat = modelo.predict([data])[0]
    proba_prob = modelo.predict_proba([data])[0][1]

    return Salida(
        id_paquete = entrada.id_paquete,
        categoria= proba_cat,
        confianza= proba_prob
    )


def guardar_csv(resultados: list[Salida], ruta: Path) -> None:
    salidas = []
    for i in resultados:
        salidas.append(i.dict())
    df = pd.DataFrame(salidas)
    df.to_csv(ruta, index= False)



def ejecutar(entrada: Path, modelo: Path, salida: Path) -> None:
    data = leer_csv(entrada)
    modelo = cargar_modelo(modelo)
    resultados = []
    for i in data:
        resultados.append(predecir(i, modelo))
    guardar_csv(resultados, salida)


if __name__ == "__main__":
    ejecutar(
        Path("data/raw/paquetes.csv"),
        Path("models/modelo.joblib"),
        Path("resultados.csv"),
    )
