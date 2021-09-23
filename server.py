#  coding: utf-8 
import socketserver
from urllib import request

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        header = self.data.decode().split('\n')
        URL = (header[0].split()[1])
        request_type = header[0].split()[0]
        print(request_type + URL)

        if(URL == '/' or URL == '/index.html' or URL == '/index.html/'):
            self.request.sendall(bytes("HTTP/1.1 200 OK Herro Dear Client\n", "utf-8"))
            self.request.sendall(bytes('Content-Type: text/html\n\n', "utf-8"))
            self.request.sendall(open('www/index.html').read().encode())

        elif(URL == '/favicon.ico'):
            # self.request.sendall(open('www/favicon.ico').read().encode())
            return
        
        elif(request_type != 'GET'):
            self.request.sendall(bytes("HTTP/1.1 405 Method Not Allowed wai u do dis\n\n", "utf-8"))

        else:
            if(URL.endswith('.css') or URL.endswith('.html')):
                try:
                    data = open('www' + URL).read()
                    if(URL.endswith('.css')):
                        mime = 'Content-Type: text/css\n\n'
                        self.request.sendall(bytes("HTTP/1.1 200 OK\n", "utf-8"))
                        self.request.sendall(bytes(mime + data, "utf-8"))
                    elif(URL.endswith('.html')):
                        mime = 'Content-Type: text/html\n\n'
                        self.request.sendall(bytes("HTTP/1.1 200 OK\n", "utf-8"))
                        self.request.sendall(bytes(mime + data, "utf-8"))
                    else:
                        self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))    
                except FileNotFoundError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except IsADirectoryError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except NotADirectoryError:
                    print('Cannot find Directory: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
            elif(URL.endswith('/')):
                try:
                    data = open('www' + URL + 'index.html').read()
                    mime = 'Content-Type: text/html\n\n'
                    self.request.sendall(bytes("HTTP/1.1 200 OK\n", "utf-8"))
                    self.request.sendall(bytes(mime + data, "utf-8"))
                except FileNotFoundError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except IsADirectoryError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except NotADirectoryError:
                    print('Cannot find Directory: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
            else:
                try:
                    data = open('www' + URL + '/index.html').read()
                    self.request.sendall(bytes("HTTP/1.1 301 MOVED\n", "utf-8"))
                    mime = 'Content-Type: text/html\n\n'
                    self.request.sendall(bytes("HTTP/1.1 200 OK\n", "utf-8"))
                    self.request.sendall(bytes(mime + data, "utf-8"))
                except FileNotFoundError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except IsADirectoryError:
                    print('Cannot find File: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))
                except NotADirectoryError:
                    print('Cannot find Directory: ' + URL)
                    self.request.sendall(bytes('HTTP/1.1 404 FILE NOT FOUND\n', "utf-8"))

            


if __name__ == "__main__":
    print('hello world')
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
