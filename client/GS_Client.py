import Request
import sys

def main():
  #parse params
  serverHost = sys.argv[1]
  serverPort = int(sys.argv[2])
  path = sys.argv[3]

  if (path=='/getImage'):
    r = Request.Request(serverHost, serverPort, 'GET', path)
    image = Request.sendRequest(r)
    #write imagefile
    f = open('output.jpg',r'wb')
    f.write(image)
    f.close()
  else:
    r = Request.Request(serverHost, serverPort, 'POST', path)
    outputText = Request.sendRequest(r)
    print(outputText)

if __name__=="__main__":
  main()

