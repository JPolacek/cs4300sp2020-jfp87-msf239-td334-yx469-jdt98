from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import itertools
import json
# import search_functions as sf

project_name = "Stretches: Find a stretch to help you pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"

def boolean_search(query):
    """
    Given a query, return the stretches that work on each body part
    """
    q_lower = query.lower()
    q_body_parts = q_lower.split(' and ')
    return_dict = {}

    with open('data/yogajournal.json') as f:
        data = json.load(f)

    for i in range(1, len(q_body_parts)+1):
        combos = list(itertools.combinations(q_body_parts, i))
        for combo in combos:
            combo_set = set(combo)
            combo_string = ', '.join(combo_set)
            return_dict[combo_string] = []
            for stretch in data:
                c_body_parts = set(data[stretch]["body_part"])
                if set(combo_set).issubset(c_body_parts):
                    return_dict[combo_string].append(stretch)
    
    if len(return_dict) == 1:
        return return_dict

    for key in return_dict:
        return_dict[key] = sorted(return_dict[key])
    
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

    return deduped_return_dict

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')

	bs = {}
	if query:
		bs = boolean_search(query)

	no_stretches = True
	for stretch in bs:
		if bs[stretch] != []:
			no_stretches = False
			continue

	if no_stretches:
		data = [""]
		output_message = 'There are no results for this position :('
	else:
		output_message = "Your search: " + query
		data = bs.values
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



