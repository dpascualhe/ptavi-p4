#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import ast
import time

port = ast.literal_eval(sys.argv[1])
fichero = 'registered.txt'

def register2file(fichero, dicc):
 """
   Imprimir el diccionario de clientes
 """

    fich = open(fichero, 'w')
    for cliente in dicc.keys():
        ip = dicc[user][0]
        tiempo = dicc[user][1]
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tiempo))
        texto = cliente + '\t' + ip + '\t' + str_time + '\r\n'
        fich.write(texto)
    fich.close()

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    SIPRegisterHandler clase
    """

    ListCliente = {}
    def handle(self):

        for i in self.ListCliente.keys():
            if self.ListCliente[i][1] < time.time(): # comparando tiempo de
                del self.ListCliente[i] #expirar y borrar cliente
                print self.ListCliente

        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write("Hemos recibido tu peticion")
        datos_clientes = list(self.client_address)
        print datos_clientes
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            lista = self.rfile.read()
            print lista
            lista = lista.split()
            correo = lista[2]
            ip = datos_clientes(0)
            if lista[0] == 'REGISTER':
                if lista[6] == '0': # comprobamos el expirar
                    if correo in self.ListCliente:
                        del self.ListCliente[correo] # borramos cliente
                    register2file(fichero, ListCliente)
                else:
                    self.ListCliente[correo] = (ip, time.time()+float(lista[6]))
                    # añadimos cliente
                    register2file(fichero, ListCliente) # imprimimos diccionario
                self.wfile.write("SIP/2.0 200 OK\r\n\r\n")
            
            if not lista:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = SocketServer.UDPServer(("", port), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
