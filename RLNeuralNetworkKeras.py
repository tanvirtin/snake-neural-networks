from keras.models import Sequential, model_from_json
from keras.layers import Dense, Activation
from keras.layers.advanced_activations import LeakyReLU
from keras import optimizers
from keras.callbacks import TensorBoard
import numpy as np

class KerasNeuralNetwork(object):
    def __init__(self, dimensions, pre_trained = True, learning_rate = 1e-2):
        self.model = Sequential()
        self.model.add(Dense(dimensions[1], activation = 'relu', input_dim = dimensions[0]))
        #self.model.add(LeakyReLU(alpha=.001))
        #self.model.add(Dense(35, activation = "relu", input_dim = dimensions[1]))
        self.model.add(Dense(dimensions[-1], activation = 'sigmoid'))
        self.rms_props = optimizers.RMSprop(lr = learning_rate)
        self.model.compile(optimizer = self.rms_props, loss = 'mse')
        self.tensorboard = TensorBoard(log_dir = "./logs", histogram_freq = 0, write_graph = True, write_images = False)

        # if not pre_trained:
        #     try:
        #         self.loaded_model = open("./keras-nn-data/rl-model.json", "r")
        #         if self.loaded_model:
        #             self.model.load_weights("./keras-nn-data/rl-model.h5")
        #             print("The network weights have been loaded from disk...")
        #     except:
        #         pass

        # if pre_trained is mentioned
        if pre_trained:
            try:
                self.loaded_model = open("./keras-nn-data/best-rl-model.json", "r")
                if self.loaded_model:
                    self.model.load_weights("./keras-nn-data/best-rl-model.h5")
                    print("The best network has been loaded from disk...")
            except:
                print("Untrained Neural Network is being used...")
                pass


    def query(self, input_data):
        input_data = np.array(input_data).reshape(-1, 5)
        return self.model.predict(input_data)

    def fit(self, training_data, num_batches, num_epochs):
        inputs = np.array([i[0] for i in training_data]).reshape(-1, 5)
        outputs = np.array([i[1] for i in training_data]).reshape(-1, 1)
        self.model.fit(inputs, outputs, epochs = num_epochs, batch_size = num_batches, callbacks = [self.tensorboard])
        model_json = self.model.to_json()

        # with open("./keras-nn-data/rl-model.json", "w") as json_file:
        #     json_file.write(self.model.to_json())
        #
        # self.model.save_weights("./keras-nn-data/rl-model.h5")
        #
        # print("Model is saved to disk...")
