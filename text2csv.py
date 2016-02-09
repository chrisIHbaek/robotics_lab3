import os
import numpy as np

note_input = np.array([])

if (os.path.exists('./input.csv')):
	matrix = np.loadtxt('input.csv', delimiter=',')
else:
	matrix = []

f = open("smoke_input.txt", "r")

for line in f:
	note_input = np.append(note_input, float(line))

#note_input.reshape
if (os.path.exists('./input.csv')):
	matrix = np.c_[matrix, note_input]
else:
	matrix = note_input

print matrix

np.savetxt('input.csv', matrix, delimiter=',')
