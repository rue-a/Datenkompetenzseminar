# -*- coding: utf-8 -*-
# %%
import re
from csv import DictReader
import geopandas as gpd
import spacy
import math

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


# %%
"""
- use natural language processing to find places in the 
first 100 entries of the fliegel index

- review the results
"""


# read white people index
i = -1
with open("../data/Fliegel_WhitePeople_setsIsolated_table.tsv", "r") as csv_in:

    # read CSV from in file
    white_people_in = DictReader(csv_in, delimiter="\t")

    # iterate over all factoids
    for row in white_people_in:
        # counter
        i += 1
        if i == 50:
            break

        # skip empty factoids
        if row["factoid"] and len(row["factoid"]) > 1:

            # clean text: (rm occurences of "No.", rm multiple spaces
            # with single space, rm leading and trailing whitespaces)
            cleaned_text = re.sub(
                "[ ]+", " ", row["factoid"].replace("No.", "")
            ).strip()

            phrase = nlp(cleaned_text)

            # red cross as default
            place_identifier = "\033[91m✘\033[0m"
            entity_label_info_string = "\t"
            for entity in phrase.ents:
                entity_label_info_string += f"{entity.text}: {entity.label_},"
                if entity.label_ == "LOC" or entity.label_ == "GPE":
                    # set red cross to green tick
                    place_identifier = "\033[92m✔\033[0m"
            entity_label_info_string = (
                place_identifier + entity_label_info_string.strip(",")
            )
            print(phrase)
            print(entity_label_info_string)
            print()

# %%

"""
- collect factoids with identified place names in a list (geo_factoids)

- match places identified in the factoids against known known places
from the fliegel gazetteer (a gazetteer is a list of place names with 
coordinates assigned), to enrich factoids with coordinates

- review only first 3000 factoids

"""

geo_factoids = []
with open("../data/Fliegel_WhitePeople_setsIsolated_table.tsv", "r") as csv_in:

    # read CSV from in file
    white_people_in = DictReader(csv_in, delimiter="\t")

    i = -1
    # iterate over all factoids
    for row in white_people_in:

        i += 1
        if i == 3000:
            break

        # skip empty factoids
        if row["factoid"] and len(row["factoid"]) > 1:

            # clean text: (rm occurences of "No.", rm multiple spaces
            # with single space, rm leading and trailing whitespaces)
            cleaned_text = re.sub(
                "[ ]+", " ", row["factoid"].replace("No.", "")
            ).strip()

            phrase = nlp(cleaned_text)

            entity_label_info_string = "\t"
            for entity in phrase.ents:
                entity_label_info_string += f"{entity.text}: {entity.label_},"
                if (
                    entity.label_ == "LOC"
                    or entity.label_ == "GPE"
                    or entity.label_ == "ORG"
                ):
                    row["place"] = entity.text
                    geo_factoids.append(row)


with open("../data/fliegel_gazetteer.csv", "r") as csv_in:
    gazetteer = []
    for row in DictReader(csv_in, delimiter=","):
        gazetteer.append(row)

geo_factoids_georeferenced = []
for row in geo_factoids:
    for gazetteer_row in gazetteer:
        if row["place"] == gazetteer_row["place_name"]:
            row["latitude"] = gazetteer_row["latitude"]
            row["longitude"] = gazetteer_row["longitude"]
            geo_factoids_georeferenced.append(row)


# %%

"""
- review results with geopandas package

- geopandas is based on pandas package 
    -> provides geospatial capabilities
    - https://geopandas.org/en/stable/

- pandas is a mighty package to analyse tabular
data in python (https://pandas.pydata.org/docs/)
"""

# create data frame without spatial reference
gdf = gpd.GeoDataFrame(geo_factoids_georeferenced)
# parse latitude and longitude columns as spatial reference
gdf["geometry"] = gpd.points_from_xy(gdf["longitude"], gdf["latitude"])
gdf.crs = "EPSG:4326"

# %%
gdf.explore(column="year", cmap="viridis", legend_kwds={"fontsize": "small"})

# %%
# count occurences of places in gdf['places'] column and store
# in new data frame
count_gdf = gdf["place"].value_counts().reset_index()
count_gdf.columns = ["place", "count"]


# load gazetteer fiels as geo data frame
gazetteer_gdf = gpd.read_file("../data/fliegel_gazetteer.csv")
gazetteer_gdf["geometry"] = gpd.points_from_xy(
    gazetteer_gdf["longitude"], gazetteer_gdf["latitude"]
)
gazetteer_gdf.crs = "EPSG:4326"

# Merge count_gdf with gazetteer_gdf on the 'place' column
count_gdf = count_gdf.merge(gazetteer_gdf, left_on="place", right_on="place_name")
# merge returns a pandas data frame, so we have to initialize
# count_gdf again as geo data frame
count_gdf = gpd.GeoDataFrame(count_gdf)


# %%

count_gdf.explore(
    # column="count",
    style_kwds={
        "style_function": lambda record: {
            "radius": math.sqrt((record["properties"]["count"])) + 3
        }
    },
)
