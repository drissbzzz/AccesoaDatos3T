import customtkinter as ctk
from tkinter import ttk
from services import incidencia_service
from tkinter import messagebox

color_boton = "#FF6B00"
color_hover = "#FF8C00"
color_fondo = "#1a1a1a"


class Incidencias(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Incidencias")
        self.resizable(False, False)
        self.configure(fg_color=color_fondo)
        ancho, alto = 1300, 650
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.construir_ui()

    def construir_ui(self):
        #Dos columnas 2/3 izquierda, 1/3 derecha
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Columna izquierda
        frame_izq = ctk.CTkFrame(self, fg_color=color_fondo, corner_radius=0)
        frame_izq.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        frame_izq.grid_rowconfigure(1, weight=1)
        frame_izq.grid_columnconfigure(0, weight=1)

        #Filtros
        frame_filtros = ctk.CTkFrame(frame_izq, fg_color="#2a2a2a", corner_radius=8)
        frame_filtros.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        #Titulo de filtros
        filtros_label = ctk.CTkLabel(frame_filtros, text="Filtros", font=ctk.CTkFont(size=13, weight="bold"))
        filtros_label.grid(row=0, column=0, columnspan=6, padx=10, pady=(8, 4), sticky="w")
        #Elementos de filtros
        #Activo ID
        activo_label = ctk.CTkLabel(frame_filtros, text="Activo ID:")
        activo_label.grid(row=1, column=0, padx=(10, 4), pady=8)
        self.entry_filtro_activo = ctk.CTkEntry(frame_filtros, width=80)
        self.entry_filtro_activo.grid(row=1, column=1, padx=(0, 10), pady=8)
        #Prioridad
        prioridad_label = ctk.CTkLabel(frame_filtros, text="Prioridad:")
        prioridad_label.grid(row=1, column=2, padx=(0, 4), pady=8)
        self.combo_filtro_prioridad = ctk.CTkComboBox(frame_filtros, width=140,values=["Todos", "Alta", "Media", "Baja"])
        self.combo_filtro_prioridad.set("Todos")
        self.combo_filtro_prioridad.grid(row=1, column=3, padx=(0, 10), pady=8)
        #Estado
        estado_label = ctk.CTkLabel(frame_filtros, text="Estado:")
        estado_label.grid(row=1, column=4, padx=(0, 4), pady=8)
        self.combo_filtro_estado = ctk.CTkComboBox(frame_filtros, width=140,values=["Todos", "En espera", "Resolviendo","Resuelta", "Cerrada"])
        self.combo_filtro_estado.set("Todos")
        self.combo_filtro_estado.grid(row=1, column=5, padx=(0, 10), pady=8)
        #Boton Buscar
        btn_buscar = ctk.CTkButton(frame_filtros, text="Buscar", width=80,fg_color=color_boton, hover_color=color_hover,command=self.buscar)
        btn_buscar.grid(row=1, column=6, padx=10, pady=8)
        #Boton para quitar todos los filtros
        btn_limpiar = ctk.CTkButton(frame_filtros, text="Limpiar", width=80,fg_color=color_boton, hover_color=color_hover,command=self.limpiar_filtros)
        btn_limpiar.grid(row=1, column=7, padx=(0, 10), pady=8)

        #Tabla
        frame_tabla = ctk.CTkFrame(frame_izq, fg_color="#2a2a2a", corner_radius=8)
        frame_tabla.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        #Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam") #Para poder personalizar la tabla
        style.configure("Treeview", #Personalizacion de todos los elementos de la tabla
                         background="#2a2a2a",
                         foreground="white",
                         fieldbackground="#2a2a2a",
                         rowheight=28,
                         font=("Arial", 9))
        style.configure("Treeview.Heading", #Personalización de los titulos
                         background=color_boton,
                         foreground="white",
                         font=("Arial", 9, "bold"))
        style.map("Treeview", background=[("selected", color_hover)]) #Si seleccionas un elemento, cambia el color de fondo
        columnas = ("ID", "Activo ID", "Fecha Apertura", "Prioridad",
                    "Categoría", "Descripción", "Estado", "Técnico")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,
                                   show="headings", selectmode="browse")

        #Cabeceras y anchos de la tabla
        anchos = [40, 70, 110, 80, 90, 180, 90, 110] #con esto le asignamos anchos a cada columna de la tabla
        for col, ancho in zip(columnas, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        #Scrollbar para navegar verticalmente en la tabla
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        #Al seleccionar una fila se rellena el formulario
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila) #Bind hace que cuando se selecciona algo en el tree view se llama al metodo seleccionar fila

        #Log
        frame_log = ctk.CTkFrame(frame_izq, fg_color="#2a2a2a", corner_radius=8)
        frame_log.grid(row=2, column=0, sticky="ew")
        frame_log.grid_columnconfigure(0, weight=1)
        log_label = ctk.CTkLabel(frame_log, text="Ultimo evento:", font=ctk.CTkFont(size=11))
        log_label.grid(row=0, column=0, padx=10, pady=(6, 0), sticky="w")
        self.texto_log = ctk.CTkLabel(frame_log, text="", font=ctk.CTkFont(size=11), text_color="#aaaaaa")
        self.texto_log.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="w")

        #Columna derecha
        frame_der = ctk.CTkFrame(self, fg_color="#2a2a2a", corner_radius=8)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        frame_der.grid_columnconfigure(0, weight=1)
        frame_der.grid_columnconfigure(1, weight=1)
        form_label = ctk.CTkLabel(frame_der, text="Formulario", font=ctk.CTkFont(size=14, weight="bold"))
        form_label.grid(row=0, column=0, columnspan=2, pady=(15, 10))

        #Campos del formulario
        campos = ["Activo ID", "Prioridad", "Categoría", "Descripción", "Técnico", "Estado"]
        self.entries = {}
        #Creamos un bucle para hacer cada elemento automaticamente (para no crear uno por uno)
        for i, campo in enumerate(campos):
            #Label de cada campo
            label = ctk.CTkLabel(frame_der, text=f"{campo}:")
            label.grid(row=i+1, column=0, padx=(15, 5), pady=5, sticky="e")
            if campo == "Prioridad": #En caso de que sea el campo de Prioridad, hacemos un combobox con las opciones
                elemento = ctk.CTkComboBox(frame_der, width=160, values=["Alta", "Media", "Baja"])
            elif campo == "Categoría": #En caso de que sea el campo de Categoría, hacemos un combobox con las opciones
                elemento = ctk.CTkComboBox(frame_der, width=160, values=["Hardware", "Software"])
            elif campo == "Estado": #En caso de que sea el campo de Estado, hacemos un combobox con las opciones
                elemento = ctk.CTkComboBox(frame_der, width=160,values=["En espera", "Resolviendo", "Resuelta"])
            else:
                #Un entry para los campos que sean de texto libre
                elemento = ctk.CTkEntry(frame_der, width=160)
            #Añadimos el elemento en cuestion al lado del label
            elemento.grid(row=i+1, column=1, padx=(0, 15), pady=5, sticky="w")
            self.entries[campo] = elemento #Guardamos en el diccionario entries para manipularlo de manera sencilla en el futuro

        #Botones CRUD
        frame_crud = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_crud.grid(row=len(campos)+1, column=0, columnspan=2, pady=(15, 5)) #Añadimos el frame de los botones justo al final debajo del ultimo campo

        btn_crear = ctk.CTkButton(frame_crud, text="Crear", width=100,fg_color=color_boton, hover_color=color_hover,command=self.crear)
        btn_crear.grid(row=0, column=0, padx=5)
        btn_cambiar = ctk.CTkButton(frame_crud, text="Cambiar Estado", width=130,fg_color=color_boton, hover_color=color_hover,command=self.cambiar_estado)
        btn_cambiar.grid(row=0, column=1, padx=5)
        btn_eliminar = ctk.CTkButton(frame_crud, text="Eliminar", width=100,fg_color=color_boton, hover_color=color_hover,command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=5)

        #Boton exportar (incidencias solo exporta a JSON)
        frame_export = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_export.grid(row=len(campos)+2, column=0, columnspan=2, pady=(5, 15)) #Añadimos el frame del boton justo debajo de los otros
        btn_exportar = ctk.CTkButton(frame_export, text="Exportar JSON", width=200,fg_color=color_boton, hover_color=color_hover,command=self.exportar)
        btn_exportar.grid(row=0, column=0, padx=5)

        #Cargar datos de la tabla al abrir la interfaz
        self.cargar_tabla()

    #Metodos
    def actualizar_log(self, mensaje):
        self.texto_log.configure(text=mensaje)

    def limpiar_formulario(self):
        for campo, elemento in self.entries.items():
            if isinstance(elemento, ctk.CTkEntry): #si el elemento del entries, es un entry borra el texto
                elemento.delete(0, "end")
            else:
                elemento.set("") #si no es un entry, pone un valor vacio en el combobox

    def seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        valores = self.tabla.item(seleccion[0])["values"]
        #Asignamos por posición exacta
        #valores = (id=0, activo_id=1, fecha=2, prioridad=3, categoria=4, descripcion=5, estado=6, tecnico=7)
        self.entries["Activo ID"].delete(0, "end")
        self.entries["Activo ID"].insert(0, str(valores[1]))
        self.entries["Prioridad"].set(str(valores[3]))
        self.entries["Categoría"].set(str(valores[4]))
        self.entries["Descripción"].delete(0, "end")
        self.entries["Descripción"].insert(0, str(valores[5]))
        self.entries["Estado"].set(str(valores[6]))
        self.entries["Técnico"].delete(0, "end")
        self.entries["Técnico"].insert(0, str(valores[7]))

    def cargar_tabla(self, incidencias=None):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila) #Borramos cada elemento antes de rellenar para no duplicarlo
        if incidencias is None: #Si no le pasamos ninguna lista filtrada, le pasamos todas las incidencias
            incidencias = incidencia_service.obtener_incidencias()
        for i in incidencias: #Insertamos cada incidencia
            self.tabla.insert("", "end", values=(
                i.id, i.activo_id, i.fecha_apertura, i.prioridad,
                i.categoria, i.descripcion, i.estado, i.tecnico
            ))

    def buscar(self):
        activo_filtro = self.entry_filtro_activo.get()
        prioridad_filtro = self.combo_filtro_prioridad.get()
        estado_filtro = self.combo_filtro_estado.get()
        todas = incidencia_service.obtener_incidencias()
        incidencias = []
        for i in todas:
            #Comprobar filtro activo ID
            if activo_filtro and str(i.activo_id) != activo_filtro:
                continue
            #Comprobar filtro prioridad
            if prioridad_filtro != "Todos" and i.prioridad != prioridad_filtro:
                continue
            #Comprobar filtro estado
            if estado_filtro != "Todos" and i.estado != estado_filtro:
                continue
            incidencias.append(i) #Si pasa por todos los filtros, se añade a la lista que se mandara a la tabla
        self.cargar_tabla(incidencias)
        self.actualizar_log(f"{len(incidencias)} incidencias encontradas")

    def limpiar_filtros(self): #Limpiamos los filtros
        self.entry_filtro_activo.delete(0, "end")
        self.combo_filtro_prioridad.set("Todos")
        self.combo_filtro_estado.set("Todos")
        self.cargar_tabla() #Cargamos la tabla entera de nuevo

    def crear(self):
        try:
            #Recoger datos del formulario para crear la nueva incidencia
            activo_id = self.entries["Activo ID"].get()
            prioridad = self.entries["Prioridad"].get()
            categoria = self.entries["Categoría"].get()
            descripcion = self.entries["Descripción"].get()
            tecnico = self.entries["Técnico"].get()
            #Llamamos al service con los datos pasados por parámetro
            incidencia_service.crear_incidencia(activo_id, prioridad, categoria, descripcion, tecnico)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Incidencia creada correctamente para activo {activo_id}")
        except ValueError as e:
            self.actualizar_log(f"{e}")
        except Exception as e: #Manejamos errores aparte del value error que definimos antes
            self.actualizar_log(f"Error inesperado: {e}")

    def cambiar_estado(self):
        try:
            #Verificar que hay una fila seleccionada
            seleccion = self.tabla.selection()
            if not seleccion:
                self.actualizar_log("Selecciona una incidencia para cambiar el estado")
                return
            #Obtener el ID de la fila seleccionada
            id_incidencia = self.tabla.item(seleccion[0])["values"][0]
            #Recoger el nuevo estado del formulario
            estado = self.entries["Estado"].get()
            #Llamar al service
            incidencia_service.cambiar_estado(estado, id_incidencia)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Incidencia {id_incidencia} actualizada a '{estado}'")
        except ValueError as e:
            self.actualizar_log(f"{e}")
        except Exception as e: #Manejamos errores aparte del value error que definimos antes
            self.actualizar_log(f"Error inesperado: {e}")

    def eliminar(self):
        try:
            #Verificar que hay una fila seleccionada
            seleccion = self.tabla.selection()
            if not seleccion:
                self.actualizar_log("Selecciona una incidencia para eliminar")
                return
            #Obtener id para el mensaje
            id_incidencia = self.tabla.item(seleccion[0])["values"][0]
            #Confirmación antes de eliminar
            confirmar = messagebox.askyesno("Confirmar eliminación",f"¿Estás seguro de que quieres eliminar la incidencia {id_incidencia}?")
            if not confirmar: #Si se da a que no, se termina el método
                return
            #Llamar al service
            incidencia_service.eliminar_incidencia(id_incidencia)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Incidencia {id_incidencia} eliminada correctamente")
        except Exception as e:
            self.actualizar_log(f"{e}")

    def exportar(self):
        pass