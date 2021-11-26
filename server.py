import socket
from collections import defaultdict
from threading import Lock, Thread
import time
from time import gmtime, strftime
import os
import platform

MAX_SEND = 2096
MAX_RCV = 2096
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
VERSION_NOT_SUPPORTED = 505
VERSION = "P2P-CI/1.0"
SERVER_OS = platform.platform()
RFC_PATH = "./RFC/Client1/"
active_peers = set()
rfcsNosWithTitles = defaultdict(str)
rfcsNosWithPeers = defaultdict(set)



def client_handle(conn, address):
    while True:
        data = conn.recv(MAX_RCV)
        rows = data.decode().splitlines()
        row1 = rows[0].split()
        command = row1[0]
        if command == "ADD":
            rfc_number = row1[2]
            row4 = rows[3].split()
            rfcTitle = row4[1]
            rfc_fileName = RFC_PATH + rfcTitle + rfc_number + ".txt"
            current_time = strftime("%a, %d %b %Y %X GMT", gmtime())
            mod_time = strftime("%a, %d %b %Y %X GMT", time.localtime(os.path.getmtime(rfc_fileName)))
            
            with Lock():
                active_peers.add(address)
                #print(active_peers)
                rfcsNosWithTitles[int(rfc_number)] = rfcTitle
                rfcsNosWithPeers[int(rfc_number)].add(address)
            with open(rfc_fileName, 'r') as open_file:
                fileData = open_file.read()
            dataLength = str(len(fileData))
            response = f"""
            {VERSION} {OK} OK,
            Date: {current_time},
            OS: {SERVER_OS},
            Last-Modified: {mod_time},
            Content-Length: {dataLength},
            Content-Type: text/text"""
            conn.sendall(response.encode())
        elif command == "lookuplist":
            conn.send(pickle.dumps(rfcsNosWithPeers))

        elif command == "lookup":
            conn.send(bytes("In the look up command on server side","utf-8"))
            with Lock():
                rfc_no = conn.recv(2048).decode()
                rfc_no = int(rfc_no.strip('[').strip(']').replace("'", ""))
                print(type(rfc_no),rfc_no,"rfc_no")
                conn.send(bytes(str(rfcsNosWithPeers[rfc_no]),"utf-8"))
        elif command == "disconnect":
            conn.send(bytes("Connection closing","utf-8"))
            #remove from active peers, remove from RFC 
            # hostname = conn.recv(2048).decode()
            # conn.send(bytes("Hostname reached","utf-8"))
            # port = conn.recv(2048).decode()
            # conn.send(bytes("Port Number reached","utf-8"))
            with Lock():
                print(active_peers,address)
                active_peers.remove(address)
                print("Active peers",active_peers)
                for i in rfcsNosWithPeers:
                    if address in rfcsNosWithPeers[i]:
                        # rfcNumberToBeRemovedFromThatPeer = i
                        rfcsNosWithPeers[i].remove(address)
                print("RFCs With Peers",rfcsNosWithPeers)
                # for i in rfcs:
                #     if rfcs[i][1] == (address):
                #         del rfcs[i]
                # print(rfcs)
            conn.close()
            break 
server_ip = '127.0.0.1'
server_port = 7734
server_address = (server_ip,server_port)
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(server_address)
serverSocket.listen()
while True:
    print('Waiting for clients: ')
    conn, address = serverSocket.accept()
    thread = Thread(target=client_handle,args=(conn,address))
    thread.start()
