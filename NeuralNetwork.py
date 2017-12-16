from tqdm import tqdm
import numpy as np
import math
import scipy.special

# This neural network is specially designed for genetic algorithm
class NeuralNetwork:

	# initialise the neural network
	def __init__(self, dimensions):
		# this array will contain all the layers of the neural network
		self.layers = []
		self.biases = []

		# constructing the hidden layers
		for i in range(1, len(dimensions)):
			hidden_layer = []
			# number of weight arrays will be determined by the number of neurons
			# in the current layer
			for j in range(dimensions[i]):
				# number of weights per neuron is equal to the number of nodes
				# in the previous layer
				# very important for the weights to be assigned with random values from -1 to +1
				# as our algorithm adds up the change in weight
				hidden_layer.append(np.random.uniform(-1, 1, dimensions[i - 1]))

			# add the bias neuron
			self.biases.append(np.random.uniform(-1, 1, dimensions[i - 1]))

			# make the hiddenLayer into a np array
			hiddenLayer = np.array(hidden_layer)

			self.layers.append(hidden_layer)

	# need to return biases so that it can get swapped for crossover where two best parents breed to get a new child
	def retrieve_bias_weights_per_neuron(self):
		return self.biases


	def retrieve_weights_per_neuron(self):
		return [self.layers[i][j] for i in range(len(self.layers)) for j in range(len(self.layers[i]))]

	def feed_forward(self, inputs):
		# will contain arrays of all the outputs in each layer of the neural network
		outputs = []

		# this will loop over the layers of weights
		for i in range(len(self.layers)):
			# if we are in the first layer we are dealing with the inputs provided
			# to the neural network
			if i == 0:
				output = scipy.special.expit(np.dot(self.layers[i], inputs) + self.biases[i])
			# else we are dealing with the output of the hidden layers
			else:
				output = scipy.special.expit(np.dot(self.layers[i], outputs[i - 1]) + self.biases[i])

			output = np.array(output)
			# we finally append the hiddenOutput to the layers of hiddenOutputs
			outputs.append(output)

		return outputs

	# query the neural network
	def query(self, inputs):
		# convert inputs list to 2d array
		inputs = np.transpose(np.array([np.array(inputs)]))
		# get the last layer of the output
		return self.feed_forward(inputs)[-1]


def main():
	nn = NeuralNetwork([2, 2, 1])

	print(nn.retrieve_weights_per_neuron())
	print(nn.retrieve_bias_weights_per_neuron())

	print(nn.query([0, 1]))


if __name__ == "__main__":
	main()
