import numpy as numpy
import scipy
import json
import pickle
import copy

"""
[social] deals with implementing social data into the search
engine.
"""


REDDIT_DATA_PATH = "data/reddit_pose_data.json"


def social_sort(dictionary, top_n=5):
    """
    social_sort(dictionary, top_n=10) resorts the documents for each key in
    dictionary

    [dictionary] is a ranked dict of documents for each key

    The key is a four tuple: (stretch name, url, image, description string)
    """

    # get reddit data dictionary
    f = open(REDDIT_DATA_PATH, "rb")
    reddit_data_dict = json.load(f)
    f.close()

    ranked_dict = dict()
    for key in dictionary:
        document_list = dictionary[key]
        len_list = len(document_list)

        # split list into portion to sort and portion not to sort
        to_sort_list = document_list
        not_sort_list = []
        if len_list >= top_n:
            to_sort_list = document_list[:top_n]
            not_sort_list = document_list[top_n:]

        # sort the top_n documents by their reddit popularity
        sorted_list = sorted(
            to_sort_list,
            key=lambda tup: reddit_data_dict[tup[0]],
            reverse=True)

        # rejoin lists
        full_list = sorted_list + not_sort_list

        #limit to 10 search results per pose
        full_list = full_list[:10]
 
        ranked_dict[key] = full_list

    return ranked_dict
