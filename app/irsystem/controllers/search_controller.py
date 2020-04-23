from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import itertools
import json
import re
# import search_functions as sf

project_name = "Stretches: Find a stretch to help your pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"

def boolean_search(query):
	"""
	Given a query, return the stretches that work on each body part
	"""
	strip_set = lambda x : {ele.strip() for ele in x}
	q_lower = query.lower()
	q_body_parts = re.split('and |, ', q_lower)
	while '' in q_body_parts:
		q_body_parts.remove('')

	return_dict = {}

	with open('data/yogajournal.json') as f:
		data = json.load(f)

	for i in range(1, len(q_body_parts)+1):
		combos = list(itertools.combinations(q_body_parts, i))
		for combo in combos:
			combo_set = strip_set(set(combo))
			combo_string = ', '.join(combo_set)
			return_dict[combo_string] = []
			for stretch in data:
				c_body_parts = set(data[stretch]["body_part"])
				if set(combo_set).issubset(c_body_parts):
					return_dict[combo_string].append(stretch)

	rm_dict = []
	for key in return_dict:
		return_dict[key] = sorted(return_dict[key])
		if return_dict[key] == []:
			rm_dict.append(key)
	
	for key in rm_dict:
		del return_dict[key]

	rd = {}
	for bp in return_dict:
		rd[bp] = []
		for i, s in enumerate(return_dict[bp]):
			tup = (s, data[s]["url"])
			rd[bp].append(tup)

	print("rd: " + str(rd))

	if len(rd) == 1:
		return rd

	deduped_return_dict = {}
	for combo in list(itertools.combinations(rd, 2)):
		a = combo[0]
		b = combo[1]

		if a not in b and b not in a:
			continue
		
		a_pointer = 0
		last_a = len(rd[a])
		a_list = []

		b_pointer = 0
		last_b = len(rd[b])
		b_list = []

		while(a_pointer < last_a and b_pointer < last_b):
			a_val = return_dict[a][a_pointer]
			b_val = return_dict[b][b_pointer]

			if a_val == b_val:
				if a in b:
					b_list.append(b_val)
				else:
					a_list.append(a_val)
				a_pointer += 1
				b_pointer += 1
			elif a_val < b_val:
				a_list.append(a_val)
				a_pointer += 1
			elif b_val < a_val:
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
	
	return deduped_return_dict

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	bs = {}
	if query:
		bs = boolean_search(query)

	no_result_text = ''

	keys_to_remove = [key for key in bs if bs[key] == []]

	for key in keys_to_remove:
		no_result_text = 'There are no results for ' + query + ' :('
		del bs[key]		

	if len(bs) == 0:
		data = [""]
		output_message = no_result_text
	else:
		output_message = "Your search: " + query
		data = bs
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



