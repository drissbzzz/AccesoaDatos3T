import re
from model.activo import Activo
from repositories import activo_repository
from datetime import datetime

def crear_activo(codigo, tipo, marca, modelo, n_serie, ubicacion, fecha_alta, estado):
    #Validar que todos los campos estén rellenos
    campos = [codigo, tipo, marca, modelo, n_serie, ubicacion, fecha_alta, estado]
    if not all(campos):  #all() devuelve True si todos los elementos son distintos de vacío
        raise ValueError("Todos los campos son obligatorios") #Lanzamos el error de valor para poder manejarlo con la UI
    #Validar formato del código ACT-XXXX
    patronCod=r"^ACT-\d{4}$" #Mediante esta regex comprobaremos el formato del codigo
    if not (re.match(patronCod, codigo)): #Si la regex no encuentra coincidencia
        raise ValueError("Formato de codigo erroneo")
    #Validar formato de la fecha DD-MM-AAAA
    patronFecha = r"^\d{2}-\d{2}-\d{4}$"  # Mediante esta regex comprobaremos el formato de la fecha
    if not (re.match(patronFecha, fecha_alta)):  # Si la regex no encuentra coincidencia
        raise ValueError("Formato de fecha erroneo")
    """Si todo sale bien se envia el objeto activo a repositories"""
    fecha = datetime.strptime(fecha_alta, "%d-%m-%Y").date() #Pasamos de String a date para el objetivo Activo
    activo = Activo(codigo, tipo, marca, modelo, n_serie, ubicacion, fecha, estado)
    activo_repository.insertar_activo(activo)
    return activo

def obtener_activos():
    return activo_repository.obtener_todos()

def obtener_activo_por_id(id_activo):
    return activo_repository.buscar_por_id(id_activo)

def actualizar_activo(id_activo, codigo, tipo, marca, modelo, n_serie, ubicacion, fecha_alta, estado):
    #Validar que todos los campos estén rellenos
    campos = [codigo, tipo, marca, modelo, n_serie, ubicacion, fecha_alta, estado]
    if not all(campos):  #all() devuelve True si todos los elementos son distintos de vacío
        raise ValueError("Todos los campos son obligatorios") #Lanzamos el error de valor para poder manejarlo con la UI
    #Validar formato del código ACT-XXXX
    patronCod=r"^ACT-\d{4}$" #Mediante esta regex comprobaremos el formato del codigo
    if not (re.match(patronCod, codigo)): #Si la regex no encuentra coincidencia
        raise ValueError("Formato de codigo erroneo")
    #Validar formato de la fecha DD-MM-AAAA
    patronFecha = r"^\d{2}-\d{2}-\d{4}$"  # Mediante esta regex comprobaremos el formato de la fecha
    if not (re.match(patronFecha, fecha_alta)):  # Si la regex no encuentra coincidencia
        raise ValueError("Formato de fecha erroneo")
    """Si todo sale bien se envia el objeto activo a repositories"""
    fecha = datetime.strptime(fecha_alta, "%d-%m-%Y").date() #Pasamos de String a date para el objetivo Activo
    activo = Activo(codigo, tipo, marca, modelo, n_serie, ubicacion, fecha, estado, id_activo)
    activo_repository.actualizar(activo)
    return activo

def eliminar_activo(id_activo):
    return activo_repository.eliminar(id_activo)