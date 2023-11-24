from re import compile
from pwinput import pwinput
from base64 import urlsafe_b64encode
from socket import socket, AF_INET, SOCK_STREAM
from hashlib import sha224, sha256, sha384, sha512, md5
from random import choice

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6489  # The port used by the server
FILE = "new_codebase.py"
version_r = compile("^200 - HSI Remote Script Update System v\d+\.\d+$")
hash_methods = [
    (sha224, "sha224"),
    (sha256, "sha256"),
    (sha384, "sha384"),
    (sha512, "sha512"),
    (md5, "md5")
]

def connect(HOST, PORT):
    with socket(AF_INET, SOCK_STREAM) as s:
        print("Connecting...")
        s.connect((HOST, PORT))
        print("Connected\n")
        print("Requesting Product Information...")
        s.sendall(b"info")
        data = s.recv(1024)
        print(f"Recived Data: \"{data.decode('UTF-8')}\"\n")
        print("Validating Data using REGEX...")
        if version_r.match(data.decode("utf-8")) is None:
            print("Invalid Product Information\n")
            return
        print("Valid Product Information\n")
        print("################################################################################\n")
        if input(" THE REMOTE DEVICE MIGHT SPOOF ITS IDENTITY\n DO YOU STILL WANT TO ATTEMPT TO AUTHENTICATE\n AUTHENTICATION SENDS AN ENCRYPTED VERSION OF THE PASSWORD\n\n CONTINUE? ( y / n ): ").lower() != "y":
            return
        password = pwinput(prompt='\n PLEASE ENTER THE PASSWORD FOR THE REMOTE DEVICE\n\n PASSWORD: ', mask='*')
        if pwinput(prompt=' CONFIRM:  ', mask='*') != password:
            print("\n PASSWORD MISSMATCH")
            print("\n################################################################################")
            return
        print("\n################################################################################")
        print("\nChoosing Encryption Method...")
        hash_method: tuple = choice(hash_methods)
        print(f"Chosen Encryption Method: {hash_method[1]}")
        print(f"Encrypting password with {hash_method[1]}...")
        hash = hash_method[0](password.encode("UTF-8"))
        hash = hash.hexdigest()
        print(f"Encrypted Password: {hash[:7]}{len(hash[7:]) * '*'}\n")
        print("Sending Hash Method to Remote Device...")
        s.sendall(f"auth {hash_method[1]}".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        if not data.startswith("200 - "):
            print(f"There was an invalid response from the remote device: Code {data.split(' - ')[0]}")
        server_hash = data.split(' - ')[1]
        next_method = data.split(' - ')[2]
        print(f"Recived Data:\n Hash: {server_hash[:7]}{len(server_hash[7:]) * '*'}\n Next Hash Method: {next_method}\n")
        print("Checking Hashes...")
        if not server_hash == hash:
            print("Invalid Hash!\n\nPlease Check if you have entered the correct Password\nPlease Check if the Server address is correct")
        print("Both Hashes are identical\n")
        if input(" THE REMOTE DEVICE MIGHT SPOOF ITS IDENTITY\n DO YOU STILL WANT TO ATTEMPT TO AUTHENTICATE\n THE DATA FROM THE NEXT STEP CANNOT GET DECODED\n THE DATA FROM THE NEXT STEP CAN BE USED TO AUTHENTICATE TO THE REMOTE DEVICE\n MAKE SURE YOU ARE CONNECTED TO THE RIGHT SERVER BEFORE CONTINUING\n\n CONTINUE? ( y / n ): ").lower() != "y":
            return
        if not [i for i in hash_methods if i[1] == next_method]:
            print("\nThe Remote Device returned an invalid hashing method!")
            return
        hash_method = [i for i in hash_methods if i[1] == next_method][0]
        print(f"\nEncrypting password with {hash_method[1]}...")
        hash = hash_method[0](password.encode("UTF-8"))
        hash = hash.hexdigest()
        print(f"Encrypted Password: {hash[:7]}{len(hash[7:]) * '*'}\n")
        print("Sending Hash to Server...")
        s.sendall(f"auth {hash}".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print(f"Recieved Data: {data}\n")
        if data.split(" - ")[0] != "200":
            print("Authentication Failed!")
            return
        print("Authentication Success!\n")
        print("Querying Authentication from Remote Host...")
        s.sendall(f"auth".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print(f"Recived Data: {data}")
        if data.split(" - ")[0] != "200":
            print("Authentication Failed!\nThere must be a Server Side issue!")
            return
        print("Success! You are now authenticated!\n")
        print(f"Reading \"{FILE}\"...")
        f = open(FILE, "r")
        c = f.read()
        f.close()
        print("Read\n")
        print(f"Base 64 Url Encoding \"{FILE}\"")
        b64 = urlsafe_b64encode(c.encode("utf-8"))
        print("Base 64 Encoded!\n")
        print(f"Base64: {b64}\n")
        print(f"Sending Base64 to Remote Device")
        s.sendall(f"update {b64.decode('utf-8')}".encode("utf-8"))
        data = s.recv(1024).decode("utf-8")
        print(f"Received data: {data}")
        if data.split(" - ")[0] != "200":
            print("There was an Error!")
            return
        print("Success! Remote Device is Updated!\n")

connect(HOST, PORT)