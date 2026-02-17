import customtkinter as ctk

from utils.config import config

#Configuración global de apariencia
color_boton = config["color_boton"]
color_hover = config["color_hover"]
color_fondo = config["color_fondo"]

class Home(ctk.CTkToplevel):
    def __init__(self, parent, rol):
        super().__init__(parent)
        self.rol = rol
        self.title("Gestión de Activos e Incidencias")
        self.update_idletasks()  #Obtener dimensiones reales para centrar contenido
        ancho_ventana = 600
        alto_ventana = 350
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.geometry(f"600x350+{x}+{y}")
        self.resizable(False, False)
        self.configure(fg_color=color_fondo)
        self.construir_ui()

    def construir_ui(self):
        #Preparo dos divisiones de la pantalla: un tercio para la columna de opciones y otras dos para el logo
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        #Menú
        menu = ctk.CTkFrame(self, fg_color=color_hover, corner_radius=0)
        menu.grid(row=0, column=0, sticky="nsew")
        #Configuración de los tamaños y ubicaciones
        self.grid_rowconfigure(0, weight=1)
        menu.grid_rowconfigure(0, weight=1)
        menu.grid_rowconfigure(4, weight=1)
        menu.grid_columnconfigure(0, weight=1)
        #Botones
        btnActivos = ctk.CTkButton(menu, text="Activos", fg_color=color_hover, hover_color=color_boton, command=self.activos)
        btnActivos.grid(row=1, column=0, padx=8)
        btnIncidencias = ctk.CTkButton(menu, text="Incidencias", fg_color=color_hover,hover_color=color_boton, command=self.incidencias)
        btnIncidencias.grid(row=2, column=0)
        btnEstadisticas = ctk.CTkButton(menu, text="Estadísticas", fg_color=color_hover,hover_color=color_boton, command=self.estadisticas)
        btnEstadisticas.grid(row=3, column=0)
        btnSalir = ctk.CTkButton(menu, text="Salir", fg_color=color_hover,hover_color=color_boton, command=self.login)
        btnSalir.grid(row=5, column=0)
        #División de la derecha
        contenido = ctk.CTkFrame(self, fg_color=color_fondo, corner_radius=0)
        contenido.grid(row=0, column=1, sticky="nsew")
        contenido.grid_rowconfigure(0, weight=1)
        contenido.grid_columnconfigure(0, weight=1)
        self.logo = ctk.CTkImage(light_image=__import__("PIL").Image.open("ui/images/home.png"),size=(400, 300))
        ctk.CTkLabel(contenido, image=self.logo, text="").grid(row=0, column=0)

    def login(self):
        self.destroy()

    def activos(self):
        from ui.activos_ui import Activos
        app = Activos(self, self.rol)
        app.grab_set()

    def incidencias(self):
        from ui.incidencias_ui import Incidencias
        app = Incidencias(self, self.rol)
        app.grab_set()

    def estadisticas(self):
        from ui.estadisticas_ui import Estadisticas
        app = Estadisticas(self, self.rol)
        app.grab_set()
