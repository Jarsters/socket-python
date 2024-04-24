import socket
import json
import time

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
        message, username = opener_packet(message)
        if(message == "daftar client"):
            print(f"{username}: Meminta daftar client!")
            packet = wrapper_packet(clients_key_username, address) # Objek Daftar Client
            socket.sendto(packet, address)
        elif(message.lower().startswith("halo server!")):
            username = message.split("Aku ")[1]
            clients_key_username[username] = address
            clients_key_address[address] = username
            print(f"{username}: {message}")
            packet = wrapper_packet(f"Halo Client! Addressmu adalah {address}", address_server)
            socket.sendto(packet, address)
        else:
            print(f"{username}: {message}")


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 55555))
    address_server = server_socket.getsockname()
    clients_key_address[address_server] = "Server"
    clients_key_username["Server"] = address_server

    print("Server online...")

    # message, address = server_socket.recvfrom(1024)

    listener(server_socket)
    server_socket.close()