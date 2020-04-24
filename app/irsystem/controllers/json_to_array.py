import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer


c_SPACE = " "


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

# TODO: collect all the unique words in the documents
# TODO: make an array with number of documents as rows, and columns as words


def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=2, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.

    Note: This function may log a deprecation warning. This is normal, and you
    can simply ignore it.

    Params: {max_features: Integer,
             max_df: Float,
             min_df: Float,
             norm: String,
             stop_words: String}
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(max_features=max_features, stop_words=stop_words, max_df=max_df, min_df=min_df, norm=norm)


stretch_list = stretch_json_to_list("../../../DataProcessing/exercise.json")
n_feats = 5000
stretches_tf_idf = np.empty([len(stretch_list), n_feats])  # alloc memory
tfidf_vec = build_vectorizer(n_feats, "english")
stretches_tf_idf = tfidf_vec.fit_transform(
    [d for d in stretch_list]).toarray()
index_to_vocab = {i: v for i, v in enumerate(tfidf_vec.get_feature_names())}
processor = tfidf_vec.build_preprocessor()
tokenizer = tfidf_vec.build_tokenizer()
query = tokenizer(processor("stretch my leg and my head"))
query_fit = tfidf_vec.transform(query)
