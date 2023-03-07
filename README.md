# Spanish Verb Conjugator

## Description

This repository contains a small Python script to fetch the conjugation of Spanish verbs.
Moreover it provides capability to transform the verbs into a format used in
[MisterDerpie/anki-deck-creator](https://github.com/MisterDerpie/anki-deck-creator).

The conjugations are from [conjugacion.es](https://www.conjugacion.es/).
An excerpt of a possible output

```json
{
   "verb":"comer",
   "translation":"to eat",
   "regular":true,
   "conjugations":[
      {
         "group":"Indicativo",
         "tenses":[
            {
               "tense":"Presente",
               "conjugations":[
                  "yo como",
                  ...
               ]
            }, ...
         ]
      },
      {
         "group":"Subjuntivo",
         "tenses":[...]
      }
   ]
}
```

For an example of the full output see [this Gist](https://gist.github.com/MisterDerpie/e2393583d55b8fcc1ae2a1fa7bf03a95).

Note that Python object representations only partially exist.
You can use the objects `TimeTable` and `TimeTableGroup` to get an object representation.
The `TimeTable` does not support deep nesting by person.

## Dependencies

- [Python Requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

```
$ pip3 install beautifulsoup4 requests
```

## Usage

### Large Example

This example provides multiple things

- Cached retrieval of words
- Convert retrieved verbs to AnkiDeckCreator format
- Filters only specific tenses

```python
from conjugation_table import VerbFetcher
from converter import AnkiDeckCreatorVocabularyConverter
from cache import JsonFileCache
import json

cache = JsonFileCache("verbs")
verb_list = [
    "ser",
    "ir",
    "visitar",
]
verbs = [VerbFetcher.get_verb_cache(verb, cache) for verb in verb_list]

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
```

### Non Cached Retrieval

This is the straightforward way to use it.

```python
from conjugation_table import VerbFetcher

verb = VerbFetcher.get_verb(input("Provide a verb: "))

print(verb.to_json())
```

### Cached Retrieval

The cache interface is defined in `cache.py`.
In addition, there is a local filesystem JSON Cache implemented as an example

```python
from conjugation_table import VerbFetcher
from cache import JsonFileCache

cache = JsonFileCache("verbs")            # Has to be a directory
VerbFetcher.get_verb_cache("ser", cache)  # Writes verb if absent
VerbFetcher.get_verb_cache("ser", cache)  # Read should be I/O bound fast
```

Note that the cached version does not return a `VerbConjugation` object as of now.
This is due to the absence of a `from_dict` method.

### Transform to Anki Deck Creator Format

In `converter.py` the `AnkiDeckCreatorVocabularyConverter` is defined.
This does not generate a full AnkiDeck, but only a set of cards for a single word.

When retrieving a dict of shape `VerbConjugation`, you can provide a filter in form of a dict.
The shape is as below.

```json
{ "Group": ["Tense1", "Tense2", ... ] }
```

The key in the root of the object is the respective group, e.g. Indicativo or Subjuntivo.
Its value is a list of tenses that you would like to be output.

```python
verb = VerbFetcher.get_verb("ser").to_dict()

_filter = {"Indicativo": ["Presente"]}
converted = AnkiDeckCreatorVocabularyConverter(verb, _filter).convert()

print(json.dumps(converted, ensure_ascii=False))
```

produces

```json
[
   {
      "english":"to be - Indicativo, Presente",
      "spanish":"ser<br/><br/>yo soy<br/>tú eres<br/>él es<br/>nosotros somos<br/>vosotros sois<br/>ellos son"
   }
]
```