from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import itertools
import json
import re
from app.irsystem.controllers.edit_distance import *
from app.irsystem.controllers.search_functions import *

project_name = "Stretches: Find a stretch to help your pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"
data = ''
valid_query_invalid_bp = "We're uncertain what body part you're looking for, your query doesn't make sense."

with open('data/description_yoga_json.json') as f:
		data = json.load(f)

def find_similar_query(query, query_list):
	all_body_parts = []
	for stretch in data:
	    all_body_parts += data[stretch]["body_part"]

	return edit_distance_search(query, list(set(all_body_parts)))

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	no_result_text = ''
	keys_to_remove = []
	potential_typos = []
	typos = False
	no_known_typos = False

	bs = {}
	if query:
		bs = boolean_search(data, query)
		keys_to_remove = [key for key in bs if bs[key] == []]
		for term in clean_up(query):
			if term not in keys_to_remove and term not in bs.keys():
				typos = True
			potential_typos += [bp for dist, bp in \
				find_similar_query(term, [key for key in keys_to_remove if ',' not in key]) if dist < 3 and dist > 0]
		potential_typos = list(set(potential_typos))

	for key in keys_to_remove:
		del bs[key]		

	if len(bs) == 0:
		if query:
			import_data = potential_typos
			no_result_text = 'There are no results for ' + query +\
				' :(\nConsider trying any of these other body areas:'
			if len(potential_typos) == 0:
				no_known_typos = True
				import_data = valid_query_invalid_bp
		else:
			import_data = [""]

		output_message = no_result_text
	else:
		output_message = "Your search: " + query
		import_data = bs

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=import_data, \
		success=(len(bs) != 0), potential_typos=potential_typos, typos=typos,\
			no_known_typos=no_known_typos)