class Room:
    """ Representa una Habitación """

    current_id = 0  # Variable Estática que indica el último número de indetificación asignado.
    assigned_ids = [] # Listado de las Variables Asignadas
    released_ids = [] # Identificaciones que han sido liberadas.

    @staticmethod
    def assign_id(target_id):
        """Intenta asignar la ID indicada

        Si la ID objetivo es -1, buscará la id disponible de menor
        valor. Si es otra buscará si está disponible.

        :param target_id: ID objetivo
        :returns: ID asignada
        :raises Exception: Si la ID objetivo ya está ocupada."""

        assigned_id = -1
        if target_id == -1:
            if len(Room.released_ids) == 0:
                while True:
                    Room.current_id = Room.current_id + 1
                    if Room.current_id not in Room.assigned_ids:
                        break
                assigned_id = Room.current_id

            else:
                assigned_id = Room.released_ids.pop()

        else:
            if target_id in Room.assigned_ids:
                raise Exception(f'El id {id} ya está registrado en el sistema.')
            else:
                assigned_id = target_id

        Room.assigned_ids.append(assigned_id)
        return assigned_id

    def __init__(self, plazas, equipamiento, precio, target_id = -1):
        """ Constructor Parametrizado de Room

        :param plazas: número máximo de ocupantes que pueden alojarse.
        :param equipamiento: lista con todos los servicios.
        :param precio: precio por noche
        """

        # Inicialiación de los atributos del objeto.
        self.id = Room.assign_id(target_id)
        self.plazas = plazas
        self.equipamiento = equipamiento.copy()
        self.precio = precio
        self.disponible = True

    def ocupar(self):
        """ Indica que una habitación ya no está disponible

        Comprueba que la habitación esté disponible y modifica su atributo
        disponible a True

        :raises Exception: Notifica que la habitación ya está ocupada.
        """

        if not self.disponible:
            raise Exception(f'La habitación {self.id} no se puede ocupar puesto que ya está asignada a otro cliente.')
        else:
            self.disponible = False

    def liberar(self):
        """ Indica que una habitación vuelve a estar disponible

        Comprueba que la habitación esté ocupada y modifica su atributo
        disponible a True

        :raises Exception: Notifica que la habitación no está ocupada
        """

        if self.disponible:
            raise Exception(f'La habitación {self.id} no está ocupada.')
        else:
            self.disponible = True