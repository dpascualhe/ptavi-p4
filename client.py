#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])

    if sys.argv[3] == "register":
        LINE = "REGISTER" + " sip:" + sys.argv[4] + " SIP/2.0\r\n" + \
        "Expires: " + sys.argv[5] + "\r\n\r\n"
    else:

        linea = sys.argv[3:]
        LINE = ""
        iteracion = 0
        for palabra in linea:
            iteracion = iteracion + 1
            if iteracion == 1:
                LINE = LINE + palabra
            else:
                LINE = LINE + " " + palabra

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))
    print "Enviando: " + LINE
    my_socket.send(LINE + '\r\n')
    data = my_socket.recv(1024)
    print 'Recibido -- ', data
    print "Terminando socket..."
    my_socket.close()
    print "Fin."
except IndexError:
    print "Usage: client.py ip puerto register sip_address expires_value"
