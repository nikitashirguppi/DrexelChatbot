file_name = "gac_data_combined.csv"
out_name = "trained_model.m5"
num_of_gas = 20 
max_question_length = 25 #used to be 100
top_words = 5000
filt = '.?"\/!,<>@#$%^&*_-+=|}{][:;~`'
embedding_vector_length = 64
percent_test = 0.01
#Note: It is very important that the above values be set in the same way for
#      both this script and the gac class file.


import csv
import math
import numpy
numpy.random.seed(0)

from zlib import adler32
from keras.preprocessing import text
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers import LSTM
from keras.layers import Dense

def my_hash(item):
    to_hash = item.replace("'", " ")
    for c in filt:
        to_hash = to_hash.replace(c, "")

    final = []
    words = to_hash.lower().split(" ")
    for word in words:
        final.append(adler32(word.encode()) % top_words)
    return final

try:
    csvfile = open(file_name, newline='')
except OSError:
    print("Error opening file")
    exit()

x = []
y = []
reader = csv.reader(csvfile)
next(reader) #Throw out the first line
try:
    for record in reader:
        if record[4] == "yes" or record[3] == '0': #Only train on in scope things. (out of scope errors are okay)
            x.append(my_hash(record[2]))
            temp = [0] * num_of_gas
            temp[int(record[3])] = 1
            y.append(temp)
except ValueError:
    print("Error: malformed data")
    exit()

csvfile.close()

x = sequence.pad_sequences(x, maxlen=max_question_length)

split_point = math.floor(len(x) * percent_test)
x_test = numpy.array(x[:split_point])
x_train = numpy.array(x[split_point:])
y_test = numpy.array(y[:split_point])
y_train = numpy.array(y[split_point:])

model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_question_length))
model.add(LSTM(50)) #this was 100...
model.add(Dense(num_of_gas, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
print(model.summary())

model.fit(x_train, y_train, validation_data=(x_test, y_test), nb_epoch=16, batch_size=64)

scores = model.evaluate(x_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

try:
    model.save(out_name) #apparently saving a model requires some package that is not installable on windows
except ImportError:
    print("Failed to save model, missing required libraries.")
input("Press enter to exit...")
