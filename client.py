#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 22:03:17 2024

@author: oradzie
"""

import tkinter as tk
from tkinter import scrolledtext
import socket
import threading

class ChatClient(tk.Tk):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.name = ''
        self.title("Chat Client")
        
        self.chat_history = scrolledtext.ScrolledText(self, width=60, height=20)
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.entry = tk.Entry(self, width=40)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        
        # popup = tk.Toplevel(self)
        # popup.title("Inserisci nome")
        # name_entry = tk.Entry(popup, width=40)
        # name_entry.grid(row=1, column=0, padx=10, pady=10)
        
        # confirm_name = tk.Button(popup, text="Conferma", command=self.client_socket.send(name_entry.get().encode()))
        # confirm_name.grid(row=1, column=1, padx=10, pady=10)
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        # name = input("Insert your name: ")
        self.client_socket.send("Orazio".encode())
        
        # Start a thread to receive messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def send_message(self, event=None):
        message = self.entry.get()
        if message:
            self.client_socket.send(message.encode())
            self.entry.delete(0, tk.END)
            self.chat_history.insert(tk.END, f"Tu: {message}\n")
            self.chat_history.see(tk.END)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                message = message.split(' ')
                self.chat_history.insert(tk.END, f"{message[0]}: {' '.join(message[1:])}\n")
                self.chat_history.see(tk.END)
            except Exception as e:
                print("[ERRORE]", e)
                break

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 5555

    app = ChatClient(HOST, PORT)
    app.mainloop()
