import numpy as np

class FeedForwardNeuralNetwork:
    def __init__(self):
        self.noOfLayers=0
        self.weights={}
        self.activationFunctionOfEachLayer={}
        self.noOfUnitsInEachLayer={}
        self.activations={}

    def predict(self, test_X):
        A_prev=test_X

        # forward prop
        for i in range(1, self.noOfLayers + 1):
            Z = np.dot(self.weights["W" + str(i)], A_prev) + self.weights["B" + str(i)]

            A_test = None
            if self.activationFunctionOfEachLayer["g" + str(i)] == "sigmoid":
                A_test = self.sigmoid(Z)

            elif self.activationFunctionOfEachLayer["g" + str(i)] == "tanh":
                A_test = self.tanh(Z)

            else:
                raise NameError(
                    "Invalid activation function name: " + self.activationFunctionOfEachLayer["g" + str(i)])

            A_prev = A_test
        predictions = A_prev

        for i in range(predictions.shape[1]):
            predictions[0, i] = 1 if predictions[0, i] > 0.5 else 0

        return predictions


    def addFeedForwardLayer(self,activationFunction='sigmoid', noOfUnits=10):

        self.noOfLayers += 1
        self.noOfUnitsInEachLayer["L"+str(self.noOfLayers)]=noOfUnits
        self.activationFunctionOfEachLayer["g"+str(self.noOfLayers)]=activationFunction
        #self.weights["W"+str(self.noOfLayers)]=W
        #self.weights["B"+str(self.noOfLayers)]=b


    def sigmoid(self, Z):
        return  1 / (1 + np.exp(-Z))

    def tanh(self, Z):
        return np.tanh(Z)


    def train(self, trainSet, trainLabels, noOfIterations=10, learningRate=0.01, validationSet=None, validationLabels=None ):

        self.m=np.shape(trainSet)[1]
        self.activations["A0"]=trainSet
        self.noOfUnitsInEachLayer["L"+str(0)]=np.shape(trainSet)[0] #for A0, it is the number of features

        #creating weight matrices and initalizing them with random values
        for i in range(1, self.noOfLayers+1):
            B = np.zeros(shape=(self.noOfUnitsInEachLayer["L"+str(i)], 1))
            W = np.random.randn(self.noOfUnitsInEachLayer["L"+str(i)], self.noOfUnitsInEachLayer["L" + str(i-1)]) * 0.01
            self.weights["W"+str(i)]=W
            self.weights["B"+str(i)]=B


        for itrNo in range(noOfIterations):

            # forward prop
            for i in range(1, self.noOfLayers + 1):
                Z = np.dot(self.weights["W" + str(i)], self.activations[("A" + str(i - 1))]) + self.weights["B" + str(i)]
                self.activations["Z" + str(i)] = Z

                A = None
                if self.activationFunctionOfEachLayer["g" + str(i)] == "sigmoid":
                    A = self.sigmoid(Z)

                elif self.activationFunctionOfEachLayer["g" + str(i)] == "tanh":
                    A = self.tanh(Z)

                else:
                    raise NameError(
                        "Invalid activation function name: " + self.activationFunctionOfEachLayer["g" + str(i)])

                self.activations["A" + str(i)] = A
            # end of forward prop

            predictions = np.array(self.activations["A" + str(self.noOfLayers)])
            for j in range(predictions.shape[1]):
                predictions[0, j] = 1 if predictions[0, j] > 0.5 else 0

            # computing error
            cost = -(1 / self.m) * np.sum((trainLabels * np.log(self.activations["A" + str(self.noOfLayers)]) + (1 - trainLabels) * np.log(1 - self.activations["A" + str(self.noOfLayers)])), axis=1)

            print("Iteration= ", itrNo+1, ". Cost= ", cost, ". Train Accuracy= {}%".format(100 - np.mean(np.abs(predictions - trainLabels)) * 100), '. ', sep='', end='')

            # printing validation accuracy if validation set is passed as parameter
            if validationSet is None:
                print('')

            else:
                validationPredictions = self.predict(validationSet)
                print("Validation Accuracy: {}%".format(
                    100 - np.mean(np.abs(validationPredictions - validationLabels)) * 100))

            # computing derivative (backward prop)
            dZ_L = np.subtract(self.activations["A" + str(self.noOfLayers)], trainLabels)
            dW_L = (1 / self.m) * np.dot(dZ_L, self.activations["A" + str(self.noOfLayers - 1)].T)
            db_L = (1 / self.m) * np.sum(dZ_L, axis=1, keepdims=True)
            dZ_next = dZ_L

            #updating weights of last layer
            self.weights["W" + str(i)] = self.weights["W" + str(i)] - learningRate * dW_L
            self.weights["B" + str(i)] = self.weights["B" + str(i)] - learningRate * db_L

            #computing gradients for remaing layers
            for i in range(self.noOfLayers - 1, 0, -1):

                dZ = np.dot(self.weights["W" + str(i + 1)].T, dZ_next)

                if self.activationFunctionOfEachLayer["g" + str(i)] == 'sigmoid':
                    dZ = dZ * (self.activations["A" + str(i)] * (1 - self.activations["A" + str(i)]))

                elif self.activationFunctionOfEachLayer["g" + str(i)] == 'tanh':
                    dZ = dZ * (1 - np.square(self.activations["A" + str(i)]))

                dW = (1 / self.m) * np.dot(dZ, self.activations["A" + str(i - 1)].T)

                dB = (1 / self.m) * np.sum(dZ, axis=1, keepdims=True)

                #updating gradients
                self.weights["W" + str(i)] = self.weights["W" + str(i)] - learningRate * dW
                self.weights["B" + str(i)] = self.weights["B" + str(i)] - learningRate * dB
                dZ_next = dZ

