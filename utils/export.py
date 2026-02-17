import csv
import json


def exportar_activos_csv(activos, ruta):
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            #Cabecera del CSV
            cabecera = ["ID", "Código", "Tipo", "Marca", "Modelo",
                        "Nº Serie", "Ubicación", "Fecha Alta", "Estado"]
            writer = csv.writer(archivo)
            writer.writerow(cabecera)
            #Escribir cada activo como una fila
            for a in activos:
                writer.writerow([a.id, a.codigo, a.tipo, a.marca, a.modelo,
                    a.n_serie, a.ubicacion, a.fecha_alta, a.estado])
        return True
    except Exception as e:
        return False

def exportar_incidencias_json(incidencias, ruta):
    try:
        #Convertir cada incidencia a un diccionario y volcarla
        datos = []
        for i in incidencias:
            datos.append(i.to_dict())
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        return False