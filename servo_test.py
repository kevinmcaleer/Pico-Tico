from machine import Pin, PWM
from time import sleep
p1 = Pin(0)
p2 = Pin(1)
p3 = Pin(2)

pwm1 = PWM(p1)
pwm2 = PWM(p2)
pwm3 = PWM(p3)

pwm1.freq(50)
pwm2.freq(50)
pwm3.freq(50)

min_pulse = 1200
max_pulse = 8620
# min_pulse = 550
# max_pulse = 2500

print("min")
pwm1.duty_u16(min_pulse)
sleep(1)
print("max")
pwm1.duty_u16(max_pulse)
sleep(1)

step = 100
speed = 0.1
while True:
    for n in range (min_pulse, max_pulse, step):
        print(n)
        pwm1.duty_u16(n)
        pwm2.duty_u16(n)
        pwm3.duty_u16(n)
        sleep(speed)

    for n in range (max_pulse, min_pulse, step):
        print(n)
        pwm1.duty_u16(n)
        pwm2.duty_u16(n)
        pwm3.duty_u16(n)
        sleep(speed)