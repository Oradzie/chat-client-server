import socket
import threading

clients = {}

# Funzione per gestire i client
def handle_client(client_socket, addr, name):
    print(f"[NUOVA CONNESSIONE] {name} connesso.")
    
    while True:
        # Ricevi i dati dal client
        data = client_socket.recv(1024)
        if data:
            message = (name, data.decode())
            print(message)
            broadcast(f"{message[0]}: {message[1]}")
        else:
            client_socket.close()
            clients.pop(name)
            print(f"[DISCONNESSIONE] {name} disconnesso.")
            broadcast(f"{name} si é disconnesso")
            break

# Funzione per inviare messaggi a tutti i client
def broadcast(message):
    for client in clients.values():
        client.send(message.encode())

def serverStart():
    # Configurazione del server
    HOST = '0.0.0.0'
    PORT = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permette di riutilizzare l'indirizzo
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] In ascolto su {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            data = client_socket.recv(1024)
            if data:
                name = (addr, data.decode())[-1]
            
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, name))
                client_thread.start()
                
                broadcast(f"{name} si é unito alla chat room")
                
                if name in clients.keys():
                    client_socket.send("Nome giá in uso".encode())
                
                clients[name] = client_socket

    except KeyboardInterrupt:
        for client in clients.values():
            print(f"\nChiudo il clinet {client[1]}")
            client.close()
        clients.clear()
        print("\n[SERVER] Tutti i client disconnessi.")
        print("\n[SERVER] Server chiuso.")
        server.close()
    
if __name__ == "__main__":
    serverStart()