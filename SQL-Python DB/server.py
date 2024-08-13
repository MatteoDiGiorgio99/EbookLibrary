import socket
import os
from _thread import *
from DB import *

# Definizione delle variabili
HOST = 'localhost'
PORT = 5050
serverSideSocket = socket.socket()
threadCount = 0


def multi_threaded_client(connection):
    connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))
    connection.close()

# Connessione alla socket
try:
    serverSideSocket.bind((HOST, PORT))
    print('Socket Bind Success!')
except socket.error as err:
    print(str(err))

# Server in ascolto
serverSideSocket.listen(10)
print('Socket is now listening...')

# Accettazione di piu client
while True:
    Client, address = serverSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))
    buf = Client.recv(64)
    #print(buf)
    if "Add" in buf.decode('utf-8'): 
        AddData(buf.decode('utf-8'))
               
    if "View" in buf.decode('utf-8'):
        ViewAll()  
        
    if "Delete" in buf.decode('utf-8'):
        Delete(buf.decode('utf-8'))
        
    if "Update" in buf.decode('utf-8'):   
        Update(buf.decode('utf-8'))
        
    if "Login_Client" in buf.decode('utf-8'):
        Login_Client(buf.decode('utf-8'))

    if "Login_Admin" in buf.decode('utf-8'):
        Login_Admin(buf.decode('utf-8'))
    
    if "AddClient" in buf.decode('utf-8'):
        AddClient(buf.decode('utf-8'))
    
    if "Rental" in buf.decode('utf-8'):
        Rental(buf.decode('utf-8'))
    
    if "Preference" in buf.decode('utf-8'):
        Preference(buf.decode('utf-8'))
       
serverSideSocket.close()

