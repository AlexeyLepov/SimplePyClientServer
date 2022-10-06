import socket
import os
import redis


my_redis = redis.Redis(host="my-db", port = 6379)
if input("delete all keys in db? 0/1"):
    for i in my_redis.scan_iter():
        my_redis.delete(i)
print("redis connected")
input("press enter");
sock = socket.socket()
sock.bind( ("", 8888) )
sock.listen(1)
con, addr = sock.accept()

while True:
    print("listening...")
    data = con.recv(2**32)
    udata = data.decode("utf-8").split()
    match udata:
        case ["post", key, value]:
            # with open(f"{key}.txt", "w") as file:
            #     file.truncate(0)
            #     file.write(value)
            
            my_redis.set(key, value)
            print(f"post, {key=}, {value=}")
            con.send(b"Ok!")
            
        case ["get", key]:
            print("getting")
            # try:
            #     with open(f"{key}.txt", "r") as file:
            #         contents = file.read()
            #         con.send(bytes(contents, "utf-8"))
            # except IOError:
            #   con.send(b"No such file in directory")
            
            ans = my_redis.get(key)
            if ans is not None:
                con.send(ans)
            else:
                con.send(b"No such file in directory")
            print(f"get {key=}")
            
        case ["delete", key]:
            # if os.path.exists(f"{key}.txt"):
            #     os.remove(f"{key}.txt")
            #     con.send(b"OK!")
            # else:
            #     con.send(b"The file does not exist") 
            if my_redis.delete(key):
                con.send(b"OK!")
            else:
                con.send(b"Unknown key!")
            print(f"delete {key=}")
        case ["search", value]:
            res = []
            for key in my_redis.scan_iter():
                contents = my_redis.get(key).decode("utf-8")
                if contents == value:
                    res.append(key.decode("utf-8"))
            if res == []:
                con.send(b"Empty result!")
            else:
                con.send(bytes(", ".join(res), "utf-8"))
        case _:
            con.send(b"unknown command")
            print("Error")