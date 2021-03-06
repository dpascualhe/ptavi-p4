#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys


# Cliente UDP simple.

# Control de uso
if len(sys.argv) != 6 or sys.argv[3] != "register":
    print "Usage: client.py ip puerto register sip_address expires_value"
    raise SystemExit


# Dirección IP del servidor.
SERVER = sys.argv[1]
PORT = int(sys.argv[2])

# Formamos la peticion
PETICION = ""
PETICION = "REGISTER sip:" + sys.argv[4] + " SIP/2.0\r\n"
PETICION += "Expires: " + sys.argv[5] + "\r\n"


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

# Enviamos un string
print "Enviando: " + PETICION
my_socket.send(PETICION + '\r\n')

# Recibimos datos del servidor
data = my_socket.recv(1024)
print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
