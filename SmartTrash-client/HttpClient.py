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

def startClient():
    pass    

def start():
    serverThread = threading.Thread(target=startClient)
    serverThread.start()
