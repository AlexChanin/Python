#Description: This program classifies patients as having chronic kidney disease (ckd) or not.
#             Using Artificial Neural Networks

#Resources: (1) Data set information : https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease
#           (2) Kaggle : https://www.kaggle.com/vijaygill/chronic-kidney-disease-prediction-using-keras/data

'''
Data Set Information:

age	-	age	
bp	-	blood pressure 
sg	-	specific gravity 
al	- albumin 
su	-	sugar 
rbc	-	red blood cells 
pc	-	pus cell 
pcc	-	pus cell clumps 
ba	-	bacteria 
bgr	-	blood glucose random 
bu	-	blood urea 
sc	-	serum creatinine 
sod	-	sodium 
pot	-	potassium 
hemo	-	hemoglobin 
pcv	-	packed cell volume 
wc	-	white blood cell count 
rc	-	red blood cell count 
htn	-	hypertension 
dm	-	diabetes mellitus 
cad	-	coronary artery disease 
appet	-	appetite 
pe	-	pedal edema 
ane	-	anemia 
class	-	classification

'''

#Import Libraries
import glob
from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import keras as k
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt

#load the data 
    from google.colab import files #Only use for Google Colab
    uploaded = files.upload()      #Only use for Google Colab
    df = pd.read_csv("kidney_disease.csv")
    
    #Print the first 5 rows
    df.head()

#Get the shape of the data (the number of rows & columns)
df.shape

#Create a list of columns to retain
columns_to_retain = ["sg", "al", "sc", "hemo",
                         "pcv", "wbcc", "rbcc", "htn", "classification"]

#columns_to_retain = df.columns, Drop the columns that are not in columns_to_retain
df = df.drop([col for col in df.columns if not col in columns_to_retain], axis=1)
    
# Drop the rows with na or missing values
df = df.dropna(axis=0)

#Transform non-numeric columns into numerical columns
for column in df.columns:
        if df[column].dtype == np.number:
            continue
        df[column] = LabelEncoder().fit_transform(df[column])

#Print / show the first 5 rows of the new cleaned data set
df.head()

#Split the data into independent'X'(the features) and dependent 'y' variables (the target)
X = df.drop(["classification"], axis=1)
y = df["classification"]

#Feature Scaling
#the min-max scaler method scales the dataset so that all the input features lie between 0 and 1 inclusive
x_scaler = MinMaxScaler()
x_scaler.fit(X)
column_names = X.columns
X[column_names] = x_scaler.transform(X)

#Split the data into 80% training and 20% testing & Shuffle the data before splitting
X_train,  X_test, y_train, y_test = train_test_split(
        X, y, test_size= 0.2, shuffle=True)

#Build The model
#  The models input shape/dimensions is the number of features/columns in the data set
#  The model will have 2 layers:
#      (i) The first with 256 neurons and the ReLu activation function & a initializer which 
#          defines the way to set the initial random weights of the Keras layers. 
#          We'll use a initializer that generates tensors with a normal distribution.
#     (ii) The other layer will have 1 neuron with the activation function 'hard_sigmoid'
model = Sequential()
model.add(Dense(256, input_dim=len(X.columns),
                    kernel_initializer=k.initializers.random_normal(seed=13), activation="relu"))
model.add(Dense(1, activation="hard_sigmoid"))

#Compile the model
# Loss measuers how well the model did on training , and then tries to improve on it using the optimizer.
# The loss function we will use is binary_crossentropy for binary (2) classes.
model.compile(loss='binary_crossentropy', 
                  optimizer='adam', metrics=['accuracy'])

#Train the model
history = model.fit(X_train, y_train, 
                    epochs=2000, #The number of iterations over the entire dataset to train on
                    batch_size=X_train.shape[0]) #The number of samples per gradient update for training

#Save the model
model.save("ckd.model")

#Visualize the models accuracy and loss
plt.plot(history.history["acc"])
plt.plot(history.history["loss"])
plt.title("model accuracy & loss")
plt.ylabel("accuracy and loss")
plt.xlabel("epoch")
plt.legend()
#plt.grid(which="both")
#plt.savefig("ckd.png")

print("-------------------------------------------------------------------")
print("Shape of training data: ", X_train.shape)
print("Shape of test data    : ", X_test.shape )
print("-------------------------------------------------------------------")

for model_file in glob.glob("*.model"):
  print("Model file: ", model_file)
  model = load_model(model_file)
  pred = model.predict(X_test)
  pred = [1 if y>=0.5 else 0 for y in pred] #Threshold, transforming probabilities to either 0 or 1 depending if the probability is below or above 0.5
  scores = model.evaluate(X_test, y_test)
  print("Original  : {0}".format(", ".join([str(x) for x in y_test])))
  print("Predicted : {0}".format(", ".join([str(x) for x in pred])))
  print("Scores    : loss = ", scores[0], " acc = ", scores[1])
  print("-------------------------------------------------------------------")
  print() #Print Space
