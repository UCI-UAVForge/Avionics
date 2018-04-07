from socket import *
import sys

class Request:
  def __init__(this, host, port, requestType='GET', path='', args={}):
    this.host = host
    this.port = port
    this.requestType = requestType
    this.path = path
    this.args = args
    
def getResponse(clientSocket, bufsize=1024):
  buffer = b''
  while True:
    recv = clientSocket.recv(bufsize)
    buffer += recv
    if not recv:
      break
  return buffer

def makeQueryString(args):
  argStrings = []
  for key in args.keys():
    argStrings.append(key+'='+args[key])
  return '&'.join(argStrings)

def sendRequest(request, bufsize=1024):  
  host = request.host
  port = request.port
  request_type = request.requestType
  path = request.path
  args = request.args

  try:
    if request_type is not 'GET' and request_type is not 'POST':
      request_type='GET'

    responseData = ''
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    clientSocket.send(request_type.encode('utf-8') + b' ' + path.encode('utf-8'))
    if len(args) > 0:
      clientSocket.send(b'?'+makeQueryString(args).encode('utf-8'))
    clientSocket.send(b' HTTP/1.1\r\n')

    clientSocket.send(b'Host: '+host.encode('utf-8')+b':'+bytes(port)+b'\r\n')
    clientSocket.send(b'\r\n\r\n')
    clientSocket.shutdown(SHUT_WR)
    text = ''
    buffer = getResponse(clientSocket,bufsize)
    
    responseData = buffer.split(b'\r\n\r\n')[1]
  except ConnectionResetError:
    print ('Connection reset by server %s:%s!'%(host,port))
  except ConnectionRefusedError:
    print ('Connection refused by server %s:%s!'%(host,port))
  except IOError as ioerror:
    print ("IO error: {0}".format(ioerror))
    print ('An IO error occured!')
  finally:
    clientSocket.close()
  return responseData

def main():
  pass
  
if __name__=="__main__":
  main()
else:
  print("Loaded Request.py")

