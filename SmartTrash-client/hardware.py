import RPi.GPIO as GPIO

"""
mg995舵机的控制一般需要一个20ms的时基脉冲，该脉冲的高电平部分一般为0.5ms~2.5ms范围内的角度控制脉冲部分。
以180度角度舵机为例，那么对应的控制关系是这样的：
　　0.5ms————–0度；
　　1.0ms————45度；
　　1.5ms————90度；
　　2.0ms———–135度；
　　2.5ms———–180度；
"""

IN1=18
IN2=23
GPIO.setmode(GPIO.BOARD)
def init():
    global p1
    global p2
    GPIO.setup(IN2, GPIO.OUT)
    p1= GPIO.PWM(IN1, 50)#50-频率
    p2= GPIO.PWM(IN2, 50)
    p1.start(angle2duty(90))
    p2.start(angle2duty(90))
    #p1.ChangeDutyCycle(0)
def close():
    p1.stop()
    p2.stop()
    GPIO.cleanup()
    
def angle2duty(degree):
    if degree>180 or degree<0:
        print('err:ang2dut:'+degree)
        return angle2duty(90)
    return degree/180*2+0.5