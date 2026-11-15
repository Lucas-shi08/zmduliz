import http.server
import mimetypes
import os
import socketserver

mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('font/woff2', '.woff2')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8788


class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass


socketserver.TCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), H) as httpd:
    print('serving on', PORT, flush=True)
    httpd.serve_forever()
