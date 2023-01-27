from aiDrive.src.utils.neural_network import NeuralNetwork
import datetime
import random
import math
import numpy as np

layers = [38, 20, 2]

class GeneticAlgorithm():
    def __init__(self, num_networks):
        self.num_networks = num_networks
        self.networks = []
        self.filename = "model_weights.csv"
        self.elite_proportion = 0.2

        for i in range(num_networks):
            self.networks.append(NeuralNetwork())
        
    def update_networks(self):
        # sort networks by fitness
        self.sort_networks_by_fitness()

        # get top 10 
        elite_networks = self.get_elite_parents()
        child_networks = []

        # select parents for new 50 networks]
        for i in range(self.num_networks):
            parent1 = self.select_parent(elite_networks)
            parent2 = self.select_parent(elite_networks)

            child_genes = self.get_child_genes(parent1, parent2)
            # child_genes = parent1.weights

            # mutate genes
            # child_genes = self.mutate_genes(child_genes)

            # unflatten weights
            # child_genes = self.unflatten_weights(child_genes)

            child_networks.append(NeuralNetwork(layers=layers, weights=child_genes))

        self.networks = child_networks

    def sort_networks_by_fitness(self):
        def getFitness(e):
            return e.fitness

        self.networks.sort(reverse=True, key=getFitness)
    
    def get_elite_parents(self):
        return self.networks[:-math.floor((len(self.networks) * (1 - self.elite_proportion)))]

    def select_parent(self, parents):
        return random.choice(parents)

    def get_child_genes(self, parent1, parent2):
        # for now just return whatever

        return 
        # flatten weights
        # p1_genes = self.flatten_weights(parent1.weights)
        # p2_genes = self.flatten_weights(parent2.weights)

        # first_crossover = random.randint(0, len(p1_genes) - 1)
        # second_crossover = first_crossover
        # while second_crossover == first_crossover: second_crossover = random.randint(0, len(p1_genes) - 1)


        # print("p1_genes:", len(p1_genes[2]))
        # child_genes = []
        # child_genes += p1_genes[0:first_crossover] if random.randint(0, 1) == 0 else p2_genes[0:first_crossover]

        # child_genes += p1_genes[first_crossover: second_crossover] if random.randint(0, 1) == 0 else p2_genes[first_crossover: second_crossover]

        # child_genes += p1_genes[second_crossover: len(p1_genes)] if random.randint(0, 1) == 0 else p2_genes[second_crossover: len(p1_genes)]

        # if (len(child_genes) != len(p1_genes) or len(child_genes) != len(p2_genes)):
        #     raise Exception("you are dumb")

    def mutate_genes(self, weights):
        # TODO implement mutation
        return weights

    def flatten_weights(self, weights):
        weights = np.array(weights)
        weights.flatten()
        return weights

    def unflatten_weights(self, weights):
        new_list = []
        curr_index = 0

        for layer in layers:
            intermediary_list = []
            for i in range(layer):
                intermediary_list.append(weights[curr_index])
                curr_index += 1
            new_list.append(intermediary_list)

        return new_list

