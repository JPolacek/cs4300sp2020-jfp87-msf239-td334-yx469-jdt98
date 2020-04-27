import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn.utils import resample
import pickle
from sklearn import preprocessing
sv = pd.read_csv("survey.csv")
ox = np.array(sv['fs'])
oy = np.array(sv['ss'])
index_list = ['abs', 'ankles', 'arms', 'back', 'belly', 'bladder', 'brain', 'chest','feet', 'hamstrings', 'hands', 'heart', 'hips', 'knees', 'legs', 'liver', 'lower back', 'lungs', 'neck', 'pelvis', 'shoulders', 'spine', 'thighs', 'thyroid']
le = preprocessing.LabelEncoder()
le.fit(index_list)

oox = pd.get_dummies(le.transform(ox))
ooy = le.transform(oy)

x = oox
y = ooy
print(x)

for i in range(10):
    x1,y1 = resample(oox,ooy,random_state=i)
    x = np.concatenate((x,x1))
    y = np.concatenate((y,y1))

x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1)

dt = DecisionTreeClassifier()
dt.fit(x_train,y_train)
y_pred = dt.predict(x_test)
species = np.array(y_test)
predictions = np.array(y_pred)

a = np.array(confusion_matrix(species, predictions))
sum_c = 0
lena = len(a)
for i in range(lena):
    sum_c += a[i][i]
accuracy = sum_c / np.sum(a)

pickle.dump(dt,open('model.sav','wb'))
