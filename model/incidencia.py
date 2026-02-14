from datetime import date


class Incidencia: #Clase Incidencia que simula cada fila de la base de datos en .py

    def __init__(self, activo_id, prioridad, categoria,
                 descripcion, tecnico, estado="En espera", fecha_apertura=None, id=None):
        self.activo_id = activo_id
        self.fecha_apertura = fecha_apertura or date.today() #En caso de no haber fecha en el constructor añade la de hoy
        self.prioridad = prioridad
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = estado #En caso de no haber nada, le da el valor por defecto (En espera)
        self.tecnico = tecnico
        self.id = id #Como será auto_increment, el constructor puede no recibir y sqlite lo asignará

    def __str__(self):
        return f"Activo: {self.activo_id} | Técnico: {self.tecnico} | Estado: {self.estado}"

    def to_dict(self): #Vamos a necesitar volcar datos en un json, asi que preparamos el formateo a dict para mandarlo posteriormente
        return {
            "id": self.id,
            "activo_id": self.activo_id,
            "fecha_apertura": str(self.fecha_apertura),
            "prioridad": self.prioridad,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "estado": self.estado,
            "tecnico": self.tecnico
        }