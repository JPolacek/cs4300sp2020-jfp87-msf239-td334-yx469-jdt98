import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import json

start_letter = ord("A")
end_letter = ord("Z")
letters = [chr(n) for n in range(start_letter, end_letter + 1)]

numbers = [n for n in range(100)]

header = "Stretches for the "
header_len = len(header)

major_muscles_stretched = "The major muscles being stretched."

stretch_df = pd.read_csv("Ultimate-Guide-to-Stretching-Flexibility-converted.csv")

nrow, ncol = stretch_df.shape

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

exercise_dict = dict()
major_muscles_dict = dict()

header_to_alpha = dict()
alpha_to_header = dict()
### initialize headers ###
start_alpha = start_letter
for i in range(nrow):
    original_row = stretch_df.iloc[i]
    first_row = original_row[0]
    row = str(first_row)
    if header in row[0: header_len]:
        header_to_alpha[row] = chr(start_alpha)
        alpha_to_header[chr(start_alpha)] = row
        
        start_alpha += 1
        

for i in range(nrow):
    original_row = stretch_df.iloc[i]
    first_row = original_row[0]
    row = str(first_row)

    if type(row) == str and row[0] in letters and is_int(row[1 : 3]) and int(row[1 : 3]) in numbers:
        first_letter = row[0]
        exercise_dict[first_letter].append(row)

    elif header in row[0: header_len]:
        exercise_dict[header_to_alpha[row]] = []

### I am going to try to extract out the body parts that are targeted

def flatten(lst):
    collector = []
    if type(lst) != list:
        collector.append(lst)
        return collector
    else:
        for elt in lst:
            collector += flatten(elt)
        return collector

punctuation = [".", ",", ":", ";"]
spaces = ["\n", "\t", " ", ""]

def remove_punct(s):
    if "." in s:
        first = s.split(".")[0]
        return first
    else:
        return s

header_names = []
muscle_names = []
sport_names = []
next_rows = []
exists_muscle = True
exists_sport = True
for i in range(nrow):
    original_row = stretch_df.iloc[i]
    row = str(original_row[0])
    if header in row[0: header_len]: 
        header_name = row[header_len : ]
        header_names.append(header_name)
        
        if (not exists_muscle):
            muscle_names.append([])
        if (not exists_sport):
            sport_names.append([])
            
        
        next_rows = [(i + 1), (i + 2), (i + 3)]
        
        exists_muscle = False
        exists_sport = False
    if i in next_rows:
        if "The major muscles being stretched." in row:
            split_muscles = row.split("stretched.")
            # print(split_muscles[1].split())
            muscles = re.findall('[A-Z][^A-Z]*', split_muscles[1])
            #https://www.w3resource.com/python-exercises/re/python-re-exercise-43.php
            # to split at upper case only
            muscles = list(map(lambda s : s.strip(), muscles))
            muscles = list(map(lambda s : s.lower(), muscles))
            # print(muscles)
            muscle_names.append(muscles)
            exists_muscle = True
        # else:
        #     muscle_names.append([])
        if "Sports  that  benefit  from  these" in row:
            include_row = row.split("include")[1]
            split_row = include_row.split(";")[1:]
            # print(split_row)
            further_split = [s.split("and") for s in split_row]
            
            
            # print(flatten(further_split))
            sports = flatten(further_split)
            sports_cleaned = [s.strip() for s in sports]
            # print(sports_cleaned)
            
            sports_cleaned_2 = flatten([s.split(",") for s in sports])
            sports_cleaned_3 = [s.strip() for s in sports_cleaned_2]
            sports_cleaned_4 = []
            for s in sports_cleaned_3:
                if "like" in s:
                    after = s.split("like")
                    sports_cleaned_4.append(after)
                else:
                    sports_cleaned_4.append(s)
                    
            sports_cleaned_5 = flatten(sports_cleaned_4)
            sports_final = list(filter(lambda s : s not in punctuation, sports_cleaned_5))
            sports_final = list(map(lambda s : s.lower(), sports_final))
            sports_final = list(map(lambda s : s.strip(), sports_final))
            sports_final = list(filter(lambda s : s not in spaces, sports_final))
            sports_final = list(map(lambda s : remove_punct(s), sports_final))
            # print(sports_final)
            sport_names.append(sports_final)
            
            exists_sport = True
            
        # else:
        #     sport_names.append([])
        
            # print(row)
        # print("&" *12)
        # print(row)
        # print("!" *12)
        

named_dict = {}
i = 0
for key in exercise_dict:
    named_dict[header_names[i]] = {"description" : exercise_dict[key], "muscles" : muscle_names[i], "sports" : sport_names[i]}
    i += 1
        

# f = open("exercise.json", "w")
# json.dump(named_dict, f)
# f.close()

        
        
# distr = [len(exercise_dict[key]) for key in exercise_dict]
# 
# 
# 
# objects = [key for key in header_to_alpha]
# objects = list(map(lambda s : s.split("Stretches for the ")[1], objects))
# y_pos = np.arange(len(objects))
# 
# plt.bar(y_pos, distr, align='center', alpha=0.5)
# plt.xticks(y_pos, objects, rotation = 30)
# plt.xlabel('Data Label Amount')
# plt.title('Targeted Area vs Number of Stretches')
# 
# plt.show()

    
