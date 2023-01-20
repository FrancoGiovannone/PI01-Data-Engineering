
#Importación de las librerias
from fastapi import FastAPI

import pandas as pd

#Creo la app
app = FastAPI(title = "PI Data Engineering")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}



#Consulta 1: Cantidad de veces que aparece una keyword en el título de peliculas/series, por plataforma.
@app.get("/get_word_count")
def get_word_count(plat: str, keyword: str):
    df = pd.read_csv("data_total.csv")
    titulos_partidos = []
    cantidad = 0
    for titulo in df["title"][df["plataforma"] == plat]:
        titulos_partidos.append(titulo.split(" "))
    for i in titulos_partidos:
        if keyword in i:
            cantidad+=1
    return {"plataforma":plat,
              "cantidad": cantidad}


#Consulta 2: Cantidad de películas por plataforma con un puntaje mayor a XX en determinado año.
@app.get("/get_score_count")
def get_score_count(plat: str, puntaje: int, anio: int):
    df = pd.read_csv("data_total.csv")
    consulta = df[(df["plataforma"]== plat) & (df["release_year"] == anio) & (df["score"] > puntaje) & (df["duration_type"] == "min")]
   
    return {"plataforma": plat,
    "cantidad": consulta.shape[0]}

#Consulta 3: La segunda película con mayor score para una plataforma determinada, según el orden alfabético de los títulos.
@app.get("/get_second_score")
def get_second_score(plat: str):
    df = pd.read_csv("data_total.csv")
    consulta = df[(df["plataforma"] == plat) & (df["duration_type"] == "min")]
    consulta_ordenada = consulta.sort_values(["score","title"], ascending = (False, True))
    
    return {"title":list(consulta_ordenada["title"])[1],
            "score":list(consulta_ordenada["score"])[1]}

#Consulta 4: Película que más duró según año, plataforma y tipo de duración.
@app.get("/get_longest")
def get_longest(plat: str, durtype: str, anio: int):
    df = pd.read_csv("data_total.csv")
    mas_larga = df[(df["release_year"] == anio) & (df["plataforma"] == plat) & (df["duration_type"] == durtype)]
    mas_larga = mas_larga.sort_values("duration_int", ascending = False ).head(1)
    pelicula = list(mas_larga["title"])[0]
    duracion = list(mas_larga["duration_int"])[0]
    
    return {"title": pelicula, 
         "duration": duracion,
    "duration_type": durtype}


#Consulta 5: Cantidad de series y películas por rating.
@app.get("/get_rating_count")
def get_rating_count(rating: str):
    df = pd.read_csv("data_total.csv")
    consulta = df[df["rating"] == rating]
    cantidad = consulta.shape[0]

    return {"rating": rating,
            "catidad":cantidad}