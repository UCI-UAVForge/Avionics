from socket import *
import GPhotoWrapper
from Response import Response

def main():
  try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 6789))
  except OSError:
    print('Unable to open the socket. Terminate any processes using port 6789 and try again later.')
    return
  
  serverSocket.listen(1)

  serverUp = True

  while serverUp:
    print("Ready to serve...")
    (connectionSocket, addr) = serverSocket.accept()
    r = Response()
    
    try:
      message = connectionSocket.recv(2048)

      print(message.decode())
    
      argString = message.split()[1].decode()
      params = {}
      path = ''

      print("args %s"%argString)

      if '?' in argString:
        path = argString.split('?')[0]
        parts = argString.split('?')[1].split('&')
        for part in parts:
          key = part.split('=')[0]
          value = part.split('=')[1]
          params[key] = value
          print('%s = %s'%(key,value))
      else:
        path = argString

      print("path: %s"%path)
      print("params %s"%params)
      
      outputdata = b'nope'

      if path == '/getImage':
        filename = params.get('fname','current')
        
        print("getting response for: " + str(filename))
        f = open(filename+'.jpg', "rb")
        outputdata = f.read()
        f.close()

        r = Response('200', outputdata, 'image/jpg')

      elif path == '/capture':
        filename = params.get('fname','current')
        outputdata = GPhotoWrapper.captureImageAndDownload(filename)
        
        r = Response('200', outputdata, 'text/plain')
        
      elif path == '/shutdown':
        r = Response('200', 'Server Sutting Down. Goodbye.')
        serverUp = False

      else:
        r = Response('404', '404 Not Found')
      connectionSocket.send(bytes(r))
    except IOError:
      r = Response('404', '404 Not Found')
      connectionSocket.send(bytes(r))
    except KeyError:
      r = Response('400', '400 Bad Request')
      connectionSocket.send(bytes(r))
    except IndexError:
      r = Response('500', '500 Internal Server Error')
      connectionSocket.send(bytes(r))
    finally:
      connectionSocket.close()
  serverSocket.close()

if __name__=='__main__':
  main()
