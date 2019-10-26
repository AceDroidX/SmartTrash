#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
from time import sleep
import threading
import urllib.request
import urllib.parse
from PIL import Image
import sys,io,uuid,json,time,string
import api,main

sys.path.append('../SmartTrash-client')
from image import token, image_to_base64, image_classify

threadLock = threading.Lock()

# 服务器监视端口号
PORT = 23333
imgdic = {}
imglist = []

class Server(http.server.SimpleHTTPRequestHandler):
    sendstr = ""

    def send(self, string):
        global threadLock
        self.sendstr = string
        threadLock.acquire()
        with open('log.txt', 'a',encoding='utf-8') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()
                    )+"---"+self.address_string()+"--->[send]"+string+"\n")
        threadLock.release()
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header('Content-Length',
                             len(self.sendstr.encode('utf-8')))
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        self.wfile.write(self.sendstr.encode('utf-8'))
        return

    def do_GET(self):
        global threadLock
        # 从地址中分割出若干参数
        parseResult = urllib.parse.urlparse(self.path)
        params = parseResult.path.split('/')
        querys = urllib.parse.parse_qs(parseResult.query)
        threadLock.acquire()
        with open('log.txt', 'a',encoding='utf-8') as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()
                    )+"---"+self.address_string()+"--->[get]"+self.path+"\n")
        threadLock.release()
        # 捕获所有错误，防止程序崩溃
        try:
            if params[1] == 'ping':
                self.send('SmartTrash')
            elif params[1] == 'name':
                result = api.getType(params[2])
                self.send(result)
            elif params[1] == 'namem1':
                result = api.getType(params[2],1)
                self.send(result)
            elif params[1] == 'db-update':
                if main.usedb==False:
                    self.send('err:服务器关闭了数据添加功能')
            elif params[1] == 'object_detection':
                img = imgdic[querys['input'][0]]
                origin = image_classify(img)
                threadLock.acquire()
                with open('response-ic.json', 'w',encoding='utf-8') as f:
                    f.write(json.dumps(origin,ensure_ascii=False))
                    f.write("\n")
                threadLock.release()
                if str(origin).find('err')!=-1:
                    self.send('图像识别错误，请重新拍摄')
                # 老版本
                result = {}
                result['img'] = querys['input'][0]
                result['data'] = json.loads(json.dumps(origin,ensure_ascii=False).replace(
                    '"keyword":', '"class_name":'))['result']
                if True:  #将第一个物体名替换成mode1结果
                    result['data'][0]['class_name'] = api.getType(result['data'][0]['class_name'],1)
                # if True:  # 将所有物体名直接转换成名字+类型
                #     for index in range(len(result['data'])):
                #         result['data'][index]['class_name'] = result['data'][index]['class_name']+" "+api.getType(
                #             result['data'][index]['class_name'])
                threadLock.acquire()
                with open('response.json', 'w',encoding='utf-8') as f:
                    f.write(json.dumps(result,ensure_ascii=False))
                    f.write("\n")
                threadLock.release()
                self.send(json.dumps(result,ensure_ascii=False))
                # 新版本
                # trashname = origin['result'][0]['keyword']
                # trashroot = origin['result'][0]['root']
                # trashtype = api.getType(trashname,1)
                # self.send(trashtype)
            # 其他指令：无效
            else:
                self.send('无效指令'.encode('utf-8'))
        except IndexError:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.wfile.write('http地址参数错误:IndexError'.encode('utf-8'))
        except:
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.wfile.write('指令或参数存在未知错误'.encode('utf-8'))
            # self.wfile.write(sys.exc_info()[0])
            raise

    def do_POST(self):
        global threadLock
        try:
            global imgdic
            global imglist
            print('getpost')
            length = int(self.headers['Content-Length'])
            img = Image.open(io.BytesIO(self.rfile.read(length)))
            # img.save('/mnt/f/image.jpg')
            threadLock.acquire()
            imgid = str(uuid.uuid4())
            if len(imglist) >= 10:
                imgdic.pop(imglist.pop(0))
            imglist.append(imgid)
            imgdic[imgid] = img
            with open('log.txt', 'a',encoding='utf-8') as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()
                                      )+"---"+self.address_string()+"--->[imgid]"+imgid+"\n")
            print(imgid)
            threadLock.release()
            self.protocol_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header('Content-Length', len(imgid.encode('utf-8')))
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header("Connection", "keep-alive")
            self.end_headers()
            self.wfile.write(imgid.encode('utf-8'))
            # print('saved')
        except:
            self.wfile.write('指令或参数存在未知错误'.encode('utf-8'))
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
