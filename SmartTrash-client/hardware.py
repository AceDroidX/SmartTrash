import pigpio
import time
import os
# 40-90 90-140
IN1 = 23
IN2 = 18
changetime = 1
pi = None
turnangle=90
turnang2=60

def angle2duty(degree):
    if degree > 180 or degree < 0:
        print('err:ang2dut:'+degree)
        return angle2duty(90)
    #print((0.5 + degree / 180 * 2)/20*2000)
    return (0.5 + degree / 180 * 2)/20*2000


def init():
    global pi
    if pi != None:
        return
    cmd = os.popen('ps -Al|grep pigpiod').read()
    if cmd.find('pigpiod') == -1:
        os.popen('sudo pigpiod')
        time.sleep(0.5)
    pi = pigpio.pi()
    pi.set_PWM_frequency(IN1, 50)
    pi.set_PWM_range(IN1, 2000)
    pi.set_PWM_dutycycle(IN1, angle2duty(90))
    time.sleep(changetime)
    pi.set_PWM_frequency(IN2, 50)
    pi.set_PWM_range(IN2, 2000)
    pi.set_PWM_dutycycle(IN2, angle2duty(90))


def change(port, angle):
    global pi
    if pi == None:
        init()
    print('change angle:'+str(port)+'    '+str(angle))
    pi.set_PWM_dutycycle(port, angle2duty(angle))


def reset():
    global pi
    global changetime
    if pi == None:
        init()
    pi.set_PWM_dutycycle(IN1, angle2duty(90))
    time.sleep(changetime)
    pi.set_PWM_dutycycle(IN2, angle2duty(90))


def run(trashtype):
    global changetime
    if pi == None:
        init()
    if type(trashtype)==int:
        trashtype=str(trashtype)
    #'可回收', '有害', '厨余(湿)', '其他(干)'
    if trashtype == '可回收' or trashtype == '0':
        change(IN1, 90-turnangle)
        time.sleep(changetime)
        change(IN2, 90-turnang2)
    elif trashtype == '有害' or trashtype == '1':
        change(IN1, 90-turnangle)
        time.sleep(changetime)
        change(IN2, 90+turnang2)
    elif trashtype == '厨余(湿)' or trashtype == '2':
        change(IN1, 90+turnangle)
        time.sleep(changetime)
        change(IN2, 90-turnang2)
    elif trashtype == '其他(干)' or trashtype == '3':
        change(IN1, 90+turnangle)
        time.sleep(changetime)
        change(IN2, 90+turnang2)
    else:
        print('err:hardware run trashtype')
    time.sleep(changetime)
    reset()


if __name__ == '__main__':
    init()
    while True:
        #run(input('in1>'))
        num=int(input('in1>'))
        change(IN1,num)
        #num=int(input('in2>'))
        #change(IN2,num)
