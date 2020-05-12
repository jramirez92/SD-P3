from bottle import run, request, response, HTTPResponse, get, post, put
from json import dumps
from room import Room

""" Listado de todas las habitaciones registradas """
registry = {1: Room(2, ['Frigorífico'])}


def seleccionarHabitacion(id, response):
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


@post('/')
def altaHabitacion():
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

    # TO DO : ISSUE 7 #
    pass


@get('/<id>')
def getHabitacion(id):
    """ Obtiene una habitación por su id.

    Parameters
    ----------
    id: identificador único de la habitación

    Response
    --------
    Si existe, objeto por JSON (Response code 200),
    si no response code 404
    """

    target = seleccionarHabitacion(id, response)

    if target is None:
        return response
    else:
        return dumps(target.__dict__)


@get('/')
def getAll():
    """ Devuelve un listado con todas las habitaciones.

    Response
    --------
    Listado por JSOn con response code 200, si no existe
    ninguna response code 204.
    """

    # TO-DO : ISSUE 9 #
    pass


@put('/<id:int>/equipamiento/modificar')
def modificarEquipamiento(id):
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

    target = seleccionarHabitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        target.equipamiento = data.copy()
        return dumps(target.__dict__)


@put('/<id:int>/equipamiento/add')
def addEquipamiento(id):
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

    target = seleccionarHabitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        for e in data:
            if e not in target.equipamiento:
                target.equipamiento.append(e)

        response.status = 200
        return dumps(target.__dict__)


@put('/<id:int>/equipamiento/eliminar')
def eliminarEquipamiento(id):
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

    target = seleccionarHabitacion(id, response)

    if target is None:
        return response
    else:
        data = request.json['equipamiento']
        for e in data:
            try:
                target.equipamiento.remove(e)
            except ValueError:
                pass

        return dumps(target.__dict__)

@get('/<id:int>/plazas')
def getPlazas(id):
    """Devuelve el número de plazas de la habitación

    :param id: Identificador único de la habitación
    :returns Número de plazas de la habitación."""

    target = seleccionarHabitacion(id,response)

    if target is None:
        return response
    else:
        return target.plazas

@put('/<id:int>/plazas')
def modificarPlazas(id):
    """Modifica el número de plazas de la habitación

    :param id: Identificador único de la habitación.
    :param plazas: JSON con el nuevo número de plazas
    :returns Objeto modificado por JSON
    """

    target = seleccionarHabitacion(id,response)
    if target is None:
        return response
    else:
        try:
            target.plazas = request.json['plazas']
            return dumps(target.__dict__)
        except KeyError:
            response.status = 400
            response.body = f'No se ha indicado el nuevo número de plazas para habitación {id}.'
            return response


if __name__ == "__main__":
    run(host='localhost', port=8080)
