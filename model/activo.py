from datetime import date


class Activo: #Clase Activc que simula cada fila de la base de datos en .py

    def __init__(self, codigo, tipo, marca, modelo, n_serie, ubicacion,
                 fecha_alta=None, estado="Operativo", id=None):
        self.codigo = codigo
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.n_serie = n_serie
        self.ubicacion = ubicacion
        self.fecha_alta = fecha_alta or date.today() #En caso de no haber fecha en el constructor añade la de hoy
        self.estado = estado #En caso de no haber nada, le da el valor por defecto (Operativo)
        self.id = id #Como será auto_increment, el constructor puede no recibir y sqlite lo asignará

    def __str__(self):
        return f"Activo({self.codigo} | {self.tipo} | {self.estado})"

    def to_dict(self): #Vamos a necesitar volcar datos en un json, asi que preparamos el formateo a dict para mandarlo posteriormente
        return {
            "id": self.id,
            "codigo": self.codigo,
            "tipo": self.tipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "n_serie": self.n_serie,
            "ubicacion": self.ubicacion,
            "fecha_alta": str(self.fecha_alta),
            "estado": self.estado
        }