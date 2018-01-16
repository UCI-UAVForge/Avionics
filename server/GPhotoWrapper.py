import os, subprocess, signal
from time import sleep

def captureImageAndDownload(fname):
  p = subprocess.Popen(['sudo', 'gphoto2', '--capture-image-and-download', '--filename='+fname+'.jpg', '--force-overwrite'], stdout=subprocess.PIPE)
  out, err = p.communicate()
  print(out)
  return out


"""
p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
out, err = p.communicate()
for line in out.splitlines():
	if b'gvfsd-gphoto2' in line:
		pid = int(line.split(None, 1)[0])
		os.kill(pid, signal.SIGKILL)
"""

def test():
  captureImageAndDownload('000')
  sleep(1)
  captureImageAndDownload('001')
  sleep(1)
  captureImageAndDownload('002')
  sleep(1)


if __name__=='__main__':
  test()
else:
  print("Loaded GPhotoWrapper")
  
"""
os.system("sudo gphoto2 --capture-image-and-download --filename=001.jpg --force-overwrite")
photoNum = 3
sleep(1)
os.system("sudo gphoto2 --camera "Sony Alpha-A6000 (Control)" --capture-image-and-download --filename=" + str(photoNum) + ".jpg --force-overwrite")
sleep(1)
os.system("sudo feh " + str(photoNum) + ".jpg -.")
"""
