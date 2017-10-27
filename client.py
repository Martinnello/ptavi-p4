#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Cliente UDP con socket a un servidor
"""
import sys
import socket


try:
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    MESSAGE = sys.argv[3] 
   
    if len(sys.argv) > 3:
        MESSAGE = ''
        CADENA = sys.argv [3:]
        for item in CADENA:
            MESSAGE += ' ' + ite  

except IndexError:
    sys.exit("    Usage:   python3 client.py <Server> <Port> <Message>")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, PORT))
    print("Enviando:", MESSAGE)
    my_socket.send(bytes(MESSAGE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
