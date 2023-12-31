import numpy as np

class NeuralNetwork():
    def __init__(self, layers=None, weights=None):
        self.layers = [9, 8, 2]
        self.fitness = -1000
        self.weights = weights
        self.activations = []
        self.set_weights()

    def set_weights(self):
        if self.weights != None: return
        self.weights = []
            
        for i in range(len(self.layers) -1): 
            self.weights.append(np.random.rand(self.layers[i], self.layers[i+1]))


    def forward_propagation(self, input):
        # hidden layer
        z1 = np.dot(input, self.weights[0])
        a1 = self.sigmoid(z1)
        
        # Output layer
        z2 = np.dot(a1, self.weights[1])
        a2 = self.sigmoid(z2)
        return(a2)
    
    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

