from bottle import run, request, response, delete, get, post, put
from json import dumps, load
from room import Room
from os import remove, path, mkdir, listdir
import logging

""" Listado de todas las habitaciones registradas """
registry = {}


def habitaciones_ocupadas(serializar=False):
    """ Devuelve la lista de las habitaciones ocupadas

    :param serializar: Si es True devolverá los diccionarios
    de los objetos para que puedan ser serializados para su
    transmisión.

    :returns Lista de las habitaciones ocupadas"""

    ocupadas = {}

    for key in registry:
        if not registry[key].disponible:
            if serializar:
                ocupadas[key] = registry[key].__dict__
            else:
                ocupadas[key] = registry[key]

    return ocupadas


def habitaciones_disponibles(serializar=False):
    """ Devuelve la lista de las habitaciones disponibles

    :param serializar: Si es True devolverá los diccionarios
    de los objetos para que puedan ser serializados para su
    transmisión.

    :returns Lista de las habitaciones disponibles"""

    disponibles = {}

    for key in registry:
        if registry[key].disponible:
            if serializar:
                disponibles[key] = registry[key].__dict__
            else:
                disponibles[key] = registry[key]

    return disponibles


def update(target_id):
    """ Hace persistente cualquier modificación en una habitación.

    Se busca la habitación por su ID en el registro, si no encuentra
    ninguna habitación busca en los fichero y elimina su fichero.
    Si existe y los datos son diferentes, sobreescribe el fichero, si
    existe en el registro pero no en los ficheros genera uno nuevo.

    :param target_id: Identificador único de la habitación."""

    url = f'ArchivosServidor/Habitacion{target_id}.json'
    try:
        target = registry[target_id]
        with open(url, 'r') as file:
            target_data = load(file)
        if target_data is None or not dumps(target_data) == target.__dict__:
            with open(url, 'w') as file:
                file.write(dumps(target.__dict__))

    except FileNotFoundError:
        with open(url, 'w') as file:
            file.write(dumps(target.__dict__))

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


@post('/')
def alta_habitacion():
    """ Añade una nueva habitación al Servidor

    Se reciben por JSON el valor del atributo
    plazas, una lista con el equipamiento
    y el precio por noche de la habitacion.

    :returns: Si crea la habitacion response code 200,
    si no response code 400
    """

    data = request.json

    try:
        target = Room(data['plazas'], data['equipamiento'], data['precio'])
        registry[target.id] = target
        update(target.id)

        response.status = 201
        response.content_type = "application/json"
        return dumps(target.__dict__)

    except KeyError:
        response.status = 400
        return 'Los campos plaza, equipamiento y precio son requeridos.'

    except ValueError:
        response.status = 400
        return 'Los campos plazas y precio tienen que ser positivos.'


@delete('/<target_id:int>')
def borrar_habitacion(target_id):
    """
    Selecciona la habitación correspondiente  con la variable target_id

    Busca una habitación en el registro con esa id, si existe y esta
    desocupada la borra. Si no existe o existe pero esta ocupada
    modifica la response de la función de nivel superior con status
    404 o 400 respectivamente y un mensaje informativo, devuelve None

    :param target_id: Identificador único de la habitación.
    :type target_id: int
    :returns: Si funciona HTTPResponse 200 si no HTTPResponse 409 o 404.
    """

    response.content_type = "application/json"
    try:
        target = registry[int(target_id)]
        if not target.disponible:
            response.status = 409
            return dumps({"error_description": f"La habitación {target_id} está ocupada, no se permiten"
                                               f" modificaciones."})
        else:
            del registry[target_id]
            remove(f'ArchivosServidor/Habitacion{target_id}.json')
            return 'True'

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})

    except FileNotFoundError:
        response.status = 200
        return f'La habitación {target_id} no se encontraba en los ficheros del sistema, ha sido eliminada' \
               f' del registro.'


@get('/<target_id:int>/disponibilidad')
def get_disponibilidad(target_id):
    """ Devuelve la disponibilidad de una habitación.

    @:returns: True si está disponible, False caso contrario"""

    try:
        return registry[int(target_id)].disponible
    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} está ocupada, no se permiten"
                                           f" modificaciones."})


@put('/<target_id:int>/disponibilidad')
def modificar_disponibilidad(target_id):
    """ Ocupa una habitación por su id.

    Modifica el valor del parámetro disponible de una habitación,
    este parámetro se pasa por QUERY VARIABLE, por ejemplo:

        .../1/disponibilidad?disponible=true

    Si no existe modifica la response de la función de nivel superior con status
    404 y un mensaje informativo.

    :param target_id: Identificador único de la habitación.
    :type target_id: int

    :returns: True si está disponible, False si está ocupada.
    """

    response.content_type = "application/json"
    try:
        target = registry[int(target_id)]
        if request.query.disponible in ("true", "True", "TRUE"):
            if not target.disponible:
                target.disponible = True

        elif request.query.disponible in ("false", "False", "FALSE"):
            if target.disponible:
                target.disponible = False

        else:
            response.status = 400
            return dumps({"error_description": "La dispobilidad es un valor boleano."})

        update(target_id)
        return dumps(target.disponible)

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


@get('/<target_id>')
def get_habitacion(target_id):
    """ Obtiene una habitación por su id.

    :param target_id: identificador único de la habitación
    :returns:Si existe, objeto por JSON (Response code 200), si no response code 404
    """
    response.content_type = "application/json"
    try:
        return dumps(registry[int(target_id)].__dict__)

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


@get('/')
def get_all():
    """ Devuelve un listado con todas las habitaciones.

    :returns: Listado de todas las habitaciones registradas en el sistema.
    Si no existe ninguna response code 204
    """

    response.content_type = "application/json"
    if len(registry) == 0:
        response.status = 204
    else:
        json_registry = {}
        for key in registry:
            json_registry[key] = registry[key].__dict__
        return dumps(json_registry)


@get('/ocupadas')
def get_ocupadas():
    """Obtiene un listado de todas las habitaciones ocupadas

    :returns Listado de habitacones ocupadas en JSON"""

    response.content_type = "application/json"
    return habitaciones_ocupadas(True)


@get('/disponibles')
def get_disponibles():
    """ Obtiene un listado de todas las habitaciones ocupadas.

    :returns Listado de habitaciones disponibles en JSON"""

    response.content_type = "application/json"
    return habitaciones_disponibles(True)


@get('/<target_id:int>/equipamiento')
def get_equipamiento(target_id):
    """ Devuelve el equipamiento de la habitación.

    :param target_id: Identificador único de la habitación.

    :returns: Listado con el equipamiento de la habitación."""

    response.content_type = "application/json"
    try:
        return dumps(registry[int(target_id)].equipamiento)
    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


# noinspection PyBroadException
@put('/<target_id:int>/equipamiento')
def modificar_equipamiento(target_id):
    """ Sustituye la lista de equipamiento de una
    habitación por la recibida por JSON.
    
    Se recibe la ID por parámetros de la URL y la
    nueva lista de equipamiento por JSON. Esta nueva
    lista sustituye a la que tenía la habitación.

    Si no existe se devuelve una HTTPResponse con
    error 404.

    Si existe pero esta ocupada devuelve una HTTPResponse
    con error 409

    :param target_id: Identificador único de la habitación
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400, 404 o 409 segun el error.
    """

    response.content_type = "application/json"
    try:
        target = registry[int(target_id)]
        if not target.disponible:
            response.status = 409
            return dumps({"error_description": f"La habitación {target_id} está ocupada, no se permiten"
                                               f" modificaciones."})
        elif request.json.get('equipamiento') is None:
            response.status = 400
            return dumps({'error_description': 'El campo equipamiento no se ha encontrado en la petición.'})
        else:
            target.equipamiento = request.json['equipamiento'].copy()
            update(target_id)
            return True

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


@put('/<target_id:int>/equipamiento/add')
def add_equipamiento(target_id):
    """ Añade el nuevo o nuevos equipamiento a la 
    habitación.

    Se recibe una lista por JSON que debe ser anexionada
    a la ya existente. Comprueba que no se repitan
    elementos, es decir, antes de añadir un nuevo
    elemento comprueba que no esté ya en la lista.

    Si no existe se devuelve HTTPResponse con error
    404.

    Si existe pero esta ocupada devuelve una HTTPResponse
    con error 409

    Parameters:
    -----------
    :param target_id: Identificador único de la habitación.
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400, 404 o 409 segun el error.
    """

    try:
        target = registry[int(target_id)]
        if not target.disponible:
            response.status = 409
            return dumps({"error_description": f"La habitación {target_id} está ocupada, no se permiten"
                                               f" modificaciones."})
        else:
            data = request.json['equipamiento']
            for e in data:
                if e not in target.equipamiento:
                    target.equipamiento.append(e)

            update(target_id)
            response.status = 200
            return dumps(target.__dict__)

    except KeyError:
        response.status = 404
        return response


@put('/<target_id:int>/equipamiento/eliminar')
def eliminar_equipamiento(target_id):
    """ Elimina el equipamiento contenido en la lista 
    recibida de la habitación.

    Se recibe una lista por JSON y se eliminan todos
    los elementos coincidentes con la lista de la 
    habitación.

    Si no existe se devuelve HTTPResponse con error
    404.

    Si existe pero esta ocupada devuelve una HTTPResponse
    con error 409

    :param target_id: Identificador único de la habitación.
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400, 404 o 409 segun el error.
    """

    try:
        target = registry[int(target_id)]
        if not target.disponible:
            response.status = 409
            return dumps({"error_description": f"La habitación {target_id} está ocupada, no se permiten"
                                               f" modificaciones."})
        else:
            data = request.json.get('equipamiento')
            response.content_type = "application/json"
            if data is None:
                response.status = 400
                return '{"error_description":"No se ha encontrado el parámetro equipamiento en la petición"}'
            else:
                for e in data:
                    try:
                        target.equipamiento.remove(e)
                    except ValueError:
                        pass

                update(target_id)
                return dumps(target.__dict__)

    except KeyError:
        response.status = 404
        return '{"error_description": "La habitación no está registrada en el sistema."}'


@get('/<target_id:int>/plazas')
def get_plazas(target_id):
    """Devuelve el número de plazas de la habitación

    Si no existe se devuelve HTTPResponse con error
    404.

    :param target_id: Identificador único de la habitación
    :returns Número de plazas de la habitación.
    Si no HTTPResponse 404"""

    response.content_type = "application/json"
    try:
        return registry[int(target_id)].plazas
    except KeyError:
        response.status = 404
        return '{"error_description": "La habitación no está registrada en el sistema."}'


@put('/<target_id:int>/plazas')
def modificar_plazas(target_id):
    """Modifica el número de plazas de la habitación

    El nuevo valor se pasa por QUERY VARIABLE

        .../1/plazas?plazas=4

    Si no existe se devuelve HTTPResponse con error
    404.

    Si existe pero esta ocupada devuelve una HTTPResponse
    con error 409

    :param target_id: Identificador único de la habitación.
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 404 o 409 segun el error.
    """

    response.content_type = "application/json"
    try:
        if not registry[int(target_id)].disponible:
            response.status = 409
            return '{"error_description":"La habitación está ocupada, no se puede modificar."}'
        else:
            registry[int(target_id)].plazas = request.query.plazas
            update(target_id)
            return dumps({'plazas': registry[target_id].plazas})

    except KeyError:
        response.status = 404
        return response


@get('/<target_id:int>/precio')
def get_precio(target_id):
    """Devuelve el precio de la habitación

    Si no existe se devuelve HTTPResponse con error
    404.

    :param target_id: Identificador único de la habitación
    :returns precio de la habitación. Si no HTTPResponse 404"""

    response.content_type = "application/json"
    try:
        return dumps(registry[int(target_id)].precio)
    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


@put('/<target_id:int>/precio')
def modificar_precio(target_id):
    """Modifica el precio por noche de la habitación

    El nuevo valor del precio se pasa por QUERY VARIABLE

    Si no existe se devuelve HTTPResponse con error
    404.

    Si existe pero esta ocupada devuelve una HTTPResponse
    con error 409

    :param target_id: Identificador único de la habitación.
    :returns Si funciona objeto modificado por JSON
    Si no HTTPResponse 404 o 409 segun el error
    """

    try:
        if not registry[int(target_id)].disponible:
            response.status = 409
            return '{"error_description":"La habitación está ocupada, no se puede modificar."}'
        else:
            registry[target_id].precio = request.query.precio
            update(target_id)
            return registry[target_id].precio

    except KeyError:
        response.status = 404
        return dumps({"error_description": f"La habitación {target_id} no está registrada en el sistema."})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Inicializando Servicio')
    logging.info('\t· Buscando ArchivosServidor/')

    # Detección directorio ArchivosServidor
    try:
        mkdir('ArchivosServidor/')
        logging.info('\t\t No se ha detectado el directorio ArchivosServidor, se ha generado uno nuevo.')
    except FileExistsError:
        logging.info('\t\t Directorio ArchivosServidor/ detectado.')

    # Carga de las habitaciones en memoria
    logging.info('\t · Carga de Habitaciones en memoria')
    for h in listdir('ArchivosServidor/'):
        with open(f'ArchivosServidor/{h}', 'r') as file:
            json_data = load(file)
            try:
                habitacion = Room(json_data['plazas'], json_data['equipamiento'], json_data['precio'], json_data['disponible'], json_data['id'])
                registry[habitacion.id] = habitacion
                logging.info(f'\t\t Habitación {habitacion.id} cargada en memoria.')
            except IndexError:
                logging.error(f'El id {json_data["id"]} ya está cargado en memoria, la habitación no ha sido cargada.')

    logging.info('Inicialización finalizada.')
    run(host='localhost', port=8080)