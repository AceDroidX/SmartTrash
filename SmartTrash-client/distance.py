#导入 GPIO库
import RPi.GPIO as GPIO
import time
import ui,main
import threading
 
distmin=25
whiletime=1
distmax=1
 
#设置 GPIO 模式为 BCM
GPIO.setmode(GPIO.BCM)
#定义 GPIO 引脚
GPIO_TRIGGER = 20
GPIO_ECHO = 21
#设置 GPIO 的工作方式 (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
def distance():
    # 发送高电平信号到 Trig 引脚
    GPIO.output(GPIO_TRIGGER, True)
    # 持续 10 us 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start_time = time.time()
    stop_time = time.time()
    # 记录发送超声波的时刻1
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()
    # 记录接收到返回超声波的时刻2
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()
    # 计算超声波的往返时间 = 时刻2 - 时刻1
    time_elapsed = stop_time - start_time
    # 声波的速度为 343m/s， 转化为 34300cm/s。
    distance = (time_elapsed * 34300) / 2
    return distance
 
def run():
    pass
 
def start():
    time.sleep(0.5)
    while True:
        global dist
        dist = distance()
        print("Measured Distance = {:.2f} cm".format(dist))#debug
        if dist<distmin and dist>distmax:
            print('distance.start:dist<distmin')
            if main.usemulti:
                ui.run_multi()
            else:
                ui.run()
        time.sleep(whiletime)
        
def startThread():
    serverThread = threading.Thread(target=start)
    serverThread.start()
    
if __name__ == '__main__':
    '''
    ui.startui()
    time.sleep(0.5)
    start()
    '''

    try:
        while True:
            dist = distance()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

