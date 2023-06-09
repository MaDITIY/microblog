from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from flask import url_for

from app import db
from app.search import add_to_index
from app.search import query_index
from app.search import remove_from_index


class Searchable:
    """Allows to search for models in search engine."""
    @classmethod
    def search(
        cls, expression: dict, page: int, per_page: int
    ) -> tuple:
        """Search  for models via searchengine"""
        ids, total = query_index(
            index=cls.__tablename__,
            query=expression,
            page=page,
            per_page=per_page,
        )
        if total == 0:
            return cls.query.filter_by(id=0), 0
        case_when_condition = []
        for i in range(len(ids)):
            case_when_condition.append((ids[i], i))
        result_objects = cls.query.filter(
            cls.id.in_(ids)
        ).order_by(db.case(*case_when_condition, value=cls.id))
        return result_objects, total

    @classmethod
    def before_commit(cls, session: Session) -> None:
        """Store before commit session state."""
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session: Session) -> None:
        """Perform search engine DB update upon app DB changes."""
        # TODO: Add index error handling.
        for obj in session._changes['add'] + session._changes['update']:
            if isinstance(obj, Searchable):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, Searchable):
                remove_from_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls) -> None:
        """Perporm model reindexing."""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class PaginatedAPI:
    """Allows to represent paginated instance query via API."""
    @staticmethod
    def to_collection_dict(
            query: Query,
            page: int,
            per_page: int,
            endpoint: str,
            **kwargs: dict
    ) -> dict:
        """Build a representation of collection of instances."""
        resources = query.paginate(
            page=page,
            max_per_page=per_page,
            error_out=False,
        )
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(
                    endpoint, page=page, per_page=per_page, **kwargs
                ),
                'next': url_for(
                    endpoint, page=page + 1, per_page=per_page, **kwargs
                ) if resources.has_next else None,
                'prev': url_for(
                    endpoint, page=page - 1, per_page=per_page, **kwargs
                ) if resources.has_prev else None
            }
        }
        return data


db.event.listen(db.session, 'before_commit', Searchable.before_commit)
db.event.listen(db.session, 'after_commit', Searchable.after_commit)
