from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading	
import SocketServer
import httplib, urllib
import json
import datetime

host = '10.0.1.9'
web_port = 8000
music_port = 8001

edison1_ip = "10.0.1.9"

edison2_ip = "10.0.1.4"

bpm = 100
song_idx = 1

user_performance = []

class MyHandler(SimpleHTTPRequestHandler):   

    def do_POST(self):
        print 'HTTP post received'
        leng = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(leng)
        print self.request_version, self.command
        print self.headers
        print body
        print "=========Above content are for debugging purpose======="


        reply ="POST request received"

        body_content = str(body).split("=")
        print "\nbody_content =", body_content
        if(body_content[0] == "bpm"): #set bpm           
            if(body_content[1] != ""):
                global bpm
                bpm = int(body_content[1])
                print "debug::bpm set successfully"
                print "debug::new bpm =", bpm

        if(body_content[0] == "options"): #set song
            global song_idx
            song_idx = int(body_content[1])
            print song_idx

        if(body_content[0] == "read_bpm"): #browser read bpm
            reply = str(bpm)

        if(body_content[0] == "comparison"): #browser read bpm
            bpm = 153.0
            spb = float(60/bpm)
            robot_song = read_song('marry_had_a_little_lamb.txt')
            for note in robot_song:
                note[1] = float(note[1] * spb)
            user_song = read_user_song('marry_user.txt')
            print "user_song=", user_song

            robot_song_new = perfect2single(robot_song)
            print "robot_song_new=", robot_song_new
            print len(robot_song_new)
            user_song_new = manual2single(user_song)
            print "user_song_new=", user_song_new
            print len(user_song_new)
            reply = [robot_song_new, user_song_new]


        #reply back
        self.send_response(200)
        self.send_header("Content-Length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

        if(body_content[0] == "usr_data"):
            global user_performance
            user_performance = json.loads(body_content[1])
            song2file(user_performance, "marry_user.txt")

        if(body_content[0] == "get_bpm"): #read bpm from potentiometer 
            send_http_post(edison1_ip+":"+str(music_port), "getBPM")


        if(body_content[0] == "btn"): #play based on modes
            if(body_content[1] == "robot_play"):
                robot_play()
            elif(body_content[1] == "user_play"):
                user_play()
            elif(body_content[1] == "heart_play"):
                heart_play()
            elif(body_content[1] == "simon"):
                simon_game()

        print "http post request handled successfully"


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def send_http_post(url, body):  
    print "http post to ", url
    conn = httplib.HTTPConnection(url)
    conn.request("POST", "", body)
    response = conn.getresponse()
    data = response.read()
    print "response from http post", data
    conn.close()
    return data

def song2file(songArray,fileName):
    f = open(fileName, 'w')
    for e in songArray:
        line = str(e[0]) + ' ' + str(e[1])+'\n'
        f.write(line)
    f.close()


def perfect2single(noteInfo):
    out=[]
    for e in noteInfo:
        note=e[0]
        time=e[1]
        for i in range(0,int(time*10)):
            out+=[note]
    return out  

def manual2single(noteInfo):
    out=[]
    prevSt=0
    for e in noteInfo:
        note=e[0]
        time=e[1]-prevSt
        prevSt=e[1]
        for i in range(0,int(time*10)):
            out+=[note]
    return out  


def read_song():
    print "reading the song"
    if (song_idx == 1):
        file_name = 'smoke_on_the_water.txt'
    if (song_idx == 2):
        file_name = 'marry_had_a_little_lamb.txt'
    if (song_idx == 3):
        file_name = 'HotCrossBuns.txt'
    if (song_idx == 4):
        file_name = 'iron_man.txt' 

    print "file_name=", file_name

    f = open(file_name, 'r')

    song = []

    for line in f:
        note_info = line.split(" ")
        note_info[0] = int(note_info[0])
        note_info[1] = 4 / float(note_info[1])
        song.append(note_info)

    return song

def edison1_should_play(note):
    return True if note < 3 else False;

def robot_play():
    print "About to play the song"
    song = read_song()
    edison1_song = [x if edison1_should_play(x[0]) else [0, x[1]] for x in song ]
    edison2_song = [x if not edison1_should_play(x[0]) else [0, x[1]] for x in song ]

    print "debugging:: edison1_song = ", edison1_song
    print "debugging:: edison2_song = ", edison2_song

    currenttime = datetime.datetime.now()
    starttime = str(currenttime + datetime.timedelta(seconds=4))
    pre_content = "r" + "||" + starttime + "||" + str(bpm)+"||"
    # print "Sending info to Edison 1"
    send_http_post(edison1_ip+":"+str(music_port), pre_content +json.dumps(edison1_song))

    # print "Sending info to Edison 2"
    send_http_post(edison2_ip+":"+str(music_port), pre_content +json.dumps(edison2_song))
    print "Info sent, wait for edison to play"
    

def user_play():
    print "enter manual mode"
    currenttime = datetime.datetime.now()
    starttime = str(currenttime + datetime.timedelta(seconds=4))
    pre_content = "u" + "||" + starttime
    # print "Sending info to Edison 1"
    send_http_post(edison1_ip+":"+str(music_port), pre_content)

    # print "Sending info to Edison 2"
    send_http_post(edison2_ip+":"+str(music_port), pre_content)

def heart_play():
    print "heartbeat mode"
    currenttime = datetime.datetime.now()
    starttime = str(currenttime + datetime.timedelta(seconds=4))
    pre_content = "h" + "||" + starttime
    print "message to sent = ", pre_content
    # print "Sending info to Edison 1"
    # send_http_post(edison1_ip+":"+str(music_port), pre_content)

    print "Sending info to Edison 2"
    send_http_post(edison2_ip+":"+str(music_port), pre_content )

def simon_game():
    currenttime = datetime.datetime.now()
    starttime = str(currenttime + datetime.timedelta(seconds=4))
    pre_content = "simon" + "||" + starttime
    print "message to sent = ", pre_content
    # print "Sending info to Edison 1"
    # send_http_post(edison1_ip+":"+str(music_port), pre_content)

    print "Sending info to Edison 2"
    send_http_post(edison2_ip+":"+str(music_port), pre_content )

print "Starting server at address %s:%s" % (host, web_port)
try:
    SocketServer.TCPServer.allow_reuse_address = True
    server = ThreadedHTTPServer((host, web_port), MyHandler)
    server.serve_forever()    
except KeyboardInterrupt:
    print 'key pressed'
    server.shutdown()