from tqdm import tqdm
import numpy as np
import math
import scipy.special

# neural network class definition
class NeuralNetwork(object):

	# initialise the neural network
	def __init__(self, dimensions, learningRate):
		# try:
		# 	self.layers = np.load("./nn-data/nn-weights.npy")
		# 	print("The network weights have been loaded from disk...")
		# except:
		# 	print("The network weights couldn't be loaded from disk...")
		# 	# # this array will contain all the layers of the neural network
		# 	self.layers = []
		# 	# we construct the hidden layers
		# 	for i in range(1, len(dimensions)):
		# 		hiddenLayer = []
		# 		# number of weight arrays will be determined by the number of neurons
		# 		# in the current layer
		# 		for j in range(dimensions[i]):
		# 			# number of weights per neuron is equal to the number of nodes
		# 			# in the previous layer
		# 			# very important for the weights to be assigned with random values from -1 to +1
		# 			# as our algorithm adds up the change in weight
		# 			hiddenLayer.append(np.random.uniform(-1, 1, dimensions[i - 1]))
        #
		# 		# make the hiddenLayer into a np array
		# 		hiddenLayer = np.array(hiddenLayer)
        #
		# 		self.layers.append(hiddenLayer)

		# # this array will contain all the layers of the neural network
		self.layers = []
		# we construct the hidden layers
		for i in range(1, len(dimensions)):
			hiddenLayer = []
			# number of weight arrays will be determined by the number of neurons
			# in the current layer
			for j in range(dimensions[i]):
				# number of weights per neuron is equal to the number of nodes
				# in the previous layer
				# very important for the weights to be assigned with random values from -1 to +1
				# as our algorithm adds up the change in weight
				hiddenLayer.append(np.random.uniform(-1, 1, dimensions[i - 1]))

			# make the hiddenLayer into a np array
			hiddenLayer = np.array(hiddenLayer)

			self.layers.append(hiddenLayer)

		# learning rate
		self.learningRate = learningRate
		# activation function
		self.f = lambda x: scipy.special.expit(x)
		# differentiated activation function
		self.fPrime = lambda x: x * (1 - x)

	def backPropagation(self, inputs, targets):
		# conversion of inputs and target arrays to transposed np matrixes
		inputs = np.transpose(np.array([np.array(inputs)]))
		targets = np.transpose(np.array([np.array(targets)]))

		# np array of outputs in each layer retrieved
		outputs = self.feedForward(inputs)

		# the error of each neuron in the output layer
		outputsError = targets - outputs[len(outputs) - 1]

		# the array of  errors of each neuron in each layer
		hiddenErrors = [None] * (len(outputs) - 1)

		# we loop backwards excluding the last layer as the hiddenlayer has a size of number of weight layers - 1
		for i in reversed(range(len(outputs) - 1)):
			hiddenError = 0
			if i == len(outputs) - 2:
				hiddenError = np.dot(np.transpose(self.layers[i + 1]), outputsError)
			else:
				hiddenError = np.dot(np.transpose(self.layers[i + 1]), hiddenErrors[i + 1])

			hiddenErrors[i] = hiddenError

		# update the weights using weight decay
		for i in reversed(range(len(self.layers))):
			if i == len(self.layers) - 1:
				self.layers[i] += (self.learningRate * np.dot((outputsError * self.fPrime(outputs[i])), np.transpose(outputs[i - 1])))
			elif i == 0:
				self.layers[i] += (self.learningRate * np.dot((hiddenErrors[i] * self.fPrime(outputs[i])), np.transpose(inputs)))
			else:
				self.layers[i] += (self.learningRate * np.dot((hiddenErrors[i] * self.fPrime(outputs[i])), np.transpose(outputs[i - 1])))

	def train(self, inputs, targets):
		self.backPropagation(inputs, targets)

	def fit(self, training_data, num_batches, num_epochs):

		data_per_batch = int(len(training_data) / num_batches)

		batches = []

		for i in range(len(training_data)):
			# if i is a multiple of data per batch we have reached the number of element
			# that one batch can hold
			if i % data_per_batch == 0:
				# if only i isnt the 0 we append the batch to the total number of batches
				if i != 0:
					# append the batch if i is not the first index
					batches.append(batch)
				batch = []
			batch.append(training_data[i])

		for epoch in range(num_epochs):
			print("On epoch: {}".format(epoch + 1))
			for i in range(len(batches)):
				print("On batch number: {}".format(i + 1))
				for j in tqdm(range(len(batches[i]))):
					self.train(batches[i][j][0], batches[i][j][1])

		# np.save("./nn-data/nn-weights.npy", self.layers)
        #
		# print("The network weights have been loaded from disk...")



	def feedForward(self, inputs):
		# will contain arrays of all the outputs in each layer of the neural network
		outputs = []

		# this will loop over the layers of weights
		for i in range(len(self.layers)):
			# if we are in the first layer we are dealing with the inputs provided
			# to the neural network
			if i == 0:
				output = self.f(np.dot(self.layers[i], inputs))
			# else we are dealing with the output of the hidden layers
			else:
				output = self.f(np.dot(self.layers[i], outputs[i - 1]))

			output = np.array(output)
			# we finally append the hiddenOutput to the layers of hiddenOutputs
			outputs.append(output)

		return outputs

	# query the neural network
	def query(self, inputs):
		# convert inputs list to 2d array
		inputs = np.transpose(np.array([np.array(inputs)]))
		return self.feedForward(inputs)[-1]
