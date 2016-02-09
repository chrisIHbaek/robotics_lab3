# neurolab wine classification example

import numpy as np
import neurolab as nl
import pylab as plt

#np.seterr(divide='ignore', invalid='ignore')

def vec2ind(vector):
	index = 0
	if (np.array_equal(vector,[1, 0, 0])):
		index = 1
	elif (np.array_equal(vector,[0, 1, 0])):
		index = 2
	elif (np.array_equal(vector,[0, 0, 1])):
		index = 3
	return index

#Random seed generator
np.random.seed(212345)

#load data into matrices

x = np.loadtxt(open("input.csv", "rb"), delimiter=",")
t = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0], 
			 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1], 
			 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# t = t.reshape(1, len(t))

# Get max and min for each attribute
min_max = [i for i in range(len(x))]

for i in range(len(x)):
	min_max[i] = [x[i][np.argmin(x[i])]-1.2, x[i][np.argmax(x[i])]+1.2,]

#print min_max
# Get the size of each layer (hidden layer and output layer)
hidden_layer_size = 10 # number of neurons in hidden layer. It is defined by user.
output_layer_size = 3 # number of neurons in output layer. It is the number of targets.
size = [hidden_layer_size, output_layer_size]

x = x.transpose() # the function expects the transpose of the matrix
t = t.transpose()

# Normalize the target (it needs to be in range of [-1,1])
normf = nl.tool.Norm(t)
norm_t = normf(t)

# Create network with 2 layers and random initialized
net = nl.net.newff(min_max,size,[nl.trans.TanSig(), nl.trans.SoftMax()])
#net.trainf = nl.train.train_ncg # Conjugate gradient algorithm

# Train network
error = net.train(x, norm_t, epochs=500, show=10, goal=0.02)

print error
#plt.subplot(111)
plt.plot(error)
plt.xlabel('Epoch number')
plt.ylabel('error (default SSE)')

inp = np.loadtxt(open("smoke_input.txt", "rb"), delimiter=",")
inp = np.c_[inp, inp]
inp = inp.transpose()
#inp = inp.reshape(1, len(inp[0]))

print inp
# Simulate network
output = net.sim(inp)

# Denormalize the output
norm_output = normf.renorm(output)

# Round
for i in range(len(norm_output)):
	for j in range(len(norm_output[i])):
		norm_output[i][j] = round(norm_output[i][j], 0)

print norm_output

target_index = [i for i in range(len(t))]
output_index = [i for i in range(len(norm_output))]

for i in range(len(t)):
	target_index[i] = vec2ind(t[i])

for i in range(len(norm_output)):
	output_index[i] = vec2ind(norm_output[i])

#print target_index
print output_index




# for i in range(len(norm_output)):
# 	for j in range(len(norm_output[i])):
# 		norm_output[i][j] = round(norm_output[i][j], 0)

# print norm_outputimport
