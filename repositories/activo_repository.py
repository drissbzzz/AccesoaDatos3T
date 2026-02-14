from db.database import obtener_conexion
from model.activo import Activo


def insertar_activo(activo): #Inserción de un nuevo activo en la tabla
    conexion = obtener_conexion()  # abre la conexión
    cursor = conexion.cursor() # crear el cursor
    cursor.execute("""INSERT INTO activos (codigo, tipo, marca, modelo, 
                             n_serie, ubicacion, fecha_alta, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (
        activo.codigo,
        activo.tipo,
        activo.marca,
        activo.modelo,
        activo.n_serie,
        activo.ubicacion,
        activo.fecha_alta,
        activo.estado)) #Inserta los valores en orden en los "?"

    conexion.commit() #confirma los cambios
    conexion.close() #cierra la consulta

def obtener_todos(): #Devuelve todos los activos en una lista
    conexion = obtener_conexion() #Abre conexion
    cursor = conexion.cursor() #Crea el cursor
    cursor.execute("SELECT * FROM activos") #Consulta de todos los activos

    filas = cursor.fetchall()   #Lista de tuplas de SQLite
    conexion.close()            #Cerramos la conexión
    activos = []
    for fila in filas:
        activo = Activo( #Convertimos cada tupla en un objeto Activo
            id=fila[0],
            codigo=fila[1],
            tipo=fila[2],
            marca=fila[3],
            modelo=fila[4],
            n_serie=fila[5],
            ubicacion=fila[6],
            fecha_alta=fila[7],
            estado=fila[8]
        )
        activos.append(activo)
    return activos

def buscar_por_id(id_activo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
                    SELECT * FROM activos                 
                    WHERE id=?
                """, ( id_activo,))  # Inserta los valores en orden en los "?"
    fila = cursor.fetchone()
    conexion.close()  #cierra la consulta
    if fila is None:  #en caso de no encontrar nada
        return None
    activo = Activo( #Almacenamos el activo obtenido en un objeto Activo
        id=fila[0],
        codigo=fila[1],
        tipo=fila[2],
        marca=fila[3],
        modelo=fila[4],
        n_serie=fila[5],
        ubicacion=fila[6],
        fecha_alta=fila[7],
        estado=fila[8]
    )
    return activo

def actualizar(activo):
    conexion = obtener_conexion()  # abre la conexión
    cursor = conexion.cursor()  # crear el cursor
    cursor.execute("""
            UPDATE activos 
            SET codigo=?, tipo=?, marca=?, modelo=?,
                n_serie=?, ubicacion=?, fecha_alta=?, estado=?
            WHERE id=?
        """, (
        activo.codigo,
        activo.tipo,
        activo.marca,
        activo.modelo,
        activo.n_serie,
        activo.ubicacion,
        activo.fecha_alta,
        activo.estado,
        activo.id
    ))  # Inserta los valores en orden en los "?"
    conexion.commit()  # confirma los cambios
    conexion.close()  # cierra la consulta

def eliminar(id_activo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()  # crear el cursor
    cursor.execute("""
                DELETE FROM activos                 
                WHERE id=?
            """, ( id_activo,))  # Inserta los valores en orden en los "?"
    conexion.commit()  # confirma los cambios
    conexion.close()  # cierra la consulta