Este proyecto es una aplicación web pensada para facilitar la planificación y gestión de eventos dentro de un museo. Su objetivo principal es reducir errores humanos y automatizar comprobaciones repetitivas: valida horarios, controla aforos, gestiona la disponibilidad de objetos y personal, evita solapamientos y, cuando no es posible programar un evento en el intervalo solicitado, propone alternativas prácticas, es decir, el siguiente hueco disponible. Está orientada a coordinadores, jefes de sala y personal de logística que necesitan una herramienta fiable para tomar decisiones rápidas y coherentes.

La aplicación está escrita en Python con Flask para la interfaz web, guarda los datos en JSON y usa HTML y CSS para la presentación. A continuación se explica con detalle qué hace cada parte, cómo interactúan entre sí y qué hace cada clase y función principal.

Lo que hace, literalmente:
Permite crear, listar, ver y eliminar eventos garantizando que cada evento respete horarios, capacidad, disponibilidad de objetos y personal, y evita solapamientos; si no cabe, propone el siguiente intervalo disponible.

Estructura del proyecto:
- Python (lógica y servidor)
  - "main.py" — rutas Flask y control de flujo web.
  - "models.py" — definiciones de las entidades del dominio.
  - "resources.py" — inicialización de recursos disponibles (objetos, personal, espacios).
  - "manager.py" — reglas de negocio: validaciones, comprobación de solapamientos, asignación y búsqueda de huecos.
  - "json_manager.py" — funciones para guardar y cargar eventos desde "eventos.json".

- Plantillas HTML (templates/):
  - "presentacion.html", "index.html", "crear_evento.html", "info_evento.html".

- Estilos CSS (static/):
  - Archivos por página para separar estilos y facilitar mantenimiento.

- Persistencia:
  - "eventos.json" — archivo que contiene la lista de eventos guardados entre ejecuciones.

Flujo de uso (qué hace el usuario y qué hace el sistema)
1. Iniciar la aplicación: python main.py.
2. Abrir el navegador en `http://127.0.0.1:5000/` [(127.0.0.1 in Bing)](https://www.bing.com/search?q="http%3A%2F%2F127.0.0.1%3A5000%2F").
3. Crear un evento desde /crear_evento completando: nombre, contraseña, lugar, capacidad, inicio, fin, objetos y personal.
4. El servidor valida el evento (función Adder): horario, capacidad, solapamientos, disponibilidad de objetos y personal.
   - Si todo es válido, el evento se añade a la lista y se guarda en eventos.json.
   - Si hay conflicto, el sistema intenta encontrar y sugerir el siguiente hueco disponible.
5. Consultar la lista de eventos en /eventos.
6. Ver detalles en /info_evento/<id>.
7. Eliminar un evento en /eliminar_evento/<id> proporcionando la contraseña del evento o la clave general.

Explicación al dedillo de las clases (qué representan, atributos, responsabilidades y ejemplos)

Clase Personal:
Propósito: modelar un tipo de trabajador del museo (por ejemplo: técnico, historiador, servicio).
Atributos típicos:
- name (str): nombre del tipo de personal, por ejemplo "Tecnico".
- total (int): número total de personas de ese tipo disponibles en el museo.

Responsabilidad: mantener la cantidad disponible de cada tipo de trabajador y servir como referencia para las comprobaciones de disponibilidad.

Ejemplo de uso: al crear un evento se solicita cuántas unidades de cada tipo se necesitan; el sistema suma las asignaciones en el intervalo y compara con total.

Notas de implementación: suele implementarse con métodos sencillos como __init__ y __repr__. No debe contener lógica de calendario; su responsabilidad es solo representar el recurso humano.

Clase Object
Propósito: representar recursos materiales (proyectores, vitrinas, telescopios, etc.).
Atributos típicos:
- name (str): nombre del objeto, por ejemplo "Proyector".
- total (int): cantidad total disponible.
- personal_required (dict opcional): si el uso del objeto exige personal especializado, por ejemplo {"Tecnico": 1}.

Responsabilidad: modelar la disponibilidad física y, si aplica, la dependencia de personal para su uso.

Ejemplo de uso: si un evento solicita 2 proyectores, el sistema comprobará que la suma de proyectores reservados en ese intervalo no supere total. Si el objeto requiere personal, la validación también debe reservar el personal necesario.

Notas de implementación: los objetos se identifican por name y se usan como claves en diccionarios de asignación dentro de Event.

Clase Space
Propósito: representar una sala o espacio físico del museo.
Atributos típicos:
- name (str): nombre de la sala, por ejemplo "Teatro para conferencias".
- capacity (int): aforo máximo permitido.
- personal_required (dict opcional): personal mínimo necesario para operar la sala (por ejemplo, seguridad o técnicos).

Responsabilidad: servir como contenedor de restricciones físicas (aforo) y de requisitos mínimos de personal; las comprobaciones de solapamiento se realizan por Space.

Ejemplo de uso: al crear un evento, se compara event.capacity con space.capacity y se valida que la sala esté libre en el intervalo solicitado.

Notas de implementación: las instancias de Space se inicializan en resources.py y se referencian por nombre desde los eventos cargados del JSON.

Clase Event
Propósito: entidad central que representa una reserva o evento.
Atributos típicos:
- init (datetime): fecha y hora de inicio.
- end (datetime): fecha y hora de fin.
- capacity (int): aforo previsto para el evento.
- place (Space): referencia a la sala donde se realizará.
- personal (dict): asignación de personal por tipo, por ejemplo {"Tecnico": 1, "Servicio": 2}.
- objects (dict): asignación de objetos por tipo, por ejemplo {"Proyector": 2}.
- password (str): contraseña para permitir eliminación o edición.
- name (str): nombre descriptivo del evento.

Responsabilidad: encapsular todos los datos necesarios para reservar un hueco en el calendario y servir como unidad de persistencia.

Ejemplo de uso: Event(init, end, capacity, place, personal_dict, objects_dict, password, name).

Notas de implementación: debe incluir métodos de serialización (por ejemplo to_dict) para convertir fechas a ISO y facilitar la escritura en JSON, y un constructor o método de fábrica para reconstruir desde JSON (from_dict).

Explicación al dedillo de las funciones principales (intención, pasos y resultados)

Las funciones descritas a continuación son las piezas clave de la lógica de negocio. La explicación incluye la intención, el algoritmo general y el resultado esperado.

eventos_solapan(e1, e2)
Intención: determinar si dos eventos se solapan en tiempo y lugar.
Algoritmo:
1. Comprobar si e1.place.name == e2.place.name (mismo espacio). Si no, no hay solapamiento relevante para la misma sala.
2. Comparar intervalos: dos eventos solapan si e1.init < e2.end y e2.init < e1.end. Esta condición cubre todos los casos de intersección de intervalos.
3. Opcionalmente, normalizar zonas horarias o truncar segundos si la aplicación lo requiere.
Resultado: devuelve True si hay solapamiento en la misma sala; False en caso contrario.
Casos límite: si e1.end == e2.init se considera no solapamiento (evento termina justo cuando empieza el otro), salvo que se quiera imponer un margen de seguridad.

Adder(event, events)
Intención: validar y añadir un evento a la lista events si cumple todas las reglas; en caso contrario, ofrecer una sugerencia de reprogramación.
Pasos detallados:
1. Validación básica de fechas: comprobar que event.init < event.end y que ambos están dentro del horario permitido (por ejemplo, entre 09:00 y 21:00). Si falla, devolver error inmediato.
2. Validación de capacidad: comparar event.capacity con event.place.capacity. Si event.capacity excede la capacidad de la sala, devolver error.
3. Comprobación de solapamientos: iterar sobre events y usar eventos_solapan para detectar conflictos en la misma sala. Si se detecta solapamiento, marcar conflicto.
4. Disponibilidad de objetos y personal: para el intervalo propuesto:
   - Construir acumuladores: para cada tipo de objeto y personal, sumar las cantidades ya reservadas en eventos que solapan parcialmente con el intervalo propuesto.
   - Comparar la suma más la cantidad solicitada con el total disponible (definido en resources.py). Si alguna suma excede el total, marcar conflicto.
5. Decisión final:
   - Si no hay conflictos, añadir event a events, llamar a guardar_eventos(events) y devolver confirmación.
   - Si hay conflictos, llamar a Buscar_Hueco(event, events) para intentar encontrar una alternativa; devolver error con la sugerencia (si existe).
Resultado: inserta el evento y persiste, o devuelve un error con información útil y, cuando sea posible, una alternativa.

Buscar_Hueco(evento_propuesto, events)
Intención: encontrar el siguiente intervalo disponible que cumpla las mismas condiciones del evento propuesto.
Algoritmo detallado:
1. Calcular la duración dur = evento_propuesto.end - evento_propuesto.init.
2. Definir un rango de búsqueda (por ejemplo, hasta X días adelante) y un paso de avance (por ejemplo 15 o 30 minutos).
3. Para cada candidato start_candidate desde evento_propuesto.init avanzando por el paso:
   - Definir end_candidate = start_candidate + dur.
   - Verificar que start_candidate y end_candidate estén dentro del horario permitido.
   - Verificar que la sala esté libre: para cada evento en events, comprobar eventos_solapan con el candidato; si alguno solapa, descartar candidato.
   - Verificar disponibilidad de objetos y personal en ese candidato (mismo procedimiento de acumulación que en Adder).
   - Si todas las comprobaciones pasan, devolver (start_candidate, end_candidate) como propuesta.
4. Si no se encuentra ninguna ventana válida dentro del rango, devolver None.
Resultado: una propuesta de inicio/fin alternativos o None.

Remove(event, events, password)
Intención: eliminar un evento si la contraseña es correcta o si se usa la clave general.
Pasos:
1. Comparar la contraseña proporcionada con event.password o con la clave general definida en la aplicación.
2. Si coincide, eliminar el evento de events.
3. Llamar a guardar_eventos(events) para persistir el cambio.
4. Devolver confirmación; si no coincide, devolver error de autenticación.
Resultado: evento eliminado y persistencia actualizada, o error por contraseña incorrecta.

Info(event)
Intención: construir una representación legible del evento para mostrar en la interfaz.
Pasos:
1. Extraer atributos de Event y formatear fechas en cadenas legibles (por ejemplo, YYYY-MM-DD HH:MM).
2. Construir un diccionario con claves legibles: Nombre, Inicio, Fin, Capacidad, Lugar, Personal, Objetos.
3. Devolver el diccionario para que la plantilla info_evento.html lo renderice.
Resultado: diccionario listo para la vista.

guardar_eventos(events)
Intención: persistir la lista de eventos en eventos.json.
Pasos:
1. Para cada Event en events, convertirlo a un diccionario serializable: fechas en formato ISO (.isoformat()), referencias a place por nombre, y diccionarios de personal y objects con cantidades.
2. Escribir la lista de diccionarios en eventos.json con json.dump usando indentación para legibilidad.
3. Manejar errores de E/S y, si es necesario, realizar copias de seguridad antes de sobrescribir.
Resultado: archivo eventos.json actualizado.

cargar_eventos(events, espacios, objetos, personal)
Intención: reconstruir la lista events desde eventos.json al iniciar la aplicación.
Pasos:
1. Leer eventos.json y parsear la lista de diccionarios.
2. Para cada entrada:
   - Convertir las cadenas ISO a datetime.
   - Buscar la instancia Space correspondiente en espacios por nombre.
   - Reconstruir los diccionarios de personal y objects mapeando nombres a instancias o manteniendo nombres según la implementación.
   - Crear una instancia Event con los datos reconstruidos.
3. Añadir cada Event a la lista events.
4. Manejar entradas corruptas con logs y saltar eventos inválidos en lugar de romper la carga completa.
Resultado: events poblada con los eventos guardados listos para ser usados por la aplicación.

Ejemplos de uso concretos
- Evento válido: taller de 2 horas en sala con capacidad suficiente y recursos libres → Adder valida y guarda.
- Solapamiento: intento de reservar la misma sala en horario ocupado → Adder detecta conflicto y Buscar_Hueco propone alternativa.
- Falta de objetos: se solicitan más proyectores de los disponibles → Adder rechaza y sugiere reprogramar o reducir cantidad.
- Eliminación: organizador elimina su evento con contraseña correcta → evento borrado y JSON actualizado.

Buenas prácticas y recomendaciones de mantenimiento
- Centralizar validaciones en manager.py para facilitar pruebas unitarias.
- Añadir pruebas unitarias para Adder, eventos_solapan y Buscar_Hueco.
- Implementar control de concurrencia si varios usuarios crean eventos simultáneamente (bloqueos o transacciones).
- Añadir logs estructurados para auditar cambios (creación, edición, eliminación).
- Considerar migrar a una base de datos relacional si la escala o concurrencia crece.
- Añadir interfaz de administración para gestionar recursos sin editar código.

Cómo contribuir o adaptar el proyecto
- Cambiar recursos: editar resources.py.
- Cambiar reglas de validación: modificar manager.py.
- Cambiar persistencia: reemplazar json_manager.py por un adaptador a base de datos manteniendo la interfaz guardar_eventos / cargar_eventos.
- Añadir pruebas: crear un módulo tests/ con casos para cada función crítica.

Notas finales
Este documento explica con lenguaje claro la intención y el funcionamiento de cada clase y función principal. Si quieres, puedo:
- convertir este texto a un archivo .txt listo para descargar,
- generar un eventos.json de ejemplo con más casos,
- escribir pruebas unitarias básicas para manager.py,
- o crear un base.html para unificar la barra de navegación en todas las plantillas.

Indica cuál de estas tareas prefieres que haga a continuación.

