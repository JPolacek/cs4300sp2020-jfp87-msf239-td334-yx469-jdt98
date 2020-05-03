import pickle
from sklearn import preprocessing
import numpy as np


BODY_PARTS = ['abs', 'ankles', 'arms', 'back', 'belly', 'bladder', 'brain', 'chest', 'feet', 'hamstrings', 'hands', 'heart',
              'hips', 'knees', 'legs', 'liver', 'lower back', 'lungs', 'neck', 'pelvis', 'shoulders', 'spine', 'thighs', 'thyroid']


def get_recom(userinput):
    result = []
    loadmodel = pickle.load(open('ml/model.sav', 'rb'))
    index_list = ['abs', 'ankles', 'arms', 'back', 'belly', 'bladder', 'brain', 'chest', 'feet', 'hamstrings', 'hands', 'heart',
                  'hips', 'knees', 'legs', 'liver', 'lower back', 'lungs', 'neck', 'pelvis', 'shoulders', 'spine', 'thighs', 'thyroid']
    le = preprocessing.LabelEncoder()
    le.fit(index_list)
    for i in userinput:
        numinput = le.transform([i])
        vinput = np.zeros(len(index_list)-1)
        vinput[numinput] = 1
        result.append(loadmodel.predict([vinput])[0])

    return result

# Put user's previous input in this function, it would return the recommendation which this user would also like to search.


def get_related_body_parts(user_input_lst, n_recs=5):
    """
    get_routine(user_input, n_recs) gives up to n different recommendations 
    given an initial user input for a stretch

    [user_input_lst]  is a list user_inputs, all must be body parts in BODY_PARTS

    Returns: [List] of at most n different recommendations , at least one different 
    recommendation

    Requires: n_recs >= 1
    """
    recs = set()
    num_body_parts = len(user_input_lst)
    for user_input in user_input_lst:
        user_input = user_input.lower().strip()
        if user_input in BODY_PARTS:
            _input = [user_input]
            for _ in range(n_recs//num_body_parts):
                recommendation_lst = get_recom(_input)
                _input = recommendation_lst
                recs.add(recommendation_lst[0])

    recs = list(recs)
    if len(recs) > n_recs:
        recs = recs[:n_recs]
    return recs


# print(get_routine(["arms", "legs"], n_recs=5))
