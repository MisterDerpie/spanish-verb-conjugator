import json
import logging
import re
import requests

from bs4 import BeautifulSoup
from typing import Dict, List
from cache import Cache


class TimeGroup:
    INDICATIVO = "Indicativo"
    SUBJUNTIVO = "Subjuntivo"
    IMPERATIVO = "Imperativo"
    INFINITIVO = "Infinitivo"
    GERUNDIO = "Gerundio"
    PARTICIPIO = "Participio"


class BeautifulSoupConjugation:
    bs_html: BeautifulSoup

    def __init__(self, verb: str):
        self.verb = verb
        self.html = self._fetch_verb(verb)
        self.bs_html = BeautifulSoup(self.html, "html.parser")

    def is_regular(self) -> bool:
        if "Verbo regular" in self.html:
            logging.info("Regular verb, no need to do anything")
            return True
        elif "Verbo irregular" in self.html or "Verbo auxiliar":
            logging.info(msg="Irregular")
            return False
        else:
            raise Exception("Neither regular nor irregular")

    def get_translation(self) -> str:
        result = re.findall(
            """<a href="\/ingles\/verbo\/.*?\.php">(.*?)<\/a><br\/>""",
            self.html,
        )
        if len(result) != 1:
            logging.warn(f"Expected one result for translation, found: {result}")
        return result[0]

    def get_timetables(self) -> Dict[str, List]:
        raw_time_tables = self.bs_html.find_all("div", "tempstab")
        return {
            TimeGroup.INDICATIVO: raw_time_tables[0:10],
            TimeGroup.SUBJUNTIVO: raw_time_tables[10:18],
            TimeGroup.IMPERATIVO: raw_time_tables[18:20],
            TimeGroup.INFINITIVO: raw_time_tables[20:22],
            TimeGroup.GERUNDIO: raw_time_tables[22:24],
            TimeGroup.PARTICIPIO: [raw_time_tables[24]],
        }

    def _fetch_verb(self, verb: str) -> str:
        result = requests.get(f"https://www.conjugacion.es/del/verbo/{verb}.php")
        if result.status_code != 200:
            raise Exception(f'Error retrieving "{verb}", {result.status_code}')
        return result.content.decode("utf-8")


class TimeTable:
    group: str
    tense: str
    conjugations: List[str]

    def __init__(self, group: str, time_table_raw: List[str]):
        self.group = group
        self.tense = time_table_raw.find("h3", "tempsheader").string
        content_string_list = "".join(
            [str(tag) for tag in time_table_raw.find("div", "tempscorps").contents]
        )
        self.conjugations = [
            re.sub("(<b>)|(</b>)", "", conjugation.replace("  ", " "))
            for conjugation in content_string_list.split("<br/>")
            if conjugation
        ]

    def to_dict(self) -> Dict:
        return {
            "group": self.group,
            "tense": self.tense,
            "conjugations": self.conjugations,
        }

    def to_dict_without_group(self) -> Dict:
        dict_without_group = self.to_dict()
        del dict_without_group["group"]
        return dict_without_group


class TimeTableGroup:
    group: str
    time_tables: List[TimeTable]

    def __init__(self, group: str, tenses: List):
        self.group = group
        self.time_tables = []
        for tense in tenses:
            self.time_tables.append(TimeTable(group, tense))

    def to_dict(self) -> Dict:
        time_table_group_dict = {
            "group": self.group,
            "tenses": [table.to_dict_without_group() for table in self.time_tables],
        }
        return time_table_group_dict


class VerbConjugation:
    verb: str
    is_regular: bool
    translation: str
    conjugations: List

    def __init__(
        self,
        verb: str,
        translation: str,
        is_regular: bool,
        time_tables: Dict[str, List],
    ):
        self.verb = verb
        self.translation = translation
        self.is_regular = is_regular
        self.conjugations = [
            TimeTableGroup(group, time_tables[group]).to_dict() for group in time_tables
        ]

    def to_dict(self) -> Dict:
        return {
            "verb": self.verb,
            "translation": self.translation,
            "regular": self.is_regular,
            "conjugations": self.conjugations,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


class VerbFetcher:
    @staticmethod
    def get_verb(verb: str) -> VerbConjugation:
        verb_soup = BeautifulSoupConjugation(verb)
        conjugation = VerbConjugation(
            verb,
            verb_soup.get_translation(),
            verb_soup.is_regular(),
            verb_soup.get_timetables(),
        )
        return conjugation

    @staticmethod
    def get_verb_cache(verb: str, cache: Cache) -> Dict:
        if cache.is_present(verb):
            return cache.read(verb)

        conjugation = VerbFetcher.get_verb(verb).to_dict()
        cache.write(verb, conjugation)

        return conjugation
