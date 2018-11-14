import csv, numpy, sys

from sklearn.neighbors import LocalOutlierFactor

training_data = numpy.genfromtxt(sys.argv[1], delimiter=',')

target = numpy.genfromtxt(sys.argv[2], delimiter=',')

target = numpy.reshape(target, (-1,3))

data_array = numpy.r_[training_data, target]



#Fit the model

lof_model = LocalOutlierFactor(n_neighbors=1)
prediction = lof_model.fit_predict(data_array)
prediction_target = prediction[100:]


print(prediction_target)
