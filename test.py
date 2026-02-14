# test.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.database import obtener_conexion, iniciar_BDD
from model.activo import Activo
from model.incidencia import Incidencia
from repositories import activo_repository, incidencia_repository


def separador(titulo):
    print(f"\n{'='*50}")
    print(f"  {titulo}")
    print(f"{'='*50}")


def limpiar_bd():
    """Limpia las tablas antes de cada ejecución del test"""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM incidencias")   # primero por la FK
    cursor.execute("DELETE FROM activos")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='activos'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='incidencias'")
    conexion.commit()
    conexion.close()
    print("✅ Base de datos limpiada")


def test_activos():

    # ─────────────────────────────
    # CREATE
    # ─────────────────────────────
    separador("TEST 1: Insertar activos")

    activo1 = Activo(
        codigo="ACT-0001",
        tipo="Portátil",
        marca="Dell",
        modelo="Latitude 5420",
        n_serie="SN123456",
        ubicacion="Aula 101",
        estado="Operativo"
    )
    activo2 = Activo(
        codigo="ACT-0002",
        tipo="Impresora",
        marca="HP",
        modelo="LaserJet 400",
        n_serie="SN654321",
        ubicacion="Secretaría",
        estado="Operativo"
    )

    activo_repository.insertar_activo(activo1)   # ← tu nombre exacto
    activo_repository.insertar_activo(activo2)
    print("✅ Dos activos insertados correctamente")

    # ─────────────────────────────
    # READ - obtener todos
    # ─────────────────────────────
    separador("TEST 2: Obtener todos los activos")

    activos = activo_repository.obtener_todos()
    print(f"✅ Activos encontrados: {len(activos)}")
    for a in activos:
        print(f"   → {a}")

    # ─────────────────────────────
    # READ - buscar por id
    # ─────────────────────────────
    separador("TEST 3: Buscar activo por ID")

    activo = activo_repository.buscar_por_id(1)
    if activo:
        print(f"✅ Activo encontrado: {activo}")
    else:
        print("❌ No encontrado")

    activo_inexistente = activo_repository.buscar_por_id(999)
    if activo_inexistente is None:
        print("✅ ID inexistente devuelve None correctamente")

    # ─────────────────────────────
    # UPDATE
    # ─────────────────────────────
    separador("TEST 4: Actualizar activo")

    activo.estado = "Averiado"
    activo.ubicacion = "Taller"
    activo_repository.actualizar(activo)

    activo_actualizado = activo_repository.buscar_por_id(1)
    print(f"✅ Estado actualizado: {activo_actualizado.estado}")
    print(f"✅ Ubicación actualizada: {activo_actualizado.ubicacion}")

    # ─────────────────────────────
    # DELETE
    # ─────────────────────────────
    separador("TEST 5: Eliminar activo")

    activo_repository.eliminar(2)
    activos_tras_borrar = activo_repository.obtener_todos()
    print(f"✅ Activos tras eliminar: {len(activos_tras_borrar)}")


def test_incidencias():

    # ─────────────────────────────
    # CREATE
    # ─────────────────────────────
    separador("TEST 6: Insertar incidencia")

    incidencia1 = Incidencia(
        activo_id=1,
        prioridad="Alta",
        categoria="Hardware",
        descripcion="Pantalla rota",
        tecnico="Juan Pérez"
        # estado → "En espera" por defecto
        # fecha  → date.today() por defecto
    )

    incidencia_repository.insertar_incidencia(incidencia1)  # ← tu nombre exacto
    print(f"✅ Incidencia insertada con estado: {incidencia1.estado}")
    print(f"✅ Fecha generada automáticamente: {incidencia1.fecha_apertura}")

    # ─────────────────────────────
    # READ - obtener todas
    # ─────────────────────────────
    separador("TEST 7: Obtener todas las incidencias")

    incidencias = incidencia_repository.obtener_todos()
    print(f"✅ Incidencias encontradas: {len(incidencias)}")
    for i in incidencias:
        print(f"   → {i}")

    # ─────────────────────────────
    # READ - buscar por estado
    # ─────────────────────────────
    separador("TEST 8: Buscar por estado")

    en_espera = incidencia_repository.buscar_por_estado("En espera")
    print(f"✅ Incidencias 'En espera': {len(en_espera)}")

    # ─────────────────────────────
    # UPDATE - cambiar estado
    # ─────────────────────────────
    separador("TEST 9: Cambiar estado de incidencia")

    incidencia_repository.actualizar_estado("En proceso", 1)  # ← tu orden: estado, id
    incidencia = incidencia_repository.buscar_por_id(1)
    print(f"✅ Estado actualizado a: {incidencia.estado}")

    # ─────────────────────────────
    # FK - integridad referencial
    # ─────────────────────────────
    separador("TEST 10: Clave foránea - activo inexistente")

    try:
        incidencia_invalida = Incidencia(
            activo_id=999,        # este activo NO existe
            prioridad="Baja",
            categoria="Software",
            descripcion="Prueba FK",
            tecnico="Ana García"
        )
        incidencia_repository.insertar_incidencia(incidencia_invalida)
        print("❌ ERROR: debería haber fallado la FK")
    except Exception as e:
        print(f"✅ FK funciona correctamente, error capturado: {e}")


if __name__ == "__main__":
    separador("INICIALIZANDO BASE DE DATOS")
    conexion = obtener_conexion()
    iniciar_BDD(conexion)        # ← tu firma: recibe la conexión
    limpiar_bd()
    print("✅ Base de datos inicializada")

    test_activos()
    test_incidencias()

    separador("TODOS LOS TESTS COMPLETADOS")
