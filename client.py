import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClient(tk.Tk):
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.title("Chat Client")
        
        self.protocol("WM_DELETE_WINDOW", self.handle_close)
        
        self.chat_history = scrolledtext.ScrolledText(self, width=60, height=20)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.entry = tk.Entry(self, width=40)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        
        # Start a thread to receive messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.entry.delete(0, tk.END)

    def handle_close(self):
        self.client_socket.close()
        self.after(500, self.destroy)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.chat_history.insert(tk.END, f"{message}\n")
                    self.chat_history.see(tk.END)
                else:
                    print("Sarai disconnesso dal server...")
                    break
            except (Exception, OSError):
                print("Sarai disconnesso dal server...")
                break
            
        self.handle_close()

if __name__ == "__main__":
    HOST = input("Insert the ip of the server: ")
    PORT = int(input("Insert the port the server is listening to: "))
    name = input("Insert your name: ")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.send(name.encode())

    app = ChatClient(client_socket)
    app.mainloop()
