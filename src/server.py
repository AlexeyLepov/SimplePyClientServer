import socket
import os

sock = socket.socket()
sock.bind( ("127.0.0.1", 8888) )
sock.listen(1)
con, addr = sock.accept()

while True:
    print("listening...")
    data = con.recv(2**32)
    udata = data.decode("utf-8").split()
    match udata:
        case ["post", key, value]:
            with open(f"{key}.txt", "w") as file:
                file.truncate(0)
                file.write(value)
            print(f"post, {key=}, {value=}")
            con.send(b"Ok!")
        case ["get", key]:
            print("getting")
            try:
                with open(f"{key}.txt", "r") as file:
                    contents = file.read()
                    con.send(bytes(contents, "utf-8"))
            except IOError:
                con.send(b"No such file in directory")
            print(f"get {key=}")
        case ["delete", key]:
            if os.path.exists(f"{key}.txt"):
                os.remove(f"{key}.txt")
                con.send(b"OK!")
            else:
                con.send(b"The file does not exist") 
            print(f"delete {key=}")
        case ["search", value]:
            res = []
            files = os.listdir(".")
            for file in files:
                if file.endswith(".txt"):
                    with open(file, "r") as f:
                        contents = f.read()
                        if contents == value:
                            res.append(file)
            if res == []:
                con.send(b"Empty result!")
            else:
                con.send(bytes(", ".join(res), "utf-8"))
        case _:
            con.send(b"unknown command")
            print("Error")