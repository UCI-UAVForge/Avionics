from socket import *
import sys
import time

class Request:
  def __init__(this, host, port, requestType='GET', path='', args={}):
    this.host = host
    this.port = port
    this.requestType = requestType
    this.path = path
    this.args = args
    
def getResponse(clientSocket):
  buffer = b''
  while True:
    recv = clientSocket.recv(4096*1024)
    buffer += recv
    if not recv:
      break
  return buffer

def makeQueryString(args):
  argStrings = []
  for key in args.keys():
    argStrings.append(key+'='+args[key])
  return '&'.join(argStrings)

def sendRequest(request):
  host = request.host
  port = request.port
  request_type = request.requestType
  path = request.path
  args = request.args
  
  if request_type is not 'GET' and request_type is not 'POST':
    request_type='GET'

  responseData = ''
  start = time.time()
  clientSocket = socket(AF_INET, SOCK_STREAM)
  clientSocket.connect((host, port))
  try:
    clientSocket.send(request_type.encode('utf-8') + b' ' + path.encode('utf-8'))
    if len(args) > 0:
      clientSocket.send(b'?'+makeQueryString(args).encode('utf-8'))
    clientSocket.send(b' HTTP/1.1\r\n')

    clientSocket.send(b'Host: '+host.encode('utf-8')+b':'+bytes(port)+b'\r\n')
    clientSocket.send(b'\r\n\r\n')

    text = ''
    buffer = getResponse(clientSocket)
    finish = time.time()
    print('download took %f seconds' % (finish-start))
    
    responseData = buffer.split(b'\r\n\r\n')[1]
    clientSocket.close()
  except IOError:
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

