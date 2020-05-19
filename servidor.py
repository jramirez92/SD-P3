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

    try:
        target = registry[target_id]
        target_url = f'ArchivosServidor/Habitacion{target_id}.json'
        if path.exists(target_url):
            with open(target_url, 'rw') as file:
                if load(file) != target.__dict__:
                    file.write(dumps(target.__dict__))

        else:
            with open(target_url,'w') as file:
                file.write(dumps(target.__dict__))

    except KeyError:
        logging.error(f'La id no corresponde a ninguna habitación.')
        raise KeyError


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


@delete('/delete/<target_id>')
def borrar_habitacion(target_id):
    """
    Selecciona la habitación correspondiente  la variable id

    Busca una habitación en el registro con esa id, si existe y esta
    desocupada la borra. Si no existe o existe pero esta ocupada
    modifica la response de la función de nivel superior con status
    404 o 400 respectivamente y un mensaje informativo, devuelve None

    :param target_id: Identificador único de la habitación.
    :type target_id: int
    :returns: Si funciona HTTPResponse 200 si no HTTPResponse 409 o 404.
    """

    try:
        target = registry[target_id]
        if target.disponible:
            response.status = 409
            return f'La habitación {target_id} está ocupada en este momento, debe ser liberada previamente.'
        else:
            del registry[target_id]
            remove(f'ArchivosServidor/Habitacion{target_id}.json')
            return f'La habitación {target_id} ha sido eliminada del sistema.'

    except KeyError:
        response.status = 404
        return f'La habitación {target_id} no está registrada en el sistema.'

    except FileNotFoundError:
        response.status = 200
        return f'La habitación {target_id} no se encontraba en los ficheros del sistema, ha sido eliminada del registro.'


@put('/<target_id>/ocupar')
def ocupar_habitacion(target_id):
    """ Ocupa una habitación por su id.

    Busca una habitación en el registro con esa id, si existe y esta
    desocupada la ocupa. Si no existe o existe pero esta ocupada
    modifica la response de la función de nivel superior con status
    404 o 400 respectivamente y un mensaje informativo, devuelve None

    :param target_id: Identificador único de la habitación.
    :type id: int

    :returns: Si funciona HTTPResponse 200 si no HTTPResponse 409 o 404.
    """

    try:
        target = registry[target_id]
        if target.disponible:
            target.disponible = False
            update(target_id)
            return response
        else:
            response.status = 409
            return f'La habitación {target_id} ya está ocupada'

    except KeyError:
        response.status = 404
        return f'La habitación {target_id} no está registrada en el sistema.'


@put('/<target_id>/liberar')
def liberar_habitacion(target_id):
    """ Libera una habitación por su id.

    Busca una habitación en el registro con esa id, si existe y esta
    ocupada la libera. Si no existe o existe pero esta desocupada
    modifica la response de la función de nivel superior con status
    404 o 400 respectivamente y un mensaje informativo, devuelve None

    :param id: Identificador único de la habitación.
    :type id: int

    :returns: Si funciona HTTPResponse 200 si no HTTPResponse 409 o 404.
    """

    try:
        target = registry[target_id]
        if target.disponible:
            target.disponible = False
            update(target_id)
            return response
        else:
            response.status = 409
            return f'La habitación {target_id} no está ocupada.'

    except KeyError:
        response.status = 404
        return f'La habitación {target_id} no está registrada en el sistema.'


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
        return '{"error_description": "La habitación no está registrada en el sistema."}'


@get('/')
def get_all():
    """ Devuelve un listado con todas las habitaciones.

    :returns: Listado de todas las habitaciones registradas en el sistema.
    """

    response.content_type = "application/json"
    if len(registry) == 0:
        response.status = 204
        return ''
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
        return dumps(registry[target_id].equipamiento)
    except KeyError:
        response.status = 404
        return '{"error_description": "La habitación no está registrada en el sistema."}'


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

    :param target_id: Identificador único de la habitación
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 404.
    """

    try:
        target = registry[target_id]
        target.equipamiento = request.json['equipamiento'].copy()
        update(target_id)

        response.content_type = "application/json"
        return dumps(target.__dict__)

    except KeyError:
        response.content_type = 404
    except Exception:
        response.content_type = 400
    finally:
        return response


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

    Parameters:
    -----------
    :param target_id: Identificador único de la habitación.
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400.
    """

    try:
        target = registry[target_id]
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

    :param target_id: Identificador único de la habitación.
    :returns: Si funciona HTTPResponse 200 con el nuevo objeto
    por JSON. Si no HTTPResponse 400.
    """

    try:
        target = registry[target_id]
        data = request.json['equipamiento']
        for e in data:
            try:
                target.equipamiento.remove(e)
            except ValueError:
                pass

        update(target_id)
        response.content_type = "application/json"
        return dumps(target.__dict__)

    except KeyError:
        response.status = 400
        return response


@get('/<target_id:int>/plazas')
def get_plazas(target_id):
    """Devuelve el número de plazas de la habitación

    :param target_id: Identificador único de la habitación
    :returns Número de plazas de la habitación."""

    try:
        return registry[target_id]['plazas']
    except KeyError:
        response.status = 404
        return '{"error_description": "La habitación no está registrada en el sistema."}'


@put('/<target_id:int>/plazas')
def modificar_plazas(target_id):
    """Modifica el número de plazas de la habitación

    :param target_id: Identificador único de la habitación.
    """

    try:
        registry[target_id]['plazas'] = request.json['plazas']
        update(target_id)
        return response;
    except KeyError:
        response.status = 404
        return response


@get('/<target_id:int>/precio')
def get_precio(target_id):
    response.content_type = "application/json"
    try:
        return dumps(registry[target_id].precio)
    except KeyError:
        response.status = 404
        return '{"error_description":"La habitación no está registrada en el sistema."}'


@put('/<target_id:int>/precio')
def modificar_precio(target_id):
    """Modifica el precio por noche de la habitación

    :param target_id: Identificador único de la habitación.
    :returns Objeto modificado por JSON
    """

    try:
        registry[target_id]['precio'] = request.json['precio']
        update(target_id)
    except KeyError:
        response.status = 404
        return response


@get('/<target_id:int>/estado')
def get_disponibilidad(target_id):

    response.content_type = "application/json"
    try:
        return dumps(registry[target_id].disponible)
    except KeyError:
        response.status = 404
        return '{"error_description":"La habitación no está registrada en el sistema."}'


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
        with open(f'ArchivosServidor/{h}','r') as file:
            json_data = load(file)
            try:
                habitacion = Room(json_data['plazas'], json_data['equipamiento'], json_data['precio'], json_data['id'])
                registry[habitacion.id] = habitacion
                logging.info(f'\t\t Habitación {habitacion.id} cargada en memoria.')
            except IndexError:
                logging.error(f'El id {json_data["id"]} ya está cargado en memoria, la habitación no ha sido cargada.')

    logging.info('Inicialización finalizada.')
    run(host='localhost', port=8080)


