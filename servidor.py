from bottle import run, request, response, HTTPResponse, get

@get('/')
def inicio():
    return 'Hola Mundo'

run(host='localhost', port=8080)