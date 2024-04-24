import socket
import threading
import json
from typing import Any
import time

clients = []

def listen_server(client, who="Server"):
    while True:
        try:
            data = client.recv(1024)
            data = data.decode()
            data = json.loads(data)
            # print(f"Server: {data}")
            print(f"{who}: {data}")
        except ConnectionAbortedError:
            return "Done ga bang, doneeeee!"
        if(not data):
            return "Done ga bang, doneeeee!"

def routine_message_to_connected_client():
    global clients
    while True:
        for client in clients:
            client.send(json.dumps("Halo ini pesan rutinan dari gue bro").encode())
        time.sleep(10)

def handle_another_client(socket_to_tracker: socket.socket, address):
    socket_with_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config_socket(socket_with_client)
    print(f"Socket to tracker: {socket_to_tracker}")
    # socket_with_client.bind(socket_to_tracker.getsockname())
    print(f"Address: {address}")
    socket_with_client.bind(address)
    socket_with_client.listen()

    threading.Thread(target=routine_message_to_connected_client, daemon=True).start()
    
    while True:
        client_socket, _ = socket_with_client.accept() # _ = client_address
        clients.append(client_socket)
        print("Ada client baru konek")
        threading.Thread(target=listen_server, args=(client_socket, "Client"), daemon=True).start()

def send_message_to_server(client, message):
    client.send(json.dumps(message).encode())

def connecting_to_another_client():
    socket_connecting_to_another_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config_socket(socket_connecting_to_another_client)
    sender = input("Masukkan nama pengirim: ")
    address = input("Masukkan adress: ")
    port = int(input("Masukkan port address: "))
    socket_connecting_to_another_client.connect((address, port))

    threading.Thread(target=listen_server, args=(socket_connecting_to_another_client, sender), daemon=True).start()
    while True:
        message = input("Pesan: ")
        if(message.lower() == "exit"):
            client.close()
            break
        send_message_to_server(socket_connecting_to_another_client, message)

def config_socket(sockets: socket.socket):
    try:
        sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except:
        sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        # sockets.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    config_socket(client)
    # try:
    #     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # except:
    #     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    #     # client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(("103.178.153.189", 55555))
    # client.connect(("192.168.1.6", 55555))
    print(f"IP Socket Client: {client.getsockname()}")

    username = input("Masukkan username: ")
    client.send(f"username {username}".encode())

    ip_public = input("Masukkan ip: ")
    port = int(input("Masukkan port: "))
    address = (ip_public, port)

    threading.Thread(target=handle_another_client, args=(client,address,), daemon=True).start()
    threading.Thread(target=listen_server, args=(client,), daemon=True).start()

    while True:
        message = input("Pesan: ")
        if(message.lower() == "exit"):
            client.close()
            break
        send_message_to_server(client, message)
    connecting_to_another_client()