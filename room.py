class Room:
    """ Representa una Habitación """


    id = 0  # Variable Estática que indica el último número de indetificación asignado.


    def __init__(self, plazas, equipamiento, precio=10):
        """ Constructor Parametrizado de Room

        :param plazas: número máximo de ocupantes que pueden alojarse.
        :param equipamiento: lista con todos los servicios.
        """

        Room.id = Room.id + 1 # Aumentamos en 1 el último ID

        # Inicialiación de los atributos del objeto.
        self.id = Room.id
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


