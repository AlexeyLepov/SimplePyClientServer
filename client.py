import contextlib
import socket

conn = socket.socket()
conn.connect( ("127.0.0.1", 8888) )

while True:
    command = input()
    conn.send(bytes(command, "utf-8"))
    while True:
        with contextlib.suppress(Exception):
            response = conn.recv(1024)
            print(response.decode("utf-8"))
            break
        # try:
        #     response = conn.recv(1024)
        #     print(response.decode("utf-8"))
        #     break
        # except Exception:
        #     pass