import mraa
import time        
import perceptive_layer as pl

def user_input_record(time_interval):
        button_3 = mraa.Gpio(2)
        button_4 = mraa.Gpio(4)
        # virtual buttons  
        button_1 = mraa.Gpio(7)
        button_2 = mraa.Gpio(8)

        button_3.dir(mraa.DIR_IN)
        button_4.dir(mraa.DIR_IN)
        # feed to Edison 2   
        button_1.dir(mraa.DIR_IN)
        button_2.dir(mraa.DIR_IN)

        initial_time = time.time()
           
        previous_1 = 0
        previous_2 = 0
        previous_3 = 0
        previous_4 = 0

        record = []

        while True:                           
                timestamp = time.time() - initial_time
                             
                if (timestamp >= time_interval):
                        print "Manually mode terminated."
                        break

                current_1 = button_1.read()
                current_2 = button_2.read()
                current_3 = button_3.read()
                current_4 = button_4.read()
               
                if (current_1 != previous_1):
                        previous_1 = current_1
                        record.append(do_1(current_1, timestamp))

                if (current_2 != previous_2):
                        previous_2 = current_2
                        record.append(do_2(current_2, timestamp))

                if (current_3 != previous_3):
                        previous_3 = current_3
                        record.append(do_3(current_3, timestamp))

                if (current_4 != previous_4):
                        previous_4 = current_4
                        record.append(do_4(current_4, timestamp))
                          

                time.sleep(0.0005)

        return rearrange(record)

def do_1(value, timestamp):
        if (value == 1):
                pl.play_note(True, 1, True)
                return [1, 'p', timestamp]
        else:
                pl.play_note(True, 1, False)      
                return [1, 'r', timestamp]

def do_2(value, timestamp):
        if (value == 1):
                pl.play_note(True, 2, True)
                return [2, 'p', timestamp]
        else:
                pl.play_note(True, 2, False)      
                return [2, 'r', timestamp]

def do_3(value, timestamp):
        if (value == 1):
                pl.play_note(True, 3, True)
                return [3, 'p', timestamp]
        else:
                pl.play_note(True, 3, False)      
                return [3, 'r', timestamp]


def do_4(value, timestamp):
        if (value == 1):
                pl.play_note(True, 4, True)
                return [4, 'p', timestamp]
        else:
                pl.play_note(True, 4, False)      
                return [4, 'r', timestamp]

def rearrange(record):
        music = []

        for i in range(len(record)):
                # detect note
                if (record[i][1] == 'p' and i+1 < len(record)):
                        if (record[i+1][1] == 'r'):
                                note = record[i][0]
                                duration = record[i+1][2] - record[i][2]
                                music.append([note, duration])

                # detect break
                if (record[i][1] == 'r' and i+1 < len(record)):
                        if (record[i+1][1] == 'p'):
                                note = 0 # break
                                duration = record[i+1][2] - record[i][2]
                                music.append([note, duration])

        return music