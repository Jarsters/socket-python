import socket
import threading
import time
import json

clients = {}

# def handle_client(client_socket):
#     while True:
#         packet = client_socket.recv(1024).decode()
#         if(packet.lower() == "halo server"):
#             client_socket.send("Ada kebutuhan apa client?".encode())
#         else:
#             client_socket.send("Aku tidak mengerti dengan pesanmu!".encode())
#         print(f"Mengirimkan pesan ke client {clients[client_socket]}")

def handle_client(username):
    client_socket = clients[username].get("socket")
    while True:
        try:
            packet = client_socket.recv(1024)
            if(not packet):
                del clients[username]
                return "Done ga bang? Doneeee!"
            packet = packet.decode()
            packet = json.loads(packet)
            if not packet:
                del clients[username]
                break
            elif(packet.lower() == "halo server"):
                client_socket.send(json.dumps("Ada kebutuhan apa client?").encode())
            elif(packet.lower() == "daftar client"):
                packet_result = json.dumps(get_format_client_address())
                client_socket.send(packet_result.encode())
            else:
                client_socket.send(json.dumps("Aku tidak mengerti dengan pesanmu!").encode())
            print(f"Mengirimkan pesan ke client {username}")
        except:
            del clients[username]
            break

def routine_message_from_server():
    global clients
    while True:
        for client in clients.values():
            client.get("socket").send(json.dumps("Halo ini pesan rutinan dari server").encode())
        time.sleep(10)

def get_format_client_address():
    result = []
    for username, client in clients.items():
        result.append((username, client.get("address")[0], client.get("address")[1]))
    return result

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 55555))
    server.listen()
    print("Server online...")

    threading.Thread(target=routine_message_from_server, daemon=True).start()

    while True:
        try:
            client_socket, client_address = server.accept()
            
            username = client_socket.recv(1024).decode()
            username = username.split("username ")[1]
            # client_socket.send(json.dumps(client_address).encode())
            print(f"Ada client baru terdaftar dari alamat {client_address} -- {username}")
            # clients[client_socket] = client_address
            clients[username] = {
                "socket": client_socket,
                "address": client_address
            }
            # threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
            threading.Thread(target=handle_client, args=(username,), daemon=True).start()
        except KeyboardInterrupt as err:
            print(err)
            break
        except Exception as err:
            print(err)
            break
    print("==================AKHIR=====================")