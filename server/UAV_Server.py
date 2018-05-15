from socket import *
import time
import os
import GPhotoWrapper
from Response import Response

def main():
  try:
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', 6789))
  except OSError:
    print('Unable to open the socket. Terminate any processes using port 6789 and try again later.')
    return
  
  serverSocket.listen(1)

  serverUp = True
  missionStartTime = time.time();

  while serverUp:
    print("Ready to serve...")
    (connectionSocket, addr) = serverSocket.accept()
    r = Response()
    
    try:
      message = connectionSocket.recv(1024*1024)
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

      elif path == '/captureAndDownload':
        filename = 'img-%d'%(time.time()-missionStartTime)
        gphotoMessage = GPhotoWrapper.captureImageAndDownload(filename)
        f = open(filename+'.jpg', "rb")
        outputdata = f.read()
        f.close()
        os.remove(filename+'.jpg')
        
        r = Response('200', outputdata, 'image/jpg')
      elif path == '/start':
        clientTime = params.get('client_time',time.time())
        serverTime = time.time()

        missionStartTime = clientTime;

        format_string = '''
        <html>
          <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 2px;
            }
          </style>
          <body>
            <table>
              <tr>
                <th> </th>
                <th>Time String</th>
                <th>Unix Timestamp</th>
              </tr>
              <tr>
                <td>Client Time</td>
                <td>%s</td>
                <td>%s</td>
              </tr>
              <tr>
                <td>Server Time</td>
                <td>%s</td>
                <td>%s</td>
              </tr>
            </table>
          </body>
        </html>
        '''

        dateFormat = '%Y-%m-%d %H:%M:%S'
        
        r = Response('200', format_string %
                     (time.strftime(dateFormat,time.gmtime(((float)(clientTime)-time.timezone+3600*time.daylight))),
                      clientTime,
                      time.strftime(dateFormat,time.gmtime(((float)(serverTime)-time.timezone+3600*time.daylight))),
                      serverTime
                      ),
                     'text/html')
        
      elif path == '/shutdown':
        r = Response('200', 'Server Sutting Down. Goodbye.')
        serverUp = False

      else:
        r = Response('404', '404 Not Found')
      print("%d bytes to send" % len(bytes(r)))
      sent_bytes = connectionSocket.send(bytes(r))
      print("%d bytes sent" % sent_bytes)
      connectionSocket.shutdown(SHUT_WR)
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
      #todo: make a better delay mechanism - perhaps a manual ack?
      time.sleep(0.5)
  serverSocket.close()

if __name__=='__main__':
  main()
