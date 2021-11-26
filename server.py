import socket
from collections import defaultdict
from threading import Lock, Thread
import pickle
active_peers = set()
rfcsNosWithTitles = defaultdict(str)
rfcsNosWithPeers = defaultdict(set)
def client_handle(conn, address):
    while True:
        data = pickle.loads(conn.recv(2046))
        rows = data.splitlines()
        row1 = rows[0].split()
        command = row1[0]
        if command == "ADD":
            with Lock():
                print("In active peers lock")
                active_peers.add(address)
                print(active_peers)
            print("Out of the lock for active peers")
            # conn.send(bytes("Hello from the server","utf-8"))
            # print(conn.recv(1024).decode())
            conn.send(bytes("Received the command","utf-8"))
            rfc_number = conn.recv(1024).decode()
            conn.send(bytes("Received RFC numbers","utf-8"))
            print("received the rfc number",rfc_number)
            with Lock():
                print("In the rfc lock")
                rfcTitle = conn.recv(1024).decode()
                rfcsNosWithTitles[int(rfc_number)] = rfcTitle
                rfcsNosWithPeers[int(rfc_number)].add(address)
                print(rfcsNosWithTitles)
                print(rfcsNosWithPeers)
            
            print("Reached before successfully")
            conn.send(bytes("Successfully made additions","utf-8"))
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
serverSocket.listen(1)
while True:
    conn, address = serverSocket.accept()
    thread = Thread(target=client_handle,args=(conn,address))
    thread.start()
