from abc import ABC, abstractmethod


class QueryBase(ABC):
    @abstractmethod
    def to_query(self) -> str:
        pass
