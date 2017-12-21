from GANeuralNetwork import GANeuralNetwork
import random
import numpy as np

class GeneticAlgorithm():
    def __init__(self, pop_size=10, evolve_size=5, mutate_chance=0.8):
        self.pop_size = pop_size
        self.evolve_size = evolve_size
        self.mutate_chance = mutate_chance

    def init_population(self):
        return [GANeuralNetwork((5, 25, 1)) for _ in range(self.pop_size)]
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

        print('breeding')
        new_network = GANeuralNetwork(a.dimensions, a.weights())
        # print('a_weights', a.weights())
        # print('b_weights', b.weights())
        # print('new_weights', weights)
        return new_network


    def mutation_factor(self):
        return 1 + ((random.random() - 0.5) * 3 + (random.random() - 0.5))

    def mutate(self, network):
        print('mutating')
        elems = network.weights()
        for i, elem in enumerate(elems):
            for j, layer in enumerate(elem):
                for k in range(len(layer)):
                    if random.random() < self.mutate_chance:
                        elems[i][j][k] *= self.mutation_factor()

        new_network = GANeuralNetwork(network.dimensions, elems)
        return new_network

    def evolve_population(self, fitness_agents):
        # rank by fitness
        networks = self.ranked_networks(fitness_agents)

        # keep pick top [:evolve_size]
        evolved = networks[:self.evolve_size]
        print('init_evolved:',len(evolved))

        # randomly pick from rest
        # for network in networks[self.evolve_size:]:
            # if random.random() < self.rand_select:
                # evolved.append(network)
        print('post_random_add:',len(evolved))

        # randomly pick 2 from [evolve_size:] and breed remaining pop_size - len(evolved)
        while len(evolved) < self.pop_size:
            parentA = random.randint(0, self.evolve_size-1)
            parentB = random.randint(0, len(networks)-1)
            if parentA == parentB:
                continue
            evolved.append(self.breed(networks[parentA], networks[parentB]))
        print('post_breed:',len(evolved))

        # mutate subset of evolved
        for i, network in enumerate(evolved[self.evolve_size:]):
            if random.random() < self.mutate_chance:
                evolved[i+self.evolve_size] = self.mutate(network)
                #evolved.append(GANeuralNetwork(network.dimensions))

        return evolved
