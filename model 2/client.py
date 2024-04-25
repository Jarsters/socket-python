import socket
import json
import threading
import time

clients_key_address = {}
clients_key_username = {}

def opener_packet(packet):
    packet, username = packet.decode().split(" Pengirim@@ ")
    return json.loads(packet), username

def wrapper_packet(packet, username):
    return (json.dumps(packet) + f" Pengirim@@ {username}").encode()

def update_clients(clients):
    global clients_key_username
    for username, address in clients.items():
        if(username != "Server"):
            clients_key_username[username] = tuple(address)
    # clients_key_username = clients
    print(f"CKU: {clients_key_username}")

def listener(socket: socket.socket):
    while True:
        message, address = socket.recvfrom(1024)
        if not message:
            break
        message, username = opener_packet(message)
        if(type(message) == dict):
            update_clients(message)
        else:
            if(not clients_key_address.get(address)):
                clients_key_address[address] = username
                clients_key_username[username] = address
            print(f"{username}: {message}")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    del s
    return ip


if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ip = get_ip()
    port = int(input("Masukkan port untuk socket: "))
    client_socket.bind(('0.0.0.0', port))
    # client_socket.bind((ip, port))

    server_address = {
        "local": ('192.168.1.6', 55555),
        "vps": ("103.178.153.189", 55555)
    }
    server = None

    print("Daftar server:\
        \n\t1. Local\
        \n\t2. VPS")

    choose = input("Masukkan pilihan server: ")
    if(choose == '1' or choose.lower() == "local"):
        server = server_address["local"]
    elif(choose == '2' or choose.lower() == "vps"):
        server = server_address["vps"]
    else:
        print("Server yang dipilih salah! Mematikan client!")
        exit()

    name = input("Masukkan username: ")

    # client_socket.sendto("Halo server!".encode(), ('192.168.1.6', 55555))
    client_socket.sendto(wrapper_packet(f"Halo server! Aku {name}", name), server)

    time.sleep(1) 

    threading.Thread(target=listener, args=(client_socket,), daemon=True).start()


    while True:
        time.sleep(1)
        usernames = list(clients_key_username.keys())
        print(usernames)
        choose = input("Pilih nomor berapa: ")
        target = None
        address_target = None
        if(not choose):
            target = input("Masukkan nama target: ")
            # address = input("Masukkan address target: ")
            # port = int(input("Masukkan port: "))
            address_target = clients_key_username[target]
            f"{address_target} - {type(address_target)}"
        elif(choose.lower() == "x"):
            target = input("Masukkan username target: ")
            address_target = tuple(clients_key_username[target])
        else:
            choose = int(choose)
            target = usernames[choose - 1]
            address_target = tuple(clients_key_username[target])
        print(f"Target: {target}")
        print(f"Address target: {address_target}")
        packet = input("Masukkan pesan: ")
        if not packet:
            packet = wrapper_packet(f"Halo gua {name} salam kenal!", name)
        else:
            packet = wrapper_packet(packet, name)
        # print(address_target)
        client_socket.sendto(packet, address_target)