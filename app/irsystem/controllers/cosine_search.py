import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
from sklearn.decomposition import TruncatedSVD
import pickle

c_SPACE = " "


def get_sim(query, input_doc_mat):
    """Returns an np.array of ints representing the argsort
    for cossine similarity scores between
    all the documents in [input_doc_mat] and the [query]

    Params: {query: np.array,
             input_doc_mat: Numpy Array}
    Returns: np.array of ints
    """
    (nrows, _) = np.shape(input_doc_mat)
    scores = np.zeros((nrows))
    for key in range(nrows):
        stretch_row = input_doc_mat[key, :].flatten()
        cossim = np.dot(stretch_row, query)
        scores[key] = cossim
    score_pos = [(idx, score) for idx, score in enumerate(scores)]
    position_sort = sorted(score_pos, key=lambda tup: tup[1], reverse=True)
    return position_sort


def yoga_json_to_arr(yoga_json_path):
    with open(yoga_json_path) as f:
        j = json.load(f)
        f.close()


def stretch_json_to_list(stretch_json_path):
    document_list = []
    with open(stretch_json_path) as f:
        stretches = json.load(f)
        for stretch in stretches:
            stretch_dict = stretches[stretch]
            for exercise in stretch_dict["description"]:
                # for exercise in stretch_dict[description]:
                document_list.append(exercise)
        f.close()
    return document_list


def description_yoga_to_list(description_json_path):
    document_list = []
    with open(description_json_path) as f:
        stretches = json.load(f)
        for stretch in stretches:
            stretch_dict = stretches[stretch]
            exercise = stretch_dict["description"]
            joined_exercise = " ".join(exercise)
            document_list.append(joined_exercise)
        f.close()
    return document_list


def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=2, norm='l2', ngram_range=(1, 2)):
    """Returns a TfidfVectorizer object with the above preprocessing properties.

    Note: This function may log a deprecation warning. This is normal, and you
    can simply ignore it.

    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String
             ngram_range : Tuple of range of n-grams}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(max_features=max_features, stop_words=stop_words, max_df=max_df, min_df=min_df, norm=norm, ngram_range=ngram_range)


def body_description_cossim(body_part, description):
    """
    body_description_cossim finds the cosine similarity between the body part and
    description

    Requires: Description is in the file pointed to by
    ["../../../data/description_yoga_json.json"]
    """

    file_stretch_list = open(
        "data/stretch_descriptions_list", "rb")
    stretch_list = pickle.load(file_stretch_list)

    file_tf_idf_vectorizer = open("data/tf_idf_vectorizer", "rb")
    tfidf_vec = pickle.load(file_tf_idf_vectorizer)

    file_tf_idf_matrix = open("data/tf_idf_matrix", "rb")
    stretches_tf_idf = pickle.load(file_tf_idf_matrix)

    file_doc_to_index = open("data/doc_to_index", "rb")
    doc_to_index = pickle.load(file_doc_to_index)

    # turn body part into tf-idf weighting
    body_fit = tfidf_vec.transform([body_part]).toarray()

    # index of where the description lies in the TF_IDF array
    description_idx = doc_to_index[description]

    # get tf-idf weightins for descritpion
    description_fit = stretches_tf_idf[description_idx, :]

    # Cosine similarity between body and descritipion
    cossim = np.dot(body_fit, description_fit)
    return cossim


# print(body_description_cossim("knees",
#                               "Kneel face down with your knees and toes facing out. Lean forward and let your knees move outwards."))


def boolean_cossim(dictionary):
    """
    [boolean_cossim(dictionary)] is the ranking using cosine similarity
    for all the returned documents in the dictionary
    """
    ranked_dict = dict()
    for key in dictionary:
        document_list = dictionary[key]
        sorted_documents = sorted(
            document_list,
            key=lambda tup: body_description_cossim(key, tup[-1]),
            reverse=True)
        ranked_dict[key] = sorted_documents
    return ranked_dict


def free_form_search(query):
    """
    Free form search in progress
    Uses SVD to get latent semantic analysis
    Uses bigrams and so on to match longer pairs and triples of words that are coupled together
    Gives ranking at end of query on all documents
    """
    # stretch_list = stretch_json_to_list("../../../DataProcessing/exercise.json")
    stretch_list = description_yoga_to_list(
        "../../../data/description_yoga_json.json")
    n_feats = 5000
    stretches_tf_idf = np.empty([len(stretch_list), n_feats])  # alloc memory
    tfidf_vec = build_vectorizer(n_feats, "english")
    stretches_tf_idf = tfidf_vec.fit_transform(
        [d for d in stretch_list]).toarray()
    # index_to_vocab = {i: v for i, v in enumerate(tfidf_vec.get_feature_names())}
    # processor = tfidf_vec.build_preprocessor()

    svd = TruncatedSVD(n_components=100, n_iter=7, random_state=42)
    svd_stretches_tf_idf = svd.fit_transform(stretches_tf_idf)

    query = ["pain in lower back pins and needles"]

    transformed_query = tfidf_vec.transform(query).toarray()
    query_fit = svd.transform(transformed_query).transpose()
    rank = get_sim(query_fit, svd_stretches_tf_idf)
    print("Query is : " + query[0])
    print("Top 10 Ranking !!!")
    for idx, sim in rank[:10]:
        print(stretch_list[idx])
        print(sim)
        print("#"*10)


def pickle_data():
    """
    UTILITY FUNCTION
    Pickles the data for easy accessibility and so that no recomputation is needed

    WARNING
    REQUIRES: Call picke_data() every single time the data set is updated!!!!
    """
    stretch_list = description_yoga_to_list(
        "../../../data/description_yoga_json.json")

    n_feats = 5000
    stretches_tf_idf = np.empty([len(stretch_list), n_feats])  # alloc memory
    tfidf_vec = build_vectorizer(n_feats, "english")  # TF-IDF vectorizer

    stretches_tf_idf = tfidf_vec.fit_transform(
        [d for d in stretch_list]).toarray()  # TF-IDF matrix

    # mapping of document description to the row it occupied in the TF_IDF_Matrix
    doc_to_index = {d: i for i, d in enumerate(stretch_list)}

    file_stretch_list = open(
        "../../../data/stretch_descriptions_list", "wb")
    pickle.dump(stretch_list, file_stretch_list)

    file_tf_idf_vectorizer = open("../../../data/tf_idf_vectorizer", "wb")
    pickle.dump(tfidf_vec, file_tf_idf_vectorizer)

    file_tf_idf_matrix = open("../../../data/tf_idf_matrix", "wb")
    pickle.dump(stretches_tf_idf, file_tf_idf_matrix)

    file_doc_to_index = open("../../../data/doc_to_index", "wb")
    pickle.dump(doc_to_index, file_doc_to_index)


# pickle_data()
