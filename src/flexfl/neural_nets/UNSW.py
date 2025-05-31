from flexfl.builtins.NeuralNetworkABC import NeuralNetworkABC

class UNSW(NeuralNetworkABC):

    def keras_model(self, input_shape, output_size, is_classification):
        import keras
        layers = [
            keras.layers.Input(shape=input_shape),
            keras.layers.Dense(300, activation='relu'),
            keras.layers.Dense(100, activation='relu'),
            keras.layers.Dense(40, activation='relu'),
            keras.layers.Dense(output_size)
        ]
        if is_classification:
            layers.append(keras.layers.Softmax())
        return keras.models.Sequential(layers)
    

# "UNSW": "Evaluation of Adversarial Training on Different Types of Neural Networks in Deep Learning-based IDSs - (table II)",
# keras.layers.Dense(128, activation='relu'),
# keras.layers.Dense(96, activation='relu'),
# keras.layers.Dense(64, activation='relu'),
# keras.layers.Dropout(0.25),
