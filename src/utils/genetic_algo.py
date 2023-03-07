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
        self.elite_proportion = 0.5
        self.crossover_chance = 0.8
        self.mutation_chance = 1/20


        for i in range(num_networks):
            self.networks.append(NeuralNetwork())
        
    def update_networks(self):
        # sort networks by fitness
        self.sort_networks_by_fitness()

        # get top 10 
        elite_networks = self.get_elite_parents()
        child_networks = []

        # select parents for new 50 networks]
        for i in range(int(self.num_networks / 2)):
            parent1 = self.select_parent(elite_networks)
            parent2 = self.select_parent(elite_networks)

            child1_genes, child2_genes = self.get_child_genes(parent1, parent2)

            child_networks.append(NeuralNetwork(layers=layers, weights=child1_genes))
            child_networks.append(NeuralNetwork(layers=layers, weights=child2_genes))

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

        child1_genes = []
        child2_genes = []


        #crossover
        for i in range(0, len(parent1.weights)):
            if random.random() < self.crossover_chance:
                w1_flat = parent1.weights[i].flatten()
                w2_flat = parent2.weights[i].flatten()

                crossover_point = random.randint(0, w1_flat.size)


                w1 = np.concatenate((w1_flat[:crossover_point], w2_flat[crossover_point:]))
                w2 = np.concatenate((w2_flat[:crossover_point], w1_flat[crossover_point:]))


                w1 = w1.reshape(np.shape(parent1.weights[i]))
                w2 = w2.reshape(np.shape(parent2.weights[i]))

                child1_genes.append(w1)
                child2_genes.append(w2)

            else:
                child1_genes.append(parent1.weights[i])
                child2_genes.append(parent2.weights[i])

        for i in range(len(child1_genes)):
            row, col = np.shape(child1_genes[i])
            mutation_chance = 1/(row * col)
            for r in range(row):
                for c in range(col):
                    if (random.random() < mutation_chance):
                        child1_genes[i][r, c] = random.random()

                    if (random.random() < mutation_chance):
                        child2_genes[i][r, c] = random.random()



        if (len(child1_genes) != len(child2_genes) or len(child1_genes) != len(parent1.weights) or len(child1_genes) != len(parent2.weights)):
            raise Exception("child gene length mismatch")

        return child1_genes, child2_genes



    def mutate_genes(self, weights):
        # TODO implement mutation
        return weights

    def flatten_weights(self, weights):
        for i ,layer in enumerate(weights):
            weights[i] = layer.flatten()

        return weights

