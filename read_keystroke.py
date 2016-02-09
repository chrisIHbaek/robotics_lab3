import time
import sys, tty, termios

def get_key():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	tty.setraw(sys.stdin.fileno())
	ch = sys.stdin.read(1)
	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return ch

def get_note():
	key = get_key()
	if (key == 'a'):
		return 1
	elif (key == 's'):
		return 2
	elif (key == 'd'):
		return 3
	elif (key == 'f'):
		return 4
	else:
		return 5

# open a file to write input
f = open('smoke_input.txt', 'w')

# Wait until the first keystroke
print 'note\ttimestamp'
note = get_note()
initial_time = time.time()
f.write(str(note) + '\n') # record the key
f.write('0\n') # record the initial timestamp (0)
print str(note) + '\t' + '0'

while True:
	note = get_note()
	timestamp = time.time() - initial_time
	if (note == 5):
		break
	f.write(str(note) + '\n') # record the key
	f.write(str(timestamp) + '\n') # record the initial timestamp (0)
	print str(note) + '\t' + str(timestamp)



# f = open('smoke_input.txt', 'w')

# while True:

