import customtkinter as ctk
from tkinter import ttk
from services import activo_service
from tkinter import messagebox


color_boton = "#FF6B00"
color_hover = "#FF8C00"
color_fondo = "#1a1a1a"


class Activos(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Gestión de Activos")
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
        filtros_label=ctk.CTkLabel(frame_filtros, text="Filtros",font=ctk.CTkFont(size=13, weight="bold"))
        filtros_label.grid(row=0, column=0, columnspan=6, padx=10, pady=(8, 4), sticky="w")
        #Elemntos de filtros
        #Id
        id_label = ctk.CTkLabel(frame_filtros, text="ID:")
        id_label.grid(row=1, column=0, padx=(10, 4), pady=8)
        self.entry_filtro_id = ctk.CTkEntry(frame_filtros, width=80)
        self.entry_filtro_id.grid(row=1, column=1, padx=(0, 10), pady=8)
        #Tipo
        tipo_label = ctk.CTkLabel(frame_filtros, text="Tipo:")
        tipo_label.grid(row=1, column=2, padx=(0, 4), pady=8)
        self.combo_filtro_tipo = ctk.CTkComboBox(frame_filtros, width=140,values=["PC", "Portátil", "Impresora", "Router", "Otro"])
        self.combo_filtro_tipo.set("Todos")
        self.combo_filtro_tipo.grid(row=1, column=3, padx=(0, 10), pady=8)
        #Estado
        estado_label=ctk.CTkLabel(frame_filtros, text="Estado:")
        estado_label.grid(row=1, column=4, padx=(0, 4), pady=8)
        self.combo_filtro_estado = ctk.CTkComboBox(frame_filtros, width=140,values=["Todos", "Operativo","Averiado", "Retirado"])
        self.combo_filtro_estado.set("Todos")
        self.combo_filtro_estado.grid(row=1, column=5, padx=(0, 10), pady=8)
        #Boton Buscar
        btn_buscar = ctk.CTkButton(frame_filtros, text="Buscar", width=80,fg_color=color_boton, hover_color=color_hover,command=self.buscar)
        btn_buscar.grid(row=1, column=6, padx=10, pady=8)
        #Boton para quitar todos los filtros
        btn_limpiar = ctk.CTkButton(frame_filtros, text="Limpiar", width=80, fg_color="#555555", hover_color="#777777",command=self.limpiar_filtros)
        btn_limpiar.grid(row=1, column=7, padx=(0, 10), pady=8)

        #Tabla
        frame_tabla = ctk.CTkFrame(frame_izq, fg_color="#2a2a2a", corner_radius=8)
        frame_tabla.grid(row=1, column=0, sticky="nsew", pady=(0, 8))
        frame_tabla.grid_rowconfigure(0, weight=1)
        frame_tabla.grid_columnconfigure(0, weight=1)
        #Estilo de la tabla
        style = ttk.Style()
        style.theme_use("clam")#Para poder personalizar la tabla
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
        style.map("Treeview", background=[("selected", color_hover)])#Si seleccionas un elemento, cambia el color de fondo
        columnas = ("ID", "Código", "Tipo", "Marca", "Modelo","Nº Serie", "Ubicación", "Fecha Alta", "Estado")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas,show="headings", selectmode="browse")

        #Cabeceras y anchos de la tabla
        anchos = [40, 90, 90, 90, 100, 100, 100, 90, 90] #con esto le asignamos anchos a cada columna de la tabla
        for col, ancho in zip(columnas, anchos):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=ancho, anchor="center")

        #Scrollbar para navegar verticalmente en la tabla
        scroll = ttk.Scrollbar(frame_tabla, orient="vertical",command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        #Al seleccionar una fila se rellena el formulario
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila) #Bind hace que cuando se selecciona algo en el tree view se llama al metodo seleccionar fila

        #Log
        frame_log = ctk.CTkFrame(frame_izq, fg_color="#2a2a2a", corner_radius=8)
        frame_log.grid(row=2, column=0, sticky="ew")
        frame_log.grid_columnconfigure(0, weight=1)
        log_label = ctk.CTkLabel(frame_log, text="Ultimo evento:",font=ctk.CTkFont(size=11))
        log_label.grid(row=0, column=0, padx=10, pady=(6, 0), sticky="w")
        self.texto_log = ctk.CTkLabel(frame_log, text="",font=ctk.CTkFont(size=11),text_color="#aaaaaa")
        self.texto_log.grid(row=1, column=0, padx=10, pady=(0, 6), sticky="w")

        #Columna derecha
        frame_der = ctk.CTkFrame(self, fg_color="#2a2a2a", corner_radius=8)
        frame_der.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        frame_der.grid_columnconfigure(0, weight=1)
        frame_der.grid_columnconfigure(1, weight=1)
        form_label = ctk.CTkLabel(frame_der, text="Formulario", font=ctk.CTkFont(size=14, weight="bold"))
        form_label.grid(row=0, column=0, columnspan=2, pady=(15, 10))

        #Campos del formulario
        campos = ["Código", "Tipo", "Marca", "Modelo","Nº Serie", "Ubicación", "Estado"]
        self.entries = {}
        #Creamos un bucle para hacer cada elemento automaticamente (para no crear uno por uno)
        for i, campo in enumerate(campos):
            #Label de cada campo
            label = ctk.CTkLabel(frame_der, text=f"{campo}:")
            label.grid(row=i+1, column=0, padx=(15, 5), pady=5, sticky="e")
            if campo == "Tipo": #En caso de que sea el campo de Tipo, hacemos un combobox con las opciones del filtro
                elemento = ctk.CTkComboBox(frame_der, width=160,values=["PC", "Portátil", "Impresora", "Router", "Otro"])
            elif campo == "Estado": #En caso de que sea el campo de Estado, hacemos un combobox con las opciones del filtro
                elemento = ctk.CTkComboBox(frame_der, width=160, values=["Operativo", "Averiado", "Retirado"])
            else:
                #Un entry para los campos que sean de texto libre
                elemento = ctk.CTkEntry(frame_der, width=160)
            #Añadimos el elemento en cuestion al lado del label
            elemento.grid(row=i+1, column=1, padx=(0, 15), pady=5, sticky="w")
            self.entries[campo] = elemento #Guardamos en el diccionario entries para manipularlo de manera sencilla en el futuro

        #Botones
        frame_crud = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_crud.grid(row=len(campos)+1, column=0, columnspan=2, pady=(15, 5)) #Añadimos el frame de los botones justo en la final debajo del ultimo campo

        btn_crear=ctk.CTkButton(frame_crud, text="Crear",width=100, fg_color=color_boton, hover_color=color_hover,command=self.crear)
        btn_crear.grid(row=0, column=0, padx=5)
        btn_editar=ctk.CTkButton(frame_crud, text="Editar",width=100,fg_color=color_boton, hover_color=color_hover,command=self.editar)
        btn_editar.grid(row=0, column=1, padx=5)
        btn_eliminar = ctk.CTkButton(frame_crud, text="Eliminar",width=100,fg_color=color_boton, hover_color=color_hover,command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=5)

        # Botones importar/exportar
        frame_import = ctk.CTkFrame(frame_der, fg_color="transparent")
        frame_import.grid(row=len(campos)+2, column=0, columnspan=2, pady=(5, 15))#Añadimos el frame de los botones i/e justo debajo de los otros
        btn_import = ctk.CTkButton(frame_import, text="Importar CSV", width=140,fg_color=color_boton, hover_color=color_hover,command=self.importar)
        btn_import.grid(row=0, column=0, padx=5)

        btn_exportar = ctk.CTkButton(frame_import, text="Exportar", width=140,fg_color=color_boton, hover_color=color_hover,command=self.exportar)
        btn_exportar.grid(row=0, column=1, padx=5)

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
        #Asignamos por posición exacta saltando la fecha
        self.entries["Código"].delete(0, "end")
        self.entries["Código"].insert(0, str(valores[1]))
        self.entries["Tipo"].set(str(valores[2]))
        self.entries["Marca"].delete(0, "end")
        self.entries["Marca"].insert(0, str(valores[3]))
        self.entries["Modelo"].delete(0, "end")
        self.entries["Modelo"].insert(0, str(valores[4]))
        self.entries["Nº Serie"].delete(0, "end")
        self.entries["Nº Serie"].insert(0, str(valores[5]))
        self.entries["Ubicación"].delete(0, "end")
        self.entries["Ubicación"].insert(0, str(valores[6]))
        self.entries["Estado"].set(str(valores[8]))  #Limpiamos cada elemento y añadimos el de la fila seleccionada

    def cargar_tabla(self, activos=None):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)#Borramos cada elemento antes de rellenar para no duplicarlo
        if activos is None: #Si no le pasamos ninguna lista de activos filtrada, le pasamos todos los activos
            activos = activo_service.obtener_activos()
        for a in activos: #Insertamos cada activo
            print(f"id={a.id} codigo={a.codigo} fecha={a.fecha_alta} estado={a.estado}")  # ← añade esto
            self.tabla.insert("", "end", values=(
                a.id, a.codigo, a.tipo, a.marca, a.modelo,
                a.n_serie, a.ubicacion, a.fecha_alta, a.estado
            ))

    def buscar(self):
        id_filtro = self.entry_filtro_id.get()
        tipo_filtro = self.combo_filtro_tipo.get()
        estado_filtro = self.combo_filtro_estado.get()
        todos = activo_service.obtener_activos()
        activos = []
        for a in todos:
            #Comprobar filtro ID
            if id_filtro and str(a.id) != id_filtro:
                continue
            #Comprobar filtro tipo
            if tipo_filtro != "Todos" and a.tipo != tipo_filtro:
                continue
            #Comprobar filtro estado
            if estado_filtro != "Todos" and a.estado != estado_filtro:
                continue
            activos.append(a) #Si pasa por todos los filtros, se añade a la lista que se mandara a la tabla
        self.cargar_tabla(activos)
        self.actualizar_log(f"{len(activos)} activos encontrados")

    def limpiar_filtros(self): #Limpiamos los filtros
        self.entry_filtro_id.delete(0, "end")
        self.combo_filtro_tipo.set("Todos")
        self.combo_filtro_estado.set("Todos")
        self.cargar_tabla() #Cargamos la tabla entera de nuevo

    def crear(self):
        try:
            #Recoger datos del formulario para crear el nuevo activo
            codigo = self.entries["Código"].get()
            tipo = self.entries["Tipo"].get()
            marca = self.entries["Marca"].get()
            modelo = self.entries["Modelo"].get()
            n_serie = self.entries["Nº Serie"].get()
            ubicacion = self.entries["Ubicación"].get()
            estado = self.entries["Estado"].get()
            #Llamamos al service con los datos pasados por parámetro
            activo_service.crear_activo(codigo, tipo, marca, modelo,n_serie, ubicacion, estado)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Activo {codigo} creado correctamente")
        except ValueError as e:
            self.actualizar_log(f" {e}")
        except Exception as e:  #Manejamos errores aparte del value error que definimos antes
            if "UNIQUE" in str(e): #Si está presente unique en el error
                self.actualizar_log("El código o nº de serie ya existe")
            else:
                self.actualizar_log(f"Error inesperado: {e}")

    def editar(self):
        try:
            #Verificar que hay una fila seleccionada para poder editar un activo real
            seleccion = self.tabla.selection()
            if not seleccion:
                self.actualizar_log("Selecciona un activo para editar")
                return
            #Obtener el ID de la fila seleccionada
            id_activo = self.tabla.item(seleccion[0])["values"][0]
            #Recoger datos del formulario
            codigo = self.entries["Código"].get()
            tipo = self.entries["Tipo"].get()
            marca = self.entries["Marca"].get()
            modelo = self.entries["Modelo"].get()
            n_serie = self.entries["Nº Serie"].get()
            ubicacion = self.entries["Ubicación"].get()
            estado = self.entries["Estado"].get()
            #Llamar al services con los parámetros de nuevo
            activo_service.actualizar_activo(id_activo, codigo, tipo, marca, modelo,n_serie, ubicacion, estado)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Activo {codigo} editado correctamente")
        except ValueError as e:
            self.actualizar_log(f"{e}")
        except Exception as e:  # Manejamos errores aparte del value error que definimos antes
            if "UNIQUE" in str(e):  # Si está presente unique en el error
                self.actualizar_log("El código o nº de serie ya existe")
            else:
                self.actualizar_log(f"Error inesperado: {e}")

    def eliminar(self):
        try:
            #Verificar que hay una fila seleccionada
            seleccion = self.tabla.selection()
            if not seleccion:
                self.actualizar_log("Selecciona un activo para eliminar")
                return
            #Obtener id para el mensaje
            id = self.tabla.item(seleccion[0])["values"]
            id_activo = id[0]
            #Confirmación antes de eliminar
            confirmar = messagebox.askyesno("Confirmar eliminación",f"¿Estás seguro de que quieres eliminar {id_activo}?")
            if not confirmar: #Si se da a que no, se termina el método
                return
            # Llamar al service
            activo_service.eliminar_activo(id_activo)
            self.cargar_tabla()
            self.limpiar_formulario()
            self.actualizar_log(f"Activo {id_activo} eliminado correctamente")
        except Exception as e:
            self.actualizar_log(f"{e}")

    def importar(self):
        pass  

    def exportar(self):
        pass