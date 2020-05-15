from unittest import TestCase
from json import dumps
import requests


class Test(TestCase):
    BASE = "http://localhost:8080/"
    HEADER = {'content-type':'application/json'}

    def test_alta_habitacion_1(self):
        self.plazas1 = 2
        self.equipamiento1 = ['Aire Acondicionado','Televisión','Minibar']
        self.precio1 = 15
        payload = {'plazas':self.plazas1, 'equipamiento':self.equipamiento1, 'precio':self.precio1}
        r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
        self.assertEqual(r.json()['plazas'],self.plazas1)
        self.assertEqual(r.json()['equipamiento'], self.equipamiento1)
        self.assertEqual(r.json()['precio'],self.precio1)


    def test_alta_habiacion_2(self):
        self.plazas2 = 4
        self.equipamiento2 = ['Aire Acondicionado','Televisión','Minibar','Terraza']
        self.precio2 = 30
        payload = {'plazas':self.plazas2, 'equipamiento':self.equipamiento2, 'precio':self.precio2}
        r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
        self.assertEqual(r.json()['plazas'],self.plazas2)
        self.assertEqual(r.json()['equipamiento'], self.equipamiento2)
        self.assertEqual(r.json()['precio'],self.precio2)

    def test_alta_habiacion_3(self):
        self.plazas3 = 1
        self.equipamiento3 = ['Minibar','Terraza']
        self.precio3 = 5
        payload = {'plazas':self.plazas3, 'equipamiento':self.equipamiento3, 'precio':self.precio3}
        r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
        self.assertEqual(r.json()['plazas'],self.plazas3)
        self.assertEqual(r.json()['equipamiento'], self.equipamiento3)
        self.assertEqual(r.json()['precio'],self.precio3)

    def test_alta_habitacion_4(self):
        self.plazas4 = 5
        self.equipamiento4 = ['Minibar','Terraza', 'Aire Acondicionado', 'Televisión', 'Piscina']
        self.precio4 = 60
        payload = {'plazas':self.plazas4, 'equipamiento':self.equipamiento4, 'precio':self.precio4}
        r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
        self.assertEqual(r.json()['plazas'],self.plazas4)
        self.assertEqual(r.json()['equipamiento'], self.equipamiento4)
        self.assertEqual(r.json()['precio'],self.precio4)

    def test_alta_habitacion_5(self):
        self.plazas5 = 1
        self.equipamiento5 = []
        self.precio5 = 5
        payload = {'plazas': self.plazas5, 'equipamiento': self.equipamiento5, 'precio':self.precio5}
        r = requests.post(Test.BASE, data=dumps(payload), headers=Test.HEADER)
        self.assertEqual(r.json()['plazas'], self.plazas5)
        self.assertEqual(r.json()['equipamiento'], self.equipamiento5)
        self.assertEqual(r.json()['precio'],self.precio5)