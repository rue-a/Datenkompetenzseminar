# -*- coding: utf-8 -*-
# %%

import re
from csv import DictReader, DictWriter

import spacy

nlp = spacy.load("en_core_web_sm")

# ------------------------------------------------------------------
# Spacy named entity types:
# ------------------------------------------------------------------
# PERSON:      People, including fictional.
# NORP:        Nationalities or religious or political groups.
# FAC:         Buildings, airports, highways, bridges, etc.
# ORG:         Companies, agencies, institutions, etc.
# GPE:         Countries, cities, states.
# LOC:         Non-GPE locations, mountain ranges, bodies of water.
# PRODUCT:     Objects, vehicles, foods, etc. (Not services.)
# EVENT:       Named hurricanes, battles, wars, sports events, etc.
# WORK_OF_ART: Titles of books, songs, etc.
# LAW:         Named documents made into laws.
# LANGUAGE:    Any named language.
# DATE:        Absolute or relative dates or periods.
# TIME:        Times smaller than a day.
# PERCENT:     Percentage, including ”%“.
# MONEY:       Monetary values, including unit.
# QUANTITY:    Measurements, as of weight or distance.
# ORDINAL:     “first”, “second”, etc.
# CARDINAL:    Numerals that do not fall under another type.
# ------------------------------------------------------------------

# read white people index
i = -1
with open("../data/Fliegel_WhitePeople_setsIsolated_table.tsv", "r") as csv_in:

    # read CSV from in file
    white_people_in = DictReader(csv_in, delimiter="\t")

    # iterate over all factoids
    for row in white_people_in:
        # counter
        i += 1
        if i == 100:
            break

        # skip empty factoids
        if row["factoid"] and len(row["factoid"]) > 1:

            # clean text
            cleaned_text = re.sub(
                "[ ]+", " ", row["factoid"].replace("No.", "")
            ).strip()

            phrase = nlp(cleaned_text)

            for entity in phrase.ents:
                print(f"{entity.text}, entity type: {entity.label_}")


# %%
