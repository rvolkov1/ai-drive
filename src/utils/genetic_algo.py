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
        self.mutation_chace = 1/20

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
            #child_genes = self.unflatten_weights(child_genes)

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

        child_genes = []

        #crossover
        for i in range (len(p1.weights)):
            p1_genes = 
            
                
        #child_genes = parent1.weights # temporary solution

        #unflatten genes



        if (len(child_genes) != len(p1_genes) or len(child_genes) != len(p2_genes)):
            raise Exception("you are dumb")

        return child_genes



    def mutate_genes(self, weights):
        # TODO implement mutation
        return weights

    def flatten_weights(self, weights):
        for i ,layer in enumerate(weights):
            weights[i] = layer.flatten()

        return weights

