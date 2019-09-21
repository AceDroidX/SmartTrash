#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys
import threading
import os
import image

isdebug = True

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

# -----------------------------
if __name__ == '__main__':
    # setup
    if isdebug:
        print("命令行参数:%s" % sys.argv)
    about()
    print("SmartTrash已启动\n控制台帮助请输入help")
    # ----------------------------

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
            image.getType(image.result)
        elif cmd == '':
            pass
        else:
            print("未知命令 输入help查看帮助")
        cmd = ""
        # --------------------------------------
