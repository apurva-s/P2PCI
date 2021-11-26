import socket 
import pickle
def add(socketForConnectingToCentralServer,rfc_number,rfc_title):
    #connect to the central server 
    print(rfc_number,rfc_title)
    socketForConnectingToCentralServer.send(bytes("add","utf-8"))
    print(socketForConnectingToCentralServer.recv(2048).decode())
    socketForConnectingToCentralServer.send(bytes(str(rfc_number),"utf-8"))
    print(socketForConnectingToCentralServer.recv(2048).decode())
    socketForConnectingToCentralServer.send(bytes(str(rfc_title),"utf-8"))
    print("My own client address", socketForConnectingToCentralServer.getsockname())
    #do I have to disconnect before this connection closes? remove from peers  
    print(socketForConnectingToCentralServer.recv(2048).decode())
    return 
def lookup(rfc_no):
    socketForConnectingToCentralServer.send(bytes("lookup","utf-8"))
    print(socketForConnectingToCentralServer.recv(2048).decode())
    socketForConnectingToCentralServer.send(bytes(str(rfc_no),"utf-8"))
    print("peer for rfc",socketForConnectingToCentralServer.recv(2048).decode())
    return
def lookuplist():
    socketForConnectingToCentralServer.send(bytes("lookuplist","utf-8"))
    rfc_d = socketForConnectingToCentralServer.recv(10000)
    # print(rfc_d)
    # for i in rfc_d:
    #     print(rfc_d[i])
#pickle.loads(pickled_animals)
    rfc_d = pickle.loads(rfc_d)
    for i in rfc_d:
        print(i, list(rfc_d[i]))
    # rfc_d = rfc_d[28::]
    # rfc_d = rfc_d[:-1]
    # print(rfc_d)
    return 
def disconnect():
    socketForConnectingToCentralServer.send(bytes("disconnect","utf-8"))
    print(socketForConnectingToCentralServer.recv(2048).decode())
    socketForConnectingToCentralServer.close()
    exit(0)
    return 

server_ip = '127.0.0.1'
server_port = 7734
server_address = (server_ip,server_port)
socketForConnectingToCentralServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketForConnectingToCentralServer.connect(server_address)
# socketForConnectingToCentralServer.send(bytes("Message from the client to the central server","utf-8"))
# print(socketForConnectingToCentralServer.recv(5124))
while True:
    print("1.Add 2.Look Up 3.List 4.Exit")
    ans = input()
    if ans == "1":
        print('add')
        raw = list(map(str,input("Enter space separated RFC number and Title:").split()))
        rfc_number, rfc_title = raw[0],raw[1]
        add(socketForConnectingToCentralServer,rfc_number,rfc_title)
        print("Finished add functionality")
    elif ans == "2":
        print("Look up an RFC and download it ")
        rfc_no = list(map(str,input("Enter RFC number:").split()))
        lookup(rfc_no)
    elif ans == "3":
        print("List")
        lookuplist()
    elif ans == "4":
        print("Disconnect")
        disconnect()
    