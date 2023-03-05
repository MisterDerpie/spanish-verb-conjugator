#!/bin/python3
from conjugation_table import VerbFetcher

verb = VerbFetcher.get_verb(input("Provide a verb: "))

print(verb.to_json())
