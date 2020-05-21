import logging
from random import randint
from unittest import TestCase
from json import dumps
import requests


class Test(TestCase):
    BASE = "http://localhost:8080/"
    HEADER = {'content-type':'application/json'}

    EQUIPAMIENTO = ['Televisión', 'Minibar', 'Teléfono', 'Cocina', 'Aire Acondicionado', 'Terraza',
                    'Cafetera', 'Escritorio']


    @staticmethod
    def generar_equipamiento():
        equipamiento = []
        for _ in range(8):
            candidato = Test.EQUIPAMIENTO[randint(0, 7)]
            if candidato not in equipamiento:
                equipamiento.append(candidato)

        return equipamiento


    def test_alta_habitacion(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.info('Inicializando Test')

        plazas = []
        equipamientos = []
        precios = []

        logging.info('Generando datos de habitaciones.')

        for i in range(50):
            plazas.append(randint(2, 6))
            equipamientos.append(Test.generar_equipamiento())
            precios.append(plazas[i] * len(equipamientos[i]) * randint(3,5))

        logging.info('Inicializando test de AltaHabitación')

        for i in range(50):
            payload = {'plazas':plazas[i], 'equipamiento':equipamientos[i], 'precio':precios[i]}
            r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
            self.assertEqual(r.json()['plazas'], plazas[i])
            self.assertEqual(r.json()['equipamiento'], equipamientos[i])
            self.assertEqual(r.json()['precio'], precios[i])
