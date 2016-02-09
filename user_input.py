import mraa
import time
import reactive_layer as rl
import perceptive_layer as pl

def user_input(timer):

	button_1 = mraa.Gpio(2)
	button_2 = mraa.Gpio(4)
	# virtual buttons
	button_1_out = mraa.Gpio(7)
	button_2_out = mraa.Gpio(8)

	button_1.dir(mraa.DIR_IN)
	button_2.dir(mraa.DIR_IN)
	# feed to Edison 2 
	button_1_out.dir(mraa.DIR_OUT)
	button_2_out.dir(mraa.DIR_OUT)

	initial_time = time.time()

	while True:
		timestamp = time.time() - initial_time

		if (timestamp >= timer):
			print "Manually mode terminated."
			break

		if (button_1.read() == 1):
	                pl.play_note(True, 1, True)      
			button_1_out.write(1)
		else:
	                pl.play_note(True, 1, False)      
			button_1_out.write(0)
		if (button_2.read() == 1):
			pl.play_note(True, 2, True)
			button_2_out.write(1)
		else:
			pl.play_note(True, 2, False)
			button_2_out.write(0)		

		time.sleep(0.0005)
