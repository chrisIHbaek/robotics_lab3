import time
import perceptive_layer as pl
import user_input_record as ui

def simon():
    itr = 1
    pattern = [1, 3, 2, 4, 4, 3, 1, 2, 4, 2]

    timer = 3
    
    while True:
        for i in range(0, itr):
	    time.sleep(0.3)
            pl.play_note(False, pattern[i], 0.7)
    
        response = ui.user_input_record(timer)
        note_array = []
        
        for i in range(0, len(response)):
		if (response[i][0] != 0):
            		note_array.append(response[i][0])

        valid = cmp(pattern[0:itr], note_array)

	print pattern[0:itr]
	print note_array
	print valid
        
        if(valid == 0):
            if(itr<4):
                itr += 1
                timer += .75
            else:
                return True
        else:
            return False


