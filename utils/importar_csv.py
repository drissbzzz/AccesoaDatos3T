import csv
from model.activo import Activo
from utils.logger import registrar_info, registrar_error


def importar_activos_csv(ruta):
    activos = []
    errores = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)  #Lee el CSV como diccionarios usando la cabecera 
            for i, fila in enumerate(lector, start=2):  #Empieza en la fila 2 porque la fila 1 es la cabecera
                try:
                    #Crear objeto Activo usando la fila i
                    activo = Activo(
                        codigo=fila["Código"].strip(),
                        tipo=fila["Tipo"].strip(),
                        marca=fila["Marca"].strip(),
                        modelo=fila["Modelo"].strip(),
                        n_serie=fila["Nº Serie"].strip(),
                        ubicacion=fila["Ubicación"].strip(),
                        estado=fila["Estado"].strip()
                        #Tenemos puesto que fecha_alta se genere automáticamente
                        #El id lo asigna SQLito
                    )
                    activos.append(activo)
                except KeyError as e:
                    errores.append(f"Fila {i}: Falta la columna {e}")
                except Exception as e:
                    errores.append(f"Fila {i}: {e}")
        registrar_info(f"Preparados para importar correctamente: {len(activos)} | Teniendo {len(errores)} errores")
        return activos, errores
    except FileNotFoundError:
        registrar_error(f"Archivo no encontrado: {ruta}")
        return [], ["Archivo no encontrado"]
    except Exception as e:
        registrar_error(f"Error al importar CSV: {e}")
        return [], [f"Error al leer el archivo: {e}"]