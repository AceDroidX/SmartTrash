import pigpio

IN1=18
IN2=23

def angle2duty(degree):
    if degree>180 or degree<0:
        print('err:ang2dut:'+degree)
        return angle2duty(90)
    print((0.5 + degree / 180 * 2)/20*2000)
    return (0.5 + degree / 180 * 2)/20*2000

def init():
    global pi
    pi = pigpio.pi()
    pi.set_PWM_frequency(IN1, 50)
    pi.set_PWM_range(IN1, 2000)
    pi.set_PWM_dutycycle(IN1,angle2duty(90))
    pi.set_PWM_frequency(IN2, 50)
    pi.set_PWM_range(IN2, 2000)
    pi.set_PWM_dutycycle(IN2,angle2duty(90))

def change(port,angle):
    global pi
    pi.set_PWM_dutycycle(port,angle2duty(angle))
    
if __name__ == '__main__':
    init()
    while(True):
        num=angle2duty(float(input('>')))
        change(IN1,num)
        change(IN2,num)