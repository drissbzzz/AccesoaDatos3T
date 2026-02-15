from db.database import iniciar_BDD, obtener_conexion
from ui.login_ui import LoginWindow

if __name__ == "__main__":
    # Inicializar la base de datos al arrancar
    conexion = obtener_conexion()
    iniciar_BDD(conexion)
    # Arrancar la aplicación
    app = LoginWindow()
    app.mainloop()