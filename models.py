from datetime import datetime

class Personal:
    def __init__(self, name, total=1):
        self.name = name
        self.total = total   # el total en todo el museo

class Object():
    def __init__(self, name, personal=None, total=1):
        self.name = name
        self.personal = personal if personal else {}  # dict {Personal: cantidad requerida} mouskerramienta para mas tarde 
        self.total = total   # lo mismo que con personal

class Space:
    #aqui usamos las mismas definiciones que en el anterior 
    def __init__(self, name, capacity, personal=None):
        self.name = name
        self.capacity = capacity 
        self.personal = personal if personal else {}  # dict {Personal: cantidad requerida} 

class Event:
    #ahi esta cada variable explicada para que no te me enredes en el futuro 
    def __init__(self, init, end, capacity, place, personal, objects, password, name="Evento sin nombre"):
        self.init = init # datetime inicio
        self.end = end # datetime fin
        self.capacity = capacity # capacidad numérica
        self.place = place# objeto Space
        self.personal = personal# dict {Personal: cantidad}
        self.objects = objects# dict {Object: cantidad}
        self.password = password# contraseña para eliminar
        self.name = name# nombre del evento