#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import ast

port = ast.literal_eval(sys.argv[1])
Cliente = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
	datos_clientes = list(self.client_address)
	print datos_clientes
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            cadena = self.rfile.read()
			if cadena != "":
				lista = cadena.split()
		        if lista[0] == 'REGISTER':
					correo = lista[1]
					correo = correo.split(":")[1]
					ip = self.client_address[0]
					Cliente[correo] = [ip]
					self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
			else:
				break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", port), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
