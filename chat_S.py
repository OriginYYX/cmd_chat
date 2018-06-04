import socket,select
import sys,threading
host='118.89.194.23'
port=12345
c_addr=(host,port)
buffer = 4096
def read(cs):
    inputs = [cs]
    while True:
        rlist,wlist,elist = select.select(inputs, [], [])
        if cs in rlist:
            try:
                print (cs.recv(buffer).decode())
            except socket.error:
                print ("不好意思，socket挂了，再您妈的见")
                exit()

def write(cs):
    while True:
        data = input()
        if data == "再您妈的见":
             cs.send(data.encode())
             cs.close()
             break
        try:
            cs.send(data.encode())
        except Exception as e:
            exit()

def main():
    cs = socket.socket()
    cs.connect(c_addr)
    t = threading.Thread(target=read,args=(cs,))
    t.start()
    t1 = threading.Thread(target=write,args=(cs,))
    t1.start()

if __name__ == "__main__":
    main()