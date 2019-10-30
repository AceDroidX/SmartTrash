#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import sys,threading,os
import HttpServer
import api

isdebug = True
usedb=True

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
    #TCPSocket.startServer()
    HttpServer.start()
    about()
    print("SmartTrash已启动\n控制台帮助请输入help")
    # ----------------------------

    if usedb:
        pass
    
    # loop
    while True:
        cmd=input("wxx>").split(' ')
        if cmd[0] == "help":
            print("SmartTrash控制台帮助")
            print("about或version-----显示版本信息")
            print("help-----显示此帮助")
            print("stop或exit-----退出程序")
            print("")
        elif cmd[0] == "stop" or cmd[0] == "exit":
            stop()
        elif cmd[0] == "about" or cmd[0] == "version":
            about()
        elif cmd[0] == '':
            pass
        else:
            print("未知命令 输入help查看帮助")
        cmd = ""
        # --------------------------------------
