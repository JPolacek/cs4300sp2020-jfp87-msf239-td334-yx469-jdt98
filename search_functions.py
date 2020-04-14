import json
import itertools

data = {}
with open('data/stretch.json') as f:
  data = json.load(f)

def boolean_search(query):
    """
    Given a query, return the stretches that work on each body part
    """
    q_lower = query.lower()
    body_parts = q_lower.split(' and ')
    return_dict = {}

    for i in range(1, len(body_parts)+1):
        combos = list(itertools.combinations(body_parts, i))
        for combo in combos:
            l = sorted(list(combo))
            combo_string = ', '.join(l)
            return_dict[combo_string] = []
            for stretch in data["stretches"]:
                body_parts_sorted = sorted(stretch["body_parts"])
                if body_parts_sorted == l:
                    return_dict[combo_string].append(stretch["name"])
    
    return return_dict