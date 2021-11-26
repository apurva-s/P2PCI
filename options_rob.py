import socket 
import os

VERSION = "P2P-CI/1.0"
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
VERSION_NOT_SUPPORTED = 505
MAX_SEND = 2096
MAX_RCV = 2096

def add(socket,rfc_number,rfc_title):
  
    add_req = f"""ADD RFC {rfc_number} {VERSION},
    Host: {server_ip},
    Port: {upload_port},
    Title: {rfc_title}"""
    
    socket.sendall(add_req.encode())
    response = socket.recv(MAX_RCV).decode()

    print("Add RFC" + rfc_number)
    print("Server response:")
    print(response)

    return 
def lookup(socket, rfc_number, rfc_title):
   lookup_request = f"""LOOKUP RFC {rfc_number} {VERSION},
   Host: {server_ip},
   Port: {upload_port},
   Title: {rfc_title}"""
   
   socket.sendall(lookup_request.encode())
   response = socket.recv(MAX_RCV).decode()
   return

def lookuplist(socket, upload_port):
  lookuplist_request = f"""LOOKUPLIST ALL {VERSION},
  Host: {server_ip},
  Port: {upload_port}"""
  socket.sendall(lookuplist_request.encode())
  response = socket.recv(MAX_RCV).decode()
  print("List RFC")
  print("Server response:")
  print(response)
    # print(rfc_d)
    # for i in rfc_d:
    #     print(rfc_d[i])
#pickle.loads(pickled_animals)
   # rfc_d = pickle.loads(rfc_d)
   # for i in rfc_d:
    #    print(i, list(rfc_d[i]))
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
        print('Add RFC action')
        raw = list(map(str,input("Enter space separated RFC number and Title:").split()))
        rfc_number, rfc_title = raw[0],raw[1]
        add(socketForConnectingToCentralServer,rfc_number,rfc_title)
        print("Finished add functionality")
      case 2:
        print("Look up an RFC and download it ")
        raw = list(map(str,input("Enter space separated RFC number and Title:").split()))
        rfc_number, rfc_title = raw[0],raw[1]
        lookup(socketForConnectingToCentralServer, rfc_number, rfc_title)
      case 3:
        response = lookuplist(socketForConnectingToCentralServer, upload_port)
        print("List RFC\n\nServer Response:\n" + response)
      case 4:
        print("Disconnect")
        disconnect()
    

    
