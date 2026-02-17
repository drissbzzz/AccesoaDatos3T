from model.incidencia import Incidencia
from repositories import activo_repository, incidencia_repository


def crear_incidencia(activo_id, prioridad, categoria, descripcion, tecnico):
    #Validar que todos los campos estén rellenos
    campos = [activo_id, prioridad, categoria, descripcion, tecnico]
    if not all(campos):  #all() devuelve True si todos los elementos son distintos de vacío
        raise ValueError("Error: Hay campos obligatorios por rellenar") #Lanzamos el error de valor para poder manejarlo con la UI
    #Validar que exista un activo_id existente
    if not(activo_repository.buscar_por_id(activo_id)):
        raise ValueError("Error: No existe el activo seleccionado") #Lanzamos el error de valor para poder manejarlo con la UI
    """Si todo sale bien se envia el objeto activo a repositories"""
    incidencia = Incidencia(activo_id, prioridad, categoria, descripcion, tecnico)
    incidencia_repository.insertar_incidencia(incidencia)
    return incidencia

def obtener_incidencias():
    return incidencia_repository.obtener_todos()

def obtener_incidencia_por_id(id_incidencia):
    return incidencia_repository.buscar_por_id(id_incidencia)

def cambiar_estado(estado, id_incidencia):
    if estado == "En espera" or estado == "Resolviendo" or estado == "Resuelta":
        incidencia_repository.actualizar_estado(estado, id_incidencia)
    else:
        raise ValueError("Error: El estado es inválido")  #Lanzamos el error de valor para poder manejarlo con la UI
def eliminar_incidencia(id_incidencia):
    return incidencia_repository.eliminar(id_incidencia)