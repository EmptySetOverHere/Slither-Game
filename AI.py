'''
A self-learning slither AI powered by neural network
Number of hidden layers: 1
Number of neurons per layer: 8
Activation Function: tanh
Loss Funcion: cosine proximity
'''

__author__ = "SiSheng"

import numpy as np
import json
import pickle

try:
    with open("game_config.json") as f:
        settings = json.loads(f.read())
        scn_size = settings['scn_size']
        scn_scale = settings['scn_scale']

    if scn_size[0]/scn_scale > 50:
        raise ValueError("This grid ratio is not supported")

except Exception as e:
    print(e)
    exit(0)        


def cos_prox(x, y):
    # x and y are both vectors
    # outputs a scalar
    return np.dot(x, y)/(np.linalg.norm(x) * np.linalg.norm(y))



def deriv_cosprox(x, y):
    # x and y are both vectors
    # outputs a vector
    # dL/dyp
    fx = cos_prox(x, y)
    return y/(np.linalg.norm(x) * np.linalg.norm(y)) - fx * (x/np.sum(np.square(x)))


def deriv_tanh(x):
    # dy/dx
    fx = np.tanh(x)
    return 1-np.square(fx)



class Neuron:

    def __init__(self, location_in_network, no_of_neurons):
        # inputs are numpy arrays
        # location_in_network is a tuple in the form of (neuron, layer)
        # no_of_neurons is the number of neurons in the previous layer
        self.generation = 0
        self.weights = np.reshape([np.random.normal(size = no_of_neurons * 2)], (no_of_neurons, 2))
        self.new_weights = np.copy(self.weights)
        self.bias = np.array([0, 0], dtype='float64')
        self.location = location_in_network
        self.dy_dx_list = []

    def feedforward(self, inputs):
        self.inputs = inputs
        total = sum(self.weights * inputs) + self.bias
        return np.tanh(total) # outputs a 1x2 vector

    def feedbackward(self):
        total = sum(self.weights * self.inputs) + self.bias

        dy_dx = []
        for each in self.dy_dx_list:
            result = self.weights * (deriv_tanh(total) * each)
            dy_dx.append(result)
        
        return dy_dx

    def receive(self, external_dy_dx_list, learning_rate):
        total = sum(self.weights * self.inputs) + self.bias
        dx_dw = self.inputs * deriv_tanh(total)
        dx_db = 1 * deriv_tanh(total)

        for each in external_dy_dx_list:
            dy_dx = each[self.location[0]]
            self.dy_dx_list.append(dy_dx)
            self.new_weights -= learning_rate * dy_dx * dx_dw
            self.bias -= learning_rate * dy_dx * dx_db

    def update(self):
        self.weights = np.copy(self.new_weights)
    


class slitherAI:

    def __init__(self, hidden_layers = None, output_layer = None, learning_rate = 10):
        self.maximum_data_size = 50
        self.no_of_hidden_layers = 1
        self.no_of_neurons = 8
        self.learning_rate = learning_rate
        self.output = []
        self.neurons = []
        self.hidden_layers = hidden_layers
        self.output_layer = output_layer

    def log_inputs(self, snk_body, fd_pos):
        self.inputs = snk_body + fd_pos
        self.inputs = np.array(self.inputs)

        for zero in range(self.maximum_data_size - len(self.inputs)):
            # padding 1 x 2 zero vectors at the bottom of the list
            self.inputs = np.append(self.inputs, np.zeros((1, 2)))

        self.inputs = np.reshape(self.inputs, (self.maximum_data_size, 2))


    def save_network(self):
        with open("AIParameters.pickle", "wb") as p:
            pickle.dump(self.hidden_layers, p)
            pickle.dump(self.output_layer, p)



    def vomit_output(self):

        if self.output_layer is None:
            self.output_layer = Neuron((0, self.no_of_hidden_layers), self.no_of_neurons)
            self.output = self.output_layer.feedforward(self.inputs)

        else:
            self.output = self.output_layer.feedforward(self.inputs)

        x, y  = self.output
        
        if  np.abs(x) < np.abs(y):
            
            if y < 0:
                self.output = np.array([0, -1])
                return "W"
            else:
                self.output = np.array([0, 1])
                return "S"

        else:
            if x < 0:
                self.output = np.array([-1, 0])
                return "A"
            else:
                self.output = np.array([1, 0])
                return "D"


    def brew(self):

        self.neurons = [] #discard the neurons created in the previous generation
        self.inputs_list = np.array([])
        
        if self.hidden_layers is None:

            self.hidden_layers = []
        
            for layer in range(self.no_of_hidden_layers):

                for n in range(self.no_of_neurons):
                    
                    if layer == 0:
                        self.neurons.append(Neuron((n, layer), self.maximum_data_size))
                    else:
                        self.neurons.append(Neuron((n, layer), self.no_of_neurons))
                
                self.hidden_layers.append(self.neurons)
                    
                for neuron in self.neurons:

                    self.inputs_list = np.append(self.inputs_list, neuron.feedforward(self.inputs))

                self.neurons = []
                self.inputs = np.reshape(self.inputs_list, (self.no_of_neurons, 2))

        else:

            for layer in self.hidden_layers:

                for neuron in layer:

                    self.inputs_list = np.append(self.inputs_list, neuron.feedforward(self.inputs))

                self.inputs = np.reshape(self.inputs_list, (self.no_of_neurons, 2))


    def propagate_backward(self, snk_head, fd_pos):
        
        y_true = fd_pos - snk_head
        Loss_value = cos_prox(self.output, y_true)
        print("Loss Value: {}".format(Loss_value))

        dy_dx_list = []
        dy_dx_list_new = []

        dL_dyp = deriv_cosprox(self.output, y_true)
        self.output_layer.receive([dL_dyp], self.learning_rate)
        dy_dx = self.output_layer.feedbackward()
        dy_dx_list += dy_dx

        self.output_layer.update()

        for layer in reversed(self.hidden_layers): # in a reversed order

            for neuron in layer:

                neuron.receive(dy_dx_list, self.learning_rate)
                dy_dx = neuron.feedbackward()
                dy_dx_list_new += dy_dx
                neuron.update()

            dy_dx_list = dy_dx_list_new
            dy_dx_list_new = []




if __name__ == '__main__':

    with open("AIParameters.pickle", "rb") as p:
            hidden_layers = pickle.load(p)
            output_layer = pickle.load(p)
    
    snk_AI = slitherAI(hidden_layers = hidden_layers, output_layer=output_layer)
    a = [np.array([1, 2]), np.array([3, 4])]
    b = [np.array([5, 6])]
    snk_AI.log_inputs(a, b)
    snk_AI.brew()
    snk_AI.vomit_output()
    snk_AI.propagate_backward(a[0], b[0])
    snk_AI.save_network()


