import tkinter as tk
from tkinter import filedialog

def open_file():
    l = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
    if l:
        with open(l, "r") as file:
            text = file.read()
        
        text_box_plain_text.delete("1.0",tk.END)
        text_box_plain_text.insert(tk.END, text)



window = tk.Tk()
window.geometry("1000x480")
window.title("RC6 network aplication")


#Buttons
#Button open
openButton = tk.Button(window, text="<-- Open File", command=open_file,background="white",foreground="red")
openButton.place(x=450, y=20, width=95, height=45)

#Button cypt
cryptButton = tk.Button(window, text="Encrypt -->",background="white",foreground="darkblue")
cryptButton.place(x=450, y=90, width=95, height=45)

#Button send packet
sendButton = tk.Button(window, text="Send data",background="red",foreground="white")
sendButton.place(x=450, y=405, width=95, height=45)

#Button decrypt
decryptButton = tk.Button(window, text="Decrypt -->",background="white",foreground="darkblue")
decryptButton.place(x=450, y=250, width=95, height=45)

#Button generate key
keyButton = tk.Button(window, text="Generate key -->",background="white",foreground="red")
keyButton.place(x=20, y=375, width=100, height=45)

#Textboxs
#Textbox plain text 
label1 = tk.Label(window,text="Plain text:")
label1.place(x=20, y=0)
text_box_plain_text = tk.Text(window)
text_box_plain_text.place(x=20, y=20, width=400, height=300)

#Textbox cypher text 
label2 = tk.Label(window,text="Cypher text:")
label2.place(x=580, y=0)
text_box_cypher_text = tk.Text(window)
text_box_cypher_text.place(x=580, y=20, width=400, height=200)
text_box_cypher_text.insert(tk.END,"Aici textul criptat") 

#Textbox decrypt text 
label3 = tk.Label(window,text="Decrypt text:")
label3.place(x=580, y=230)
text_box_decrypt_text = tk.Text(window)
text_box_decrypt_text.place(x=580, y=250, width=400, height=200)
text_box_decrypt_text.insert(tk.END,"Aici textul decriptat") 

#Textbox key
label4 = tk.Label(window,text="Key:")
label4.place(x=140, y=330)
text_key_text = tk.Text(window)
text_key_text.place(x=140, y=350, width=280, height=100)

window.mainloop()