import mraa
import threading
import json
import httplib, urllib
import SocketServer
import datetime
import time
import simon
import HeartBeat as hb
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from perceptive_layer import play_note
from perceptive_layer import initialize_arms
from user_input import user_input
from user_input_record import user_input_record

host = '10.0.1.4'
port = 8001

serverIP='10.0.1.9:8000'

have_potentiomemter = False
record_user_performance = True
have_heartbeat_sensor = True
have_simon_game = True

class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print 'HTTP post received'
        leng = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(leng)
        print self.request_version, self.command
        print self.headers
        print body
        print "=========Above content are for debugging purpose======="

        self.send_response(200)
        reply ="POST request received"
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

        print "start parsing the content"
        body_content = str(body).split("||")
        print body_content

        if body_content[0]=='getBPM':
            print (mraa.getVersion())
            if have_potentiomemter:
                x = mraa.Aio(0)
                print "x.read() = ", x.read()
                BPMvalue = 50.0+(float(x.read())/1023.0)*150.0
                print "BPMvalue=", BPMvalue
                send_http_post(serverIP, "bpm="+str(int(BPMvalue)))
                print "bpm value sent"

        elif body_content[0] == "r":
            print "debugging::about to play the song"
            print body_content
            starttime = datetime.datetime.strptime(body_content[1], "%Y-%m-%d %H:%M:%S.%f") 

            bpm = float(body_content[2])
            spb = 60/bpm
            song = json.loads(body_content[3])

            currenttime = datetime.datetime.now()
            start_in_scs = (starttime - currenttime).total_seconds()
            time.sleep(start_in_scs)
            robot_play(song, spb)
            print "Thank you for listening"            

        elif body_content[0] == "u":
            starttime = datetime.datetime.strptime(body_content[1], "%Y-%m-%d %H:%M:%S.%f") 
            currenttime = datetime.datetime.now()
            start_in_scs = (starttime - currenttime).total_seconds()
            time.sleep(start_in_scs)
            user_play()

        elif body_content[0] == "h":
            starttime = datetime.datetime.strptime(body_content[1], "%Y-%m-%d %H:%M:%S.%f") 
            currenttime = datetime.datetime.now()
            start_in_scs = (starttime - currenttime).total_seconds()
            time.sleep(start_in_scs)
            if have_heartbeat_sensor:
                heartbeat_mode(20)

        elif body_content[0] == "s":
            if have_simon_game:
                starttime = datetime.datetime.strptime(body_content[1], "%Y-%m-%d %H:%M:%S.%f") 
                currenttime = datetime.datetime.now()
                start_in_scs = (starttime - currenttime).total_seconds()
                time.sleep(start_in_scs)
                simon_game()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def send_http_post(url, body):  
    conn = httplib.HTTPConnection(url)
    conn.request("POST", "", body)
    response = conn.getresponse()
    data = response.read()
    print "response from http post", data
    conn.close()
    return data

def robot_play(song, spb):
    initialize_arms()
    for note in song:
        play_note(False, note[0], note[1] * spb)
    initialize_arms()

def user_play():
    initialize_arms()
    if record_user_performance:
        user_data = user_input_record(20)
        #sent it back to server
        send_http_post(serverIP, "usr_data=" + json.dumps(user_data))
        print "User data sent suceessfully"
    else:
        user_input(20)
    initialize_arms()
    print "debugging:: user mode ends"

def heartbeat_mode(time_interval):
    initialize_arms()
    pulse = False
    initial_time = time.time()
    while True:
        timestamp = time.time() - initial_time                     
        if (timestamp >= time_interval):
                print "heartbeat mode terminated."
                break
        output = hb.heartBeat(pulse)
        pulse = output[1]
        if (output[0] == True):
            print "heartbeat"
            play_note(False, 3, 0.1)
        time.sleep(0.01)
    initialize_arms()
    print "debugging::heartbeat_mode ends"

def simon_game():
    initialize_arms()
    print "Connect servos"
    time.sleep(7)
    print "Ready"
    time.sleep(3)
    print "Go"

    red = mraa.Gpio(12)
    blue = mraa.Gpio(13)

    red.dir(mraa.DIR_OUT)
    blue.dir(mraa.DIR_OUT)

    result = simon.simon()

    if (result == False):
        red.write(1)
    else:   
        blue.write(1)

    time.sleep(4)
    red.write(0)
    blue.write(0)
    print "debugging:: simon game ends"

print "Start listening on %s:%s" % (host, port)
try:    
    server = ThreadedHTTPServer((host, port), MyHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
except KeyboardInterrupt:
    print 'key pressed'
    server.shutdown()