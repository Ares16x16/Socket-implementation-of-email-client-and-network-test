#Development platform: Windows
#Python version: 3.8

import socket
import sys
import time

def serverSide():
    port = 40510
    host = socket.gethostname()
    print("Start as server node")

    s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    s_server.bind(('', port))
    s_server.listen()

    conn, address = s_server.accept() # Return the TCP connection
    print("Server is ready. Listening address: ", s_server.getsockname())
    print("A client has connected and it is at: \n", address, "\n")

    #==========================test1==============================
    t1finish = b'ababa'
    t1msg = b'abcdefghji'*20000000
    t1msg_40 = b'abcde'*1000000
    print("Start test1 - large transfer")
    print("From server to client")
    realtime = 0
    
    #server send large msg to client
    for i in range(40):
        #time.sleep(0.1)
        t1_start = time.perf_counter()   
        conn.send(t1msg_40)
        t1_stop = time.perf_counter()
        realtime += t1_stop - t1_start
        print("* ", end='', flush=True)
    print("")
    msg = conn.recv(5) #receive back short message
    #print("Received msg:  ", msg)
    
    
    print("Sent total: ",len(t1msg), " bytes")
    print("Elapsed time:", '%.3f'%(realtime), " s")
    print("Throughput (from client to server): ", '%.3f'%(1600/(realtime)), " Mb/s")

    msg = b''
    #client to server
    print("From client to server")
    length = 0
    while length < 200000000:
        msg += conn.recv(1000000)
        length = len(msg)
    conn.send(t1finish)
    print("Received total:  ", len(msg), " bytes")
    
       
    #==========================test2==============================
    print("\nStart test2 - small transfer")
    t2msg = t1finish*2000

    print("From server to client")
    #server send small msg to client
    t2_start = time.perf_counter()
    conn.send(t2msg)
    msgg = conn.recv(100000) 
    #print("Received msg:  ", msgg)
    t2_stop = time.perf_counter()

    print("Sent total: ",len(t2msg), " bytes")
    print("Elapsed time:", '%.3f'%(t2_stop-t2_start), " s")
    print("Throughput (from client to server): ", '%.3f'%(0.08/(t2_stop-t2_start)), " Mb/s")

    #client to server
    print("From client to server")
    msg = conn.recv(10000)
    conn.send(t1finish)
    print("Received total:  ", len(msg), " bytes")
    
    
    #==========================test3==============================   
    print("\nStart test3 - UDP pingpong")
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.bind(('', port))
    rtt = 0
    
    #server ==> client
    print("From server to client")
    udp_msg, addr = server_udp.recvfrom(1024) 
    
    start = time.perf_counter() 
    server_udp.sendto(t1finish, addr) 
    udp_msg, server = server_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #1
    start = time.perf_counter() 
    server_udp.sendto(t1finish, addr) 
    udp_msg, server = server_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #2
    start = time.perf_counter() 
    server_udp.sendto(t1finish, addr) 
    udp_msg, server = server_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #3
    start = time.perf_counter() 
    server_udp.sendto(t1finish, addr) 
    udp_msg, server = server_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #4
    start = time.perf_counter() 
    server_udp.sendto(t1finish, addr) 
    udp_msg, server = server_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #5
    print("Average RTT: ", '%.5f'%(rtt/5), " s")
    #client ==> server
    print("From client to server")
    udp_msg, addr = server_udp.recvfrom(1024)  
    server_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = server_udp.recvfrom(1024)
    server_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = server_udp.recvfrom(1024)
    server_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = server_udp.recvfrom(1024)
    server_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = server_udp.recvfrom(1024)
    server_udp.sendto(udp_msg, addr)
    print("*")
    
    
    conn.close()
    s_server.close()
    server_udp.close()



def clientSide():
    port = 40510
    print("Start as client node")
    
    s_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = sys.argv[1]
    s_client.connect((ip, port))

    print("Client has connected to server at: ", s_client.getpeername() )
    print("Client's address: ", s_client.getsockname(), "\n")

    #==========================test1==============================
    t1finish = b'abcde'
    t1msg = b'abcdefghij'*20000000
    t1msg_40 = b'abcde'*1000000
    t1msg_400 = b'abcde'*100000
    print("Start test1 - large transfer")
    msg = b''
    realtime = 0
    
    #server to client
    print("From server to client")
    length = 0
    while length < 200000000:
        msg += s_client.recv(5000000)
        length = len(msg)
    s_client.send(t1finish)
    print("Received total:  ", len(msg), " bytes")


    #client to server
    print("From client to server")

    #client send large msg to server
    for i in range(40):
        #time.sleep(0.1)
        t1_start = time.perf_counter()
        s_client.send(t1msg_40)
        t1_stop = time.perf_counter()
        realtime += t1_stop - t1_start
        print("* ", end='', flush=True)
    print("")
    msg = s_client.recv(5) #receive back short message

    #print("Received msg:  ", msg)

    
    print("Sent total: ",len(t1msg), " bytes")
    print("Elapsed time:", '%.3f'%(realtime), " s")
    print("Throughput (from client to server): ", '%.3f'%(1600/(realtime)), " Mb/s")

    
    #==========================test2==============================
    print("\nStart test2 - small transfer")
    t2msg = t1finish*2000
    
    print("From server to client")
    msg = s_client.recv(10000)
    print("Received total:  ", len(msg), " bytes")
    s_client.send(t1finish)
    print("From client to server")
    t2_start = time.perf_counter() 
    #client send small msg to server
    s_client.send(t2msg)
    msg = s_client.recv(5) #receive back short message

    #print("Received msg:  ", msg)
    t2_stop = time.perf_counter()
    print("Sent total: ",len(t2msg), " bytes")
    print("Elapsed time:", '%.3f'%(t2_stop-t2_start), " s")
    print("Throughput (from client to server): ", '%.3f'%(0.08/(t2_stop-t2_start)), " Mb/s")
    
    #==========================test3==============================
    print("\nStart test3 - UDP pingpong")
    rtt = 0
    addr = (ip, port)
    client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    #server ==> client
    print("From server to client")
    client_udp.sendto(b'ok', addr)
    
    udp_msg, addr = client_udp.recvfrom(1024)  
    client_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = client_udp.recvfrom(1024)  
    client_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = client_udp.recvfrom(1024)  
    client_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = client_udp.recvfrom(1024)  
    client_udp.sendto(udp_msg, addr)
    print("* ", end= '')
    udp_msg, addr = client_udp.recvfrom(1024)  
    client_udp.sendto(udp_msg, addr)
    print("*")
    
    #client ==> server
    print("From client to server")
    
    start = time.perf_counter() 
    client_udp.sendto(t1finish, addr)
    udp_msg, server = client_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #1
    start = time.perf_counter() 
    client_udp.sendto(t1finish, addr)
    udp_msg, server = client_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #2
    start = time.perf_counter() 
    client_udp.sendto(t1finish, addr)
    udp_msg, server = client_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #3
    start = time.perf_counter() 
    client_udp.sendto(t1finish, addr)
    udp_msg, server = client_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #4
    start = time.perf_counter() 
    client_udp.sendto(t1finish, addr)
    udp_msg, server = client_udp.recvfrom(1024)
    end = time.perf_counter() 
    rtt += end-start
    print("Reply from ",addr[0], ": time = ", '%.4f'%(end-start), "s") #5
    print("Average RTT: ", '%.5f'%(rtt/5), " s")
    
    s_client.close()
    client_udp.close()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        serverSide()
    elif len(sys.argv) == 2:    
        clientSide()