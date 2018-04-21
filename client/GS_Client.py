from Request import *
import sys
import time

def main():
  #parse params
  serverHost = sys.argv[1]
  serverPort = int(sys.argv[2])
  path = sys.argv[3]

  if (path=='/getImage' or path.startswith('/getImage?')):

    #send image request
    r = Request(serverHost, serverPort, 'GET', path)
    print("[INFO] Sending request to %s:%s..." % (serverHost,serverPort))
    start = time.time()
    image = sendRequest(r,1024*1024)
    end = time.time()
    print("[DEBUG] Got %d bytes"%(len(image)))
    print("[DEBUG] Request received in %f seconds" % (end-start))
    
    #write image file
    try:
      f = open('output.jpg',r'wb')
      f.write(image)
      print("[INFO] Image saved to %s"%("output.jpg"))
    except:
      print("[ERROR] Failed to save image!")
    finally:
      f.close()
  elif (path=='/captureAndDownload'):
    #send image request
    r = Request(serverHost, serverPort, 'GET', path)
    print("[INFO] Sending request to %s:%s..." % (serverHost,serverPort))
    start = time.time()
    image = sendRequest(r,1024*1024)
    end = time.time()
    print("[DEBUG] Got %d bytes"%(len(image)))
    print("[DEBUG] Request received in %f seconds" % (end-start))
    
    #write image file
    try:
      filename = 'img-%d'%(start)
      f = open(filename+'.jpg',r'wb')
      f.write(image)
      print("[INFO] Image saved to %s"%(filename+'.jpg'))
    except:
      print("[ERROR] Failed to save image!")
    finally:
      f.close()
  else:
    start = time.time()    
    r = Request(serverHost, serverPort, 'POST', path)
    outputText = sendRequest(r)
    end = time.time()
    print(outputText)
    print("[DEBUG] Request received in %f seconds" % (end-start))

if __name__=="__main__":
  main()

