from app.irsystem.controllers.search_functions import *

"""
Given a pose, will search for related poses


The pose searched can find the body parts related to that pose
We can then search each of those body parts with the boolean search function
"""


def pose_search(data, query, additionaL_query, limit_body_parts=2):
    """
    Returns related poses to the original Pose

    query is a pose

    REQUIRES: query is actually in the data set
    """
    related_body_parts = data[query]["body_part"]
    if len(related_body_parts) > limit_body_parts:
        related_body_parts = related_body_parts[:limit_body_parts]
    return boolean_search_routine(data, ", ".join(related_body_parts), additionaL_query)
