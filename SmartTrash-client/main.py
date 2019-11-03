#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import threading
import os,urllib,string
import image
import hardware,distance
import ui,APIKey

isdebug = True
showui=True
resetonstart=True
usedist=True
uihistory=True
checknet=True
usemulti=True

cmd = ''

# functions
def stop():
    print("退出程序中")
    os._exit(0)

def about():
    print("----------------------------")
    print('https://AceDroidX.github.io/?f=st')
    print("By AceDroidX")
    print("----------------------------")

def run():
    image.take()
    name=image.image_classify(image.image)['result'][0]['keyword']
    trashtype=image.getType(image.result['result'][0]['keyword']+'/'+image.result['result'][0]['root'])
    hardware.run(trashtype)
    return [name,trashtype]

def netchecker():
    host = urllib.parse.quote(APIKey.netchecker_url, safe=string.printable)
    request = urllib.request.Request(host)
    content = urllib.request.urlopen(request,timeout=2).read().decode("utf-8")
    return content=="SmartTrash"

# -----------------------------
if __name__ == '__main__':
    # setup
    if isdebug:
        print("命令行参数:%s" % sys.argv)
    about()
    print("SmartTrash已启动\n控制台帮助请输入help")
    # ----------------------------
    if showui:
        ui.startui()
    if resetonstart:
        hardware.reset()
    if usedist:
        distance.startThread()
    if checknet:
        if not netchecker():
            print('网络连接异常')
    # loop
    while True:
        cmd = input("wxx>")
        if cmd == "help":
            print("SmartTrash控制台帮助")
            print("about或version-----显示版本信息")
            print("help-----显示此帮助")
            print("stop或exit-----退出程序")
            print("")
        elif cmd == "stop" or cmd == "exit":
            stop()
        elif cmd == "about" or cmd == "version":
            about()
        elif cmd == "take":
            image.take()
        elif cmd == "imgc":
            image.image_classify(image.image)
        elif cmd == "get":
            image.get()
        elif cmd == 'type':
            image.getType(image.result['result'][0]['keyword']+'/'+image.result['result'][0]['root'])
        elif cmd == 'run':
            run()
        elif cmd == 'setdist':
            distance.distmin=float(input('input the distmin:'))
        elif cmd == 'setdisttime':
            distance.whiletime=float(input('input the whiletime:'))
        elif cmd == '':
            pass
        else:
            print("未知命令 输入help查看帮助")
        cmd = ""
        # --------------------------------------
