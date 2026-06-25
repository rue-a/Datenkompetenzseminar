"""
Loads travelogue data from a pre-collected CSV file and builds a de-duplicated
dictionary of TravelLocation objects, counting how many travelogues visit each
unique place.

Expected CSV columns (as produced by query.sparql):
    travelogue, travelogueLabel, publicationYear,
    subject, subjectLabel, ordinal, coords
"""

import json
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_FILE = Path("data/travelogues.csv")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class TravelLocation:
    qid: str
    label: str
    link: str
    latitude: float
    longitude: float

    def export_geojson(self) -> dict:
        """
        Serialises this place as a GeoJSON Feature with a Point geometry.

        Returns:
            A dict representing a GeoJSON Feature. The 'nb_of_visits' property
            counts how many travelogues in the dataset stop at this location.
        """

        geoson_feature = {
            # INSERT CODE HERE
            # ...
            # ...
            # ...
            # ...
            # ...
            # ...
            # ...
        }

        return geojson_feature


def write_feature_collection(features, output_path: Path) -> None:
    """
    Writes a collection of TravelLocation objects to a GeoJSON FeatureCollection
    file.

    Args:
        features:     Iterable of TravelLocation objects to serialise.
        output_path:  Destination file path; created or overwritten.
    """
    geojson_feature_collection = {
        # INSERT CODE HERE
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
        # ...
    }
    output_path.write_text(
        json.dumps(geojson_feature_collection, indent=2, ensure_ascii=False)
    )
    print(f"Wrote {len(features)} features to {output_path}.")


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def extract_qid(wikidata_uri: str) -> str:
    """Extracts the QID from a Wikidata entity URI, e.g. '.../Q12345' → 'Q12345'."""
    return wikidata_uri.rsplit("/", maxsplit=1)[-1]


def parse_wkt_point(wkt: str) -> tuple[float, float]:
    """
    Parses a WKT Point string into (latitude, longitude).

    Args:
        wkt: A string like 'Point(13.73 51.04)' — longitude first, then latitude.

    Returns:
        A (latitude, longitude) float tuple.

    Raises:
        ValueError: If the string does not match the expected WKT Point format.
    """

    # Matches "Point(<lon> <lat>)" (WKT axis order: longitude first, latitude second).
    # Each capture group ([+-]?\d+\.?\d*) accepts an optional sign, then:
    #   \d+  — one or more integer digits
    #   \.?  — optional decimal point
    #   \d*  — zero or more fractional digits
    # Examples: "-13.73", "51", "0.5", "+180.0"
    # Group 1 = longitude, group 2 = latitude.
    match = re.fullmatch(r"Point\(([+-]?\d+\.?\d*) ([+-]?\d+\.?\d*)\)", wkt.strip())
    if not match:
        raise ValueError(f"Unexpected WKT coordinate format: {wkt!r}")
    longitude, latitude = float(match.group(1)), float(match.group(2))
    return latitude, longitude


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------


def get_travel_places(csv_path: Path) -> dict[str, TravelLocation]:
    """
    Reads the CSV file and returns a dict mapping QID → TravelLocation for
    every unique place that appears across all travelogues. Places visited by
    multiple travelogues have their 'nb_of_visits' incremented accordingly.

    Args:
        csv_path: Path to the CSV file produced by query.sparql.

    Returns:
        A dict of TravelLocation objects keyed by Wikidata QID.
    """
    df = pd.read_csv(csv_path)
    df[["longitude", "latitude"]] = df["coords"].apply(
        lambda wkt: pd.Series(parse_wkt_point(wkt))
    )

    # INSERT CODE HERE
    # ...
    # ...
    # ...
    # ...
    # ...
    # ...
    # ...


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    travel_places = get_travel_places(DATA_FILE)

    write_feature_collection(travel_places.values(), Path("data/travel_places.geojson"))


if __name__ == "__main__":
    main()
