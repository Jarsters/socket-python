import socket
import threading

def listen_server(client):
    while True:
        data = client.recv(1024).decode()
        print(f"Server: {data}")

def send_message_to_server(client, message):
    client.send(message.encode())

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect(("103.178.153.189", 55555))
    threading.Thread(target=listen_server, args=(client,), daemon=True).start()
    while True:
        message = input("Pesan: ")
        if(message.lower() == "exit"):
            break
        send_message_to_server(client, message)