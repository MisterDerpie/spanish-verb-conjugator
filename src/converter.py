from typing import Dict, List, Optional


# https://github.com/MisterDerpie/anki-deck-creator
class AnkiDeckCreatorVocabularyConverter:
    _filter: Optional[Dict]
    _verb_conjugation: Dict
    _ignore_regular: bool

    def __init__(
        self,
        verb_conjugation: Dict,
        _filter: Optional[Dict],
        ignore_regular: bool = True,
    ):
        self._verb_conjugation = verb_conjugation
        self._filter = _filter
        self._ignore_regular = ignore_regular

    def convert(self) -> Dict[str, str]:
        vocabulary = []
        from_english = self._verb_conjugation["translation"]
        to_spanish = self._verb_conjugation["verb"]

        if self._ignore_regular and self._verb_conjugation["regular"]:
            return [self._build_regular(from_english, to_spanish)]

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

    def _build_regular(self, translation_from: str, translation_to: str):
        return {"english": translation_from, "spanish": translation_to}

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
