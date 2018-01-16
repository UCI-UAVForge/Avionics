from socket import *
import GPhotoWrapper

class Response:
  def __init__(this,code,message=None):
    this.code=code;
    if message:
      this.message = message
    else:
      this.message = 'No message given.'

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('localhost', 6789))

serverSocket.listen(1)

while True:
  print("Ready to serve...")
  (connectionSocket, addr) = serverSocket.accept()
  try:
    message = connectionSocket.recv(2048)

    print(message.decode())
  
    argString = message.split()[1].decode()
    params = []
    path = ''

    print("args %s"%argString)

    if '?' in argString:
      path = argString.split('?')[0]
      params = argString.split('?')[1].split('&')
    else:
      path = argString
      params = []

    print("path: %s"%path)
    print("params %s"%params)
    
    outputdata = b'nope'

    if path == '/getImage':
      filename = params[0]
      print("getting response for: " + str(filename))
      f = open(filename, "rb")
      outputdata = f.read()
      f.close()

      connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
      connectionSocket.send(b'Content-Type: image/jpg; charset=utf-8\r\n')
      connectionSocket.send(b'\r\n')

      connectionSocket.send(outputdata)
      
      connectionSocket.send(b'\r\n\r\n')
      print('sent response correctly')
      connectionSocket.close()
        
    if path == '/capture':
      outputdata = GPhotoWrapper.captureImageAndDownload('current')
      
      connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
      connectionSocket.send(b'Content-Type: text/html; charset=utf-8\r\n')
      connectionSocket.send(b'\r\n')

      connectionSocket.send(b'output:')
      connectionSocket.send(outputdata)
      connectionSocket.send(b'DONE')
      
      connectionSocket.send(b'\r\n\r\n')
      print('sent response correctly')
      connectionSocket.close()
    

  except IOError:
    connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n')
    connectionSocket.send(b'Content-Type: text/html; charset=utf-8\r\n')
    connectionSocket.send(b'\r\n')
    connectionSocket.send(b'404 Not Found\r\n')
    connectionSocket.send(b'\r\n\r\n')
    print('A 404 error occured')
    connectionSocket.close()
  except IndexError:
    connectionSocket.send(b'HTTP/1.1 500 Internal Server Error\r\n')
    connectionSocket.send(b'Content-Type: text/html; charset=utf-8\r\n')
    connectionSocket.send(b'\r\n')
    connectionSocket.send(b'500 Internal Server Error\r\n')
    connectionSocket.send(b'\r\n\r\n')
    print('A 500 error occured')
    connectionSocket.close()
serverSocket.close()
