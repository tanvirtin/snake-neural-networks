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

	# returns all the neurons in neural network into a flattend single layered array
	def retrieve_weights_per_neuron(self):
		return [self.layers[i][j] for i in range(len(self.layers)) for j in range(len(self.layers[i]))]

	def replace_neuron(self, index, new_neuron):
		# keeps track of the ith index
		on_layer = 0
		# keeps track of the jth index
		on_neuron = 0
		matching_index = 0
		for i in range(len(self.layers)):
			# on_neuron goes to 0 as we go into a new layer every time
			on_neuron = 0
			for j in range(len(self.layers[i])):
				# if matching_index is the index provided we need to break out of BOTH the loops and replace the neuron
				if matching_index == index:
					self.layers[on_layer][on_neuron] = new_neuron
					# both loops are broken down as I return
					return
				# the matching index always gets incremented whenever we are traversing through the neurons in each layer
				matching_index += 1
				# the layer index gets incremented each time as the on_neuron keeps track of the index of the neuron
				# we are on at a specific layer
				on_neuron += 1
			# we increment the layer we are on everytime the first loop iterates
			# as the first loop loops over the layers
			on_layer += 1

		if matching_index < index:
			return

	# takes in the index of the array element which will get replaced by the new bias neuron
	def replace_bias(self, index, new_bias):
		self.biases[index] = new_bias

	def feed_forward(self, inputs):
		# will contain arrays of all the outputs in each layer of the neural network
		outputs = []

		# this will loop over the layers of weights
		for i in range(len(self.layers)):
			# if we are in the first layer we are dealing with the inputs provided
			# to the neural network
			if i == 0:
				output = scipy.special.expit(np.dot(self.layers[i], inputs))
			# else we are dealing with the output of the hidden layers
			else:
				output = scipy.special.expit(np.dot(self.layers[i], outputs[i - 1]))

			output = np.array(output)
			# we finally append the hiddenOutput to the layers of hiddenOutputs
			outputs.append(output)

		return outputs

	# query the neural network
	def get_movement(self, inputs):
		# convert inputs list to 2d array
		inputs = np.transpose(np.array([np.array(inputs)]))
		# get the last layer of the output
		return self.feed_forward(inputs)[-1]


def main():
	nn = NeuralNetwork([2, 2, 1])

	print(nn.retrieve_weights_per_neuron())

	nn.replace_neuron(3, 4)

	print(nn.retrieve_weights_per_neuron())


if __name__ == "__main__":
	main()
