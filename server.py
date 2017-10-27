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
        Users = {'User':'', 'IP':''}
        print("CLIENT_IP: ", IP + "\t","CLIENT_PORT: ", PORT)
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        
        for line in self.rfile:
            line = line.decode('utf-8')
            line = line.split(' ')
            Method = line[0]
            if Method == 'REGISTER':
                User = line[1].split(':')[1]
                SIP = line[-1]
                Users['IP'] = IP
                Users['User'] = User
                print(Users)

if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler) 

    print("\n" + "Lanzando servidor UDP LOCAL - Puerto: " + str(PORT) + "\n")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
