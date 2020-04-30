import numpy as np
import pickle
import copy
from collections import Counter

# This module implements a simple rocchio that takes in user input
# and helps update the rankings

# Should we access informatiomn from a database using postgresQL to help
# rocchio, or do we just pickle data?
# Rocchio needs a dynamic memory store
# Currently, I call it a database, but it could be a dictionary that we load and tore
# a SQL database, etc, anything that can be queried fast and reliablys


def add_relevant(database, boolean_query, document):
    """
    add_relevant(database, boolean_query,document) adds the contents of the entire document to
    the database if it is relevant to the boolean_query.

    Example: user finds D1 : "extend arm up and down..." relevant to the boolean_query "neck and back".
    Calling add_relevant will add this document D1 as relevant to the boolean_query

    Boolean_query is a [string], document a possibly very loing [string]
    You can choose to truncate document if needed for speed, trading off relevance

    WARNING: Once a recommendation is given, it is permanent, and cannot be removed
    from the reelvant list

    Warning: SIMPLE TOKENIZER used: I use split() as a tokenizer

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    tokenized_doc = document.split()
    database['relevant'][boolean_query] += tokenized_doc


def add_irrelevant(database, boolean_query, document):
    """
    add_irrelevant(database, boolean_query, document) adds the contents of the entire document to
    the database if it is irrelevant to the boolean_query.

    Example: user finds D1 : "swing feet left and right..." irrelevant to the boolean_query "neck and back".
    Calling add_irrelevant will add this document D1 as irrelevant to the boolean_query

    Boolean_query is a [string], document a possibly very loing [string]
    You can choose to truncate document if needed for speed, trading off irrelevance

    WARNING: Once a recommendation is given, it is permanent, and cannot be removed
    from the irrelvant list

    Warning: SIMPLE TOKENIZER used: I use split() as a tokenizer

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    tokenized_doc = document.split()
    database['irrelevant'][boolean_query] += tokenized_doc


def clear_database(database):
    """
    clear_database(database) clears all relevant adn irrelevant fields in the database.

    Example: User has given misleading or faulty data on relevance and irrelevance.
    Use clear_database to clear out all rankings to restart without rocchio.

    WARNING: Once a database is cleared, the action is irreversible and data
    is lost permanently

    REQUIRES: 'Irrelevant and Relevatn' fields in database

    Returns: NONE
    """
    database['relevant'] = dict()
    database['irrelevant'] = dict()


def init_database():
    """
    init_database() creates a new data base with empty dictionaries
    for the relevant and irrelevant fields.

    Returns: [dictionary] of data base with empty irrelevant and relevant fields
    """
    database = dict()
    database['relevant'] = dict()
    database['irrelevant'] = dict()
    return database


def rocchio(database, boolean_query, cosine_query):
    """
    rocchio(database, boolean_query, cosine_query) takes in the boolean query
    the cosine query and the irrelevant and relevant docus in the database
    and updates the cosine query. 

    Boolean_query is a [string]
    Cosine_query is a [string]
    Database is a [dictionary]

    Returns: [string] of the rocchio updated cosine query

    Requires: Cosine similarity MUST be used after this: This query correction
    does not fix up for cosine similarity or tf-idf, so you cannot assume Cosine
    similarity is done at the same time or before rocchio()

    Warning: SIMPLE TOKENIZER used: I use split() as a tokenizer
    """
    relevant = database['relevant'][boolean_query]
    irrelevant = database['irrelevant'][boolean_query]
    tokenized_cosine_query = cosine_query.split()
    return simple_rocchio_helper(tokenized_cosine_query, relevant, irrelevant)


def simple_rocchio_helper(cosine_query, relevant, irrelevant):
    """Returns a string representing the modified cosine query. 

    Simplified rocchio without need for tokenizing beforehand;
    Literally on adds terms and deletes terms to the query

    Note: 
        If the `clip` parameter is set to True, the resulting vector should have 
        no negatve weights in it!

        Handles the cases where relevant and irrelevant are empty lists by avoiding division by 0

    Params: {cosine_query: tokenized string of what will go to the cosine similarity as a quert,
             relevant: List of List of tokens that are relevant
             irrelevant: List of List of tokens that are irrelevant

    Returns: String [in some random, undefined order]
    """
    rel_multi_set = Counter()
    for doc in relevant:
        rel_multi_set += Counter(doc)

    irrel_multi_set = Counter()
    for doc in irrelevant:
        irrel_multi_set += Counter(doc)

    query = Counter(cosine_query)

    final_multi_set = query + rel_multi_set - irrel_multi_set
    rocchio_query = " ".join(final_multi_set)

    return rocchio_query


# TODO: Need doc term frequency numpy array and TODO also word to
# index dictionary for the doc term frequncy array
# TODO: Full rocchio helper
def rocchio_helper():
    pass
