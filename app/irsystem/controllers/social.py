import numpy as numpy
import scipy
import json
import pickle
import copy
from pytrends.request import TrendReq

"""
[social] deals with implementing social data into the search
engine.
"""


REDDIT_DATA_PATH = "data/reddit_pose_data.json"

# get reddit data dictionary
f = open(REDDIT_DATA_PATH, "rb")
reddit_data_dict = json.load(f)
f.close()

# initial pytrend for Google Trends
pytrend = TrendReq()


def social_sort(dictionary, top_n=5):
    """
    social_sort(dictionary, top_n=10) resorts the documents for each key in
    dictionary

    [dictionary] is a ranked dict of documents for each key

    The key is a four tuple: (stretch name, url, image, description string)
    """

    # get reddit data dictionary
    # f = open(REDDIT_DATA_PATH, "rb")
    # reddit_data_dict = json.load(f)
    # f.close()

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
        
        # gather the trending info (i.e. how often it's mentioned) from Google Trends
        kw_list = [stretch[0] for stretch in to_sort_list]
        try:
            pytrend.build_payload(kw_list=kw_list)
            df = pytrend.interest_over_time()
            df_sum = df.sum()
            trending_dict = {stretch : df_sum.get(stretch) for stretch in kw_list}
            sorted_trending = {s[0] : s[1] for s in 
                sorted(trending_dict.items(), key=lambda x:x[1], reverse=True)}
        except:
            sorted_trending = {stretch : 0 for stretch in kw_list}

        # sort the top_n documents by their reddit popularity
        sorted_list = sorted(
            to_sort_list,
            key=lambda tup: reddit_data_dict[tup[0]] + sorted_trending[tup[0]],
            reverse=True)

        # rejoin lists
        full_list = sorted_list + not_sort_list

        # limit to 10 search results per pose
        full_list = full_list[:10]

        ranked_dict[key] = full_list

    return ranked_dict
