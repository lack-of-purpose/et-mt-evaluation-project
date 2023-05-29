import http.server
import socketserver
import time
import threading
import json
from eyeware.client import TrackerClient

PORT = 8000
# Define the handler for the web server
def mock_track():
    while 1:
        with open('out.txt', 'a') as output:
            ts = time.time()
            output.write(str(ts))
            output.write(" Coordinates x y\n")
        time.sleep(1 / 60)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    timestamps = []
    problematic_words = []

    def do_GET(self):
        if self.path == '/data.json':
            self.send_response(200)
            # Set the response headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = open('data/set7.json', 'r', encoding='utf-8')
            response = json.load(data)
            resp_json = json.dumps(response)
            # Send the response data as JSON string
            self.wfile.write(resp_json.encode())
        else:
            #self.send_response(200)
            #self.send_header("Content-type", "text/html; charset=utf-8")
            #self.end_headers()
            #super().do_GET()
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/start':
            # handle '/start' request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # write data to file
            with open('out.txt', 'w') as output:
                output.write(post_data.decode('utf-8'))
                #threading.Thread(target=self.mock_track).start()
                thread_track.start()
            # send response
        elif self.path == '/next':
            # handle '/next' request
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = body.decode('utf-8')
            words = json.loads(data)
            self.problematic_words.append(words)
            print('Next clicked!')
            # add additional data to file
            ts = time.time()
            self.timestamps.append(f'Start trial {ts}')
        elif self.path == '/choice1':
            print('choice1 clicked!')
            ts = time.time()
            self.timestamps.append(f'End trial {ts}')
            self.timestamps.append('Chosen option is 1')
        elif self.path == '/choice2':
            print('choice2 clicked!')
            ts = time.time()
            self.timestamps.append(f'End trial {ts}')
            self.timestamps.append('Chosen option is 2')
        elif self.path == '/end':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = body.decode('utf-8')
            words = json.loads(data)
            self.problematic_words.append(words)
            print('End clicked!')
            timestamps = open('timestamps.txt', 'w')
            for item in self.timestamps:
                timestamps.write(item)
                timestamps.write('\n')
            clicked_words = open('clicked_words.txt', 'w', encoding='utf-8')
            trial_num = 1
            for item in self.problematic_words:
                clicked_words.write(str(trial_num))
                clicked_words.write('\n')
                for word in item:
                    clicked_words.write(word)
                    clicked_words.write(' ')
                clicked_words.write('\n')
                trial_num += 1
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
    def mock_track(self):
        while 1:
            with open('out.txt', 'a') as output:
                ts = time.time()
                output.write(str(ts))
                output.write(" Coordinates x y\n")
            time.sleep(1 / 60)

    def track(self):
        while 1:
            with open('out.txt', 'a') as output:
                if tracker.connected:
                    ts = time.time()
                    output.write(str(ts))
                    screen_gaze = tracker.get_screen_gaze_info()
                    screen_gaze_is_lost = screen_gaze.is_lost
                    if not screen_gaze_is_lost:
                        output.write(f' Coordinates x={screen_gaze.x}, y={screen_gaze.y}\n')
                    time.sleep(1 / 60)
                else:
                    MESSAGE_PERIOD_IN_SECONDS = 2
                    time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
                    print("No connection with tracker server")

# Create the web server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    tracker = TrackerClient()
    thread_track = threading.Thread(target=mock_track)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        #pass
        #httpd.server_close()
        thread_track.join()
        httpd.shutdown()
    # Serve the web pages indefinitely
    #httpd.serve_forever()
