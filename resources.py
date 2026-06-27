from models import Personal, Object, Space

# Personal
Astrofisico = Personal("Astrofisico", total=13)
Tecnico_Telescopios = Personal("Tecnico de Telescopios", total=20)
Ingeniero = Personal("Ingeniero", total=9)
Astronomo = Personal("Astronomo", total=14)
Director = Personal("Director", total=1)
Secretario = Personal("Secretario", total=4)
Servicio = Personal("Servicio", total=30)
Historiador = Personal("Historiador", total=5)
Tecnico_Lunatron = Personal("Tecnico Lunatron", total=2)
Tecnico = Personal("Tecnico", total=6)

#la lista del personal
personal = [
    Astrofisico, Ingeniero, Astronomo, Tecnico_Telescopios, Tecnico,
    Tecnico_Lunatron, Director, Secretario, Servicio, Historiador
]

# Objetos
Telescopio_Principal = Object("Telescopio Principal", {Ingeniero: 1, Astronomo: 1}, total=1)
Telescopio_Basico = Object("Telescopio Basico", {Astronomo: 1, Tecnico_Telescopios: 1}, total=20)
Espectrografo = Object("Espectrografo", {Astrofisico: 1, Tecnico: 2}, total=12)
Proyector = Object("Proyector", {Tecnico: 1}, total=4)
Mapas_Estelares = Object("Mapas Estelares", {Historiador: 1, Tecnico: 1, Astronomo: 1}, total=13)
Meteoritos = Object("Trozos de Meteoritos", {Historiador: 1, Tecnico: 1, Astronomo: 1}, total=23)
Equipo_Lunatron = Object("Equipo especial para el Lunatron", {Tecnico_Lunatron: 1}, total=5)
Planetas_Escala = Object("Planetas a escala", {Astronomo: 1, Tecnico: 2}, total=200)
Cohetes_Escala = Object("Cohetes a escala", {Astrofisico: 1, Tecnico: 2}, total=42)

#la lista de los objetos
objetos = [
    Telescopio_Principal, Telescopio_Basico, Espectrografo, Proyector,
    Mapas_Estelares, Meteoritos, Equipo_Lunatron, Planetas_Escala, Cohetes_Escala
]

#  Espacios 
Teatro = Space("Teatro para conferencias", 100, {Servicio: 3, Tecnico: 2})
Cupula = Space("Cupula retractil", 40, {Astrofisico: 1, Astronomo: 2, Tecnico_Telescopios: 1})
Sala_UO = Space("Sala del universo observable", 70, {Tecnico: 2, Historiador: 1, Astrofisico: 1})
Laboratorio = Space("Laboratorio", 50, {Tecnico: 4, Ingeniero: 2, Servicio: 5})
Lunatron = Space("Lunatron", 8, {Tecnico_Lunatron: 2, Ingeniero: 1, Astronomo: 1, Servicio: 9})
Terraza = Space("Terraza", 70, {Servicio: 2})
Secretaria = Space("Secretaria", 2, {Secretario: 1, Tecnico: 1})
Salon_H = Space("Salon de la historia de la aviacion", 60, {Historiador: 1, Servicio: 4, Tecnico: 1})

#la lista de los objetos 
espacios = [Teatro, Cupula, Sala_UO, Laboratorio, Lunatron, Terraza, Secretaria, Salon_H]