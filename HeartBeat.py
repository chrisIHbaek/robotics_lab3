import mraa

def heartBeat(pulse):
    
    beat = False
    threshold = 500

    input = mraa.Aio(0)
    analogRead = input.read()

    print analogRead
    
    if(analogRead > threshold):
        if(pulse):
            beat = True
            pulse = False
        else:
            beat = False
    else:
        pulse = True

    return (beat, pulse)
