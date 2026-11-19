#!/usr/bin/env python3
"""Laguna di Venezia polygon from OpenStreetMap (relation 3049430, natural=water water=lagoon).

Source: Nominatim polygon_geojson response saved in raw/nominatim/laguna_venezia_2026-11-19.json.
Licence: OpenStreetMap contributors, ODbL 1.0. Simplified (tolerance 0.0003 deg, ~30 m) for web use.
"""
import json
from pathlib import Path
from shapely.geometry import shape, mapping
ROOT = Path(__file__).resolve().parents[1]
src = json.load(open(ROOT / "raw/nominatim/laguna_venezia_2026-11-19.json"))[0]
geom = shape(src["geojson"]).simplify(0.0003, preserve_topology=True)
def rnd(c):
    return [round(c[0], 6), round(c[1], 6)] if isinstance(c[0], float) else [rnd(x) for x in c]
g = mapping(geom); g = {"type": g["type"], "coordinates": rnd(json.loads(json.dumps(g["coordinates"])))}
fc = {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {
    "name": "Laguna di Venezia", "source": "OpenStreetMap relation 3049430 (natural=water, water=lagoon)",
    "source_url": "https://www.openstreetmap.org/relation/3049430", "license": "ODbL 1.0 - © OpenStreetMap contributors",
    "retrieved": "2026-11-19", "simplification": "Douglas-Peucker 0.0003 gradi"}, "geometry": g}]}
(ROOT / "public/geography/atlas_laguna_venezia.geojson").write_text(json.dumps(fc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(geom.geom_type, round(geom.area, 5))
