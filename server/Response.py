codeStrings = {
  '200':'OK',
  '400':'Bad Request',
  '404':'Not Found',
  '500':'Internal Server Error',
}

class Response:
  def __init__(this, code='200', data='Empty Response', dataType='text/html', charset='utf-8'):
    this.code = code
    this.dataType = dataType
    this.charset = charset
    this.data = data
      
  def __str__(this):
    msg = []
    msg.append('HTTP/1.1 ' + this.code + ' ' + codeStrings[this.code])
    msg.append('Content-Type: ' + this.dataType + '; charset=' + this.charset)
    msg.append('')
    msg.append(this.data)
    msg.append('')
    msg.append('')
    msg.append('')
    return '\r\n'.join(msg)

  def __bytes__(this):
    msg = []
    msg.append(b'HTTP/1.1 ' + this.code.encode('utf-8') + b' ' + codeStrings[this.code].encode('utf-8'))
    msg.append(b'Content-Type: ' + this.dataType.encode('utf-8') + b'; charset=' + this.charset.encode('utf-8'))
    msg.append(b'')
    if type(this.data) == type('string'):
      msg.append(this.data.encode('utf-8'))
    else:
      msg.append(this.data)
    msg.append(b'')
    msg.append(b'')
    msg.append(b'')
    return b'\r\n'.join(msg)

  def setPayload(this, data):
    this.data = data

  def setType(this, contentType):
    this.type = contentType
  
  def toHTTP(this):
    return bytes(this)

def test():
  r = Response('404','404 Not Found')
  print(r)
  print(bytes(r))

if __name__=='__main__':
  test()
else:
  print("Loaded Response")
