# type: ignore

"""
Module name: search.py
Author: Michele Grieco
Description:
    Elasticsearch integration for indexing and searching model instances.
Usage:
    - add_to_index(index, model): Add a model instance to the Elasticsearch index.
    - remove_from_index(index, model): Remove a model instance from the Elasticsearch index.
    - query_index(index, query, page, per_page): Query the Elasticsearch index for a given search term.
"""

from flask import current_app

def add_to_index(index, model) -> None:
    """
    Add a model instance to the Elasticsearch index.
    The model must have a __searchable__ attribute listing the fields to index.
    :param index: The name of the Elasticsearch index.
    :param model: The model instance to index.
    :return: None
    """
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)


def remove_from_index(index, model) -> None:
    """
    Remove a model instance from the Elasticsearch index.
    :param index: The name of the Elasticsearch index.
    :param model: The model instance to remove from the index.
    :return: None
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page) -> tuple[list[int], int]:
    """
    Query the Elasticsearch index for a given search term.
    :param index: The name of the Elasticsearch index.
    :param query: The search term.
    :param page: The page number for pagination.
    :param per_page: The number of results per page.
    :return: A tuple containing a list of matching record IDs and the total number of matches
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        query={'multi_match': {'query': query, 'fields': ['*']}},
        from_=(page - 1) * per_page,
        size=per_page)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']