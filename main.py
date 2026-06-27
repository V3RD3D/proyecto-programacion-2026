from flask import Flask, render_template, request
from models import *
from resources import *
from manager import *
from datetime import datetime
from json_manager import *

app = Flask(__name__)
events = []

#cargamos todos los archivos del json para empezar 
cargar_eventos(events, espacios, objetos, personal)

#esto en flask es para crear una ruta segun el html que se le pase 
@app.route("/presentacion")
def presentacion():
    return render_template("presentacion.html")

@app.route("/")
def home():
    # al entrar en la raíz, mostramos la presentación
    return render_template("presentacion.html")

@app.route("/eventos")
def eventos():
    # nueva ruta para mostrar la lista de eventos
    return render_template("index.html", events=events)

# para crear los eventos 

#esto lo que hace es leer los elementos de la pagina , le asigna a las variables 
#que ya creamos en models pero ahora html las puede leer como variables en (gracias a flask)
@app.route("/crear_evento", methods=["GET"])
def crear_evento_get():
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return render_template("crear_evento.html",
                           objetos=objetos,
                           personal=personal,
                           espacios=espacios,
                           current_datetime=now)

@app.route("/crear_evento", methods=["POST"])
def crear_evento_post():
    try:
        #datos básicos del formulario
        nombre = request.form["nombre"]
        contraseña = request.form["contraseña"]
        place_name = request.form["place"]

        #buscar el lugar seleccionado
        places = {esp.name: esp for esp in espacios}
        if place_name not in places:
            return "Error: El lugar seleccionado no existe"
        lugar = places[place_name]

        #capacidad y fechas
        capacidad = int(request.form["capacidad"])
        inicio = datetime.fromisoformat(request.form["inicio"])
        fin = datetime.fromisoformat(request.form["fin"])

        #objetos seleccionados
        objetos_evento = {}
        for obj in objetos:
            if f"object_{obj.name}" in request.form:
                qty = int(request.form.get(f"object_qty_{obj.name}", 0))
                if qty > 0:
                    objetos_evento[obj] = qty

        #personal seleccionado
        personal_evento = {}
        for p in personal:
            if f"personal_{p.name}" in request.form:
                qty = int(request.form.get(f"personal_qty_{p.name}", 0))
                if qty > 0:
                    personal_evento[p] = qty

        #crear evento y validar con manager 
        nuevo_evento = Event(inicio, fin, capacidad, lugar, personal_evento, objetos_evento, contraseña, nombre)
        Adder(nuevo_evento, events)  # aquí se hacen todas las verificaciones de solapamiento, capacidad, objetos y personal

        # Guardar en el json
        guardar_eventos(events)

        #mostrar lista actualizada
        return render_template("index.html", events=events)

    except Exception as e:
        return f"Error al crear evento: {e}"

@app.route("/info_evento/<int:event_id>")
def info_evento(event_id):
    if 0 <= event_id < len(events):
        evento = events[event_id]
        info = Info(evento)
        return render_template("info_evento.html", info=info)
    return "Evento no encontrado"

@app.route("/eliminar_evento/<int:event_id>", methods=["POST"])
def eliminar_evento(event_id):
    if 0 <= event_id < len(events):
        evento = events[event_id]
        contraseña = request.form["contraseña"]
        try:
            Remove(evento, events, contraseña)
            guardar_eventos(events)  # <-- aquí el fix
            return render_template("index.html", events=events)
        except Exception as e:
            return f"Error al eliminar evento: {e}"
    return "Evento no encontrado"

if __name__ == "__main__":
    app.run(debug=True)
