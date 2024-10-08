from http.server import SimpleHTTPRequestHandler, HTTPServer
import socket
import os

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/message':
            self.path = '/message.html'
        elif self.path.startswith('/static/'):
            self.path = self.path
        else:
            self.path = '/error.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/submit-message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = self.parse_post_data(post_data)
            self.send_to_socket(data)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Message received and sent to socket server.')
        else:
            self.send_error(404)

    def send_to_socket(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5000))
        sock.sendall(data.encode('utf-8'))
        sock.close()

    def parse_post_data(self, post_data):
        data = {}
        for pair in post_data.split('&'):
            key, value = pair.split('=')
            data[key] = value
        return str(data)

def run(server_class=HTTPServer, handler_class=MyHandler, port=3000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
