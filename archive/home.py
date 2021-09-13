from machine import Pin, PWM
from time import sleep

LEFT_SERVO_PIN = 1
RIGHT_SERVO_PIN = 2
LIFT_SERVO_PIN = 0

min_duty = 1200
max_duty = 8620

left = Pin(LEFT_SERVO_PIN)
lift = Pin(LIFT_SERVO_PIN)
right = Pin(RIGHT_SERVO_PIN)

l = PWM(left)
r = PWM(right)
up = PWM(lift)

PEN_DOWN = 110 # Degrees
LIFT1 = 100
PEN_UP = 70

def mapValue(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def pulse_from_angle(angle)->int:
    """ Returns the pulse from an Angle provided """
    pulse = int(mapValue(angle, 0,180,min_duty, max_duty))
    return pulse

angle = 70
pulse = int(mapValue(angle, 0, 180, min_duty, max_duty))
up.duty_u16(pulse)

pulse = pulse_from_angle(120)
l.duty_u16(pulse)
pulse = pulse_from_angle(60)
r.duty_u16(pulse)

print("Setting Lift to 90 Degrees, connect servo horn and press any key...")
input()

key = "1"
while key != 'q':
    key = input("Angle [Press Q to Quit] >")
    if key != 'q':
        pulse = int(mapValue(int(key), 0, 180, min_duty, max_duty))
        up.duty_u16(pulse)

print("setting Left Servo")

angle = 130
pulse = int(mapValue(angle, 0, 180, min_duty, max_duty))
l.duty_u16(pulse)

print("Setting Left to 130 Degrees, connect servo horn and press any key...")
input()

key = "1"
while key != 'q':
        key = input("Angle [Press Q to Quit] >")
        if key != 'q':
            pulse = int(mapValue(int(key), 0, 180, min_duty, max_duty))
            l.duty_u16(pulse)

print("setting Right Servo")

angle = 140
pulse = int(mapValue(angle, 0, 180, min_duty, max_duty))
r.duty_u16(pulse)

print("Setting Right to 140 Degrees, connect servo horn and press any key...")
input()

key = "1"
while key != 'q':
        key = input("Angle [Press Q to Quit] >")
        if key != 'q':
            pulse = int(mapValue(int(key), 0, 180, min_duty, max_duty))
            r.duty_u16(pulse)