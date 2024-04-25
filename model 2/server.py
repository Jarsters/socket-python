import socket
import json
import time
import threading
from pprint import pprint

clients_key_address = {}
clients_key_username = {}

# def send_message(socket: socket.socket, message):
#     message, address = socket.recvfrom(1024)
#     message = json.dumps(message).encode()
#     for client in clients.values():
#         socket.sendto(message.encode(), client.get("address"))

def opener_packet(packet):
    packet, username = packet.decode().split(" Pengirim@@ ")
    return json.loads(packet), username

def wrapper_packet(packet, address):
    sender = clients_key_address[address]
    return (json.dumps(packet) + f" Pengirim@@ {sender}").encode()

def listener(socket: socket.socket):
    global address_server
    while True:
        message, address = socket.recvfrom(1024)
        if not message:
            break
        print(f"{address} - {type(address)}")
        message, username = opener_packet(message)
        if(message == "daftar client"):
            print(f"{username}: Meminta daftar client!")
            pprint(clients_key_username)
            packet = wrapper_packet(clients_key_username, address) # Objek Daftar Client
            socket.sendto(packet, address)
        elif(message.lower().startswith("halo server!")):
            username = message.split("Aku ")[1]
            clients_key_username[username] = address
            clients_key_address[address] = username
            print(f"{username}: {message}")
            packet = wrapper_packet(f"Halo Client! Addressmu adalah {address}", address_server)
            socket.sendto(packet, address)
        elif(message.lower().startswith("kirim ke")):
            clear_message = message.replace("kirim ke ", "")
            username_target, message = clear_message.split(" @@pesan@@ ")
            print(address)
            target = clients_key_username[username_target]
            packet = wrapper_packet(f"{message}", address)
            socket.sendto(packet, target)
        else:
            print(f"{username}: {message}")

# def ping_every_clients(server_socket):
#     # server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     # server_socket.bind(('0.0.0.0', 55556))
#     while True:
#         sender_address = clients_key_username["Server"]
#         packet = wrapper_packet("", sender_address)
#         for client_target in clients_key_username.values():
#             print(client_target)
#             server_socket.sendto(packet, client_target)
#         time.sleep(3)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    del s
    return ip

if __name__ == "__main__":
    ip = get_ip()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((ip, 55555))
    address_server = server_socket.getsockname()
    clients_key_address[address_server] = "Server"
    clients_key_username["Server"] = address_server

    print("Server online...")

    listener(server_socket)
    server_socket.close()