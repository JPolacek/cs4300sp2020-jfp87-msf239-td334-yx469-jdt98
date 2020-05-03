import json

synonyms = {}
body_parts = []

with open('data/description_yoga_json.json') as f:
	data = json.load(f)

for stretch in data:
	body_parts += data[stretch]["body_part"]

body_parts = list(set(body_parts))
for body_part in body_parts:
	synonyms[body_part] = []

synonyms = {'lower back': ['back', 'spine', 'abs'], \
	'lungs': ['chest', 'sides'], \
	'sides': ['lungs', 'abs', 'lower-back', 'back', 'stomach', 'liver'], \
	'shins': ['legs', 'achilles', 'ankles', 'calves'], \
	'legs': ['adductors', 'abductors', 'shins', 'feet', 'quads', 'feet', 'toes', 'glutes', 'knees', 'achilles', 'calves', 'hamstrings', 'thighs'], \
	'lower-back': ['sides', 'liver', 'bladder', 'abs', 'abductors'], \
	'feet': ['toes', 'ankles'], \
	'foot': ['feet'], \
	'quads': ['thighs'], \
	'buttocks': ['glutes'], \
	'ankles': ['feet'], \
	'chest': ['lungs', 'thyroid', 'heart'], \
	'adductors': ['hips', 'pelvis'], \
	'abs': ['sides', 'stomach', 'belly'], \
	'neck': ['shoulders'], \
	'liver': ['sides'], \
	'bladder': ['sides'], \
	'toes': ['feet'], \
	'glutes': ['buttocks'], \
	'spine': ['abs', 'back', 'lower-back'], \
	'belly': ['stomach', 'abs', 'liver', 'bladder'], \
	'shoulders': ['neck'], \
	'achilles': ['ankles', 'shins'], \
	'pelvis': ['adductors', 'abductors'], \
	'knees': [], \
	'ankles': ['achilles', 'shins', 'feet'], \
	'calves': ['shins', 'achilles'], \
	'arms': ['shoulders', 'hands'], \
	'heart': ['chest'], \
	'stomach': ['sides', 'belly'], \
	'back': ['sides'], \
	'hamstrings': ['adductors'], \
	'hands': [], \
	'hips': ['adductors'], \
	'brain': [], \
	'thighs': ['quads', 'hamstrings', 'glutes', 'adductors'], \
	'abductors': ['hip'], \
	'thyroid': []}

