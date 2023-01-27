import numpy as np

class NeuralNetwork():
    def __init__(self, layers=None, weights=None):
        self.inputs = 12
        self.hidden_layer_neurons = 8
        self.outputs = 2
        self.fitness = -1000
        self.weights = None
        self.activations = []
        self.set_weights()

    def set_weights(self):
        if self.weights != None: return
        self.weights = []

        self.weights.append(np.random.randn(self.inputs, self.hidden_layer_neurons))
        self.weights.append(np.random.randn(self.hidden_layer_neurons, self.outputs))
        self.weights

    def forward_propagation(self, input):
        # hidden
        z1 = np.dot(input, self.weights[0])
        a1 = self.sigmoid(z1)
        
        # Output layer
        z2 = np.dot(a1, self.weights[1])
        a2 = self.sigmoid(z2)
        return(a2)
    
    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

