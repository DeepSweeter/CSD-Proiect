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
openButton = tk.Button(window, text="Open File", command=open_file)
openButton.place(x=450, y=20, width=95, height=45)

#Button cypt
cryptButton = tk.Button(window, text="Encrypt")
cryptButton.place(x=450, y=90, width=95, height=45)

#Button send packet
sendButton = tk.Button(window, text="Send data")
sendButton.place(x=450, y=320, width=95, height=45)

#Button decrypt
decryptButton = tk.Button(window, text="Decrypt")
decryptButton.place(x=450, y=250, width=95, height=45)

#Textboxs
#Textbox plain text 
label1 = tk.Label(window,text="Plain text:")
label1.place(x=20, y=0)
text_box_plain_text = tk.Text(window)
text_box_plain_text.place(x=20, y=20, width=400, height=430)

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


window.mainloop()
