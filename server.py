#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

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
                self.sip_dir = peticion[1].split(":")[1]
                clients[self.sip_dir] = self.client_address[0]
                # Procesamos la cabecera 'expires'
                cabecera = peticion_lines[1]
                self.expire_sec = int(cabecera.split(" ")[1])
                if self.expire_sec == 0:
                    del clients[self.sip_dir]                
                # Enviamos OK 
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            
            if not peticion_string:
                break
            print "El cliente nos manda " + peticion_string
            
        # Imprimimos la dirección del cliente       
        print self.client_address
        print clients

        self.register2file()
    
    # Lleva un registro de los clientes conectados
    def register2file(self):
        # Abrimos el fichero...
        fich = open('registered.txt','w')
        fich.write('User\tIP\tExpires\r\n')
            
        # Obtenemos el tiempo de expiración
        expire = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()+self.expire_sec))
        clients[self.sip_dir] = [self.client_address[0], expire]
        
        for client in clients.keys():
            fich.write(client + '\t' + clients[client][0] + '\t' + clients[client][1] + '\r\n') 
        fich.close()       
            

# Extraemos el puerto de los argumentos
PORT = int(sys.argv[1])

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    print "Lanzando servidor SIP register..."

    #Inicializamos los diccionarios de clientes
    clients = {}
    clients_time = {}

    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    serv.serve_forever()
