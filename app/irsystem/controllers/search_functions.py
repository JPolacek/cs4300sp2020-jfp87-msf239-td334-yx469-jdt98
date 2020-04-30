import json
import itertools
import re
from app.irsystem.controllers.cosine_search import *
from data.body_part_synonyms import synonyms

strip_set = lambda x : {ele.strip() for ele in x}

def clean_up(s):
	q_lower = s.lower()
	q_body_parts = re.split('and |, ', q_lower)
	while '' in q_body_parts:
		q_body_parts.remove('')
	
	return list(strip_set(q_body_parts))

def boolean_search(data, query):
	"""
	Given a query, return the stretches that work on each body part
	"""
	
	q_body_parts = clean_up(query)

	return_dict = {}

	for i in range(1, len(q_body_parts)+1):
		combos = list(itertools.combinations(q_body_parts, i))
		for combo in combos:
			combo_set = strip_set(set(combo))
			combo_string = ', '.join(combo_set)
			if combo_string in synonyms:
				combo_set = set(combo_set.union(synonyms[combo_string]))
			return_dict[combo_string] = []
			for stretch in data:
				c_body_parts = set(data[stretch]["body_part"])
				if len(set(combo_set).intersection(c_body_parts)) != 0:
					return_dict[combo_string].append((stretch, data[stretch]["url"], \
						data[stretch]["image_name"], ' '.join(data[stretch]["description"])))

	rm_dict = []
	for key in return_dict:
		return_dict[key] = sorted(return_dict[key])
		if return_dict[key] == []:
			rm_dict.append(key)
	
	for key in rm_dict:
		del return_dict[key]

	if len(return_dict) == 1:
		return boolean_cossim(return_dict)

	deduped_return_dict = {}
	for combo in list(itertools.combinations(return_dict, 2)):
		a = combo[0]
		b = combo[1]

		if a not in b and b not in a:
			continue
		
		a_pointer = 0
		last_a = len(return_dict[a])
		a_list = []

		b_pointer = 0
		last_b = len(return_dict[b])
		b_list = []

		while(a_pointer < last_a and b_pointer < last_b):
			a_val = return_dict[a][a_pointer]
			b_val = return_dict[b][b_pointer]

			if a_val[0] == b_val[0]:
				if a in b:
					b_list.append(b_val)
				else:
					a_list.append(a_val)
				a_pointer += 1
				b_pointer += 1
			elif a_val[0] < b_val[0]:
				a_list.append(a_val)
				a_pointer += 1
			elif b_val[0] < a_val[0]:
				b_pointer += 1

		if a in deduped_return_dict:
			temp = deduped_return_dict[a]
			deduped_return_dict[a] = list(set(temp + a_list))
		else:
			deduped_return_dict[a] = a_list
		
		if b in deduped_return_dict:
			temp = deduped_return_dict[b]
			deduped_return_dict[b] = list(set(temp + b_list))
		else:
			deduped_return_dict[b] = b_list

	for key in rm_dict:
		deduped_return_dict[key] = []
    
	return boolean_cossim(deduped_return_dict)