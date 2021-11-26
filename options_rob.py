import socket 
import os
from collections import defaultdict
from threading import Lock, Thread
import time
from time import gmtime, strftime
import platform

VERSION = "P2P-CI/1.0"
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
VERSION_NOT_SUPPORTED = 505
VERSION = "P2P-CI/1.0,"
CLIENT_OS = platform.platform()
MAX_SEND = 2096
MAX_RCV = 2096
RFC_PATH = "./RFC/Client1/"

client_ip = '127.0.0.1'
active_peers = set()
rfcsNosWithTitles = defaultdict(str)
rfcsNosWithPeers = defaultdict(set)

upload_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
upload_socket.bind(client_ip, 0)
upload_port = upload_socket.getsockname()[1]

def Serve_Clients():
  upload_port.listen()

  while True:
    client_sock, client_address = upload_socket.accept()
    data = client_sock.recv(MAX_RCV)
    rows = data.decode().splitlines()
    row1 = rows[0].split()
    rfcVersion = row1[3]
    command = row1[0]
    row4 = rows[3].split()
    rfcTitle = row4[1]
    if rfcVersion != VERSION:
                response = f"""{VERSION_NOT_SUPPORTED} P2P-CI Version Not Supported"""
                client_sock.sendall(response.encode())
    else:
      rfc_fileName = RFC_PATH + rfcTitle + rfc_number + ".txt"
      current_time = strftime("%a, %d %b %Y %X GMT", gmtime())
      mod_time = strftime("%a, %d %b %Y %X GMT", time.localtime(os.path.getmtime(rfc_fileName)))

      with Lock():
        active_peers.add(client_address)
        rfcsNosWithTitles[int(rfc_number)] = rfcTitle
        rfcsNosWithPeers[int(rfc_number)].add(client_address)
      with open(rfc_fileName, 'r') as open_file:
        fileData = open_file.read()
      dataLength = str(len(fileData))

      response = f"""
                {VERSION} {OK} OK,
                Date: {current_time},
                OS: {CLIENT_OS},
                Last-Modified: {mod_time},
                Content-Length: {dataLength},
                Content-Type: text/text"""

      client_sock.sendall(response.encode())
      client_sock.close()


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
   filedata = " "

   socket.sendall(lookup_request.encode())
   response = socket.recv(MAX_RCV).decode()
   result = input("Download y/n? ")

   if result == "y":
     
     file_path = RFC_PATH + 'rfc' + rfc_number + ".txt"
     new_file = open(file_path, 'w')
     new_file.write(filedata)
     new_file.close()

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
    socketForConnectingToCentralServer.close()
    exit(0)
    return

def download(rfc_number, host, port):


def print_available_options():
    print("1. ADD")
    print("2. LOOKUP/DOWNLOAD")
    print("3. LIST")
    print("4. DISCONNECT")

Serve_Clients = Thread(target=Serve_Clients)
Serve_Clients.start()

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
    

    
