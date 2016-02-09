import simon
import mraa
import time
import perceptive_layer as pl

pl.initialize_arms()
print "Connect servos"
time.sleep(7)
print "Ready"
time.sleep(3)
print "Go"

red = mraa.Gpio(12)
blue = mraa.Gpio(13)

red.dir(mraa.DIR_OUT)
blue.dir(mraa.DIR_OUT)

result = simon.simon()

if (result == False):
	red.write(1)
else:	
	blue.write(1)

time.sleep(4)
red.write(0)
blue.write(0)
