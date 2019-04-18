import socket, sys, threading

listeningPorts = sys.argv[1].split(',')
protocol = sys.argv[2]
serverIPAddresses = sys.argv[3].split(',')
clientIPAddress = sys.argv[4]   
bufferSize = 1024
CLOSE_CONNECTION = 'close'
TCP_PROTOCOL= 'tcp'
UDP_PROTOCOL= 'udp'
TIME_OUT =5

def tcpClient(ip,port):
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  #client.settimeout(TIME_OUT)
  try:
     client.connect((ip,port))
     ipAdd = socket.gethostbyname(socket.gethostname())
     print("tcp client [",ipAdd,"] connecting to server [",ip,"]  at port [",port,"]")
     client.close()
     print("closing tcp client [",ipAdd,"] connected to server [",ip,"]  at port [",port,"]")
  except Exception as e:
     sys.stderr.write('Failed to connect tcp server ['+str(ip)+'] at port ['+str(port)+']  ' )
     sys.stderr.write(str(e))

def udpClient(ip,port):
  udpclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
  udpclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  udpclient.settimeout(TIME_OUT)
  ipAdd = socket.gethostbyname(socket.gethostname())
  print("udp client [",ipAdd,"] connecting to server [",ip,"]  at port [",port,"]")
  try:
      udpclient.sendto('Hello', (ip,port))
      data, addr = udpclient.recvfrom(1024)
      if data == CLOSE_CONNECTION :
        udpclient.close()
        print("closing udp client [",ipAdd,"] connected to server [",ip,"]  at port [",port,"]")
  except Exception as e:
     sys.stderr.write('Failed to connect udp server ['+str(ip)+'] at port ['+str(port)+']  ' )
     sys.stderr.write(str(e))

def handleRequest(ip,port):
  if protocol == TCP_PROTOCOL:
     clientConnThread = threading.Thread(target=tcpClient, args=(ip,port,))
     clientConnThread.start()
  else:
     clientConnThread = threading.Thread(target=udpClient, args=(ip,port,))
     clientConnThread.start()

if socket.gethostbyname(socket.gethostname()) in clientIPAddress == True or socket.gethostname() in clientIPAddress == True:
 for ip in serverIPAddresses:
   for port in listeningPorts:
     range = port.split('-') 
     frm = int(range[0])
     if len(range) > 1 :
        to = range[1]
        while frm < (int(to)+1):
          handleRequest(ip,frm)
          frm=frm+1   
     else:
        handleRequest(ip,frm)

