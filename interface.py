import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from rc6 import *

def open_file():
    l = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if l:
        with open(l, "r") as file:
            text = file.read()
        
        text_box_plain_text.delete("1.0",tk.END)
        text_box_plain_text.insert(tk.END, text)

def select_key():
    key = ''
    k = filedialog.askopenfilename(filetypes=[("Text file", ".*txt")])
    if k:
        with open(k, "r") as file:
            key = file.read()
        text_key_text.delete("1.0",tk.END)
        text_key_text.insert(tk.END,key)

def bencrypt():
    ctext = ''
    key = text_key_text.get("1.0",tk.END)
    key = bytes.fromhex(key.replace(" ",""))
    obj = rc6(key)

    p_text = text_box_plain_text.get("1.0",tk.END)
    p_text = bytes.fromhex(p_text.replace(" ",""))
    ctext = obj.encrypt(p_text)

    x = ' '.join([f'{i:02x}' for i in ctext])

    text_box_cypher_text.delete("1.0",tk.END)
    text_box_cypher_text.insert(tk.END,x)

def bdecrypt():
    dtext = ''
    key = text_key_text.get("1.0",tk.END)
    key = bytes.fromhex(key.replace(" ",""))
    obj = rc6(key)

    c_text = text_box_cypher_text.get("1.0",tk.END)
    c_text = bytes.fromhex(c_text.replace(" ",""))
    dtext = obj.decrypt(c_text)

    x = ' '.join([f'{i:02x}' for i in dtext])

    text_box_decrypt_text.delete("1.0",tk.END)
    text_box_decrypt_text.insert(tk.END,x)


window = tk.Tk()
window.geometry("1000x480")
window.title("RC6 network aplication")

#Buttons

#Button open
openButton = tk.Button(window, text="<- Open File", command=open_file, background="white", foreground="red",font =("Times New Roman",11,"bold"), relief="groove")
openButton.place(x=450, y=20, width=95, height=45)

#Button crypt
cryptButton = tk.Button(window, text="Encrypt ->", command=bencrypt, background="white", foreground="darkblue", font =("Times New Roman",11,"bold"), relief="groove")

cryptButton.place(x=450, y=90, width=95, height=45)

#Button decrypt
decryptButton = tk.Button(window, text="Decrypt ->", command=bdecrypt, background="white", foreground="darkblue", font =("Times New Roman",11,"bold"), relief="groove")

decryptButton.place(x=450, y=250, width=95, height=45)

#Button send packet
sendButton = tk.Button(window, text="Send data", background="red", foreground="white", font =("Times New Roman",11,"bold"), relief="groove")
sendButton.place(x=450, y=405, width=95, height=45)

#Button generate key
keyButton = tk.Button(window, text="Generate key ->", command=select_key, background="white", foreground="red", font =("Times New Roman",10,"bold"), relief="groove")
keyButton.place(x=20, y=375, width=100, height=45)

#Textboxs

#Textbox plain text 
label1 = tk.Label(window,text="Plain text:", font =("Arial Black",8))
label1.place(x=20, y=0)
text_box_plain_text = tk.Text(window, font =("Times New Roman",14),foreground="green", relief="solid")
text_box_plain_text.place(x=20, y=20, width=400, height=300)

#Textbox cypher text 
label2 = tk.Label(window,text="Cypher text:", font =("Arial Black",8))
label2.place(x=580, y=0)
text_box_cypher_text = tk.Text(window, font =("Times New Roman",14),foreground="darkred", relief="solid")
text_box_cypher_text.place(x=580, y=20, width=400, height=200)
#text_box_cypher_text.insert(tk.END,"Aici textul criptat") 

#Textbox decrypt text 
label3 = tk.Label(window,text="Decrypt text:", font =("Arial Black",8))
label3.place(x=580, y=230)
text_box_decrypt_text = tk.Text(window, font =("Times New Roman",14),foreground="darkgreen", relief="solid")
text_box_decrypt_text.place(x=580, y=250, width=400, height=200)
#text_box_decrypt_text.insert(tk.END,"Aici textul decriptat") 

#Textbox key
label4 = tk.Label(window,text="Key:", font =("Arial Black",8))
label4.place(x=140, y=330)
text_key_text = tk.Text(window, font =("Times New Roman",12),foreground="purple", relief="solid")
text_key_text.place(x=140, y=350, width=280, height=100)

#Combobox IP
label5 = tk.Label(window,text="Select IP:", font =("Arial Black",8))
label5.place(x=440, y=330)
comboboxIP = ttk.Combobox(window,font =("Times New Roman",11,"bold"),foreground="darkgreen")
comboboxIP['values'] = ('192.168.1.1', '192.168.1.2', '192.168.1.3')
comboboxIP.current(0)
comboboxIP.place(x=440, y=350, width=115, height=30)

window.mainloop()