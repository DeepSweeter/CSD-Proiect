import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
from rc6 import *
import socket

dir_path = ".//Received Data"
file_names = [i for i in os.listdir(dir_path) if i.endswith('.txt')]
file_names.insert(0, "None")


def open_file():
    l = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if l:
        with open(l, "r") as file:
            text = file.read()

        text_box_plain_text.delete("1.0", tk.END)
        text_box_plain_text.insert(tk.END, text)


def select_key():
    key = ''
    k = filedialog.askopenfilename(filetypes=[("Text file", ".*txt")])
    if k:
        with open(k, "r") as file:
            key = file.read()
        text_key_text.delete("1.0", tk.END)
        text_key_text.insert(tk.END, key)


def bencrypt():
    ctext = ''
    key = text_key_text.get("1.0", tk.END)
    key = bytes.fromhex(key.replace(" ", ""))
    obj = rc6(key)

    p_text = text_box_plain_text.get("1.0", tk.END)
    p_text = bytes.fromhex(p_text.replace(" ", ""))
    ctext = obj.encrypt(p_text)

    x = ' '.join([f'{i:02x}' for i in ctext])

    text_box_cypher_text.delete("1.0", tk.END)
    text_box_cypher_text.insert(tk.END, x)


def bdecrypt():
    dtext = ''
    key = text_key_text.get("1.0", tk.END)
    key = bytes.fromhex(key.replace(" ", ""))
    obj = rc6(key)

    c_text = text_box_cypher_text.get("1.0", tk.END)
    c_text = bytes.fromhex(c_text.replace(" ", ""))
    dtext = obj.decrypt(c_text)

    x = ' '.join([f'{i:02x}' for i in dtext])

    text_box_decrypt_text.delete("1.0", tk.END)
    text_box_decrypt_text.insert(tk.END, x)


def update_textBoxCT(event):
    selected_file = comboboxRM.get()

    if selected_file != 'None':
        with open(os.path.join(dir_path, selected_file), 'r') as f:
            x = f.readlines()

        cypherText = x[0].strip("\n")
        key = x[1].strip("\n")
    else:
        text_box_cypher_text.delete('1.0', tk.END)
        text_key_text.delete('1.0', tk.END)
        return

    text_box_cypher_text.delete('1.0', tk.END)
    text_box_cypher_text.insert(tk.END, cypherText)
    text_key_text.delete('1.0', tk.END)
    text_key_text.insert(tk.END, key)


def clearAll():
    text_box_plain_text.delete("1.0", tk.END)
    text_box_cypher_text.delete("1.0", tk.END)
    text_box_decrypt_text.delete("1.0", tk.END)
    text_key_text.delete("1.0", tk.END)
    return


window = tk.Tk()
window.geometry("1000x510")
window.title("RC6 network aplication")
window.resizable(False, False)

# Buttons

# Button open
openButton = tk.Button(window, text="<- Open File", command=open_file, background="white", foreground="red",
                       font=("Times New Roman", 11, "bold"), relief="groove")
openButton.place(x=450, y=20, width=95, height=45)

# Button crypt
cryptButton = tk.Button(window, text="Encrypt ->", command=bencrypt, background="white", foreground="darkblue",
                        font=("Times New Roman", 11, "bold"), relief="groove")
cryptButton.place(x=450, y=90, width=95, height=45)

# Button decrypt
decryptButton = tk.Button(window, text="Decrypt ->", command=bdecrypt, background="white", foreground="darkblue",
                          font=("Times New Roman", 11, "bold"), relief="groove")
decryptButton.place(x=450, y=250, width=95, height=45)

# Button send packet
sendButton = tk.Button(window, text="Send data", background="red", foreground="white",
                       font=("Times New Roman", 11, "bold"), relief="groove")
sendButton.place(x=450, y=405, width=95, height=45)

# Button generate key
keyButton = tk.Button(window, text="Generate \nkey ->", command=select_key, background="white", foreground="red",
                      font=("Times New Roman", 11, "bold"), relief="groove")
keyButton.place(x=20, y=370, width=100, height=50)

# Button clear textBoxs
clearButton = tk.Button(window, text="Clear all", command=clearAll, background="white", foreground="blue",
                        font=("Times New Roman", 9, "bold"), relief="groove")
clearButton.place(x=210, y=465, width=100, height=25)

# Textboxs

# Textbox plain text
label1 = tk.Label(window, text="Plain text:", font=("Arial Black", 8))
label1.place(x=20, y=0)
text_box_plain_text = tk.Text(window, font=("Times New Roman", 14), relief="solid")
text_box_plain_text.place(x=20, y=20, width=400, height=300)

# Textbox cypher text
label2 = tk.Label(window, text="Cypher text:", font=("Arial Black", 8))
label2.place(x=580, y=0)
text_box_cypher_text = tk.Text(window, font=("Times New Roman", 14), foreground="darkred", relief="solid")
text_box_cypher_text.place(x=580, y=20, width=400, height=200)

# Textbox decrypt text
label3 = tk.Label(window, text="Decrypt text:", font=("Arial Black", 8))
label3.place(x=580, y=230)
text_box_decrypt_text = tk.Text(window, font=("Times New Roman", 14), foreground="darkgreen", relief="solid")
text_box_decrypt_text.place(x=580, y=250, width=400, height=200)

# Textbox key
label4 = tk.Label(window, text="Key:", font=("Arial Black", 8))
label4.place(x=140, y=330)
text_key_text = tk.Text(window, font=("Times New Roman", 12), relief="solid")
text_key_text.place(x=140, y=350, width=280, height=100)

# Combobox IP
label5 = tk.Label(window, text="Select IP:", font=("Arial Black", 8))
label5.place(x=440, y=330)
comboboxIP = ttk.Combobox(window, font=("Times New Roman", 11, "bold"), foreground="darkgreen")
comboboxIP['values'] = ('192.168.1.1', '192.168.1.2', '192.168.1.3')
comboboxIP.current(0)
comboboxIP.place(x=440, y=350, width=115, height=30)

# combobox received message
label6 = tk.Label(window, text="Received message:", font=("Arial Black", 8))
label6.place(x=440, y=155)
comboboxRM = ttk.Combobox(window, font=("Times New Roman", 11, "bold"))
comboboxRM['state'] = 'readonly'
comboboxRM['values'] = file_names
comboboxRM.current(0)
comboboxRM.bind("<<ComboboxSelected>>", update_textBoxCT)
comboboxRM.place(x=440, y=175, width=115, height=30)

# My IP
ip = socket.gethostbyname(socket.gethostname())
label7 = tk.Label(window, text="My IP: ", font=("Arial Black", 9))
label7.place(x=580, y=465)
text_box_myip = tk.Text(window, font=("Times New Roman", 12), relief="flat")
text_box_myip.place(x=630, y=465, width=120, height=20)
text_box_myip.insert(tk.END, ip)
text_box_myip.config(state="disable")

# Domain name
dName = socket.gethostname()
label8 = tk.Label(window, text="Name : ", font=("Arial Black", 9))
label8.place(x=770, y=465)
text_box_DN = tk.Text(window, font=("Times New Roman", 12), relief="flat")
text_box_DN.place(x=830, y=465, width=120, height=27)
text_box_DN.insert(tk.END, dName)
text_box_DN.config(state="disable")

window.mainloop()