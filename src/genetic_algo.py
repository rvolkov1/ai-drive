import numpy as np

def sigmoid(z):
    return 1/(1+np.exp(-z))

def normalize_inputs(value, highbound, signed):
    # normalize to value between 0 and 1
    if (not signed): return value / highbound

    return 0.5 + value / (highbound * 2)

    

class NeuralNetwork():
    # inspired by Welch Labs: neural networks demystified
    def __init__(self):
        self.drivers = []
        self.input_layer_size = 36 + 2
        self.hidden_layer_size = 21
        self.output_layer_size = 4
    
        # initialize weights
        self.W1 = np.random.randn(self.input_layer_size, self.hidden_layer_size)
        self.W2 = np.random.randn(self.hidden_layer_size, self.output_layer_size)

    def forward_propagation(self, inputs):
        self.z2 = np.dot(inputs, self.W1)
        self.a2 = sigmoid(self.z2)
        self.z3 = np.dot(self.a2, self.outputs)