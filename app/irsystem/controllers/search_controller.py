from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import itertools
import json
import re
import app.irsystem.controllers.edit_distance as ed
import app.irsystem.controllers.search_functions as sf

project_name = "Stretches: Find a stretch to help your pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"
data = ''
valid_query_invalid_bp = "We're uncertain what body part you're looking for, your query doesn't make sense."

with open('data/yogajournal.json') as f:
		data = json.load(f)

def find_similar_query(query, query_list):
	all_body_parts = []
	for stretch in data:
	    all_body_parts += data[stretch]["body_part"]

	return ed.edit_distance_search(query, list(set(all_body_parts)))

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	no_result_text = ''
	keys_to_remove = []
	potential_typos = []

	bs = {}
	if query:
		bs = sf.boolean_search(data, query)
		keys_to_remove = [key for key in bs if bs[key] == []]
		potential_typos = [bp for dist, bp in \
			find_similar_query(query, [key for key in keys_to_remove if ',' not in key]) if dist < 3]


	for key in keys_to_remove:
		del bs[key]		

	if len(bs) == 0:
		if query:
			print("in len bs == 0 in query")
			import_data = potential_typos
			no_result_text = 'There are no results for ' + query +\
				' :(\nConsider trying any of these other body areas:'
			if len(import_data) == 0:
				import_data = valid_query_invalid_bp
		else:
			import_data = [""]

		print(import_data)
		output_message = no_result_text
	else:
		output_message = "Your search: " + query
		import_data = bs

	print("success=" + str((len(bs) != 0)))
	print("bad_search=" + str(import_data==valid_query_invalid_bp))
	# print("data: " + str(import_data))
	print("Potential Typos: " + str(potential_typos))
	print("Typo=" + str(len(potential_typos)>0))

	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=import_data, \
		success=(len(bs) != 0), potential_typos=potential_typos, typos=(len(potential_typos)>0),\
			bad_search=(import_data==valid_query_invalid_bp))