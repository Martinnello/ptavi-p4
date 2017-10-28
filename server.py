#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Servidor de eco en UDP simple
"""
import sys
import socketserver
import json
import time


try:
    PORT = int(sys.argv[1]) 
except IndexError:
    sys.exit("    Usage:   python3 server.py <Port>")

Users = {}

class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    def register2_json(self):       # MAKE JSON FILE
    
        with open("registered.json", "w") as jsonfile:
            json.dump(Users, jsonfile, indent=3)
    
    def handle(self):      # All requests handled by this method
        IP = self.client_address[0]
        PORT =  self.client_address[1]
        print("CLIENT_IP: ", IP + "\t","CLIENT_PORT: ", PORT)

        Lines = self.rfile.read()
        Info = Lines.decode('utf-8').split()
        METHOD = Info[0]
        USER = Info[1].split(':')[1]
        EXPIRES = Info[-1]
        time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))

        if METHOD == 'REGISTER':
            Users[USER] = ["IP: " + str(IP), "EXPIRES: " + str(EXPIRES)]
            self.register2_json()
        if int(EXPIRES) == 0:
            del Users[USER]
            self.register2_json()
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print(Users)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("\n" + "Lanzando servidor UDP LOCAL - Puerto: " + str(PORT) + "\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
