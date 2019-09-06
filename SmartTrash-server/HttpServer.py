#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
from time import sleep
import threading
import sys
import urllib.request
import urllib.parse

# 服务器监视端口号
PORT = 23333
apiURL = "https://laji.lr3800.com/api.php?name="


class Server(http.server.SimpleHTTPRequestHandler):
    def send(self, string):
        self.wfile.write(string.encode('utf-8'))
        print('send:'+string)

    def do_GET(self):
        # 发送空的响应头
        self.send_response(200)
        self.end_headers()
        # 从地址中分割出若干参数
        params = self.path.split('/')
        # 捕获所有错误，防止程序崩溃
        try:
            # 因为有根目录，分割后params[0]必定是空字符串
            # # camera指令：
            # #   如果前边初始化摄像头成功，则直接返回一帧图像
            # #   否则反馈错误信息
            # if params[1] == 'camera':
            #   if cam != None:
            #     __, img = cam.read()
            #     cv2.imwrite('/tmp/camera.jpg', img)
            #     with open('/tmp/camera.jpg', 'rb') as f:
            #       self.wfile.write(f.read())
            #   else:
            #     self.wfile.write("没有检测到摄像头，请插入usb摄像头后重启系统")
            # # virtkey指令：
            # #   如果参数为单字符，则模拟这个按键
            # #   否则反馈错误信息
            # elif params[1] == 'virtkey':
            #   if len(params[2]) == 1:
            #     ord_key = ord(params[2])
            #     v.press_keysym(ord_key)
            #     v.release_keysym(ord_key)
            #   else:
            #     self.wfile.write("参数有误，virtkey指令仅支持单字符参数")
            # # cmd指令：
            # #   如果参数的python函数是合法的，则尝试执行这条指令
            # #   如果途中出错，反馈错误信息
            # elif params[1] == 'cmd':
            #   for func in PCDUINO_FUNC:
            #     if params[2].startswith(func):
            #       try:
            #         exec(params[2])
            #       except:
            #         self.wfile.write(params[2] + '函数的参数有误')
            #       break
            #   else:
            #     self.wfile.write(params[2] + '不是一个已知的函数')
            if params[1] == 'ping':
                self.send('SmartTrash')
            elif params[1] == 'name':
                print('fullurl:'+apiURL+params[2])
                req = urllib.request.Request(apiURL+params[2])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.35 Safari/537.36')
                r = urllib.request.urlopen(req)
                self.send(r.read().decode('utf-8'))
            # 其他指令：无效
            else:
                self.wfile.write('无效指令'.encode('utf-8'))
        except IndexError:
            self.wfile.write('http地址参数错误:IndexError'.encode('utf-8'))
        except:
            self.wfile.write('指令或参数存在未知错误'.encode('utf-8'))
            # self.wfile.write(sys.exc_info()[0])
            raise


# Handler = Server
# httpd = socketserver.TCPServer(("", PORT), Handler)
# httpd.serve_forever()

def startServer():
    Handler = Server
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()


def start():
    serverThread = threading.Thread(target=startServer)
    serverThread.start()
