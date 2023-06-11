from elasticsearch.exceptions import ConnectionError
from elasticsearch.exceptions import NotFoundError

from flask import current_app

from app import db


def add_to_index(index: str, model: db.Model) -> None:
    """Add given index to search engine."""
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model._fulltext_attrs:
        payload[field] = getattr(model, field)
    try:
        current_app.elasticsearch.index(index=index, id=model.id, body=payload)
    except ConnectionError:
        current_app.logger.error('Unable to establish connection to ElasticSearch.')
    except NotFoundError:
        current_app.logger.error('Search index "%s" not found.', index)
        


def remove_from_index(index: str, model: db.Model) -> None:
    """Remove given index from search engine."""
    if not current_app.elasticsearch:
        return
    try:
        current_app.elasticsearch.delete(index=index, id=model.id)
    except ConnectionError:
        current_app.logger.error('Unable to establish connection to ElasticSearch.')
    except NotFoundError:
        current_app.logger.error('Search index "%s" not found.', index)


def query_index(
    index: str, query: dict, page: int, per_page: int
) -> tuple:
    """Perform query to search engine."""
    if not current_app.elasticsearch:
        return [], 0
    try:
        search = current_app.elasticsearch.search(
            index=index,
            body={
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': ['*']
                    }
                },
                'from': (page - 1) * per_page,
                'size': per_page,
            },
        )
    except ConnectionError:
        current_app.logger.error('Unable to establish connection to ElasticSearch.')
        return [], 0
    except NotFoundError:
        current_app.logger.error('Search index "%s" not found.', index)
        return [], 0
    search_hits = search['hits']
    ids = [int(hit['_id']) for hit in search_hits['hits']]
    return ids, search_hits['total']['value']
