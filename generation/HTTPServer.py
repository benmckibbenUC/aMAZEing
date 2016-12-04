# Ben McKibben
# CMSC 22010
# aMAZEing

import time
import json
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from random import randrange
from urlparse import urlparse, parse_qs
from mazeGeneration import Maze
from stlGeneration import stlMazeWriter

HOST_NAME = ''
PORT_NUMBER = 9000

class MyHandler(BaseHTTPRequestHandler):

    def send404(s):
        s.send_response(404)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>404 | aMAZEing Maze Generator</title></head>")
        s.wfile.write("<p>Sorry, page not found.</p>")
        s.wfile.write("</body></html>")

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()    

    def do_GET(s):
        """Respond to a GET request."""
        if s.path.startswith('/generate'):
            query = parse_qs(urlparse(s.path).query)
            if 'd' in query and 'w' in query:
                try:
                    d = query['d'][0]
                    w = query['w'][0]
                    newMaze = Maze(int(d), int(w))
                    newMaze.generate()
                    newMaze.validate()
                    s.wfile.write(newMaze.serialize())
                    print time.asctime(), 'Received GET /generate, returned ' + 'x'.join([d,w]) + ' maze.'
                except Exception as e:
                    error_msg = str(e)+'\n'
                    error_msg += 'Recieved parameters:\n'
                    error_msg += str(query)
                    s.wfile.write(error_msg)
                    print time.asctime(), 'Received GET /generate. Exception raised:\n' + error_msg
                return   
            else:
                s.wfile.write('Missing d and w query parameters.')
                print time.asctime(), 'Received GET /generate, d and w query parameters missing.'
                return
        s.send404()

    def do_POST(s):
        """Respond to a POST request."""
        # respond to POST request with "maze" and possible "marble" as form parameters
        if s.path.startswith('/stl'):
            raw_data = s.rfile.read(int(s.headers['Content-Length']))
            post_data = json.loads(raw_data)
            try:
                maze_serialized = post_data['maze']
            except KeyError:
                print time.asctime(), 'Received POST /stl, no maze recieved. Raw data:\n' + raw_data
                s.wfile.write('No maze recieved.')
                return
            try:
                marble_width = post_data['marble']
            except KeyError:
                marble_width = 10
            try:
                maze = Maze.deserialize(maze_serialized)
                writer = stlMazeWriter(maze, marble_width)
                filename = str(randrange(0,10000)) # get random filename
                print time.asctime(), 'Received POST /stl, generating maze ' + filename + '...'
                path = writer.writeSTL(filename)
                with open(path, 'rb') as stlFile:
                    s.wfile.write(stlFile.read())
                print time.asctime(), 'Returned maze ' + filename
                return
            except Exception as e:
                error_msg = str(e)+'\n'
                error_msg += 'Recieved parameters:\n'
                error_msg += maze_serialized + '\n'
                error_msg += 'Marble width (defaults to 10): ' + str(marble_width)
                s.wfile.write(error_msg)
                print time.asctime(), 'Received POST /stl. Exception raised:\n' + error_msg
            return
        s.send404()

# thanks https://pymotw.com/2/BaseHTTPServer/index.html#module-BaseHTTPServer
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server_class = ThreadedHTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)