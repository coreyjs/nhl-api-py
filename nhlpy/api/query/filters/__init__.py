from abc import ABC, abstractmethod
from typing import Union


class QueryBase(ABC):
    @abstractmethod
    def to_query(self) -> str:
        pass

    @abstractmethod
    def validate(self) -> Union[bool, None]:
        return True
