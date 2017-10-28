#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cliente UDP con socket a un servidor
"""
import sys
import socket


try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    METHOD = str.upper(sys.argv[3])
    USER = sys.argv[4]
    EXPIRES = sys.argv[5]

    Register = METHOD + " sip:" + str(USER) + " SIP/2.0\r\n"
    Expire = "Expires: " + str(EXPIRES) + "\r\n\r\n"
    Info = Register + Expire
    print("Enviando:", Info)

except IndexError:
    sys.exit(" Usage: python3 client.py IP Port register Mail exp_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((IP, PORT))

    if METHOD == "REGISTER":
        my_socket.send(bytes(Info, 'utf-8'))
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
    else:
        sys.exit(" Usage: python3 client.py IP Port register Mail exp_value")

print("Socket terminado. \r\n")
