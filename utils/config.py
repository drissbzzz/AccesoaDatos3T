import json

ruta = "config.json"

def cargar_config():
    #Lee el json y lo transforma a un diccionario
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

#Cargar configuracion al importar el script
config = cargar_config()