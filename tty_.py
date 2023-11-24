import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 6489  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while 1:
        data = input(f"tty@{HOST}:{str(PORT)}> ")
        if data == ":quit":
            break
        s.sendall(data.encode("utf-8"))
        data = s.recv(1024)
        print(data.decode("utf-8"))