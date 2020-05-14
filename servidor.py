from bottle import run, request, response, HTTPResponse, get, post, put
from json import dumps
from room import Room

""" Listado de todas las habitaciones registradas """
registry = {1: Room(2, ['Frigorífico'])}


def seleccionar_habitacion(id, response):
    """
    Selecciona la habitación correspondiente  la variable id

    Busca una habitación en el registro con esa id, si existe la devuelve, si no
    existe modifica la response de la función de nivel superior con status
    404 y un mensaje informativo y devuelve None

    :param id: Identificador único de la habitación.
    :type id: int
    :param response: Respuesta que se va a enviar al cliente
    :type response: Bottle Response
    :return: Habitación coincidente con ID
    """

    target = registry.get(int(id))
    if target is None:
        response.status = 404
        response.body = f'La habitación {id} no está registrada en el sistema.'
        return None
    else:
        return target


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


@post('/')
def alta_habitacion():
    """ Añade una nueva habitación al Servidor

    Se reciben por JSON el valor del atributo
    plazas y una lista con el equipamiento.

    Parameters
    ----------
    plazas: Número de personas que pueden dormir.
    equipamiento: Lista con los extras de la habitaciñon.

    Response
    --------

    """

    data = request.json
    try:
        habitacion = Room(data['plazas'], data['equipamiento'])
        registry[habitacion.id] = habitacion
        response.content_type = "application/json"
        response.body = dumps(habitacion.__dict__)
        return response

    except KeyError:
        response.status = 400
        response.body = 'La petición no incluye todos los elementos requeridos.'


@get('/<id>')
def get_habitacion(id):
    """ Obtiene una habitación por su id.

    Parameters
    ----------
    id: identificador único de la habitación

    Response
    --------
    Si existe, objeto por JSON (Response code 200),
    si no response code 404
    """

    target = seleccionar_habitacion(id, response)

    if target is None:
        return response
    else:
        return dumps(target.__dict__)


@get('/')
def get_all():
    """ Devuelve un listado con todas las habitaciones.

    Response
    --------
    Listado por JSOn con response code 200, si no existe
    ninguna response code 204.
    """

    json_registry = {}
    for key in registry:
        json_registry[key] = registry[key].__dict__
    response.content_type = "application/json"
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

@put('/<id:int>/equipamiento/modificar')
def modificar_equipamiento(id):
    """ Sustituye la lista de equipamiento de una
    habitación por la recibida por JSON.
    
    Se recibe la ID por parámetros de la URL y la
    nueva lista de equipamiento por JSON. Esta nueva
    lista sustituye a la que tenía la habitación.

    Si no existe se devuelve una HTTPResponse con
    error 404.

    Parameters
    ----------
    id: Identificador único de la habitación
    equipamiento: Lista con el nuevo equipamiento.

    Response
    --------
    Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400.
    """

    target = seleccionar_habitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        target.equipamiento = data.copy()
        response.content_type = "application/json"
        return dumps(target.__dict__)


@put('/<id:int>/equipamiento/add')
def add_equipamiento(id):
    """ Añade el nuevo o nuevos equipamiento a la 
    habitación.

    Se recibe una lista por JSON que debe ser anexionada
    a la ya existente. Comprueba que no se repitan
    elementos, es decir, antes de añadir un nuevo
    elemento comprueba que no esté ya en la lista.

    Si no existe se devuelve HTTPResponse con error
    404.

    Parameters:
    -----------
    id: Identificador único de la habitación.
    equipamiento: Lista de equipamiento a añadir.

    Response:
    ---------
    Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400.
    """

    target = seleccionar_habitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        for e in data:
            if e not in target.equipamiento:
                target.equipamiento.append(e)

        response.status = 200
        response.content_type = "application/json"
        return dumps(target.__dict__)


@put('/<id:int>/equipamiento/eliminar')
def eliminar_equipamiento(id):
    """ Elimina el equipamiento contenido en la lista 
    recibida de la habitación.

    Se recibe una lista por JSON y se eliminan todos
    los elementos coincidentes con la lista de la 
    habitación.

    Si no existe se devuelve HTTPResponse con error
    404.

    Parameters:
    -----------
    id: Identificador único de la habitación.
    equipamiento: Lista de equipamiento a eliminar.

    Response:
    ---------
    Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400.
    """

    target = seleccionar_habitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        for e in data:
            try:
                target.equipamiento.remove(e)
            except ValueError:
                pass

        response.content_type = "application/json"
        return dumps(target.__dict__)

@get('/<id:int>/plazas')
def get_plazas(id):
    """Devuelve el número de plazas de la habitación

    :param id: Identificador único de la habitación
    :returns Número de plazas de la habitación."""

    target = seleccionar_habitacion(id, response)

    if target is None:
        return response
    else:
        return target.plazas

@put('/<id:int>/plazas')
def modificar_plazas(id):
    """Modifica el número de plazas de la habitación

    :param id: Identificador único de la habitación.
    :param plazas: JSON con el nuevo número de plazas
    :returns Objeto modificado por JSON
    """

    target = seleccionar_habitacion(id, response)
    if target is None:
        return response
    else:
        try:
            target.plazas = request.json['plazas']
            response.content_type = "application/json"
            return dumps(target.__dict__)
        except KeyError:
            response.status = 400
            response.body = f'No se ha indicado el nuevo número de plazas para habitación {id}.'
            return response


if __name__ == "__main__":
    run(host='localhost', port=8080)
