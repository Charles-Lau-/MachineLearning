import math
import random
BIAS = -1

"""
    This is a general implementation of two layer(input layer, and
    output layer) neural network, and use backward propogation techniques
    
"""

class Neuron:
    def __init__(self,number_of_inputs):
        self.number_of_inputs = number_of_inputs
        self.set_weights([random.uniform(0,1) for i in range(0,number_of_inputs+1)])

    def weighted_sum(self,inputs):
        """
            does not include the bias
        """
        
        return sum(value*self.weights[i] for i,value in enumerate(inputs))

    def activation(self,inputs,function_name):
        """
            get f(weighted_sum+BIAS*self.weights[-1])
        
        """
        weighted_value = self.weighted_sum(inputs)+BIAS*self.weights[-1]
        return eval(function_name+"("+str(weighted_value)+")")
        
    def set_weights(self,weights):
        self.weights = weights

    def __str__(self):
        return "Weights:%s,Bias:%s" % (str(self.weights[:-1]),str(self.weights[-1]))

class NeuronLayer:
    def __init__(self,number_of_neurons,number_of_inputs):
        self.number_of_neurons = number_of_neurons
        self.neurons = [Neuron(number_of_inputs) for _ in range(0,self.number_of_neurons)]

    def __str__(self):
        return "\n\t".join([str(neuron) for neuron in self.neurons])

class NeuronNetwork:
    """
        the layout of this neuron network is input layer-> hidden layer -> output
        layer

    """
    def __init__(self,number_of_inputs,neurons_in_first_layer,number_of_outputs):
        self.number_of_inputs = number_of_inputs
        self.number_of_outputs = number_of_outputs
        self.neurons_in_first_layer = neurons_in_first_layer
        
        self._create_network()

    def _create_network(self):
        """
            build up neuron network
            
        """
        
        #create first layer
        self.layers = [NeuronLayer(self.neurons_in_first_layer,self.number_of_inputs)]

        #create second layer
        self.layers += [NeuronLayer(self.number_of_outputs,self.neurons_in_first_layer)]

    def get_weights(self):
        """
            return the sum of weights of all neurons in the network

        """
        weights = []

        for layer in self.layers:
             for neuron in layer.neurons:
                 weights += neuron.weights

        return weights

    def update(self,inputs):
        """
            given specific inputs value like [1,2,3,4,5,6], then output the cor-
            responding output, based on weights of this neural network
        """
        assert len(inputs) == self.number_of_inputs,"Incorrect number of inputs"

        for layer in self.layers:
            outputs = []
            for neuron in layer.neurons:
                outputs.append(neuron.activation(inputs,"sigmoid"))
            inputs = outputs

        return outputs

    def backpropagation(self,training_data,learning_rate=0.4):
        pass
    
def sigmoid(activation,response=1.0):
    return 1.0/(1+math.e**(-activation/response))

if __name__ == "__main__":
   print NeuronNetwork(6,6,2).update([1,2,3,4,5,6])
