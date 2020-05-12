from bottle import run, request, response, HTTPResponse, get, post, put

""" Listado de todas las habitaciones registradas """
habitaciones = []

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

    # TO-DO : ISSUE 10 #
    pass

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

@put('/<id>')
def modificarHabitacion(id):
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

    # TO DO : ISSUE 8 #
    pass


@put('/<id>/add_eqipment')
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

    # TO-DO : ISSUE 8 #
    pass

@put('/<id>/del_equipment')
def delEquipamiento(id):
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

    # TO-DO : ISSUE 8 #
    pass





run(host='localhost', port=8080)