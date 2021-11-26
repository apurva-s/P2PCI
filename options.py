'''
import os
import platform
import socket
# print(os.name)
# print()
print(" Host:","\n","OS:",platform.system(),"OS",platform.version())


port_no = upload_sock.getsockname()[1] 
# gesthostname()




# Server - 

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),7734))
server_ip = socket.gethostname()
serverSocket.listen(1)
while True:
    conn, address = serverSocket.accept()
    break 

# Client - 
selfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
selfSocket.connect((server_ip,7734))



'''





import socket 
import pickle
import os

VERSION = "P2P-CI/1.0"
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
VERSION_NOT_SUPPORTED = 505
STATUS_CODES = {
                OK: "OK",
                BAD_REQUEST: "Bad Request",
                NOT_FOUND: "Not Found",
                VERSION_NOT_SUPPORTED: "P2P-CI Version Not Supported"
                }

def add(socket,rfc_number,rfc_title):
    #connect to the central server

    add_req = f'''ADD RFC {rfc_number} {VERSION},
                  Host: {server_ip}
                  Port: {upload_port}
                  Title: {rfc_title}'''
    
    socket.send(pickle.dumps(add_req))
    response = socket.recv(pickle.loads(response))
    return 
def lookup(rfc_no):
    socketForConnectingToCentralServer.send(bytes("lookup","utf-8"))
    print(socketForConnectingToCentralServer.recv(2048).decode())
    socketForConnectingToCentralServer.send(bytes(str(rfc_no),"utf-8"))
    print("peer for rfc",socketForConnectingToCentralServer.recv(2048).decode())
    return
def lookuplist(socket, upload_port):
    lookup_request = f'''LOOKUP RFC {rfc_number} VERSION,
                     Host:  {server_ip},
                     Port:  {upload_port},
                     Title: {rfc_title}'''
    
    socket.send(bytes("lookuplist","utf-8"))
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
def print_available_options():
    print("1. ADD")
    print("2. LOOKUP/DOWNLOAD")
    print("3. LIST")
    print("4. DISCONNECT")

server_ip = '127.0.0.1'
server_port = 7734
server_address = (server_ip,server_port)
socketForConnectingToCentralServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketForConnectingToCentralServer.connect(server_address)
upload_port = socketForConnectingToCentralServer.getsockname()[1]
# socketForConnectingToCentralServer.send(bytes("Message from the client to the central server","utf-8"))
# print(socketForConnectingToCentralServer.recv(5124))
while True:
    print_available_options()
    ans = int(input("Select your option: "))
    match ans:
      case 1:
        print('add')
        raw = list(map(str,input("Enter space separated RFC number and Title:").split()))
        rfc_number, rfc_title = raw[0],raw[1]
        add(socketForConnectingToCentralServer,rfc_number,rfc_title)
        print("Finished add functionality")
      case 2:
        print("Look up an RFC and download it ")
        rfc_no = list(map(str,input("Enter RFC number:").split()))
        lookup(rfc_no)
      case 3:
        response = lookuplist(socketForConnectingToCentralServer, upload_port)
        print("List RFC\n\nServer Response:\n" + response)
      case 4:
        print("Disconnect")
        disconnect()
    

    
