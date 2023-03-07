from conjugation_table import VerbConjugation
from typing import Dict, List, Optional
import json


# https://github.com/MisterDerpie/anki-deck-creator
class AnkiDeckCreatorVocabularyConverter:
    _filter: Optional[Dict]
    _verb_conjugation: Dict

    def __init__(self, verb_conjugation: Dict, _filter: Optional[Dict]):
        self._verb_conjugation = verb_conjugation
        self._filter = _filter

    def convert(self) -> Dict[str, str]:
        vocabulary = []
        from_english = self._verb_conjugation["translation"]
        to_spanish = self._verb_conjugation["verb"]
        conjugations = self._verb_conjugation["conjugations"]
        for conjugation in conjugations:
            group = conjugation["group"]
            if group in self._filter or not self._filter:
                tenses = conjugation["tenses"]
                for tense in tenses:
                    if tense["tense"] in self._filter[group] or not self._filter:
                        self._append_vocabulary(
                            vocabulary,
                            from_english,
                            to_spanish,
                            group,
                            tense["tense"],
                            tense["conjugations"],
                        )

        return vocabulary

    def _build_from(self, verb_native: str, group: str, tense: str) -> str:
        return f"{verb_native} - {group}, {tense}"

    def _build_to(self, verb: str, conjugations: List[str]) -> str:
        return f"{verb}<br/><br/>" + "<br/>".join(conjugations)

    def _append_vocabulary(
        self,
        vocabulary: List[str],
        english: str,
        spanish: str,
        group: str,
        tense: str,
        conjugations,
    ) -> None:
        translation_from = self._build_from(english, group, tense)
        translation_to = self._build_to(spanish, conjugations)
        vocabulary.append({"english": translation_from, "spanish": translation_to})
