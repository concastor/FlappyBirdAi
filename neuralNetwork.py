import numpy as np
import math as m
import copy
import random as rand


# 3 layered neural network template
# params:   numInputs = the number of inputs that the Neural network will receive
#           numHidden = the number of hidden layer perceptrons to use
#           numOutput = the number of outputs the Neural network will return on a guess
# Author:  Jake Richardson

class NeuralNetwork:
    # takes in the number of inputs,hidden layer and outputs
    def __init__(self, num_inputs, num_hidden, num_output):
        #node count for each layer
        self.iNodes = num_inputs
        self.hNodes = num_hidden
        self.oNodes = num_output

        # create matrices of weights between the node layers
        self.weightsIH = np.random.uniform(-1, 1, (self.hNodes, self.iNodes))
        self.weightsHO = np.random.uniform(-1, 1, (self.oNodes, self.hNodes))

        #matrices of the bias
        self.biasH = np.random.uniform(-1, 1, (self.hNodes, 1))
        self.biasO = np.random.uniform(-1, 1, (self.oNodes, 1))

        self.learnRate = 0.1
        self.mutateRate = 0.2

    # making a guess using the Feedforward algorithm
    def guess_ff(self, inputs):
        # reshaping the inputs into a matrix
        inputs = np.reshape(inputs, (len(inputs), 1))

        # generate hidden outputs
        hidden = np.dot(self.weightsIH, inputs)
        hidden = np.add(hidden, self.biasH)
        self.normalize(hidden)  #activation function

        # move from hidden layer to output layer and repeat previous steps
        output = np.dot(self.weightsHO, hidden)
        output = np.add(output, self.biasO)
        self.normalize(output)

        # convert to list for the return value
        return list(np.array(output).reshape(-1,))

    # for getting hidden and output values
    def get_ho(self, inputs):
        # reshaping the inputs into a matrix
        inputs = np.reshape(inputs, (len(inputs), 1))

        # generate hidden outputs
        hidden = np.dot(self.weightsIH, inputs)
        hidden = np.add(hidden, self.biasH)
        self.normalize(hidden)  #activation function

        # move from hidden layer to output layer and repeat previous steps
        output = np.dot(self.weightsHO, hidden)
        output = np.add(output, self.biasO)
        self.normalize(output)
        output = list(np.array(output).reshape(-1, ))

        return output, hidden

    # uses the sigmoid function as the activation function
    @staticmethod
    def sigmoid(x):
        return 1/(1 + m.exp(-x))

    # goes through matrix and runs the sigmoid function on each element
    # to put the value between 0 and 1
    def normalize(self, matrix):
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for item in it:
                item[...] = self.sigmoid(item)

    # finds the derivative of sigmoid of each element in the matrix
    @staticmethod
    def gradient(matrix):
        with np.nditer(matrix, op_flags=['readwrite']) as it:
            for item in it:
                item[...] = item * (1 - item)
        # return matrix

    # training for supervised learning using back propagation
    def train(self, inputs, answers):
        #get values
        output, hidden = self.get_ho(inputs)

        #turning into a matrix
        output = np.asmatrix(output)
        target = np.asmatrix(answers)

        #calculate the errors
        output_err = np.subtract(target, output)
        output_err = np.transpose(output_err)

        #calculate thee hidden error using transposed weights
        weights_hot = np.transpose(self.weightsHO)
        hidden_err = np.multiply(weights_hot, output_err)

        #calculatee output gradients
        self.gradient(output)
        gradient = np.multiply(output, output_err)
        gradient = np.multiply(gradient, self.learnRate)

        #calculate hidden gradient
        self.gradient(hidden)
        h_gradient = np.multiply(hidden, hidden_err)
        h_gradient = np.multiply(h_gradient, self.learnRate)

        #calculate deltas
        hidden_t = np.transpose(hidden)
        weights_ho_deltas = np.multiply(gradient, hidden_t)

        #calculate hidden deltas
        inputs_t = np.transpose(np.asmatrix(inputs))
        weights_ih_deltas = np.multiply(h_gradient, inputs_t)

        #add deltas to the weights
        self.weightsHO = np.add(self.weightsHO, weights_ho_deltas)
        self.weightsIH = np.add(self.weightsIH, weights_ih_deltas)

        #adjust bias
        self.biasO = np.add(self.biasO, gradient)
        self.biasH = np.add(self.biasH, h_gradient)

    #simplified crossover function for Neuro-evolution
    def copy(self):
        return copy.deepcopy(self)

    # mutation function for Neuro-evolution
    def mutate(self):
        self.random_mutate(self.weightsIH)
        self.random_mutate(self.weightsHO)
        self.random_mutate(self.biasH)
        self.random_mutate(self.biasO)

    #goes through all element in weight matrices and mutates them
    def random_mutate(self, a):
        with np.nditer(a, op_flags=['readwrite']) as it:
            for x in it:
                # mutates part of the weights of the matrix depending on learning rate
                mutate = rand.uniform(0, 1)
                if mutate < self.mutateRate:
                    #picks new weight
                    x[...] = rand.uniform(-1, 1)



