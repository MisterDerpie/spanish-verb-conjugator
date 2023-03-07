#!/bin/python3
from conjugation_table import VerbFetcher
from converter import AnkiDeckCreatorVocabularyConverter

verb = VerbFetcher.get_verb(input("Provide a verb: ")).to_dict()
_filter = {
    "Indicativo": [
        "Presente",
        "Pretérito perfecto compuesto",
        "Pretérito perfecto simple",
        "Futuro",
    ]
}

print(AnkiDeckCreatorVocabularyConverter(verb, _filter).convert())
