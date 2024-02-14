from typing import List
import logging

from nhlpy.api.query.filters import QueryBase


class QueryContext:
    def __init__(self, query: str, filters: List[QueryBase]):
        self.query_str = query
        self.filters = filters


class QueryBuilder:
    def __init__(self, verbose: bool = False):
        self._verbose = verbose
        if self._verbose:
            logging.basicConfig(level=logging.INFO)

    def build(self, filters: List[QueryBase]) -> QueryContext:
        output: str = ""
        for f in filters:
            if not isinstance(f, QueryBase):
                if self._verbose:
                    logging.info(f"Input filter is not of type QueryBase: {f.__name__}")

                continue

            _q = f.to_query()
            output += f"{_q} and "
        else:
            output = output[:-5]

        return QueryContext(query=output, filters=filters)
