import customtkinter as ctk

from utils.config import config

#Configuración global de apariencia
color_boton = config["color_boton"]
color_hover = config["color_hover"]
color_fondo = config["color_fondo"]

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
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

        #Título
        ctk.CTkLabel(self, text="¡Bienvenido!",font=ctk.CTkFont(size=24, weight="bold")).place(x=20, y=20)

        #Formulario
        ctk.CTkLabel(self, text="Usuario:").place(x=20, y=100)
        self.entry_usuario = ctk.CTkEntry(self, width=200)
        self.entry_usuario.place(x=100, y=100)
        ctk.CTkLabel(self, text="Password:").place(x=20, y=140)
        self.entry_password = ctk.CTkEntry(self, width=200, show="*")
        self.entry_password.place(x=100, y=140)
        ctk.CTkLabel(self, text="Rol:").place(x=20, y=180)
        self.combo_rol = ctk.CTkComboBox(self, width=200,values=["Administrador", "Técnico"])
        self.combo_rol.place(x=100, y=180)
        #Imagen logo
        self.logo = ctk.CTkImage(light_image=__import__("PIL").Image.open("ui/images/logo.png"),size=(150, 150))
        ctk.CTkLabel(self, image=self.logo, text="" ).place(x=400, y=80)

        #Botón login
        ctk.CTkButton(self, text="Login", width=150, fg_color=color_boton, hover_color=color_hover, command=self.login).place(x=400, y=250)

    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        rol = self.combo_rol.get()
        # Usuarios
        usuarios = {
            "123": {"password": "123", "rol": "Administrador"},
            "jose": {"password": "Thepunisher", "rol": "Administrador"},
            "driss": {"password": "ramadanmubarak", "rol": "Técnico"},
            "carlos": {"password": "murcian4life", "rol": "Técnico"}
        }
        if usuario in usuarios:
            if usuarios[usuario]["password"] == password:
                if usuarios[usuario]["rol"] == rol:
                    self.abrir_home(rol)  #Abre la app según el rol
                    self.entry_password.delete(0, "end")
                    self.entry_usuario.delete(0, "end")
                    return
        #Si es incorrecto
        ctk.CTkLabel(self, text="Credenciales incorrectas",text_color="red").place(x=20, y=280)
        self.entry_password.delete(0, "end")

    def abrir_home(self, rol):
        from ui.home_ui import Home
        self.withdraw()  #oculta el login
        app = Home(self, rol)  #pasa self como padre
        self.wait_window(app)
        self.deiconify()