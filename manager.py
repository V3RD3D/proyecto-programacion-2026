from datetime import datetime, time, timedelta

# para detectar los posibles solapamientos 
def eventos_solapan(e1, e2):
    # Coinciden en el mismo día
    mismo_dia = e1.init.date() == e2.init.date()
    # Coinciden en horario (horas/minutos)
    mismo_horario = e1.init.time() < e2.end.time() and e2.init.time() < e1.end.time()
    return mismo_dia and mismo_horario  #retorna un bool lider 

# para agregar un evento 
#primero hay que revisar un par de cosillas 
def Adder(event, events):
    
    # --- Validar horario del museo (solo horas/minutos, sin importar el día) ---
    apertura = time(9, 0)   # 9:00 AM
    cierre = time(21, 0)    # 9:00 PM

    if event.init.time() < apertura or event.end.time() > cierre:
        raise ValueError("El museo solo está abierto de 9:00 AM a 9:00 PM")
    
    #verificar la capacidad 
    if event.capacity > event.place.capacity:
        raise ValueError("La sala no soporta esa capacidad")
    
    objetos = {}#un diccionario vacio para ir acumulando la cantidad de objetos y verificar despues
    personal_usado = {}#otro diccionario pero esta vez la idea es hacerlo con los personales 

    #vamos a rellenar las dos listas 
    for obj, cantidad in event.objects.items(): #recorremos los objetos y la cantidad del evento en cuestion
        objetos[obj] = objetos.get(obj, 0) + cantidad #el get es una talla , fijate que se puede ponet las cosas predeterminadas en una linea 
    
    for persona, cantidad in event.personal.items():#aqui es lo mismo pero con el personal 
        personal_usado[persona] = personal_usado.get(persona,0) + cantidad

    #Solapamientos con eventos existentes (utilizando la funcion que creamos hace un ratico)
    for ev in events:
        if eventos_solapan(event, ev):
            if event.place == ev.place:
                # aquí usamos Buscar_Hueco para sugerir el próximo intervalo
                inicio, fin = Buscar_Hueco(event, events)
                raise ValueError(
                    f"Ese lugar ya está en uso. "
                    f"Próximo hueco disponible: {inicio.strftime('%d/%m/%Y %H:%M')} - {fin.strftime('%H:%M')}"
                )

            #hacer lo mismo que hace un ratico pero con todos los eventos que ya existian en la lista de eventos anteriores
            for obj, cantidad in ev.objects.items():#aqui con los objetos
                objetos[obj] = objetos.get(obj, 0) + cantidad
            
            #aqui con el personal
            for persona, cantidad in ev.personal.items():
                personal_usado[persona] = personal_usado.get(persona, 0) + cantidad

    # Validar objetos y acumular personal requerido por ellos
    #ahora que las dos listas estan completadas solo hay que verificar que todo lo acumulado no se pase 
    
    #aqui validando los objetos 
    for obj, cantidad in objetos.items():
        if cantidad > obj.total:
            raise ValueError(f"No hay suficientes {obj.name} en ese momento")
        for persona, req in obj.personal.items():
            personal_usado[persona] = personal_usado.get(persona, 0) + req

    #Un detalle hay que verificar porque el espacio tambien requiere personal (no cualqiera puede operar lo que sea)
    # Validar personal requerido por el espacio
    for persona, req in event.place.personal.items():
        personal_usado[persona] = personal_usado.get(persona, 0) + req

    # Ahora que esta todo el mundo entonces si vamos a validar el personal acumulado
    for persona, cantidad in personal_usado.items():
        if cantidad > persona.total:
            raise ValueError(f"No hay suficiente personal: {persona.name}")

    # Si todo está bien, añadir el evento ....YEI🥳
    events.append(event)

# Eliminar evento 
def Remove(event, events, password):
    #voy añadir una contraseña genral (bien cortica) y la que viene con el evento claro 
    if password == event.password or password == "esternocleidomastoideo":
        events.remove(event)
        print("Evento eliminado")
    else:
        raise ValueError("Contraseña incorrecta, no puedes eliminar este evento")

#para la información del evento (todos los recursos) 
def Info(event):
    recursos_personal = {}
    recursos_objetos = {}

    # Personal directo
    for p, qty in event.personal.items():
        recursos_personal[p.name] = recursos_personal.get(p.name, 0) + qty

    # Objetos y personal requerido por ellos
    for obj, qty in event.objects.items():
        recursos_objetos[obj.name] = recursos_objetos.get(obj.name, 0) + qty
        for p, req in obj.personal.items():
            recursos_personal[p.name] = recursos_personal.get(p.name, 0) + req

    # Personal requerido por el espacio
    for p, req in event.place.personal.items():
        recursos_personal[p.name] = recursos_personal.get(p.name, 0) + req

    return {
        "Nombre": event.name,
        "Inicio": event.init.strftime("%d/%m/%Y %H:%M"),
        "Fin": event.end.strftime("%d/%m/%Y %H:%M"),
        "Capacidad": event.capacity,
        "Lugar": event.place.name,
        "Objetos": recursos_objetos,
        "Personal": recursos_personal
    }

#buscar Hueco
# Esta función analiza el calendario y sugiere el próximo intervalo disponible
def Buscar_Hueco(evento_propuesto, events):
    apertura = time(9, 0)   # 9:00 AM
    cierre = time(21, 0)    # 9:00 PM

    # empezamos desde la fecha de inicio propuesta
    fecha_actual = evento_propuesto.init.date()
    duracion = evento_propuesto.end - evento_propuesto.init

    while True:
        # filtrar eventos del mismo día
        eventos_dia = [ev for ev in events if ev.init.date() == fecha_actual]
        eventos_dia.sort(key=lambda ev: ev.init)

        # rango del día (apertura y cierre del museo)
        inicio_dia = datetime.combine(fecha_actual, apertura)
        fin_dia = datetime.combine(fecha_actual, cierre)

        # revisar hueco antes del primer evento
        if not eventos_dia:
            if inicio_dia + duracion <= fin_dia:
                return inicio_dia, inicio_dia + duracion
        else:
            if inicio_dia + duracion <= eventos_dia[0].init:
                return inicio_dia, inicio_dia + duracion

            # revisar huecos entre eventos
            for i in range(len(eventos_dia) - 1):
                fin_evento = eventos_dia[i].end
                inicio_siguiente = eventos_dia[i+1].init
                if fin_evento + duracion <= inicio_siguiente:
                    return fin_evento, fin_evento + duracion

            # revisar hueco después del último evento
            ultimo_fin = eventos_dia[-1].end
            if ultimo_fin + duracion <= fin_dia:
                return ultimo_fin, ultimo_fin + duracion

        # si no hay hueco en este día, pasar al siguiente
        fecha_actual += timedelta(days=1)

        # seguridad: si el evento dura más que el horario del museo, nunca cabe
        if duracion > (datetime.combine(fecha_actual, cierre) - datetime.combine(fecha_actual, apertura)):
            raise ValueError("El evento es demasiado largo para caber en el horario del museo (9:00 AM - 9:00 PM)")
