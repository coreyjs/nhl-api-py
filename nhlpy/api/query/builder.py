from typing import List
import logging

from nhlpy.api.query import InvalidQueryValueException
from nhlpy.api.query.filters import QueryBase


class QueryContext:
    """A container for query information and validation state.

    This class holds the constructed query string, original filters, any validation
    errors, and a base fact query. It provides methods to check query validity.

    Attributes:
        query_str (str): The constructed query string from all valid filters
        filters (List[QueryBase]): List of original query filter objects
        errors (List[str]): List of validation error messages
        fact_query (str): Base fact query, defaults to "gamesPlayed>=1"
    """

    def __init__(self, query: str, filters: List[QueryBase], fact_query: str = None, errors: List[str] = None):
        self.query_str = query
        self.filters = filters
        self.errors = errors
        self.fact_query = fact_query if fact_query else "gamesPlayed>=1"

    def is_valid(self) -> bool:
        """Check if the query context is valid.

        Returns:
            bool: True if there are no validation errors, False otherwise
        """
        return len(self.errors) == 0


class QueryBuilder:
    """Builds and validates query strings from a list of query filters.

    This class processes a list of QueryBase filters, validates them, and combines
    them into a single query string. It handles validation errors and provides
    optional verbose logging.

    Attributes:
        debug (bool): When True, enables detailed logging of the build process
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        if self.debug:
            logging.basicConfig(level=logging.INFO)

    def build(self, filters: List[QueryBase]) -> QueryContext:
        """Build a query string from a list of filters.

        Processes each filter in the list, validates it, and combines valid filters
        into a single query string using 'and' as the connector.

        Args:
            filters (List[QueryBase]): List of query filter objects to process

        Returns:
            QueryContext: A context object containing the query string, original filters,
                and any validation errors

        Notes:
            - Skips filters that aren't instances of QueryBase
            - Collects validation errors but continues processing remaining filters
            - Combines valid filters with 'and' operator
            - Returns empty query string if no valid filters are found
        """
        result_query: str = ""
        output_filters: List[str] = []
        errors: List[str] = []
        for f in filters:
            if not isinstance(f, QueryBase):
                if self.debug:
                    logging.info(f"Input filter is not of type QueryBase: {f.__name__}")
                continue

            # Validate the filter
            try:
                if not f.validate():
                    raise InvalidQueryValueException(f"Filter failed validation: {str(f)}")
            except InvalidQueryValueException as e:
                if self.debug:
                    logging.error(e)
                errors.append(str(e))
                continue

            output_filters.append(f.to_query())
        else:
            if len(output_filters) > 0:
                result_query = " and ".join(output_filters)

        return QueryContext(query=result_query, filters=filters, errors=errors)
