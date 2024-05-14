import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import sys

# Classe che rappresenta il client, estende la classe per creare un app di Tkinter
class ChatClient(tk.Tk):
    
    # Metodo di iniziallizare i nuovi oggetti
    def __init__(self, client_socket):
        super().__init__()
        
        # Salvo in una variabile locale la socket associata al client
        self.client_socket = client_socket
        
        self.title("Chat Client")
        
        # Gestisco la chiusura della finestra in modo tale da disconnettere il client dal server
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        
        # Lista dei messaggi ricevuti
        self.chat_history = scrolledtext.ScrolledText(self, width=60, height=20)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Campo per inserire i messaggi da inviare
        self.entry = tk.Entry(self, width=40)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        # Pulsante per inviare il messaggio inserito
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Creo ed avvio un server che gestisce la ricezzione dei nuovi messaggi
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    # Metodo per inviare il nuovo messaggio al server
    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            # Se il messaggio non é vuoto mando il messaggio
            try:
                self.client_socket.send(message.encode())
                self.entry.delete(0, tk.END)
            except Exception:
                # Gestisco una possibile eccezzione generata dal invio del messaggio
                print("Errore nel invio del messaggio al server")

    # Metodo per la gestione della chiusura del client
    def handle_close(self):
        # Chiudo la socket e chiudo la finestra della gui
        self.client_socket.close()
        self.after(500, self.destroy)

    # Metodo per la gestione della ricezione dei messaggi
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    # Se ricevo un messaggio non vuoto allora lo inserisco nella chat
                    self.chat_history.insert(tk.END, f"{message}\n")
                    self.chat_history.see(tk.END)
                else:
                    # Se riveco un messaggio di lunghezza zero allora vuol dire che sono stato disconnesso dal server quindi esco dal ciclo (smetto di ricevere messaggi)
                    print("Sarai disconnesso dal server...")
                    break
            except (Exception, OSError):
                # Gestisco gli errori generati dalla chiusura del client
                print("Sarai disconnesso dal server...")
                break
        
        # Gestisco la chiusura del clients
        self.handle_close()

if __name__ == "__main__":
    # Chiedo al utente l'ip e la porta del server
    HOST = input("Insert the ip of the server: ")
    PORT = int(input("Insert the port the server is listening to: "))
    
    # Chiedo al utente il nickname che vuole utilizzare nella chat, se non inserisce nulla continuo a chiederglielo
    name = None
    while (not name):
        name = input("Insert your name: ")
        
    # Creo la socket del client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Provo a connettermi con il server
    try:
        # Faccio la richiesta di connessione
        client_socket.connect((HOST, PORT))
        
        # Mando il nickname che ho scelto
        client_socket.send(name.encode())
    except ConnectionRefusedError:
        # Gestisco il fatto che il server sia spento oppure l'indirizzo o porta sbagliati
        print("Server irraggiungibile")
        sys.exit(0)

    # Creo una nuova istanza della view e la lancio
    app = ChatClient(client_socket)
    app.mainloop()
