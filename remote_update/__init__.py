from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from hashlib import sha224, sha256, sha384, sha512, md5
from random import choice
from base64 import urlsafe_b64decode
from os import system, getpid
from os.path import dirname

version = "v1.1"
service = "HSI Remote Script Update System"

kill = False

def listen(auth_token: str, __file_:str, in_background: bool = False):
    if in_background:
        Thread(target = _listener, args=(auth_token, __file_)).start()
    else:
        _listener(auth_token, __file_)

def _listener(auth_token: str, __file_: str):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("localhost", 6489))
    global kill
    while 1:
        if kill: break
        hash_methods = [
            (sha224, "sha224"),
            (sha256, "sha256"),
            (sha384, "sha384"),
            (sha512, "sha512"),
            (md5, "md5")
        ]
        try:
            s.listen()
            conn, addr = s.accept()
            authentication = {
                "stage1_method": "",
                "stage1_hash": "",
                "stage1_completed": False,
                "stage2_method": "",
                "stage2_hash": "",
                "stage2_completed": False,
                "authenticated": False
            }
            with conn:
                #print(f"Connected by {addr}")
                while True:
                    data_r = conn.recv(1024)
                    cmd = data_r.decode("utf-8")
                    if cmd == "info":
                        data = f"200 - {service} {version}"
                    elif cmd == "stop":
                        if authentication["stage1_completed"] and authentication["stage2_completed"] and authentication["authenticated"]:
                            kill = True
                            break
                        data = f"401 - Invalid Authentication"
                    elif cmd.startswith("auth"):
                        if not authentication["stage1_completed"]:
                            method = cmd.split(" ")[1]
                            if [i for i in hash_methods if i[1] == method]:
                                method = [i for i in hash_methods if i[1] == method][0]
                                hash_methods.remove(method)
                                new_method = choice(hash_methods)
                                hash = method[0](auth_token.encode("UTF-8")).hexdigest()
                                new_hash = new_method[0](auth_token.encode("UTF-8")).hexdigest()
                                authentication["stage1_completed"] = True
                                authentication["stage1_hash"] = hash
                                authentication["stage1_method"] = method
                                authentication["stage2_method"] = new_method
                                authentication["stage2_hash"] = new_hash

                                data = f"200 - {hash} - {new_method[1]}"
                            else:
                                data = f"400 - Invalid hash method"
                        elif authentication["stage1_completed"] and not authentication["stage2_completed"]:
                            hash = cmd.split(" ")[1]
                            if hash == authentication["stage2_hash"]:
                                authentication["stage2_completed"] = True
                                authentication["authenticated"] = True
                                data = "200 - Authorized"
                            else:
                                data = "401 - Invalid Authentication"
                        elif authentication["stage1_completed"] and authentication["stage2_completed"] and authentication["authenticated"]:
                            data = "200 - Authenticated"
                        else:
                            data = "500 - Unknown Error"
                    elif cmd.startswith("update "):
                        if authentication["stage1_completed"] and authentication["stage2_completed"] and authentication["authenticated"]:
                            b64 = cmd.split(" ")[1]
                            c = urlsafe_b64decode(b64)
                            f = open("program_update.py", 'wb')
                            f.write(c)
                            f.close()
                            data = "200 - Updated"
                            conn.sendall(data.encode('utf-8'))
                            conn.close()
                            system(f'cmd /c start /min cmd /c cd /d {dirname(__file_)} ^^^& TASKKILL /F /FI "PID eq {str(getpid())}" ^^^& del {__file_} ^^^& move program_update.py {__file_} ^^^& python {__file_}')
                            exit()
                        else:
                            data = f"401 - Not Authorized"
                    else:
                        data = f"404 - Command not found"

                    if not data:
                        break
                    conn.sendall(data.encode('utf-8'))
        except ConnectionAbortedError:
            pass
