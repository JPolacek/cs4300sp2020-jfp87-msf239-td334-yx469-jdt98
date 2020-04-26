import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse
from sklearn.decomposition import TruncatedSVD

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
