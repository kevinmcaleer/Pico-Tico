# Configure the 3 servos

from machine import Pin, PWM
from time import sleep

lift_servo = PWM(Pin(0)) # was 5
left_servo = PWM(Pin(2)) # was 7
right_servo = PWM(Pin(1)) # was 6

lift_servo.freq(50)
left_servo.freq(50)
right_servo.freq(50)

lift_angle = 31
left_angle = 130
right_angle = 140

min_pulse = 1200
max_pulse = 8620

def mapValue(value, in_min, in_max, out_min, out_max):    
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# def servo(degrees):
#     servoPin = PWM(Pin(16))
#     servoPin.freq(50)
#     if degrees > 180: degrees=180
#     if degrees < 0: degrees=0
#     newDuty=min_pulse+(max_pulse-min_pulse)*(degrees/180)
#     servoPin.duty_u16(int(newDuty))

while True:
    lift_pulse = int(mapValue(lift_angle, 0,180,min_pulse,max_pulse))
    left_pulse = int(mapValue(left_angle, 0,180,min_pulse,max_pulse))
    right_pulse = int(mapValue(right_angle, 0,180,min_pulse,max_pulse))
    print("lift_angle",lift_angle, "lift_pulse", lift_pulse)
    print("left_angle",left_angle, "left_pulse", left_pulse)
    print("right_angle",right_angle, "right_pulse", right_pulse)

    lift_servo.duty_u16(lift_pulse)
    left_servo.duty_u16(left_pulse)
    right_servo.duty_u16(right_pulse)
    sleep(1)

    # lift_pulse = int(mapValue(0, 0,180,min_pulse,max_pulse))
    # left_pulse = int(mapValue(0, 0,180,min_pulse,max_pulse))
    # right_pulse = int(mapValue(0, 0,180,min_pulse,max_pulse))
    # print("lift_angle",0, "lift_pulse", lift_pulse)
    # print("left_angle",0, "left_pulse", left_pulse)
    # print("right_angle",0, "right_pulse", right_pulse)
    # lift_servo.duty_u16(lift_pulse)
    # left_servo.duty_u16(left_pulse)
    # right_servo.duty_u16(right_pulse)
    sleep(1)