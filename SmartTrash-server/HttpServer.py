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
        parseResult=urllib.parse.urlparse(self.path)
        params=parseResult.path.split('/')
        querys=urllib.parse.parse_qs(parseResult.query)
        # 捕获所有错误，防止程序崩溃
        try:
            if params[1] == 'ping':
                self.send('SmartTrash')
            elif params[1] == 'name':
                print('fullurl:'+apiURL+params[2])
                req = urllib.request.Request(apiURL+params[2])
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.35 Safari/537.36')
                r = urllib.request.urlopen(req)
                self.send(r.read().decode('utf-8'))
            elif params[1]=='object_detection':
                querys['input'][0]
                pass
            # 其他指令：无效
            else:
                self.wfile.write('无效指令'.encode('utf-8'))
        except IndexError:
            self.wfile.write('http地址参数错误:IndexError'.encode('utf-8'))
        except:
            self.wfile.write('指令或参数存在未知错误'.encode('utf-8'))
            # self.wfile.write(sys.exc_info()[0])
            raise
    def do_POST(self):
        try:
            print('getpost')
            self.send_response(200)
            self.end_headers()
            length = int(self.headers['Content-Length'])
            image = Image.open(io.BytesIO(self.rfile.read(length)))
            image.save('/mnt/f/image.jpg')
            self.wfile.write('{{"class_name":"test"}}'.encode('utf-8'))
            print('saved')
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
