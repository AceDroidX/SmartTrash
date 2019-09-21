#!/usr/bin/python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
from time import sleep
import threading
import sys
import urllib.request
import urllib.parse
from PIL import Image
import io
import uuid
import json

sys.path.append('../SmartTrash-client')
from image import token,image_to_base64,image_classify

threadLock = threading.Lock()

# 服务器监视端口号
PORT = 23333
api_get = [
    "https://laji.lr3800.com/api.php?name=",
    'http://api.choviwu.top/garbage/getGarbage?garbageName=',
    'https://www.lajiflw.cn/rubbish/search?q='
]
api_post = [
    
]
apinum = 3
imgdic={}
imglist=[]

class Server(http.server.SimpleHTTPRequestHandler):
    sendstr=""
    def send(self, string):
        self.sendstr=string

    def do_GET(self):
        # 从地址中分割出若干参数
        parseResult=urllib.parse.urlparse(self.path)
        params=parseResult.path.split('/')
        querys=urllib.parse.parse_qs(parseResult.query)
        # 捕获所有错误，防止程序崩溃
        try:
            if params[1] == 'ping':
                self.send('SmartTrash')
            elif params[1] == 'name':
                if apinum<len(api_get):
                    url=api_get[apinum]+params[2]
                else:
                    print('err:apinum')
                print('fullurl:'+url)
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.35 Safari/537.36')
                r = urllib.request.urlopen(req)
                self.send(r.read().decode('utf-8'))
            elif params[1]=='object_detection':
                img=imgdic[querys['input'][0]]
                origin=image_classify(img)
                result={}
                result['img']=querys['input'][0]
                result['data']=json.loads(json.dumps(origin).replace('"keyword":','"class_name":'))['result']
                self.send(json.dumps(result))
                pass
            # 其他指令：无效
            else:
                self.wfile.write('无效指令'.encode('utf-8'))
            self.protocol_version='HTTP/1.1'
            self.send_response(200)
            self.send_header('Content-Length',len(self.sendstr.encode('utf-8')))
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header("Connection","keep-alive")
            self.end_headers()
            self.wfile.write(self.sendstr.encode('utf-8'))
        except IndexError:
            self.protocol_version='HTTP/1.1'
            self.send_response(200)
            self.wfile.write('http地址参数错误:IndexError'.encode('utf-8'))
        except:
            self.protocol_version='HTTP/1.1'
            self.send_response(200)
            self.wfile.write('指令或参数存在未知错误'.encode('utf-8'))
            # self.wfile.write(sys.exc_info()[0])
            raise
    def do_POST(self):
        try:
            global imgdic
            global imglist
            print('getpost')
            length = int(self.headers['Content-Length'])
            img = Image.open(io.BytesIO(self.rfile.read(length)))
            #img.save('/mnt/f/image.jpg')
            threadLock.acquire()
            imgid=str(uuid.uuid4())
            if len(imglist)>=10:
                imgdic.pop(imglist.pop(0))
            imglist.append(imgid)
            imgdic[imgid]=img
            print(imgid)
            threadLock.release()
            self.protocol_version='HTTP/1.1'
            self.send_response(200)
            self.send_header('Content-Length',len(imgid.encode('utf-8')))
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header("Connection","keep-alive")
            self.end_headers()
            self.wfile.write(imgid.encode('utf-8'))
            #print('saved')
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
