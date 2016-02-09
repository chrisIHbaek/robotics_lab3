import mraa
import time

# Set up servo motors
servo_1 = mraa.Pwm(3)
servo_2 = mraa.Pwm(5)
servo_3 = mraa.Pwm(6)
servo_4 = mraa.Pwm(9)

servo_1.period_ms(20)
servo_2.period_ms(20)
servo_3.period_ms(20)
servo_4.period_ms(20)

servo_1.enable(True)
servo_2.enable(True)
servo_3.enable(True)
servo_4.enable(True)

def press_1():       
        servo_1.write(0.079)
                            
def press_2():              
        servo_2.write(0.045)
                            
def press_3():              
        servo_3.write(0.081)
                            
def press_4():              
        servo_4.write(0.063)
                            
def release_1():            
        servo_1.write(0.097)
                            
def release_2():            
        servo_2.write(0.060)
                            
def release_3():            
        servo_3.write(0.095)
                            
def release_4():            
        servo_4.write(0.076)
