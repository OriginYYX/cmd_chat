import socket,select

host = socket.gethostname()
port = 12345
server_addr = (host,port)

inputs = []

fd_name = {}

def serverInit():
    ss = socket.socket()  
    ss.bind(server_addr)  
    ss.listen(10)          
    return ss             

def newConnection(ss):
    client_conn,client_addr = ss.accept()  
    try:
        
        client_conn.send("欢迎来到warning聊天室,请输入您的昵称")
        client_name = client_conn.recv(1024).decode()
        inputs.append(client_conn)
        fd_name[client_conn] = client_name
        text = "确认一下您的昵称是: %s" % fd_name.values()
        client_conn.send(text.encode())
        for other in fd_name.keys():
            if other != client_conn and other != ss:
                text = fd_name[client_conn]+"启动！开始warning!!!"
                other.send(text.encode())
    except Exception as e:
        print (e)

def closeConnection():
    pass

def run():
    ss = serverInit()
    inputs.append(ss)
    print ("server is running...")
    while True:
        rlist,wlist,elist = select.select(inputs, [], [])
        if not rlist:
            print ("timeout...")
            ss.close()  
            break
        for r in rlist:
            if r is ss:  
                newConnection(ss)
            else:          
                disconnect = False
                try:
                    data = r.recv(1024).decode() 
                    data = fd_name[r] + " : "+ data 
                except socket.error:
                    data = fd_name[r] + " 离开了聊天室"
                    disconnect = True
                else:
                    pass
                if disconnect:
                    inputs.remove(r)
                    print (data)
                    for other in inputs:
                        if other != ss and other != r:  
                            try:
                                other.send(data.encode())
                            except Exception as e:
                                print (e)
                            else:
                                pass
                    del fd_name[r]
                else:
                    print (data)  
                    for other in inputs:
                        if other != ss and other != r:
                            try:
                                other.send(data.encode())
                            except Exception as e:
                                print (e)
if __name__ == "__main__":
    run()