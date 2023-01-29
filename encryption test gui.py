import tkinter as tk
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

"""
This function encrypts your message into the sample_message.txt file 
by using 16 character password of your choice.
"""


def encryption(message, password):
    message = pad(message.encode(), AES.block_size)
    cipher = AES.new(password.encode(), AES.MODE_ECB)
    encrypted_message = cipher.encrypt(message)

    with open('sample_message.txt', 'wb') as f:
        f.write(name.encode() + b'\n')
        f.write(dt_string.encode() + b'\n')
        f.write(encrypted_message)
    result_label.config(text="Encryption successful! Check sample_message.txt!",
                        fg="green")
    os.startfile('sample_message.txt')
    return True


"""
This function decrypts the sample_message.txt file by using your set password.
"""


def decryption(password):
    try:
        with open('sample_message.txt', 'rb') as f:
            name = f.readline().strip()
            dt_string = f.readline().strip()
            encrypted_message = f.read()
    except FileNotFoundError:
        result_label.config(text="sample_message.txt not found", fg="red")
        return False
    try:
        with open('sample_message.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            if "Decryption successful! Check sample_message.txt!" in content:
                result_label.config(text="File is already decrypted.", fg="red")
                return False
    except UnicodeDecodeError:
        pass
    try:
        cipher = AES.new(password.encode(), AES.MODE_ECB)
        decrypted_message = cipher.decrypt(encrypted_message)
        decrypted_message = unpad(decrypted_message, AES.block_size)
        with open('sample_message.txt', 'wb') as f:
            f.write(decrypted_message)
        result_label.config(text="Decryption successful! Check "
                                 "sample_message.txt!", fg="green")
        os.startfile('sample_message.txt')
        return True
    except ValueError:
        result_label.config(text="Incorrect Password or already decrypted!",
                            fg="red")
        return False


"""
This function is the heart of the code. Checks if password meets length 
requirements and calls the encryption() and decryption() when the 
message and password field are satisfied. Coded to the Executing button
"""


def execute():
    if password_entry.get().strip() == "":
        result_label.config(text="Error: Please set a 16 character password!",
                            fg="red")
        return False
    password = password_entry.get()
    if len(password) < 16 or len(password) > 16 or password.strip() == "":
        result_label.config(text="Error: Password must be 16 characters long",
                            fg="red")
        password_entry.delete(0, tk.END)
        return False

    if encryption_decryption_var.get() == "encryption":
        message = text_box.get("1.0", "end-1c")
        encryption(message, password)

    elif encryption_decryption_var.get() == "decryption":
        decryption(password)


"""
This function hides the text box and clear button when
decrypted mode is selected, otherwise does not hide 
when encrypted mode is selected.
"""


def handle_radiobutton_click():
    if encryption_decryption_var.get() == "encryption":
        text_label.grid()
        text_box.grid()
        clear_button.grid()

    else:
        text_label.grid_remove()
        text_box.grid_remove()
        clear_button.grid_remove()


"""
This is where the UI is being created for the app
"""

root = tk.Tk()
root.title("AES Encryption/Decryption GUI")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
name = os.getlogin()
encryption_mode = tk.BooleanVar(value=True)
decryption_mode = tk.BooleanVar(value=False)

instructions_label = tk.Label(root,
                              text="""
                              Welcome to AES Encryption/Decryption demo!
                              Enter a message, then create a password 
                              that is 16 characters long,then select 
                              encrypt, then click execute. Check the 
                              sample_message.txt file. Use that same 
                              password to decrypt the file.
                              """,
                              font=("Arial", 16),
                              justify=tk.CENTER)
instructions_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
instructions_label.config(anchor="w")

text_label = tk.Label(root, text="Enter message:")
text_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
text_box = tk.Text(root, height=30, width=20)
text_box.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

try:
    password_label = tk.Label(root, text="Enter password:")
    password_label.grid(row=3, column=0, padx=10, pady=10, sticky="W")
    password_entry = tk.Entry(root, show='*', width=30)
    password_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
except ValueError:
    pass

try:
    encryption_decryption_var = tk.StringVar(value="encryption")
    encryption_button = tk.Radiobutton(root, text="Encryption",
                                       variable=encryption_decryption_var,
                                       value="encryption")
    encryption_button.grid(row=5, column=0, padx=10, pady=10, sticky="W")
    decryption_button = tk.Radiobutton(root, text="Decryption",
                                       variable=encryption_decryption_var,
                                       value="decryption")
    decryption_button.grid(row=5, column=1, padx=10, pady=10, sticky="W")
    encryption_button.config(command=lambda:
                             encryption_decryption_var.set("encryption"))
    encryption_button.config(command=lambda: handle_radiobutton_click())
    decryption_button.config(command=lambda:
                             encryption_decryption_var.set("decryption"))
    decryption_button.config(command=lambda: handle_radiobutton_click())

except ValueError:
    pass

try:
    execute_button = tk.Button(root, text="Execute", command=execute)
    execute_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10,
                        ipadx=40)
except ValueError:
    pass


def delete():
    text_box.delete("1.0", "end-1c")
    result_label.config(text="Text Cleared!", fg="green")


clear_button = tk.Button(root, text="Clear Message", command=delete)
clear_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, ipadx=10)

result_label = tk.Label(root, font=("Arial", 12))
result_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
