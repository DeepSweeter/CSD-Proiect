import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from rc6 import *
import socket

dir_path = ".//Received Data"
file_names = [i for i in os.listdir(dir_path) if i.endswith('.txt')]
file_names.insert(0, "None")

class mainPanel:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.geometry("1000x510")
        self.window.title("RC6 network aplication")
        self.window.resizable(False, False)

        # Buttons

        # Button open
        self.openButton = tk.Button(self.window, text="<- Open File", command=self.open_file, background="white", foreground="red",
                               font=("Times New Roman", 11, "bold"), relief="groove")
        self.openButton.place(x=450, y=20, width=95, height=45)

        # Button crypt
        self.cryptButton = tk.Button(self.window, text="Encrypt ->", command=self.bencrypt, background="white", foreground="darkblue",
                                font=("Times New Roman", 11, "bold"), relief="groove")
        self.cryptButton.place(x=450, y=90, width=95, height=45)

        # Button decrypt
        self.decryptButton = tk.Button(self.window, text="Decrypt ->", command=self.bdecrypt, background="white", foreground="darkblue",
                                  font=("Times New Roman", 11, "bold"), relief="groove")
        self.decryptButton.place(x=450, y=250, width=95, height=45)

        # Button send packet
        self.sendButton = tk.Button(self.window, text="Send data", background="red", foreground="white",
                               font=("Times New Roman", 11, "bold"), relief="groove")
        self.sendButton.place(x=450, y=405, width=95, height=45)

        # Button generate key
        self.keyButton = tk.Button(self.window, text="Generate \nkey ->", command=self.select_key, background="white", foreground="red",
                              font=("Times New Roman", 11, "bold"), relief="groove")
        self.keyButton.place(x=20, y=370, width=100, height=50)

        # Button clear textBoxs
        self.clearButton = tk.Button(self.window, text="Clear all", command=self.clearAll, background="white", foreground="blue",
                                font=("Times New Roman", 9, "bold"), relief="groove")
        self.clearButton.place(x=210, y=465, width=100, height=25)

        # Textboxs

        # Textbox plain text
        self.label1 = tk.Label(self.window, text="Plain text:", font=("Arial Black", 8))
        self.label1.place(x=20, y=0)
        self.text_box_plain_text = tk.Text(self.window, font=("Times New Roman", 14), relief="solid")
        self.text_box_plain_text.place(x=20, y=20, width=400, height=300)

        # Textbox cypher text
        self.label2 = tk.Label(self.window, text="Cypher text:", font=("Arial Black", 8))
        self.label2.place(x=580, y=0)
        self.text_box_cypher_text = tk.Text(self.window, font=("Times New Roman", 14), foreground="darkred", relief="solid")
        self.text_box_cypher_text.place(x=580, y=20, width=400, height=200)

        # Textbox decrypt text
        self.label3 = tk.Label(self.window, text="Decrypt text:", font=("Arial Black", 8))
        self.label3.place(x=580, y=230)
        self.text_box_decrypt_text = tk.Text(self.window, font=("Times New Roman", 14), foreground="darkgreen", relief="solid")
        self.text_box_decrypt_text.place(x=580, y=250, width=400, height=200)

        # Textbox key
        self.label4 = tk.Label(self.window, text="Key:", font=("Arial Black", 8))
        self.label4.place(x=140, y=330)
        self.text_key_text = tk.Text(self.window, font=("Times New Roman", 12), relief="solid")
        self.text_key_text.place(x=140, y=350, width=280, height=100)

        # Combobox IP
        self.label5 = tk.Label(self.window, text="Select IP:", font=("Arial Black", 8))
        self.label5.place(x=440, y=330)
        self.comboboxIP = ttk.Combobox(self.window, font=("Times New Roman", 11, "bold"), foreground="darkgreen")
        self.comboboxIP['values'] = ('192.168.1.1', '192.168.1.2', '192.168.1.3')
        self.comboboxIP.current(0)
        self.comboboxIP.place(x=440, y=350, width=115, height=30)

        # combobox received message
        self.label6 = tk.Label(self.window, text="Received message:", font=("Arial Black", 8))
        self.label6.place(x=440, y=155)
        self.comboboxRM = ttk.Combobox(self.window, font=("Times New Roman", 11, "bold"))
        self.comboboxRM['state'] = 'readonly'
        self.comboboxRM['values'] = file_names
        self.comboboxRM.current(0)
        self.comboboxRM.bind("<<ComboboxSelected>>", self.update_textBoxCT)
        self.comboboxRM.place(x=440, y=175, width=115, height=30)

        # My IP
        ip = socket.gethostbyname(socket.gethostname())
        self.label7 = tk.Label(self.window, text="My IP: ", font=("Arial Black", 9))
        self.label7.place(x=580, y=465)
        self.text_box_myip = tk.Text(self.window, font=("Times New Roman", 12), relief="flat")
        self.text_box_myip.place(x=630, y=465, width=120, height=20)
        self.text_box_myip.insert(tk.END, ip)
        self.text_box_myip.config(state="disable")

        # Domain name
        dName = socket.gethostname()
        self.label8 = tk.Label(self.window, text="Name : ", font=("Arial Black", 9))
        self.label8.place(x=770, y=465)
        self.text_box_DN = tk.Text(self.window, font=("Times New Roman", 12), relief="flat")
        self.text_box_DN.place(x=830, y=465, width=120, height=27)
        self.text_box_DN.insert(tk.END, dName)
        self.text_box_DN.config(state="disable")

    def open_file(self):
        l = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
        if l:
            with open(l, "r") as file:
                text = file.read()

            self.text_box_plain_text.delete("1.0", tk.END)
            self.text_box_plain_text.insert(tk.END, text)

    def select_key(self):
        key = ''
        k = filedialog.askopenfilename(filetypes=[("Text file", ".*txt")])
        if k:
            with open(k, "r") as file:
                key = file.read()
            self.text_key_text.delete("1.0", tk.END)
            self.text_key_text.insert(tk.END, key)

    def bencrypt(self):
        ctext = ''
        key = self.text_key_text.get("1.0", tk.END)
        key = bytes.fromhex(key.replace(" ", ""))
        obj = rc6(key)

        p_text = self.text_box_plain_text.get("1.0", tk.END)
        p_text = bytes.fromhex(p_text.replace(" ", ""))
        ctext = obj.encrypt(p_text)

        x = ' '.join([f'{i:02x}' for i in ctext])

        self.text_box_cypher_text.delete("1.0", tk.END)
        self.text_box_cypher_text.insert(tk.END, x)

    def bdecrypt(self):
        dtext = ''
        key = self.text_key_text.get("1.0", tk.END)
        key = bytes.fromhex(key.replace(" ", ""))
        obj = rc6(key)

        c_text = self.text_box_cypher_text.get("1.0", tk.END)
        c_text = bytes.fromhex(c_text.replace(" ", ""))
        dtext = obj.decrypt(c_text)

        x = ' '.join([f'{i:02x}' for i in dtext])

        self.text_box_decrypt_text.delete("1.0", tk.END)
        self.text_box_decrypt_text.insert(tk.END, x)

    def update_textBoxCT(self, event):
        selected_file = self.comboboxRM.get()

        if selected_file != 'None':
            with open(os.path.join(dir_path, selected_file), 'r') as f:
                x = f.readlines()

            cypherText = x[0].strip("\n")
            key = x[1].strip("\n")
        else:
            self.text_box_cypher_text.delete('1.0', tk.END)
            self.text_key_text.delete('1.0', tk.END)
            return

        self.text_box_cypher_text.delete('1.0', tk.END)
        self.text_box_cypher_text.insert(tk.END, cypherText)
        self.text_key_text.delete('1.0', tk.END)
        self.text_key_text.insert(tk.END, key)

    def clearAll(self):
        self.text_box_plain_text.delete("1.0", tk.END)
        self.text_box_cypher_text.delete("1.0", tk.END)
        self.text_box_decrypt_text.delete("1.0", tk.END)
        self.text_key_text.delete("1.0", tk.END)
        return

mp = mainPanel()
mp.window.mainloop()