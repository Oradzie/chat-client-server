import socket
import threading

clients = []

# Funzione per gestire i client
def handle_client(client_socket, addr, name):
    print(f"[NUOVA CONNESSIONE] {name} connesso.")

    while True:
        # Ricevi i dati dal client
        try:
            data = client_socket.recv(1024)
            if data:
                message = (name, data.decode())
                print(message)
                broadcast(message)
            else:
                client_socket.close()
                clients.remove((client_socket, addr, name))
                print(f"[DISCONNESSIONE] {name} disconnesso.")
                break
        except Exception as e:
            break

# Funzione per inviare messaggi a tutti i client
def broadcast(message):
    for client in clients:
        if client[2] != message[0]:
            client[0].send(f"{message[0][1]} {message[1]}".encode())

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
                
                clients.append((client_socket, client_thread, name))

    except KeyboardInterrupt:
        for client in clients:
            print(f"Chiudo il clinet {client[2]}")
            client[0].close()
            client[1].join()
        print("\n[SERVER] Tutti i client disconnessi.")
        print("\n[SERVER] Server chiuso.")
        server.close()
    
if __name__ == "__main__":
    serverStart()