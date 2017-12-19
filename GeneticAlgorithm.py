from NeuralNetwork import NeuralNetwork
from TFNN import TFNN
from TFLearnNN import TFLearnNN
import random
import copy
import numpy as np

MUTATE_FACTOR = 1 + ((random.random() - 0.5) * 3 + (random.random() - 0.5))

class GeneticAlgorithm():
    def __init__(self, pop_size=10, evolve_size=4, rand_select=0.3, mutate_chance=0.3):
        self.pop_size = pop_size
        self.evolve_size = evolve_size
        self.rand_select = rand_select
        self.mutate_chance = mutate_chance

    def init_population(self):
        return [TFLearnNN((4, 25, 3)) for _ in range(self.pop_size)]
        #return [NeuralNetwork((8, 10, 4)) for _ in range(self.pop_size)]
        #return [TFNN((8, 10, 4)) for _ in range(self.pop_size)]

    def ranked_networks(self, fitness_agents):
        return [fa[1] for fa in sorted(fitness_agents, key=lambda x: x[0], reverse=True)]

    def breed(self, a, b):
        weights = []
        for a_l, b_l in zip(a.weights(), b.weights()):
            a_weights, a_bias = a_l[0], a_l[1]
            b_weights, b_bias = b_l[0], b_l[1]
            n_weights = np.zeros(a_weights.shape)
            n_bias = np.zeros(len(a_bias))

            slice_pos = random.randint(0, len(a_weights)-1)
            parents = [a_weights, b_weights]
            random.shuffle(parents)
            #print(slice_pos, len(parents[0]))
            #print('pre', n_weights)
            n_weights[:slice_pos] = parents[0][:slice_pos]
            #print('mid', n_weights)
            n_weights[slice_pos:] = parents[1][slice_pos:]
            #print('post', n_weights)

            weights.append([n_weights, n_bias])

        new_network = copy.copy(a)
        new_network.set_weights(weights)
        # print('a_weights', a.weights())
        # print('b_weights', b.weights())
        # print('new_weights', weights)
        return new_network

    def mutate(self, network):
        elems = network.weights()
        #print('pre_weight', elems)
        for i, elem in enumerate(elems):
            for j, layer in enumerate(elem):
                #mutated_count = 0
                for k in range(len(layer)):
                    if random.random() < self.mutate_chance:
                        #print('pre', layer[i])
                        elems[i][j][k] *= MUTATE_FACTOR
                        #mutated_count += 1
                        #print('post', layer[i])
                #print("mutated_count:", mutated_count)
        #print('post_weight', elems)
        new_network = copy.copy(network)
        new_network.set_weights(elems)
        return new_network

    def evolve_population(self, fitness_agents):
        # rank by fitness
        networks = self.ranked_networks(fitness_agents)

        # keep pick top [:evolve_size]
        evolved = networks[:self.evolve_size]
        print('init_evolved:',len(evolved))

        # randomly pick from rest
        for network in networks[self.evolve_size:]:
            if random.random() < self.rand_select:
                evolved.append(network)
        print('post_random_add:',len(evolved))

        # mutate subset of evolved
        for i, network in enumerate(evolved):
            if random.random() < self.mutate_chance:
                evolved[i] = self.mutate(network)

        # randomly pick 2 from [evolve_size:] and breed remaining pop_size - len(evolved)
        while len(evolved) < self.pop_size:
            parentA = random.randint(0, self.evolve_size-1)
            parentB = random.randint(0, self.evolve_size-1)
            if parentA == parentB:
                continue
            evolved.append(self.breed(evolved[parentA], evolved[parentB]))
        print('post_breed:',len(evolved))

        return evolved
