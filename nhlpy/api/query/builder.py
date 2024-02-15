from typing import List
import logging

from nhlpy.api.query import InvalidQueryValueException
from nhlpy.api.query.filters import QueryBase


class QueryContext:
    def __init__(self, query: str, filters: List[QueryBase], fact_query: str = None, errors: List[str] = None):
        self.query_str = query
        self.filters = filters
        self.errors = errors
        self.fact_query = fact_query if fact_query else "gamesPlayed>=1"

    def is_valid(self) -> bool:
        return len(self.errors) == 0


class QueryBuilder:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        if self._verbose:
            logging.basicConfig(level=logging.INFO)

    def build(self, filters: List[QueryBase]) -> QueryContext:
        result_query: str = ""
        output_filters: List[str] = []
        errors: List[str] = []
        for f in filters:
            if not isinstance(f, QueryBase):
                if self._verbose:
                    logging.info(f"Input filter is not of type QueryBase: {f.__name__}")
                continue

            # Validate the filter
            try:
                if not f.validate():
                    raise InvalidQueryValueException(f"Filter failed validation: {str(f)}")
            except InvalidQueryValueException as e:
                if self._verbose:
                    logging.error(e)
                errors.append(str(e))
                continue

            output_filters.append(f.to_query())
        else:
            if len(output_filters) > 0:
                result_query = " and ".join(output_filters)

        return QueryContext(query=result_query, filters=filters, errors=errors)
