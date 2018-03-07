# Avionics

## server
Contains the python code for the UAV's image transfer server along with some sample images. Should
be run from the /server directory using ```python3 UAV_Server.py```. The default host is
```localhost``` and the default port is ```6789```.

The server can be accessed by sending an HTTP GET request to the host:portnumber address. For example
to get the ```plane1.jpg``` test file, send an HTTP GET request to ```<hostname>:<port_number>/getImage?<image_name>```
(example: ```localhost:6789/getImage?patrick001.jpg```

Example Files:
- phantom5.jpg
- plane1.jpg
- patrick001.jpg

## client
Contains the python code for the GS's image transfer client. Should be run from the /client directory
using ```python3 UAV_Client.py <server_hostname> <server_port_number> /getImage```
(example: ```python3 UAV_Client.py localhost 6789 /getImage```). Any files downloaded will
be stored in the /client directory.
