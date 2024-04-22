import socket
import threading
import time

def handle_client(client_socket):
    while True:
        packet = client_socket.recv(1024).decode()
        if(packet.lower() == "halo server"):
            client_socket.send("Ada kebutuhan apa client?".encode())
        else:
            client_socket.send("Aku tidak mengerti dengan pesanmu!".encode())
        print(f"Mengirimkan pesan ke client {clients[client_socket]}")

def routine_message_from_server():
    global clients
    while True:
        for client_socket in clients.keys():
            client_socket.send("Halo ini pesan rutinan dari server".encode())
        time.sleep(10)

threading.Thread(target=routine_message_from_server, daemon=True).start()

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 55555))
    server.listen()
    clients = {}

    while True:
        client_socket, client_address = server.accept()
        clients[client_socket] = client_address
        print(f"Ada client baru terdaftar dari alamat {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()