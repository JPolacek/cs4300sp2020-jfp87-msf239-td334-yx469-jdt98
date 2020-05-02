import numpy as np
import pickle
import copy
from collections import Counter
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse

# This module implements a simple rocchio that takes in user input
# and helps update the rankings

# Should we access informatiomn from a database using postgresQL to help
# rocchio, or do we just pickle data?
# Rocchio needs a dynamic memory store
# Currently, I call it a database, but it could be a dictionary that we load and tore
# a SQL database, etc, anything that can be queried fast and reliablys


def add_relevant(database, boolean_query, pose_name):
    """
    add_relevant(database, boolean_query,pose_name) adds the contents of the entire document to
    the database if it is relevant to the boolean_query.

    Example: user finds D1 : "extend arm up and down..." relevant to the boolean_query "neck and back".
    Calling add_relevant will add this pose_name D1 as relevant to the boolean_query

    Boolean_query is a [string], pose_name is the name of the pose, e.g. "Crow Pose
    You can choose to truncate document if needed for speed, trading off relevance

    WARNING: Once a recommendation is given, it is permanent, and cannot be removed
    from the reelvant list

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    database['relevant'][boolean_query] += pose_name


def add_irrelevant(database, boolean_query, pose_name):
    """
    add_irrelevant(database, boolean_query, pose_name) adds the contents of the entire document to
    the database if it is irrelevant to the boolean_query.

    Example: user finds D1 : "swing feet left and right..." irrelevant to the boolean_query "neck and back".
    Calling add_irrelevant will add this pose_name D1 as irrelevant to the boolean_query

    Boolean_query is a [string], pose_name a possibly very loing [string]
    You can choose to truncate document if needed for speed, trading off irrelevance

    WARNING: Once a recommendation is given, it is permanent, and cannot be removed
    from the irrelvant list

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    database['irrelevant'][boolean_query] += pose_name


def clear_database(database):
    """
    clear_database(database) clears all relevant adn irrelevant fields in the database.

    Example: User has given misleading or faulty data on relevance and irrelevance.
    Use clear_database to clear out all rankings to restart without rocchio.

    WARNING: Once a database is cleared, the action is irreversible and data
    is lost permanently

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    database['relevant'] = dict()
    database['irrelevant'] = dict()


def init_database():
    """
    init_database() creates a new data base with empty dictionaries
    for the relevant and irrelevant fields.

    Returns: [dictionary] of data base with empty irrelevant and relevant fields
    """
    database = dict()
    database['relevant'] = dict()
    database['irrelevant'] = dict()
    return database


def rocchio(database, boolean_query, cosine_query):
    """
    rocchio(database, boolean_query, cosine_query) takes in the boolean query
    the cosine query and the irrelevant and relevant docus in the database
    and updates the cosine query.

    Boolean_query is a [string]
    Cosine_query is a [string]
    Database is a [dictionary]

    Returns: [string] of the rocchio updated cosine query

    Requires: Cosine similarity MUST be used after this: This query correction
    does not fix up for cosine similarity or tf-idf, so you cannot assume Cosine
    similarity is done at the same time or before rocchio()

    Warning: SIMPLE TOKENIZER used: I use split() as a tokenizer
    """
    relevant = []
    if boolean_query in database['relevant']:
        relevant = database['relevant'][boolean_query]
    irrelevant = []
    if boolean_query in database['irrelevant']:
        irrelevant = database['irrelevant'][boolean_query]
    tokenized_cosine_query = cosine_query.split()
    return simple_rocchio_helper(tokenized_cosine_query, relevant, irrelevant)


def simple_rocchio_helper(cosine_query, relevant, irrelevant):
    """Returns a string representing the modified cosine query.

    [DEPRECATED]

    WARNING: assumes that the relevant and irrelevant documents were tokenized

    Simplified rocchio without need for tokenizing beforehand;
    Literally on adds terms and deletes terms to the query

    Note:
        If the `clip` parameter is set to True, the resulting vector should have
        no negatve weights in it!

        Handles the cases where relevant and irrelevant are empty lists by avoiding division by 0

    Params: {cosine_query: tokenized string of what will go to the cosine similarity as a quert,
             relevant: List of List of tokens that are relevant
             irrelevant: List of List of tokens that are irrelevant

    Returns: String [in some random, undefined order]
    """

    print("WARNING: DEPRECATED")

    rel_multi_set = Counter()
    for doc in relevant:
        rel_multi_set += Counter(doc)

    irrel_multi_set = Counter()
    for doc in irrelevant:
        irrel_multi_set += Counter(doc)

    query = Counter(cosine_query)

    final_multi_set = query + rel_multi_set - irrel_multi_set
    rocchio_query = " ".join(final_multi_set)

    return rocchio_query


def rocchio_helper(query, relevant, irrelevant, a=.3, b=.3, c=.8, clip=True):
        """Returns a vector representing the modified query vector.

    Note:
        If the `clip` parameter is set to True, the resulting vector should have
        no negatve weights in it!

        Also, be sure to handle the cases where relevant and irrelevant are empty lists.

    Params: {query: String (the name of the movie being queried for),
             relevant: List (the names of relevant movies for query),
             irrelevant: List (the names of irrelevant movies for query),
             input_doc_matrix: Numpy Array Uses tf_idf_matrix,
             indexer: Dict: uses  pose_name_to_index,
             a,b,c: floats (weighting of the original query, relevant queries,
                             and irrelevant queries, respectively),
             clip: Boolean (whether or not to clip all returned negative values to 0)}
    Returns: Numpy Array
    """

    # get tf-idf matrix
    f = open("data/tf_idf_matrix", "rb")
    tf_idf_matrix = pickle.load(f)
    f.close()

    # get pose_name_to_index_dictionary
    f = open("data/pose_name_to_index", "rb")
    pose_name_to_index = pickle.load(f)
    f.close()

    # get tf-idf trained tokenizer to tokenize the query
    f = open("data/tf_idf_vectorizer", "rb")
    tf_idf_vectorizer = pickle.load(f)
    f.close()

    l_relevant = len(relevant)
    l_relevant = l_relevant if l_relevant > 0 else 1  # handle no relevant docs

    l_irrelevant = len(irrelevant)
    l_irrelevant = l_irrelevant if l_irrelevant > 0 else 1  # handle no irrelevant docs

    # get number of columns in tf_idf_matrix
    l_vector = np.shape(tf_idf_matrix)[1]

    sum_relevant = np.zeros((l_vector))

    for pose_name in relevant:
        idx = pose_name_to_index[pose_name]
        # update sum_relevant by adding two vectors together
        sum_relevant += tf_idf_matrix[idx, :]

    sum_irrelevant = np.zeros((l_vector))

    for pose_name in irrelevant:
        idx = pose_name_to_index[pose_name]
        sum_irrelevant += tf_idf_matrix[idx, :]

    # transformed query to tf-idf weightings corresponding
    # to training data (yoga description data set)
    # it's possible for q0 to be all 0s
    q0 = tf_idf_vectorizer.transform([query]).toarray()

    rocchio = a * q0 + b * 1/l_relevant * \
        sum_relevant - c * 1/l_irrelevant * sum_irrelevant

    if clip:
        rocchio = np.array([x if x > 0 else 0 for x in rocchio])

    return rocchio


############ UTILITIES ##########


def pickle_pose_name():
    """
    Creates a dictionary mapping pose name to the row index that the pose occupied 
    in the TF-IDF-Matrix

    Stores the pickled dictionary in ../../../data/pose_name_to_index, in the data
    directory

    Example pickled output: Dictionary where Crow Pose : Row 4 in TF-IDF Matrix

    Returns NONE:

    WARNING!!!
    REQUIRES: Call pickle_pose_name() every single time the data set is updated!!!!
    """
    f = open("../../../data/description_yoga_json.json", "r")
    documents = json.load(f)
    f.close()
    pose_name_to_index = {name: i for i, name in enumerate(documents)}

    file_doc_to_index = open("../../../data/pose_name_to_index", "wb")
    pickle.dump(pose_name_to_index, file_doc_to_index)


# LEAVE UNCOMMENTED! IF THE DATA SET CHANGES IN ANY WAY, UNCOMMENT AND CALL
# pickle_pose_name()
