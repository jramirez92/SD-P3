# -*- coding: utf-8 -*-
from json import dumps
import requests

BASE = "http://localhost:8080/"
HEADER = {'content-type': 'application/json'}

def alta_habitacion():
    print("Introduce el número de plazas de la habitación:")
    while True:
        try:
            plazas = int(input("> "))
            if plazas >= 1:
                break
            else:
                print("El numero de plazas tiene que ser mayor que 0")
        except ValueError:
            print("Debe introducir números.")
    equipamiento = []
    print("Introduce el quipamiento de la habitación ('Salir' para seguir con el procedimiento):")
    while True:
        nuevo_equipamiento = input("> ")
        if nuevo_equipamiento == "Salir":
            break;
        else:
            equipamiento.append(nuevo_equipamiento)
    print("Introduce el precio por noche de la habitacion:")
    while True:
        try:
            precio = int(input("> "))
            if precio >= 0:
                break
            else:
                print("El precio no puede ser negativo.")
        except ValueError:
            print("Debe introducir números.")

    payload = {'plazas': plazas, 'equipamiento': equipamiento, 'precio': precio}
    r = requests.post(BASE, data=dumps(payload), headers=HEADER)
    print("Habitacion creada.")
    iniciar_seleccion()

def borrar_habitacion():
    print("Opcion seleccionada borrar habitacion")
    iniciar_seleccion()

def modificar_habitacion():
    print("Opcion seleccionada modificar habitacion")
    iniciar_seleccion()

def consultar_habitaciones():
    print("Opcion seleccionada consultar todas las habitaciones")
    iniciar_seleccion()

def consultar_habitacion():
    print("Opcion seleccionada consultar una habitacion")
    iniciar_seleccion()

def consultar_habitaciones_ocupadas():
    print("Opcion seleccionada consultar habitaciones ocupadas")
    iniciar_seleccion()

def consultar_habitaciones_desocupadas():
    print("Opcion seleccionada consultar habitaciones desocupadas")
    iniciar_seleccion()

def iniciar_seleccion():
    print("Elige que opción deseas realizar: ")
    print("     1. Dar de alta una habitación.")
    print("     2. Eliminar una habitación.")
    print("     3. Modificar los datos de una habitación.")
    print("     4. Consultar la lista completa de habitaciones.")
    print("     5. Consultar una habitación mediante identificador.")
    print("     6. Consultar la lista de habitaciones ocupadas.")
    print("     7. Consultar la lista de habitaciones desocupadas.")
    print("     8. Salir.")
    while True:
        try:
            opcionseleccionada = int(input("> "))
            if opcionseleccionada >=1 and opcionseleccionada <=8:
                if opcionseleccionada == 1:
                    alta_habitacion()
                if opcionseleccionada == 2:
                    borrar_habitacion()
                if opcionseleccionada == 3:
                    modificar_habitacion()
                if opcionseleccionada == 4:
                    consultar_habitaciones()
                if opcionseleccionada == 5:
                    consultar_habitacion()
                if opcionseleccionada == 6:
                    consultar_habitaciones_ocupadas()
                if opcionseleccionada == 7:
                    consultar_habitaciones_desocupadas()
                if opcionseleccionada == 8:
                    print("Opcion seleccionada Salir.")
                    break
                break
            else:
                print("opcion no valida")
        except ValueError:
            print("Debe introducir números.")

iniciar_seleccion()