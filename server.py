#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Servidor UDP con handle de registro."""

import sys
import socketserver
import json
import time


try:
    PORT = int(sys.argv[1])
except IndexError:
    sys.exit("    Usage:   python3 server.py <Port>")


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """SIP Register and save users in .json file."""

    Users = {}

    def json2registered(self):
        """See if registered.json exist."""
        try:
            with open('registered.json', 'r') as jsonfile:
                self.Users = json.load(jsonfile)
        except FileNotFoundError:
            pass

    def register2_json(self):
        """Make registered.json file."""
        with open("registered.json", "w") as jsonfile:
            json.dump(self.Users, jsonfile, indent=3)

    def handle(self):
        """All requests handled by this method."""
        self.json2registered()
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print("CLIENT_IP: ", IP + "\t", "CLIENT_PORT: ", PORT)

        Lines = self.rfile.read()
        Info = Lines.decode('utf-8').split()
        METHOD = Info[0]
        USER = Info[1].split(':')[1]
        EXPIRES = int(Info[-1])
        Time = '%Y-%m-%d %H:%M:%S'

        if METHOD == 'REGISTER':
            try:
                if EXPIRES == 0:
                    del self.Users[USER]
                else:
                    EXPIRES += time.time()
                    Date = (time.strftime(Time, time.localtime(EXPIRES)))
                    self.Users[USER] = [str(IP), str(Date)]
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            except KeyError:
                print("User unregistered")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")

            Del_List = []
            Now = time.localtime(time.time())

            for user in self.Users:
                Date = time.strptime(self.Users[user][1], Time)
                if Date <= Now:
                    Del_List.append(user)

            for user in Del_List:
                del self.Users[user]

            print(self.Users)
            self.register2_json()


if __name__ == "__main__":
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("\n" + "Lanzando servidor UDP LOCAL - Puerto: " + str(PORT) + "\n")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "Servidor finalizado")
