import random
import math
import numpy as np

"""
    a program for digital recognition

"""

class Network():

    def __init__(self,sizes):
        """
            size contains the number of neurons in the respective layers like [2,
            3,1] in which 2 means the number of inputs 
            
        """
        self.num_layers = len(sizes)
        self.sizes  = sizes
        #self.biases contains list of vectors each of which is biases of that
        #neural network layer
        self.biases = [np.random.randn(y,1) for y in sizes[1:]]
        #self.weight contains list of matrix each of which contains y neurons and
        #each neuron contains x number of weights
        self.weights  = [np.random.randn(y,x)
                        for x,y in zip(sizes[:-1],sizes[1:])]

    def feedforward(self,inputs):
        """
            return the output of the network  
    
        """ 

        for b,w in zip(self.biases,self.weights):
             
            outputs = sigmoid_vec(np.dot(w,inputs)+b)
             
            inputs = outputs

        return outputs

    def stochastic_gradient_descent(self,trainning_data,epochs,mini_batch_size,
                                    beta):
        """
            here is how it is going. The trainning_data is splitted into several
            mini_batch with mini_batch_size size, and then we use this mini_batch
            to do one single gradient descent, we do size(tranning_data)/mini_bat
            ch_size  epoches times to iterate gradient descent

        """
        n = len(training_data)
        for j in xrange(epoches):
            random.shuffle(training_data)
            mini_batches = [
                             training_data[k:k+mini_batch_size]
                             for k in xrange(0,n,mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch,beta)

    def update_mini_batch(self,mini_batch,beta):
        """
            update weights and biases one time accroding to data mini_batch and
            beta is the learning rate

        """

        difference_weights = [np.zeros(w.shape) for w in self.weights]
        difference_biases = [np.zeros(b.shape) for b in self.biases]
        for x,y in mini_batch:
            delta_w,delta_b = self.backprop(x,y)
            difference_weights = [i+delta
                            for i,delta in zip(difference_weights,delta_w)]
            difference_biases = [i+biases
                            for i,biases in zip(difference_biases,delta_b)]
            
        self.weights = [w-(beta/len(mini_batch))*nw
                        for w,nw in zip(self.weights,difference_weights)]
        self.biases = [b-(beta/len(mini_batch))*nb
                       for b,nb in zip(self.biases,difference_biases)]

    def backprop(self,x,y):
        """
            return tuple (delta_b,delta_w) representing the gradient for cost
            function , and they are matrix , similar structure to self.biases and
            self.weights

        """
        delta_b = [np.zeros(b.shape) for b in self.biases]
        delta_w = [np.zeros(w.shape) for w in self.weights]
        #feed forward
        inputs = x
        activations = [x] #list to store all the activations, layer by layer
        weighted_inputs = [] #list to store all the weighted inputs vectors , layer by layer
        for b,w in zip(self.biases,self.weights):
            weighted_input = np.dot(w,inputs)+b
            weighted_inputs.append(weighted_input)
            activation = sigmoid_vec(weighted_input)
            activations.append(activation)
            inputs = activation

        #backward propagation
        delta =  self.cost_derivative(activations[-1],y)* \
                 sigmoid_prime_vec(weighted_inputs[-1]) # error in last layer

        delta_b[-1] = delta
        delta_w[-1] = np.dot(delta,activations[-2].transpose())

        for l in xrange(2,self.num_layers):
            weighted_input = weighted_inputs[-l]
            delta = np.dot(self.weights[-l+1].transpose(),delta) * \
                    sigmoid_prime_vec(weighted_input)

            delta_b[-1] = delta
            delta_w[-1] = np.dot(delta,activations[-l-1].transpose())

        return (delta_b,delta_w)
        
    def cost_derivative(self,output_activatioins,y):
        """
            return the vector of partial derivative  C / a for the output activa
            tion
        """

        return (output_activations - y)
    
def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

sigmoid_vec = np.vectorize(sigmoid)

def sigmoid_prime(z):

    return sigmoid(z)*(1-sigmoid(z))

sigmoid_prime_vec = np.vectorize(sigmoid_prime)

if __name__ == "__main__":
    print Network([784,30,10])
