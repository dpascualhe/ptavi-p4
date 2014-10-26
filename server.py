#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        direccion = str(self.client_address)
        direccion = direccion.split(",")
        ClienteIP = direccion[0][2:-1]
        ClientePuerto = direccion[1][1:-1]
        print "La IP del cliente es: " + ClienteIP
        print "El puerto del cliente es: " + ClientePuerto
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print "El cliente nos manda " + line
            register = line.split(" ")
            if register[0] == "REGISTER":
                objetivo = register[1]
                objetivo = objetivo.split(":")[1]
                diccionario[objetivo] = ClienteIP
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PUERTO = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    diccionario = {}
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
