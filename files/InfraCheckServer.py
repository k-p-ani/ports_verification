import socket, sys, threading

listeningPorts = sys.argv[1].split(',')
protocol = sys.argv[2]
serverIPAddresses = sys.argv[3]
bufferSize = 1024
CLOSE_CONNECTION = 'close'
TCP_PROTOCOL= 'tcp'
UDP_PROTOCOL= 'udp'

def tcpServer(port):
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(('', int(port)))
  server.listen(500)
  ipAdd = socket.gethostbyname(socket.gethostname())
  print("tcp server [",ipAdd,"] will listen at port [",port,"]")
  while True:
    print("waiting for tcp client connection")
    client, addr = server.accept()
    print("accepted tcp client connection")
    clientConnThread = threading.Thread(target=handleTCPRequest, args=(client,))
    clientConnThread.start()

def udpServer(port):
  udpserver = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  udpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  udpserver.bind(('', int(port)))
  ipAdd = socket.gethostbyname(socket.gethostname())
  print("udp server [",ipAdd,"] will listen at port [",port,"]")
  while True:
    print(" waiting for udp client connection ")
    data, address  = udpserver.recvfrom(bufferSize)
    print("data received from client ",data)
    udpserver.sendto(CLOSE_CONNECTION, address)

def handleTCPRequest(clientConn):
    request = clientConn.recv(bufferSize)
    clientConn.close()

def handleRequest(port):
  if protocol == TCP_PROTOCOL:
     clientConnThread = threading.Thread(target=tcpServer, args=(port,))
     clientConnThread.start()
  else:
     print("started udp server")
     clientConnThread = threading.Thread(target=udpServer, args=(port,))
     clientConnThread.start()
 
if ip in socket.gethostbyname(socket.gethostname()) == True or ip in socket.gethostname() == True:
  for port in listeningPorts:
    range = port.split('-') 
    frm = int(range[0])
    if len(range) > 1 :
      to = range[1]
      while frm < (int(to)+1):
        handleRequest(frm)
        frm=frm+1   
    else:
      handleRequest(frm)

