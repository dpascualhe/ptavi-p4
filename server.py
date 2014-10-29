#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time
import os


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):

    """
    Echo server class
    """

    def handle(self):
        """
        Handler de registros SIP
        """
        # Escribe dirección y puerto del cliente (de tupla client_address)
        direccion = str(self.client_address)
        direccion = direccion.split(",")
        self.cliente_ip = direccion[0][2:-1]
        cliente_puerto = direccion[1][1:-1]
        print "La IP del cliente es: ", self.cliente_ip
        print "El puerto del cliente: ", cliente_puerto
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            register = line.split(" ")
            if register[0] == "REGISTER":
                self.objetivo = register[1]
                self.objetivo = self.objetivo.split(":")[1]
                expires = line.split("\r\n")
                expires = expires[1]
                value = expires.split(": ")
                value = value[1]
                segundos = time.time()
                expires = int(segundos) + int(value)
                expires = time.strftime('%Y­%m­%d %H:%M:%S',
                                        time.gmtime(expires))
                lista = [self.cliente_ip, expires]

                for usuario in dicc:
                    if dicc[usuario][1] < \
                        time.strftime('%Y­%m­%d %H:%M:%S',
                                      time.gmtime(time.time())):
                        del dicc[usuario]
                        break

                if int(value) == 0:
                        del dicc[self.objetivo]
                else:

                    dicc[self.objetivo] = lista
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
                self.register2file()
            if not line:
                break
            print "El cliente nos manda " + line

    def register2file(self):
        """
        Archivo que toma los registros de usuarios.
        """
        archivo = open("registered.txt", "w")
        archivo.write("User\tIP\tExpires\n")
        for usuario in dicc:
            year = str(dicc[usuario][1])[0:4]
            month = str(dicc[usuario][1])[6:8]
            day = str(dicc[usuario][1])[10:12]
            hour = str(dicc[usuario][1].split(" ")[1])
            archivo.write(str(usuario) + "\t" +
                          str(dicc[usuario][0]) + "\t" + year + "-" +
                          month + "-" + day + " " + hour + "\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PUERTO = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PUERTO), SIPRegisterHandler)
    dicc = {}
    expiracion = {}
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
