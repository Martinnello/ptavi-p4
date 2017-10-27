#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor de eco en UDP simple
"""
import sys
import socketserver


class EchoHandler(socketserver.DatagramRequestHandler):
    def handle(self):      # (all requests handled by this method)
        
        self.wfile.write("Hemos recibido tu peticion")
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'))

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', 6001), EchoHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
