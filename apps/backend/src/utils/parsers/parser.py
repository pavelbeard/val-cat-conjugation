from abc import ABC, abstractmethod
from typing import Any


class Parser(ABC):
    @abstractmethod
    def parse(self, data: Any) -> Any:
        """
        Parse the given data and return the result.
        
        :param data: The data to be parsed.
        :return: The parsed result.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    