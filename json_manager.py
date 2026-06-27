import json
from datetime import datetime
from models import Event

def guardar_eventos(events, filename="eventos.json"):
    data = []
    for e in events:
        data.append({
            "name": e.name,
            "init": e.init.isoformat(),
            "end": e.end.isoformat(),
            "capacity": e.capacity,
            "place": e.place.name,
            "personal": {p.name: qty for p, qty in e.personal.items()},
            "objects": {o.name: qty for o, qty in e.objects.items()},
            "password": e.password
        })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def cargar_eventos(events, espacios, objetos, personal, filename="eventos.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        places = {esp.name: esp for esp in espacios}
        objetos_dict = {obj.name: obj for obj in objetos}
        personal_dict = {p.name: p for p in personal}

        for e in data:
            if e["place"] not in places:
                print(f"Advertencia: lugar desconocido {e['place']}, evento omitido")
                continue

            lugar = places[e["place"]]
            objetos_evento = {objetos_dict[obj]: qty for obj, qty in e["objects"].items() if obj in objetos_dict}
            personal_evento = {personal_dict[p]: qty for p, qty in e["personal"].items() if p in personal_dict}

            evento = Event(
                datetime.fromisoformat(e["init"]),
                datetime.fromisoformat(e["end"]),
                e["capacity"],
                lugar,
                personal_evento,
                objetos_evento,
                e["password"],
                e["name"]
            )
            events.append(evento)
    except FileNotFoundError:
        pass
