import http.server
import socketserver
import time
import threading
import json
from eyeware.client import TrackerClient

PORT = 8000
set_num = 10
class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()
        
    def stopped(self):
        return self._stop_event.is_set()
    
    def join(self, *args, **kwargs):
        self.stop()
        super(MyThread, self).join(*args, **kwargs)
        print('thread stopped')
    
    def run_mock(self): #for debugging purposes
        global set_num
        filename = f'out{set_num}.txt'
        while not self._stop_event.is_set():
                ts = time.time()
                time.sleep(1 / 60)
            
    def run(self):
        global set_num
        filename = f'out{set_num}.txt'
        output = open(filename, 'a')
        while not self._stop_event.is_set():
                if tracker.connected:
                    ts = time.time()
                    output.write(str(ts))
                    screen_gaze = tracker.get_screen_gaze_info()
                    screen_gaze_is_lost = screen_gaze.is_lost
                    if not screen_gaze_is_lost:
                        output.write(f' Coordinates x={screen_gaze.x} px, y={screen_gaze.y} px\n')
                else:
                    MESSAGE_PERIOD_IN_SECONDS = 2
                    time.sleep(MESSAGE_PERIOD_IN_SECONDS - time.monotonic() % MESSAGE_PERIOD_IN_SECONDS)
                    print("No connection with tracker server")
                time.sleep(1 / 90)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    timestamps = []
    problematic_words = []

    def do_GET(self):
        global set_num
        sett = f'data/set{set_num}.json'
        if self.path == '/data.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = open(sett, 'r', encoding='utf-8')
            response = json.load(data)
            resp_json = json.dumps(response)
            self.wfile.write(resp_json.encode())
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        global set_num
        if self.path == '/start':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            with open('out.txt', 'w') as output:
                output.write(post_data.decode('utf-8'))
                thread_tracker.start()
        elif self.path == '/click':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = body.decode('utf-8')
            clicked_word = json.loads(data)
            print(clicked_word)
            clicked_words = open(f'clicked_words{set_num}.txt', 'a', encoding='utf-8')
            for item in clicked_word[0]:
                clicked_words.write(str(item))
                clicked_words.write(' ')
            clicked_words.write('\n')
        elif self.path == '/next':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = body.decode('utf-8')
            words = json.loads(data)
            self.problematic_words.append(words)
            ts = time.time()
            self.timestamps.append(f'Start trial {ts}')
        elif self.path == '/choice1':
            ts = time.time()
            self.timestamps.append(f'End trial {ts}')
            self.timestamps.append('Chosen option is 1')
        elif self.path == '/choice2':
            ts = time.time()
            self.timestamps.append(f'End trial {ts}')
            self.timestamps.append('Chosen option is 2')
        elif self.path == '/end':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            thread_tracker.stop()
            thread_tracker.join()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = body.decode('utf-8')
            words = json.loads(data)
            self.problematic_words.append(words)
            print('End clicked!')
            timestamps = open(f'timestamps{set_num}.txt', 'w')
            for item in self.timestamps:
                timestamps.write(item)
                timestamps.write('\n')
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

# Create the web server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    tracker = TrackerClient()
    thread_tracker = MyThread()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
