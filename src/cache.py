from abc import ABC, abstractclassmethod
from typing import Dict


class Cache(ABC):
    @abstractclassmethod
    def read(self, key: str):
        pass

    @abstractclassmethod
    def write(self, key: str, data: Dict):
        pass

    @abstractclassmethod
    def is_present(self, key: str) -> bool:
        pass
