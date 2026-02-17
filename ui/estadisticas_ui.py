import customtkinter as ctk
from tkinter import ttk

from repositories import incidencia_repository
from utils.config import config

color_boton = config["color_boton"]
color_hover = config["color_hover"]
color_fondo = config["color_fondo"]


class Estadisticas(ctk.CTkToplevel):

    def __init__(self, parent, rol):
        super().__init__(parent)
        self.rol = rol
        self.title("Estadísticas")
        self.resizable(False, False)
        self.configure(fg_color=color_fondo)
        ancho, alto = 900, 600
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.construir_ui()

    def construir_ui(self):
        #Título principal
        titulo_label = ctk.CTkLabel(self, text="Estadísticas",font=ctk.CTkFont(size=20, weight="bold"))
        titulo_label.pack(pady=20)

        #Contenedor principal para las tres tablas
        frame_principal = ctk.CTkFrame(self, fg_color=color_fondo)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        frame_principal.grid_rowconfigure(0, weight=1)
        frame_principal.grid_rowconfigure(1, weight=1)
        frame_principal.grid_rowconfigure(2, weight=1)
        frame_principal.grid_columnconfigure(0, weight=1)

        #Incidencias por estado
        frame_estados = ctk.CTkFrame(frame_principal, fg_color="#2a2a2a", corner_radius=8)
        frame_estados.grid(row=0, column=0, sticky="nsew", pady=5)
        titulo_estados = ctk.CTkLabel(frame_estados, text="Incidencias por Estado", font=ctk.CTkFont(size=14, weight="bold"))
        titulo_estados.pack(pady=(10, 5))
        #Estilo de tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Stats.Treeview",
                        background="#2a2a2a",
                        foreground="white",
                        fieldbackground="#2a2a2a",
                        rowheight=25,
                        font=("Arial", 10))
        style.configure("Stats.Treeview.Heading",
                        background=color_boton,
                        foreground="white",
                        font=("Arial", 10, "bold"))
        style.map("Stats.Treeview", background=[("selected", color_hover)])
        columnas_estado = ("Estado", "Cantidad")
        self.tabla_estados = ttk.Treeview(frame_estados, columns=columnas_estado,show="headings", height=4, style="Stats.Treeview")
        #Cabeceras y anchos
        for col in columnas_estado:
            self.tabla_estados.heading(col, text=col)
            self.tabla_estados.column(col, width=200, anchor="center")
        self.tabla_estados.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        #Incidencias por categoría
        frame_categorias = ctk.CTkFrame(frame_principal, fg_color="#2a2a2a", corner_radius=8)
        frame_categorias.grid(row=1, column=0, sticky="nsew", pady=5)
        titulo_categorias = ctk.CTkLabel(frame_categorias, text="Incidencias por Categoría",font=ctk.CTkFont(size=14, weight="bold"))
        titulo_categorias.pack(pady=(10, 5))
        columnas_categoria = ("Categoría", "Cantidad")
        self.tabla_categorias = ttk.Treeview(frame_categorias, columns=columnas_categoria,show="headings", height=4, style="Stats.Treeview")
        #Cabeceras y anchos
        for col in columnas_categoria:
            self.tabla_categorias.heading(col, text=col)
            self.tabla_categorias.column(col, width=200, anchor="center")
        self.tabla_categorias.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        #Activos con más incidencias
        frame_activos = ctk.CTkFrame(frame_principal, fg_color="#2a2a2a", corner_radius=8)
        frame_activos.grid(row=2, column=0, sticky="nsew", pady=5)
        titulo_activos = ctk.CTkLabel(frame_activos, text="Activos con Más Incidencias",font=ctk.CTkFont(size=14, weight="bold"))
        titulo_activos.pack(pady=(10, 5))
        columnas_activos = ("Activo ID", "Código", "Incidencias")
        self.tabla_activos = ttk.Treeview(frame_activos, columns=columnas_activos,show="headings", height=4, style="Stats.Treeview")
        #Cabeceras y anchos
        anchos_activos = [100, 150, 100]
        for col, ancho in zip(columnas_activos, anchos_activos):
            self.tabla_activos.heading(col, text=col)
            self.tabla_activos.column(col, width=ancho, anchor="center")
        self.tabla_activos.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        #Botón para actualizar tabla
        btn_act = ctk.CTkButton(self, text="Actualizar",fg_color=color_boton, hover_color=color_hover,command=self.cargar_datos)
        btn_act.pack(pady=(0, 20))

        #Cargar datos al abrir la ventana
        self.cargar_datos()

    def crear_tabla(self, parent, titulo, columnas, fila):
        frame = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=8)
        frame.grid(row=fila, column=0, sticky="nsew", pady=10)
        parent.grid_rowconfigure(fila, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        #Título
        ctk.CTkLabel(frame, text=titulo,
                     font=ctk.CTkFont(size=14, weight="bold")
                     ).pack(pady=(10, 5))

        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Stats.Treeview",
                         background="#2a2a2a",
                         foreground="white",
                         fieldbackground="#2a2a2a",
                         rowheight=25,
                         font=("Arial", 10))
        style.configure("Stats.Treeview.Heading",
                         background=color_boton,
                         foreground="white",
                         font=("Arial", 10, "bold"))
        style.map("Stats.Treeview", background=[("selected", color_hover)])

        # Tabla
        tabla = ttk.Treeview(frame, columns=columnas, show="headings",
                             height=5, style="Stats.Treeview")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=150, anchor="center")

        tabla.pack(padx=10, pady=(0, 10), fill="both", expand=True)

        # Guardar referencia según el título
        if "Estado" in titulo:
            self.tabla_estados = tabla
        elif "Categoría" in titulo:
            self.tabla_categorias = tabla
        else:
            self.tabla_activos = tabla

    def cargar_datos(self):
        #Carga los datos en las tres tablas de estadísticas
        for tabla in [self.tabla_estados, self.tabla_categorias, self.tabla_activos]:
            for fila in tabla.get_children():
                tabla.delete(fila) #Limpiar tablas antes de recargar
        #Cargar datos de incidencias por estado
        datos_estado = incidencia_repository.contar_por_estado()
        for estado, cantidad in datos_estado:
            self.tabla_estados.insert("", "end", values=(estado, cantidad))
        #Cargar datos de incidencias por categoría
        datos_categoria = incidencia_repository.contar_por_categoria()
        for categoria, cantidad in datos_categoria:
            self.tabla_categorias.insert("", "end", values=(categoria, cantidad))
        #Cargar datos de activos con más incidencias
        datos_activos = incidencia_repository.activos_con_mas_incidencias()
        for activo_id, codigo, cantidad in datos_activos:
            self.tabla_activos.insert("", "end", values=(activo_id, codigo, cantidad))
