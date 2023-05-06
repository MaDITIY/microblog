from flask import current_app

from app import db


def add_to_index(index: str, model: db.Model) -> None:
    """Add given index to search engine."""
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model._fulltext_attrs:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index: str, model: db.Model) -> None:
    """Remove given index from search engine."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(
    index: str, query: dict, page: int, per_page: int
) -> tuple:
    """Perform query to search engine."""
    if not current_app.elasticsearch:
        return [], 0
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
    search_hits = search['hits']
    ids = [int(hit['_id']) for hit in search_hits['hits']]
    return ids, search_hits['total']['value']
