from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


print("""
_____________________________________________________________________________________________
Welcome to AES Encryption demo!
-------------------------------
By: Kaushal Bhingaradia
Date: Jan/18/2023

---------------------------------------------------------------------------------------------
You create a message which then gets encrypted by your own custom message (password must meet
the AES requirement). That encrypted message gets written into a sample_message.txt file. 
The program will write your name (name global variable) and date (dt_string global variable) 
in the file next to the message to indicate when the file was modified without being encrypted
but the actual message itself will be encrypted. You can decrypt the  message in the file by 
entering the password that was set during encryption. Note that the file will be modified to 
show the message that was hidden behind a encryption before.
_____________________________________________________________________________________________
""")


def main_loop():
    run = True
    while run:

        choice = input('Type 1 to encrypt a message, Type 2 to decrypt a message, Type 3 to exit >> ')

        if choice.isdigit():
            choice = int(choice)

            if choice == 3:
                print('Good-bye!')
                input()
                run = False

            elif choice == 1:
                print('Encryption mode!')
                message = input('Please enter your message >> \n').strip()
                password = input('Please set your encryption password >> \n').strip()
                if encryption(message, password):
                    continue

            elif choice == 2:
                print('Decryption mode!')
                password = input('Please enter your password >> \n').strip()
                if decryption(password):
                    continue

        else:
            print('\nNumber 1, 2, and 3 only!\n')
            continue


def encryption(message, password):
    # check if the password length is acceptable
    if len(password) < 16:
        print('Error: Password must be at least 16 characters long')
        return False

    # pad the message to a multiple of 16 bytes
    message = pad(message.encode(), AES.block_size)

    # create a new AES cipher object
    cipher = AES.new(password.encode(), AES.MODE_ECB)

    # encrypt the message
    encrypted_message = cipher.encrypt(message)

    # write the encrypted message to a file, along with the name and date
    with open('sample_message.txt', 'wb') as f:
        f.write(name.encode() + b'\n')
        f.write(dt_string.encode() + b'\n')
        f.write(encrypted_message)

    print('Encryption successful!')
    return True


def decryption(password):
    # check if the password length is acceptable
    if len(password) < 16:
        print('Error: Password must be at least 16 characters long')
        return False
    try:
        # read the encrypted message from the file
        with open('sample_message.txt', 'rb') as f:
            name = f.readline().strip()
            dt_string = f.readline().strip()
            encrypted_message = f.read()
    except FileNotFoundError:
        print('sample_message.txt not found')
        return False
    try:
        # check if the file is already decrypted
        with open('sample_message.txt', 'r', encoding='utf-8') as f:
            content = f.read()
            if "Decryption successful" in content:
                print("File is already decrypted.")
                return False
    except UnicodeDecodeError:
        pass
    # create a new AES cipher object
    cipher = AES.new(password.encode(), AES.MODE_ECB)
    # decrypt the message
    decrypted_message = cipher.decrypt(encrypted_message)
    try:
        # unpad the message
        decrypted_message = unpad(decrypted_message, AES.block_size)
    except ValueError:
        print("File is already decrypted.")
        return False
    # write the decrypted message to a file
    with open('sample_message.txt', 'wb') as f:
        f.write(decrypted_message)
    print(f'Decryption successful! File was decrypted by {name.decode()} on {dt_string.decode()}')
    return True


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
name = input('Please tell me your name >> ')
main_loop()
