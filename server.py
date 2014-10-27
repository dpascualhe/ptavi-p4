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
    Clase para SIP register 
    """
    
    def handle(self):
        # Inicializamos el diccionario de clientes
        clients = {}
        while 1:
            # Leemos lo que nos envía el cliente
            line_string = self.rfile.read()
            line = line_string.split(" ")
            # Procesamos el REGISTER
            if line[0] == "REGISTER":
                sip_dir = line[1].split(":")[1]
                clients[sip_dir] = self.client_address[0]
                # Enviamos OK 
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            if not line_string:
                break
            print "El cliente nos manda " + line_string
        # Imprimimos la dirección del cliente       
        print self.client_address
        print clients
            

# Extraemos el puerto de los argumentos
PORT = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    print "Lanzando servidor UDP de eco..."
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    serv.serve_forever()
