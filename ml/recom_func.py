import pickle
from sklearn import preprocessing
import numpy as np

def get_recom(userinput):
    result = []
    loadmodel = pickle.load(open('model.sav', 'rb'))
    index_list = ['abs', 'ankles', 'arms', 'back', 'belly', 'bladder', 'brain', 'chest','feet', 'hamstrings', 'hands', 'heart', 'hips', 'knees', 'legs', 'liver', 'lower back', 'lungs', 'neck', 'pelvis', 'shoulders', 'spine', 'thighs', 'thyroid']
    le = preprocessing.LabelEncoder()
    le.fit(index_list)
    for i in userinput:
        numinput = le.transform([i])
        vinput = np.zeros(len(index_list)-1)
        vinput[numinput] = 1
        result.append(loadmodel.predict([vinput])[0])

    return result



#Put user's previous input in this function, it would return the recommendation which this user would also like to search.
