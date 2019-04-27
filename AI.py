'''
Slither AI equiped with Neural Network
'''
import numpy as np
import json

try:
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']

    if scn_size[0]/scn_scale > 50:
        raise ValueError

except Exception as e:
    print(e)
    exit(0)        


def Loss_Fuc(NN_output, fd_pos):
    return (NN_output[0] - fd_pos[0]) ** 2 + (NN_output[1] - fd_pos[1]) ** 2

def deriv_Loss_Fuc(NN_output, fd_pos):
    return 

def sigmod(x):
    return 1/(1+np.exp(-x))

def deriv_sigmod(x):
    fx = sigmod(x)
    return np.exp(-x) * (fx ** 2)


class Neuron:

    def __init__(self, weights, bias):
        # inputs and weights are in terms of array
        self.weights = weights
        self.bias = bias

    def feedforward(self, inputs):
        total = np.dot(self.weights, inputs) + self.bias
        return sigmod(total)


class slitherAI:

    def __init__(self):
        self.maximum_data_size = 50
        self.no_of_hidden_layers = 1
        self.no_of_neurons = 8
        self.bias_list = [0] + [0] * self.no_of_hidden_layers
        self.adjacent_squares = [[0, 0] for x in range(4)]
        self.neurons = []
        self.neuron_layers = []

        for layer in range(self.no_of_hidden_layers):
            # create weights for hidden layers
            self.weights_matrix = [list(np.random.normal(size = self.maximum_data_size))]*self.no_of_neurons
            self.neuron_layers.append(self.weights_matrix)

        #create weights for last hidden layer to the output
        self.weights_matrix = [list(np.random.normal(size = self.maximum_data_size))]*4
        self.neuron_layers.append(self.weights_matrix)

    def check_valid_ouputs(self, head_pos):

        global scn_scale
        self.adjacent_squares = [[head_pos[0] + scn_scale, head_pos[1], 'D'], [head_pos[0], head_pos[1] + scn_scale, 'S'], [head_pos[0] - scn_scale, head_pos[1], 'A'], [head_pos[0], head_pos[1] - scn_scale, 'W']]


    def log_inputs(self, snk_body, fd_pos):
        self.inputs = snk_body + fd_pos
        self.inputs = self.inputs + [0] * (self.maximum_data_size - len(self.inputs))

    def save(self):
        pass

    def vomit_output(self):

        if len(self.neurons) == 4:
            return self.neurons

        else:
            raise ValueError

    def brew(self):

        self.neurons = [] #discard the neurons created in the previous generation

        for i, layer in enumerate(self.neuron_layers):

            if i == self.no_of_hidden_layers:
                # break the loop after loading the last hidden layer
                for weights in layer:
                    self.neurons.append(Neuron(weights, self.bias_list[i]).feedforward(self.inputs))

                break

            for weights in layer:

                self.neurons.append(Neuron(weights, self.bias_list[i]).feedforward(self.inputs))
                self.inputs = self.neurons
                self.neurons = [] # discard the neurons in the previous network layer

    def propagate_backward(self):
        pass
        




if __name__ == '__main__':
    print(deriv_sigmod(0))