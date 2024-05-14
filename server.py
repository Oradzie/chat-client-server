import socket
import threading

BUFFER_SIZE = 1024

# Inizializzazione lista contenete tutti i client connessi al server
clients = []

# Funzione per la gestione della rimozione dei client che si disconnessi, rimuovo il client dalla lista, stampo nel terminale del server che l'utente si é disconnesso e faccio una broadcast a tutti informando che l'utente di é disconnesso
def client_remove(client_socket, name):
    clients.remove((client_socket, name))
    print(f"[DISCONNESSIONE] {name} disconnesso.")
    broadcast(f"{name} si é disconnesso")

# Funzione per gestire i client
def handle_client(client_socket, addr, name):
    print(f"[NUOVA CONNESSIONE] {name} connesso.")
    
    # Loop per controllare la ricezione dei dati da parte del client
    while True:
        try:
            data = client_socket.recv(BUFFER_SIZE)
            if data:
                # Se ho ricevuto qualcosa da parte del client allora stampo il messaggio nel terminale del server e faccio una broadcast a tutti client del messaggio
                message = (name, data.decode())
                print(message)
                broadcast(f"{message[0]}: {message[1]}")
            else:
                # Se ricevo un messaggio di lunghezza zero vuol dire che il client ha fatto una close sulla socket e quindi chiudo la connessione, lo rimuovo dalla lista dei client connessi
                client_socket.close()
                client_remove(client_socket, name)
                break
        except (Exception, OSError):
            # Gestisco le eccezzioni dovute dalla chiusura del client da parte del server
            client_remove(client_socket, name)
            break

# Funzione per inviare messaggi a tutti i client
def broadcast(message):
    for client in clients:
        client[0].send(message.encode())

# Funzione per avviare il server
def serverStart():
    # Configurazione dei dati del server
    HOST = '0.0.0.0'
    PORT = 5555

    # Iniziallizazione socket server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permette di riutilizzare l'indirizzo
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] In ascolto su {HOST}:{PORT}")

    # Gestisco le nuove richieste di connessione al server
    try:
        while True:
            # Accetto la richiesta del client
            client_socket, addr = server.accept()
            
            # Aspetto che il client invii il suo nickname
            data = client_socket.recv(1024)
            if data:
                name = data.decode()
            
                # Creo ed avvio il thread che gestisce il nuovo client (ascolta se manda dei messaggi)
                client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, name))
                client_thread.start()
                
                # Comunico agli altri utenti che un nuovo client si é connesso
                broadcast(f"{name} si é unito alla chat room")
                
                # Aggiungo il nuovo client alla lista
                clients.append((client_socket, name))

    except KeyboardInterrupt:
        # Gestisco la chiusura del server tramite interrupt Ctrl+C
        for client in clients:
            print(f"\nChiudo il clinet {client[1]}")
            # Chiudo la scocket con il client
            client[0].close()
        # Libero la lista dei client
        clients.clear()
        print("\n[SERVER] Tutti i client disconnessi.")
        print("\n[SERVER] Server chiuso.")
        # Chiudo il server
        server.close()
    
if __name__ == "__main__":
    # Chiamo la funzione per avviare il server
    serverStart()
