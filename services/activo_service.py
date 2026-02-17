import re
from model.activo import Activo
from repositories import activo_repository
from datetime import datetime

def crear_activo(codigo, tipo, marca, modelo, n_serie, ubicacion, estado):
    #Validar que todos los campos estén rellenos
    campos = [codigo, tipo, marca, modelo, n_serie, ubicacion, estado]
    if not all(campos):  #all() devuelve True si todos los elementos son distintos de vacío
        raise ValueError("Error: Todos los campos son obligatorios") #Lanzamos el error de valor para poder manejarlo con la UI
    #Validar formato del código ACT-XXXX
    patronCod=r"^ACT-\d{4}$" #Mediante esta regex comprobaremos el formato del codigo
    if not (re.match(patronCod, codigo)): #Si la regex no encuentra coincidencia
        raise ValueError("Error: Formato de codigo erroneo")
    """Si todo sale bien se envia el objeto activo a repositories"""
    activo = Activo(codigo, tipo, marca, modelo, n_serie, ubicacion, estado=estado)
    activo_repository.insertar_activo(activo)
    return activo

def obtener_activos():
    return activo_repository.obtener_todos()

def obtener_activo_por_id(id_activo):
    return activo_repository.buscar_por_id(id_activo)

def actualizar_activo(id_activo, codigo, tipo, marca, modelo, n_serie, ubicacion, estado):
    campos = [codigo, tipo, marca, modelo, n_serie, ubicacion, estado]
    if not all(campos):
        raise ValueError("Error: Todos los campos son obligatorios")
    patronCod = r"^ACT-\d{4}$"
    if not re.match(patronCod, codigo):
        raise ValueError("Error: Formato de codigo erroneo")
    #Cargamos el activo original para conservar su fecha
    activo_original = activo_repository.buscar_por_id(id_activo)
    if activo_original is None:
        raise ValueError("Error: No existe el activo seleccionado")
    #Usamos la fecha original
    activo = Activo(codigo, tipo, marca, modelo, n_serie, ubicacion,fecha_alta=activo_original.fecha_alta,estado=estado, id=id_activo)
    activo_repository.actualizar(activo)
    return activo

def eliminar_activo(id_activo):
    return activo_repository.eliminar(id_activo)