#  coding: utf-8 
import socketserver, os
from urllib import request
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime



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
        #print(request_type + URL)
        now = datetime.now()
        stamp = mktime(now.timetuple())

        http_200 = 'HTTP/1.1 200 OK\r\n'
        http_404 = 'HTTP/1.1 404 FILE NOT FOUND\r\n'
        http_301 = 'HTTP/1.1 301 MOVED\r\n'
        http_405 = 'HTTP/1.1 405 METHOD NOT ALLOWED\r\n'
        css_mime = 'Content-Type: text/css\n\n'
        html_mime = 'Content-Type: text/html\n\n'
        date_header = 'Date: ' + format_date_time(stamp) + '\r\n'
        close_header = 'Connection: close\r\n'

        if(URL == '/' or URL == '/index.html' or URL == '/index.html/'):
            data = open('www/index.html').read()
            size_header = 'Content-Length: ' + str(os.path.getsize('www/index.html')) + '\r\n'
            self.request.sendall(bytes(http_200 + date_header + size_header + close_header + html_mime  + '\r\n' + data, "utf-8"))

        elif(URL == '/favicon.ico'):
            # I wanted favicons and I failed :( Cannot figure out how to encode
            # self.request.sendall(open('www/favicon.ico').read().encode())
            return
        
        elif(request_type != 'GET'):
            self.request.sendall(bytes(http_405 + '\r\n', "utf-8"))

        else:
            try:
                if(URL.endswith('.css') or URL.endswith('.html')):
                    data = open('www' + URL).read()
                    size_header = 'Content-Length: ' + str(os.path.getsize('www' + URL)) + '\r\n'
                    if(URL.endswith('.css')):
                        self.request.sendall(bytes(http_200 + date_header + size_header + close_header + css_mime + '\r\n' + data, "utf-8"))
                    elif(URL.endswith('.html')):
                        self.request.sendall(bytes(http_200 + date_header + size_header + close_header + html_mime + '\r\n' + data, "utf-8"))
                    else:
                        self.request.sendall(bytes(http_404, "utf-8"))    
                elif(URL.endswith('/')):
                    data = open('www' + URL + 'index.html').read()
                    size_header = 'Content-Length: ' + str(os.path.getsize('www' + URL)) + '\r\n'
                    self.request.sendall(bytes(http_200 + date_header + size_header + close_header + html_mime + '\r\n' + data, "utf-8"))
                else:
                    data = open('www' + URL + '/index.html').read()
                    size_header = 'Content-Length: ' + str(os.path.getsize('www' + URL)) + '\r\n'
                    self.request.sendall(bytes(http_301 + http_200 + date_header + size_header + close_header + html_mime + '\r\n' + data, "utf-8"))
            except FileNotFoundError:
                print('Not Found: ' + URL)
                self.request.sendall(bytes(http_404, "utf-8"))
            except IsADirectoryError:
                print('Not Found: ' + URL)
                self.request.sendall(bytes(http_404, "utf-8"))
            except NotADirectoryError:
                print('Not Found: ' + URL)
                self.request.sendall(bytes(http_404, "utf-8"))

if __name__ == "__main__":
    print('hello world')
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

# Sources Consulted:
# For formatting Date/Time:
# https://stackoverflow.com/questions/225086/rfc-1123-date-representation-in-python