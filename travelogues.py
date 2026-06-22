"""
Loads travelogue data from a pre-collected CSV file and assembles a list of
Travelogue objects, each containing its stops ordered by series ordinal.

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
class Location:
    qid: str
    label: str
    ordinal: int
    latitude: float
    longitude: float


@dataclass
class Travelogue:
    qid: str
    label: str
    publication_year: int | None
    locations: list[Location]

    def export_geojson(self) -> dict:
        """
        Serialises this travelogue as a GeoJSON Feature.

        The route is encoded as a GeoJSON LineString connecting all stops in
        ordinal order. The publication year is stored in the 'properties' dict
        under both 'year' and 'publication_year'. Coordinates follow GeoJSON
        axis order (longitude, latitude).

        Returns:
            A dict representing a GeoJSON Feature with a LineString geometry.
        """
        coordinates = [[loc.longitude, loc.latitude] for loc in self.locations]
        # coordinates = [coordinates[0], coordinates[-1]]

        return {
            "type": "Feature",
            "id": self.qid,
            "geometry": {
                "type": "LineString",
                "coordinates": coordinates,
            },
            "properties": {
                "label": self.label,
                "publication_year": self.publication_year,
                "west_to_east": self.locations[0].longitude
                - self.locations[-1].longitude,
            },
        }

    def export_source_target(self) -> dict:
        """
        Serialises the first and last stop of this travelogue as a flat dict.

        'west_to_east' is the difference in longitude between the first and
        last stop (source_lon − target_lon). A positive value means the journey
        ends further west than it begins; negative means it ends further east.

        Returns:
            A dict with id, label, publication_year, source/target coordinates,
            and the west_to_east longitude delta.
        """
        return {
            "id": self.qid,
            "label": self.label,
            "publication_year": self.publication_year,
            "source_lat": self.locations[0].latitude,
            "source_lon": self.locations[0].longitude,
            "target_lat": self.locations[-1].latitude,
            "target_lon": self.locations[-1].longitude,
            "west_to_east": self.locations[0].longitude - self.locations[-1].longitude,
        }


def write_feature_collection(travelogues: list[Travelogue], output_path: Path) -> None:
    """
    Writes all travelogues to a GeoJSON FeatureCollection file.

    Args:
        travelogues:  List of Travelogue objects to serialise.
        output_path:  Destination file path; created or overwritten.
    """
    geojson_feature_collection = {
        "type": "FeatureCollection",
        "conformsTo": ["http://www.opengis.net/spec/json-fg-1/0.3/conf/core"],
        "featureType": "Travelogue",
        "features": [t.export_geojson() for t in travelogues],
    }
    output_path.write_text(
        json.dumps(geojson_feature_collection, indent=2, ensure_ascii=False)
    )
    print(f"Wrote {len(travelogues)} features to {output_path}.")


def write_source_target_json(travelogues: list[Travelogue], output_path: Path) -> None:
    """
    Writes a JSON array of source/target records to a file, one per travelogue.

    Args:
        travelogues:  List of Travelogue objects to serialise.
        output_path:  Destination file path; created or overwritten.
    """
    source_target = [t.export_source_target() for t in travelogues]
    output_path.write_text(json.dumps(source_target, indent=2, ensure_ascii=False))
    print(f"Wrote {len(travelogues)} features to {output_path}.")


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


def load_travelogues(csv_path: Path) -> list[Travelogue]:
    """
    Reads the CSV file and returns one Travelogue per unique travelogue URI,
    each instantiated with its complete, ordinal-sorted location list.

    Uses pandas to parse the CSV, extract coordinates, and group rows by
    travelogue QID before building the final objects.

    Args:
        csv_path: Path to the CSV file produced by query.sparql.

    Returns:
        A list of Travelogue objects in CSV order, each with locations sorted
        by ascending ordinal.
    """
    df = pd.read_csv(csv_path)
    df["travelogue_qid"] = df["travelogue"].apply(extract_qid)
    df["subject_qid"] = df["subject"].apply(extract_qid)
    df[["latitude", "longitude"]] = df["coords"].apply(
        lambda wkt: pd.Series(parse_wkt_point(wkt))
    )

    travelogues = []
    for qid, group in df.groupby("travelogue_qid", sort=False):
        first = group.iloc[0]
        year = (
            int(first["publicationYear"])
            if pd.notna(first["publicationYear"])
            else None
        )
        locations = [
            Location(
                qid=row["subject_qid"],
                label=row["subjectLabel"],
                ordinal=int(row["ordinal"]),
                latitude=row["latitude"],
                longitude=row["longitude"],
            )
            for _, row in group.sort_values("ordinal").iterrows()
        ]
        travelogues.append(
            Travelogue(
                qid=str(qid),
                label=first["travelogueLabel"],
                publication_year=year,
                locations=locations,
            )
        )
    return travelogues


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    travelogues = load_travelogues(DATA_FILE)
    print(f"Loaded {len(travelogues)} travelogues from {DATA_FILE}.")

    write_feature_collection(travelogues, Path("data/travelogues.geojson"))
    write_source_target_json(travelogues, Path("data/travelogues_source_target.json"))

    # Quick preview: first travelogue with at least one stop.
    for t in travelogues:
        if t.locations:
            print(f"\nExample — {t.label} ({t.qid}), {t.publication_year}:")
            for loc in t.locations:
                print(
                    f"  #{loc.ordinal:>3}  {loc.label:<30} "
                    f"lat={loc.latitude:.4f}, lon={loc.longitude:.4f}"
                )
            break


if __name__ == "__main__":
    main()
