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
        while 1:
            # Leemos lo que nos envía el cliente y lo separamos en lineas
            peticion_string = self.rfile.read()
            peticion_lines = peticion_string.split("\r\n")
            peticion = peticion_lines[0].split(" ")
            # Procesamos el REGISTER
            if peticion[0] == "REGISTER":
                sip_dir = peticion[1].split(":")[1]
                clients[sip_dir] = self.client_address[0]
                # Procesamos la cabecera 'expires'
                cabecera = peticion_lines[1]
                expire_time = cabecera.split(" ")[1]
                if expire_time == '0':
                    del clients[sip_dir]                
                # Enviamos OK 
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            if not peticion_string:
                break
            print "El cliente nos manda " + peticion_string
        # Imprimimos la dirección del cliente       
        print self.client_address
        print clients
            

# Extraemos el puerto de los argumentos
PORT = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    print "Lanzando servidor UDP de eco..."
    #Inicializamos el diccionario de clientes
    clients = {}
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    serv.serve_forever()
