from abc import ABC, abstractclassmethod
from pathlib import Path
from typing import Dict

import json
import os


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


class JsonFileCache(Cache):
    directory: str

    def _build_key(self, key: str):
        return f"{self.directory}/{key}.json"

    def __init__(self, directory_path):
        if not os.path.isdir(directory_path):
            raise Exception(
                f"Cannot use path '{directory_path}' as it is not a directory"
            )
        self.directory = directory_path

    def read(self, key: str) -> Dict:
        return json.loads(Path(self._build_key(key)).read_text())

    def write(self, key: Dict, data: Dict) -> None:
        Path(self._build_key(key)).write_text(json.dumps(data, ensure_ascii=False))

    def is_present(self, key: str) -> bool:
        return Path(self._build_key(key)).exists()
