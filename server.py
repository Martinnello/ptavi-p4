#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor de eco en UDP simple
"""
import sys
import socketserver


try:
    PORT = int(sys.argv[1]) 
except IndexError:
    sys.exit("    Usage:   python3 server.py <Port>")


class EchoHandler(socketserver.DatagramRequestHandler):
    def handle(self):      # (all requests handled by this method)
        
        IP = self.client_address[0]
        PORT =  self.client_address[1]
        print("CLIENT_IP: ", IP + "\t","CLIENT_PORT: ", PORT)
        self.wfile.write(b"Peticion recibida")
        for line in self.rfile:
            print("El cliente envia: ", line.decode('utf-8'))

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), EchoHandler) 

    print("\n" + "Lanzando servidor UDP LOCAL - Puerto: " + str(PORT) + "\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
