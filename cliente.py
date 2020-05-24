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
    if r.status_code == 400:
        print(r.json()['error_description'])
    else:
        print("Habitación creada correctamente.")
    iniciar_seleccion()

def borrar_habitacion():
    print("Introduce la ID de la habitación que desea borrar:")
    while True:
        try:
            id_habitacion = int(input("> "))
            if id_habitacion >= 1:
                break
            else:
                print("La ID tiene que ser mayor que 0")
        except ValueError:
            print("Debe introducir números.")
    r = requests.delete(BASE + id_habitacion.__str__(), headers=HEADER)
    if r.status_code == 409 or r.status_code == 404:
        print(r.json()['error_description'])
    else:
        print("Habitación eliminada correctamente.")
    iniciar_seleccion()

def modificar_habitacion():
    print("Introduce la ID de la habitación que desea modificar:")
    while True:
        try:
            id_habitacion = int(input("> "))
            if id_habitacion >= 1:
                break
            else:
                print("La ID tiene que ser mayor que 0")
        except ValueError:
            print("Debe introducir números.")
    r = requests.get(BASE + id_habitacion.__str__(), headers=HEADER)
    if r.status_code == 404:
        print(r.json()['error_description'])
    else:
        print("Elige que opción deseas realizar: ")
        print("     1. Modificar plazas.")
        print("     2. Modificar equipamiento.")
        print("     3. Modificar precio.")
        print("     4. Modificar disponibilidad.")
        print("     5. Salir.")
        while True:
            try:
                opcionseleccionada = int(input("> "))
                if opcionseleccionada >= 1 and opcionseleccionada <= 5:
                    if opcionseleccionada == 1:
                        print("Introduce el nuevo número de plazas de la habitación:")
                        while True:
                            try:
                                plazas = int(input("> "))
                                if plazas >= 1:
                                    break
                                else:
                                    print("El numero de plazas tiene que ser mayor que 0")
                            except ValueError:
                                print("Debe introducir números.")
                        y = requests.put(BASE + id_habitacion.__str__() + '/plazas', params={'plazas': plazas}, headers=HEADER)
                        if y.status_code == 409:
                            print(y.json()['error_description'])
                        else:
                            print("El valor plazas se cambio correctamente.")
                    if opcionseleccionada == 2:
                        print("Elige que opción deseas realizar: ")
                        print("     1. Reemplazar listado completo de equipamiento.")
                        print("     2. Añadir equipamiento.")
                        print("     3. Eliminar equipamiento.")
                        print("     4. Salir.")
                        while True:
                            try:
                                opcionmodificar = int(input("> "))
                                if opcionmodificar >= 1 and opcionmodificar <= 3:
                                    equipamiento = []
                                    print("Introduce el quipamiento de la habitación ('Salir' para seguir con el procedimiento):")
                                    while True:
                                        nuevo_equipamiento = input("> ")
                                        if nuevo_equipamiento == "Salir":
                                            break;
                                        else:
                                            equipamiento.append(nuevo_equipamiento)
                                    datos = {'equipamiento': equipamiento}
                                    if opcionmodificar == 1:
                                        y = requests.put(BASE + id_habitacion.__str__() + '/equipamiento', data=dumps(datos), headers=HEADER)
                                        if y.status_code == 409:
                                            print(y.json()['error_description'])
                                        else:
                                            print("El equipamiento se cambio correctamente")
                                    if opcionmodificar == 2:
                                        y = requests.put(BASE + id_habitacion.__str__() + '/equipamiento/add', data=dumps(datos), headers=HEADER)
                                        if y.status_code == 409:
                                            print(y.json()['error_description'])
                                        else:
                                            print("El nuevo equipamiento se añadio correctamente")
                                    if opcionmodificar == 3:
                                        y = requests.put(BASE + id_habitacion.__str__() + '/equipamiento/eliminar', data=dumps(datos), headers=HEADER)
                                        if y.status_code == 409:
                                            print(y.json()['error_description'])
                                        else:
                                            print("El equipamiento se elimino correctamente")
                                    break
                                else:
                                    if opcionmodificar == 4:
                                        print("Opción seleccionada: Salir.")
                                        break
                                    else:
                                        print("Opción no valida")
                                    break
                                break
                            except ValueError:
                                print("Debe introducir números.")
                    if opcionseleccionada == 3:
                        print("Introduce el nuevo precio por noche de la habitacion:")
                        while True:
                            try:
                                precio = int(input("> "))
                                if precio >= 0:
                                    break
                                else:
                                    print("El precio no puede ser negativo.")
                            except ValueError:
                                print("Debe introducir números.")
                        y = requests.put(BASE + id_habitacion.__str__() + '/precio', params={'precio': precio}, headers=HEADER)
                        if y.status_code == 409:
                            print(y.json()['error_description'])
                        else:
                            print("El precio se cambio correctamente.")
                    if opcionseleccionada == 4:
                        if r.json()['disponible']:
                            y = requests.put(BASE + id_habitacion.__str__() + '/disponibilidad', params={'disponible': False},headers=HEADER)
                        else:
                            y = requests.put(BASE + id_habitacion.__str__() + '/disponibilidad', params={'disponible': True},headers=HEADER)
                        print("La disponibilidad de la habitación se cambio correctamente.")
                    if opcionseleccionada == 5:
                        print("Opción seleccionada: Salir.")
                        break
                    break
                else:
                    print("Opción no valida")
            except ValueError:
                print("Debe introducir números.")
    iniciar_seleccion()

def consultar_habitaciones():
    r = requests.get(BASE, headers=HEADER)
    if r.status_code == 204:
        print("No existen habitaciones registradas en el sistema.")
    else:
        for i in r.json():
            print("ID de la habitación: ", r.json()[i]['id'])
            print("     Plazas: ", r.json()[i]['plazas'])
            print("     Precio: ", r.json()[i]['precio'])
            print("     Equipamiento: ")
            for j in r.json()[i]['equipamiento']:
                print("         ", j)
            print("     Disponible: ", r.json()[i]['disponible'])
    iniciar_seleccion()

def consultar_habitacion():
    print("Introduce la ID de la habitación que desea consultar:")
    while True:
        try:
            id_habitacion = int(input("> "))
            if id_habitacion >= 1:
                break
            else:
                print("La ID tiene que ser mayor que 0")
        except ValueError:
            print("Debe introducir números.")
    r = requests.get(BASE + id_habitacion.__str__(), headers=HEADER)
    if r.status_code == 404:
        print(r.json()['error_description'])
    else:
        print("ID de la habitación: ", r.json()['id'])
        print("     Plazas: ", r.json()['plazas'])
        print("     Precio: ", r.json()['precio'])
        print("     Equipamiento: ")
        for i in r.json()['equipamiento']:
            print("         ", i)
        print("     Disponible: ", r.json()['disponible'])
    iniciar_seleccion()

def consultar_habitaciones_ocupadas():
    r = requests.get(BASE+'ocupadas', headers=HEADER)
    for i in r.json():
        print("ID de la habitación: ", r.json()[i]['id'])
        print("     Plazas: ", r.json()[i]['plazas'])
        print("     Precio: ", r.json()[i]['precio'])
        print("     Equipamiento: ")
        for j in r.json()[i]['equipamiento']:
            print("         ", j)
        print("     Disponible: ", r.json()[i]['disponible'])
    iniciar_seleccion()

def consultar_habitaciones_desocupadas():
    r = requests.get(BASE+'disponibles', headers=HEADER)
    for i in r.json():
        print("ID de la habitación: ", r.json()[i]['id'])
        print("     Plazas: ", r.json()[i]['plazas'])
        print("     Precio: ", r.json()[i]['precio'])
        print("     Equipamiento: ")
        for j in r.json()[i]['equipamiento']:
            print("         ", j)
        print("     Disponible: ", r.json()[i]['disponible'])
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
                    print("Opción seleccionada: Salir.")
                    break
                break
            else:
                print("Opción no valida")
        except ValueError:
            print("Debe introducir números.")

iniciar_seleccion()