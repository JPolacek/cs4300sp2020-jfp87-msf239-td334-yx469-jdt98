from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import itertools
import json
import re
import pickle
from app.irsystem.controllers.edit_distance import *
from app.irsystem.controllers.search_functions import *
import copy
from app.irsystem.controllers.pose_search import *

project_name = "Stretches: Find a stretch to help your pain"
net_id = "Jake Polacek:jfp87 Jonathan Tran:jdt98 Matt Frucht:msf239 Teresa Datta:td334 Yifan Xu:yx469"
data = ''
valid_query_invalid_bp = "We're uncertain what body part you're looking for, your query doesn't make sense."

with open('data/description_yoga_json.json') as f:
    original_data = json.load(f)

f = open('data/pose_names', 'rb')
pose_names = pickle.load(f)
f.close()


def find_similar_query(query, query_list):
    all_body_parts = []
    for stretch in original_data:
        all_body_parts += original_data[stretch]["body_part"]

    return edit_distance_search(query, list(set(all_body_parts)))


def find_similar_pose(pose):
    all_poses = []
    for stretch in original_data:
        all_poses += [stretch]

    return edit_distance_search(pose, list(set(all_poses)))


def difficulty_to_level(difficulty):
    if difficulty == "Beginner":
        return 1
    if difficulty == "Intermediate":
        return 2
    if difficulty == "Advanced":
        return 3
    return 0


def level_to_difficulty(level):
    if level == 1:
        return 'Beginner'
    if level == 2:
        return 'Intermediate'
    if level == 3:
        return 'Advanced'
    return "All Levels"


def filter_data_based_on_difficulty(difficulty, original_data):
    if difficulty == 0:
        return copy.deepcopy(original_data)
    new_data = dict()
    for pose in original_data:
        if original_data[pose]["difficulty"] == difficulty:
            new_data[pose] = copy.deepcopy(original_data[pose])
    return new_data


@irsystem.route('/relevant', methods=['POST'])
def update_relevant():
    print("Hello")
    print(request.args.lists())


@irsystem.route('/irrelevant', methods=['POST'])
def update_irrelevant():
    return


def search_by_pose(data, pose, additional_query, difficulty):

    query = pose

    no_result_text = ''
    keys_to_remove = []
    potential_typos = []
    typos = False
    no_known_typos = False

    suggested_routine = []

    bs = {}
    if query:
        if query in pose_names and query in data:
            bs, suggested_routine = pose_search(
                data, query, additional_query)

            keys_to_remove = [key for key in bs if bs[key] == []]
        else:
            bs = ""
            suggested_routine = []
            potential_typos += [bp for dist, bp in
                                find_similar_pose(query) if dist < 4 and dist > 0]
            potential_typos = list(set(potential_typos))

    for key in keys_to_remove:
        del bs[key]

    if len(bs) == 0:
        if query:
            import_data = potential_typos
            no_result_text = 'There are no results for ' + query + ' at the requested difficulty' +\
                ' :(\nConsider trying any of these other poses:'
            if len(potential_typos) == 0:
                no_known_typos = True
                import_data = valid_query_invalid_bp
        else:
            import_data = [""]

        output_message = no_result_text
    else:
        output_message = "Your search: " + query + " " + \
            "[" + level_to_difficulty(difficulty) + "]"
        import_data = bs

    if query in suggested_routine:
        suggested_routine.remove(query)

    enumerate_routine = enumerate(suggested_routine)

    routine_non_empty = True
    if suggested_routine == []:
        routine_non_empty = False

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=import_data,
                           success=(len(bs) != 0), potential_typos=potential_typos, typos=typos,
                           no_known_typos=no_known_typos, routine=enumerate_routine, routine_exists=routine_non_empty, poses=pose_names)


@irsystem.route('/', methods=['GET'])
def search():

    query_dict = dict(request.args.lists())

    # if 'search' in query_dict:
    #     search_items = query_dict['search']
    #     query = search_items[0]
    #     if (len(search_items) == 2):
    #         additional_query = search_items[1]
    #     else:
    #         additional_query = ""
    # else:
    #     query = request.args.get('search')

    if "search" in query_dict:
        search_items = query_dict['search']
        query = search_items[0]
    else:
        query = request.args.get('search')

    if "additional" in query_dict:
        additional_query = query_dict['additional']
        additional_query = additional_query[0]
    else:
        additional_query = ""

    if "difficulty" in query_dict:
        difficulty = query_dict['difficulty']
        difficulty = difficulty[0]
        difficulty = difficulty_to_level(difficulty)

        data = filter_data_based_on_difficulty(difficulty, original_data)

    else:
        difficulty = 0
        data = original_data

    if "pose" in query_dict and query_dict["pose"] != [""]:
        pose = query_dict["pose"]
        pose = pose[0]
    else:
        pose = None

    if pose != None:
        pose.lower()
        pose = ' '.join([w[0].capitalize() + w[1:]
                         for w in filter(lambda elt: elt != "", pose.split(' '))])
        return search_by_pose(data, pose, additional_query, difficulty)

    no_result_text = ''
    keys_to_remove = []
    potential_typos = []
    typos = False
    no_known_typos = False

    suggested_routine = []

    bs = {}
    if query:
        bs, suggested_routine = boolean_search_routine(
            data, query, additional_query)
        keys_to_remove = [key for key in bs if bs[key] == []]
        for term in clean_up(query):
            if term not in keys_to_remove and term not in bs.keys():
                typos = True
            potential_typos += [bp for dist, bp in
                                find_similar_query(term, [key for key in keys_to_remove if ',' not in key]) if dist < 4 and dist > 0]
        potential_typos = list(set(potential_typos))

    for key in keys_to_remove:
        del bs[key]

    if len(bs) == 0:
        if query:
            import_data = potential_typos
            no_result_text = 'There are no results for ' + query + \
                ' :(\nConsider trying any of these other body areas:'
            if len(potential_typos) == 0:
                no_known_typos = True
                import_data = valid_query_invalid_bp
        else:
            import_data = [""]

        output_message = no_result_text
    else:
        output_message = "Your search: " + query + " " + \
            "[" + level_to_difficulty(difficulty) + "]"
        import_data = {stretch_tup[0].title(): stretch_tup[1] for stretch_tup in sorted(
            bs.items(), key=lambda tup: len(tup[0]), reverse=True)}

    enumerate_routine = enumerate(suggested_routine)

    routine_non_empty = True
    if suggested_routine == []:
        routine_non_empty = False

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=import_data,
                           success=(len(bs) != 0), potential_typos=potential_typos, typos=typos,
                           no_known_typos=no_known_typos, routine=enumerate_routine, routine_exists=routine_non_empty, poses=pose_names)


@irsystem.route('/<pose>', methods=['GET'])
def re_search(pose):

    query_dict = dict(request.args.lists())
    if query_dict != {}:
        return search()

    pose = pose.replace("&", " ")
    no_result_text = ''
    potential_typos = []
    typos = False
    no_known_typos = False

    suggested_routine = []

    bs, suggested_routine = pose_search(original_data, pose, "")

    if len(bs) == 0:

        output_message = no_result_text
    else:
        output_message = "Your search: " + pose + " "
        import_data = {body_parts: bs[body_parts]
                       for body_parts in bs if len(bs[body_parts]) != 0}

    if pose in suggested_routine:
        suggested_routine.remove(pose)

    enumerate_routine = enumerate(suggested_routine)

    routine_non_empty = True
    if suggested_routine == []:
        routine_non_empty = False

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=import_data,
                           success=(len(bs) != 0), potential_typos=potential_typos, typos=typos,
                           no_known_typos=no_known_typos, routine=enumerate_routine, routine_exists=routine_non_empty, poses=pose_names)


@irsystem.route('/see_more/<pose>', methods=['GET'])
def see_more(pose):
    pose = pose.replace("&", " ")
    pose_data = original_data[pose]

    introduction = pose_data["introduction"]
    intro_exists = True
    if introduction == [""]:
        intro_exists = False
    introduction = " ".join(introduction)

    steps = pose_data["steps"]

    remarks = pose_data["remarks"]
    remarks_exists = True
    if remarks == [""]:
        remarks_exists = False
    remarks = " ".join(remarks)

    image = pose_data["image_name"]

    video = pose_data["video_url"]

    external = pose_data["url"]

    body_parts = set(pose_data["body_part"])

    return render_template('card.html',
                           pose=pose,
                           introduction=introduction,
                           steps=steps,
                           remarks=remarks,
                           intro_exists=intro_exists,
                           remarks_exists=remarks_exists,
                           img=image,
                           video=video,
                           external=external,
                           bps=body_parts)
