import numpy as numpy
import scipy
import json
import pickle

"""
[social] deals with implementing social data into the search
engine. 
"""

# given a search, we can find the socially related items to it
# For example, for

f = open("data/reddit_pose_data.json", "rb")
reddit_data = json.load(f)
f.close()

print(reddit_data)

f = open("data/description_yoga_json.json", "rb")
descriptions = json.load(f)
f.close()

print(descriptions)
