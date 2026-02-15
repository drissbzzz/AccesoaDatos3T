from db.database import obtener_conexion
from model.incidencia import Incidencia


def insertar_incidencia(incidencia): #Inserción de una nueva incidencia en la tabla
    conexion = obtener_conexion()  # abre la conexión
    cursor = conexion.cursor() # crear el cursor
    cursor.execute("""INSERT INTO incidencias (activo_id, prioridad, categoria, 
                    descripcion, tecnico, fecha_apertura, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (
        incidencia.activo_id,
        incidencia.prioridad,
        incidencia.categoria,
        incidencia.descripcion,
        incidencia.tecnico,
        incidencia.fecha_apertura,
        incidencia.estado)) #Inserta los valores en orden en los "?"

    conexion.commit() #confirma los cambios
    conexion.close() #cierra la consulta

def obtener_todos(): #Devuelve todas las incidencias en una lista
    conexion = obtener_conexion() #Abre conexion
    cursor = conexion.cursor() #Crea el cursor
    cursor.execute("SELECT * FROM incidencias") #Consulta de todos las incidencias

    filas = cursor.fetchall()   #Lista de tuplas de SQLite
    conexion.close()            #Cerramos la conexión
    incidencias = []
    for fila in filas:
        incidencia = Incidencia( #Convertimos cada tupla en un objeto Incidencia
            id=fila[0],
            activo_id=fila[1],
            fecha_apertura=fila[2],
            prioridad=fila[3],
            categoria=fila[4],
            descripcion=fila[5],
            estado=fila[6],
            tecnico=fila[7],
        )
        incidencias.append(incidencia)
    return incidencias

def buscar_por_id(id_incidencia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
                    SELECT * FROM incidencias                 
                    WHERE id=?
                """, ( id_incidencia,))  # Inserta los valores en orden en los "?"
    fila = cursor.fetchone()
    conexion.close()  #cierra la consulta
    if fila is None:  #en caso de no encontrar nada
        return None
    incidencia = Incidencia( #Almacenamos en un objeto Incidencia
            id=fila[0],
            activo_id=fila[1],
            fecha_apertura=fila[2],
            prioridad=fila[3],
            categoria=fila[4],
            descripcion=fila[5],
            estado=fila[6],
            tecnico=fila[7],
        )
    return incidencia

def buscar_por_estado(estado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
                        SELECT * FROM incidencias                 
                        WHERE estado=?
                    """, (estado,))  # Inserta los valores en orden en los "?"
    filas = cursor.fetchall()
    conexion.close()  # cierra la consulta
    if filas is None:  # en caso de no encontrar nada
        return None
    incidencias = []
    for fila in filas:
        incidencia = Incidencia(  # Convertimos cada tupla en un objeto Incidencia
            id=fila[0],
            activo_id=fila[1],
            fecha_apertura=fila[2],
            prioridad=fila[3],
            categoria=fila[4],
            descripcion=fila[5],
            estado=fila[6],
            tecnico=fila[7],
        )
        incidencias.append(incidencia)
    return incidencias

def eliminar(id_incidencia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM incidencias WHERE id=?", (id_incidencia,))
    conexion.commit()
    conexion.close()

def actualizar_estado(estado, id_incidencia): #Cambia el estado de una incidencia
    conexion = obtener_conexion()  # abre la conexión
    cursor = conexion.cursor()  # crear el cursor
    cursor.execute("""
            UPDATE incidencias 
            SET estado=?
            WHERE id=?
        """, (
        estado,
        id_incidencia
    ))  # Inserta los valores en orden en los "?"
    conexion.commit()  # confirma los cambios
    conexion.close()  # cierra la consulta
