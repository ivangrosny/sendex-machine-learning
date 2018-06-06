import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

# Aca defino la clase
class Support_Vector_Machine:
    # Este es el constructor
    def __init__(self, visualization=True):
        self.visualization = visualization
        self.colors = {1:'r', -1:'b'}
        if self.visualization:
            # crea un objeto figure
            self.fig = plt.figure()
            # Le agrega los ejes
            self.ax = self.fig.add_subplot(1, 1, 1)

    # Esta es la funcion para entrenar
    def fit(self, data):
        self.data = data
        #{ ||w||: [w,b]}
        opt_dict = {}

        transforms = [[1,1],
                    [-1,1],
                    [-1,-1],
                    [1,-1],]

        # busca maximo y minimos ranges
        all_data = []
        for yi in self.data:
            for featureset in self.data[yi]:
                for feature in featureset:
                    all_data.append(feature)

        self.max_feature_value = max(all_data)
        self.min_feature_value = max(all_data)

        all_data = None

        # Empieza con big steps
        step_sizes = [self.max_feature_value * 0.1,
                    self.max_feature_value * 0.01,
                    self.max_feature_value * 0.001,]

        # Extremely expensive, b no tiene que hacer pasos tan peque~no
        # no tiene que ser preciso
        b_range_multiple = 5

        #
        b_multiple = 5

        latest_optimum = self.max_feature_value * 10

        for step in step_sizes:
            w = np.array([latest_optimum, latest_optimum])
            # cuando converge
            optimized = False
            while not optimized:
                for b in np.arange(-1*(self.max_feature_value*b_range_multiple),
                        self.max_feature_value * b_range_multiple,
                        step * b_multiple):
                    for transformation in transforms:
                        w_t = w*transformation
                        found_option = True
                        # Es eslavon mas fragil del SVM
                        # SMO - ver que es
                        # yi(xi.w + b) >= 1
                        for i in self.data:
                            for xi in self.data[i]:
                                yi = i
                                if not yi*(np.dot(w_t,xi)+b) >= 1:
                                    found_option = False
                                    break

                        if found_option:
                            opt_dict[np.linalg.norm(w_t)] = [w_t,b]

                if w[0] < 0:
                    optimized = True 
                    print('Optimized a step')
                else:
                    # w
                    w = w - step

            # todas las distancias
            norms = sorted([n for n in opt_dict])
            opt_choice = opt_dict[norms[0]]

            self.w = opt_choice[0]
            self.b = opt_choice[1]

            latest_optimum = opt_choice[0][0]+step * 2

        

    # Esta es la funcion para
    def predict(self, features):
        # sign (x.w+b)
        classification = np.sign(np.dot(np.array(features), self.w)+self.b)
        return classification



# Creamos un diccionario
data_dict = {-1:np.array([[1,6],
                        [2,8],
                        [3,8],]),
            1:np.array([[5,1],
                        [6, -1],
                        [7,3],])}