from socket import *
import sys
import time

def getResponse():
  buffer = b''
  while True:
    recv = clientSocket.recv(4096*1024*128)
    buffer += recv
    if not recv:
      break
  return buffer

#parse params
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])

if len(sys.argv) > 3:
  filename = sys.argv[3]
else:
  filename = 'current'

#setup socket
start = time.time()
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverHost, serverPort))

#send requests
#take photo
#clientSocket.send(b'POST /capture?fname='+filename.encode('utf-8')+b' HTTP/1.1\r\n')
#clientSocket.send(b'Host: '+serverHost.encode('utf-8')+b':'+bytes(serverPort)+b'\r\n')
#clientSocket.send(b'\r\n\r\n')

#get response
#getResponse()

#download photo
clientSocket.send(b'GET /getImage?fname='+filename.encode('utf-8')+b' HTTP/1.1\r\n')
clientSocket.send(b'Host: '+serverHost.encode('utf-8')+b':'+bytes(serverPort)+b'\r\n')
clientSocket.send(b'\r\n\r\n')

#collect response

text = ''

buffer = getResponse()

finish = time.time()

print('download took %f seconds' % (finish-start))

f = open('output.jpg',r'bw')
f.write(bytes(buffer.split(b'\r\n\r\n')[1]))
f.close()

clientSocket.close()
