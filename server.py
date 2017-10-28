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

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    
    def handle(self):      # All requests handled by this method

        IP = self.client_address[0]
        PORT =  self.client_address[1]
        Users = {'USER':'', 'IP':'', 'EXPIRES':''}
        print("CLIENT_IP: ", IP + "\t","CLIENT_PORT: ", PORT)

                            # Lee el registro del cliente
        Lines = self.rfile.read()
        Lines = Lines.decode('utf-8')
        Info = Lines.split()
        METHOD = Info[0]
        USER = Info[1].split(':')[1]
        EXPIRES = Info[-1]

        if METHOD == 'REGISTER':
            Users['USER'] = USER
            Users['IP'] = IP
            Users['EXPIRES'] = EXPIRES
        if int(EXPIRES) == 0:
            del Users['USER']
            print(Users)
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        else:
            print(Users)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("\n" + "Lanzando servidor UDP LOCAL - Puerto: " + str(PORT) + "\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
