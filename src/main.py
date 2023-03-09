#!/bin/python3
from conjugation_table import VerbFetcher
from converter import AnkiDeckCreatorVocabularyConverter
from sqlite_cache import SqliteCache
import json

cache = SqliteCache("verbs.db")
verb_list = [
    "ser",
    "ir",
    "estar",
    "poder",
    "haber",
    "saber",
    "trabajar",
    "comer",
    "vivir",
]

verbs = []
for word in verb_list:
    lcword = word.lower()
    print(f"Processing {lcword}")
    result = VerbFetcher.get_verb_cache(lcword, cache)
    verbs.append(result)

_filter = {
    "Indicativo": [
        "Presente",
        "Pretérito perfecto compuesto",
        "Pretérito perfecto simple",
        "Futuro",
    ],
    "Gerundio": ["Simple"],
}

converted = [
    AnkiDeckCreatorVocabularyConverter(verb, _filter).convert() for verb in verbs
]
flattened = [vocabulary for nested_list in converted for vocabulary in nested_list]
print(json.dumps(flattened, ensure_ascii=False))
