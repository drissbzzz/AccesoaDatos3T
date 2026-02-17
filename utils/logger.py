from datetime import datetime
from utils.config import config

ruta = config["ruta_log"]


def registrar_info(mensaje):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Obtiene la fecha y hora y le da formato
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"[{hora}] INFO - {mensaje}\n")

def registrar_error(mensaje):
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(f"[{hora}] ERROR - {mensaje}\n")
