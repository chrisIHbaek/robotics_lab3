import time
import reactive_layer

def play_note(manual, note, duration):

    if(manual):
        if(note == 1):
            if(duration):
                reactive_layer.press_1()
            else:
                reactive_layer.release_1()
        elif(note == 2):
            if(duration):
                reactive_layer.press_2()
            else:
                reactive_layer.release_2()
        elif(note == 3):
            if(duration):
                reactive_layer.press_3()
            else:
                reactive_layer.release_3()
        elif(note == 4):
            if(duration):
                reactive_layer.press_4()
            else:
                reactive_layer.release_4()
        else:
            time.sleep(0.25)
        
    else:
        if(note == 1):
            reactive_layer.press_1()
            time.sleep(duration - 0.1)
            reactive_layer.release_1()
            time.sleep(0.1)
        elif(note == 2):
            reactive_layer.press_2()
            time.sleep(duration - 0.1)
            reactive_layer.release_2()
            time.sleep(0.1)
        elif(note == 3):
            reactive_layer.press_3()
            time.sleep(duration - 0.1)
            reactive_layer.release_3()
            time.sleep(0.1)
        elif(note == 4):
            reactive_layer.press_4()
            time.sleep(duration - 0.1)
            reactive_layer.release_4()
            time.sleep(0.1)
        else:
            time.sleep(duration)

def initialize_arms():
    reactive_layer.release_1()
    reactive_layer.release_2()
    reactive_layer.release_3()
    reactive_layer.release_4()
    time.sleep(1)

