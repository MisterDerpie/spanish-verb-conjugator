# Spanish Verb Conjugator

## Description

This repository contains a small Python script to fetch the conjugation of Spanish verbs.
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

## Dependencies

- [Python Requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

```
$ pip3 install beautifulsoup4 requests
```

## Example

```python
from conjugation_table import VerbFetcher

verb = VerbFetcher.get_verb(input("Provide a verb: "))

print(verb.to_json())
```

Note that Python object representations at the initial release only partially exist.
You can use the objects `TimeTable` and `TimeTableGroup` to get an object representation.
The `TimeTable` does not support deep nesting by person.