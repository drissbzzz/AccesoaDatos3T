import sqlite3


def obtener_conexion():
    conexion = sqlite3.connect("db/inventario.db") #Buscamos conectarnos al archivo.db, si no existe; se creará automáticamente
    conexion.execute("PRAGMA foreign_keys = ON") #SQLite tiene las foreign keys desactivadas, hay que activarlas
    return conexion

def iniciar_BDD(conexion):
    cursor = conexion.cursor() #Necesitamos el cursor que señalara donde trabajamos en la base de datos
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS activos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo      TEXT    NOT NULL UNIQUE,
        tipo        TEXT    NOT NULL,
        marca       TEXT    NOT NULL,
        modelo      TEXT    NOT NULL,
        n_serie     TEXT    NOT NULL UNIQUE,
        ubicacion   TEXT    NOT NULL,
        fecha_alta  DATE    NOT NULL,
        estado      TEXT    NOT NULL
    );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidencias (
        id              INTEGER  PRIMARY KEY AUTOINCREMENT,
        activo_id       INTEGER  NOT NULL,
        fecha_apertura  DATETIME NOT NULL,
        prioridad       TEXT     NOT NULL,
        categoria       TEXT     NOT NULL,
        descripcion     TEXT     NOT NULL,
        estado          TEXT     NOT NULL,
        tecnico         TEXT     NOT NULL,
        FOREIGN KEY (activo_id) REFERENCES activos(id)
    );""")
    conexion.commit() #Confirmar operaciones
    conexion.close() #Cerrar conexion


