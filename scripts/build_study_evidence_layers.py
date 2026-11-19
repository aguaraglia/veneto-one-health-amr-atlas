#!/usr/bin/env python3
"""Build Veneto study evidence layers from the curated literature catalog.

Geometries come from the ISTAT 2026 boundaries of this edition, from a named
facility geocoded on OpenStreetMap Nominatim (1 req/s, 2026-11-19, raw
responses in raw/nominatim/), or from the OpenStreetMap Laguna di Venezia
polygon. The script does not geocode farms, kennels or shelters and does not
invent a site the catalog does not name.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = "Il segnaposto indica dove è stato condotto lo studio, non una prevalenza."
SECTOR = {
    "healthcare_amr": "AMR clinica",
    "human_antimicrobial_use": "Consumo di antimicrobici",
    "antimicrobial_stewardship": "Stewardship antimicrobica",
    "veterinary_amr": "AMR veterinaria",
    "companion_animal_amr": "AMR negli animali d'affezione",
    "environmental_amr": "AMR ambientale",
    "foodborne_amr": "AMR alimentare",
    "wildlife_amr": "AMR nella fauna selvatica",
}
# Nominatim results checked on 2026-11-19 (raw/nominatim/results_2026-11-19.json).
# Coordinates are the facility returned for the named institution, not a sample.
POINTS = {
    "aou_padova": (11.8873455, 45.4036585, "Azienda Ospedale-Università Padova",
                   "OpenStreetMap Nominatim: Ospedale Giustinianeo, Via Ospedale Civile, Padova. Punto del polo ospedaliero centrale dell'AOU; i reparti pediatrici sono nello stesso polo."),
    "aoui_verona": (10.9841333, 45.4528634, "Azienda Ospedaliera Universitaria Integrata Verona",
                    "OpenStreetMap Nominatim: Ospedale Civile Maggiore, Piazzale Aristide Stefani 1, Borgo Trento, Verona. L'AOUI comprende anche il polo di Borgo Roma; il punto è la sede principale dell'ente nominato."),
    "angelo_mestre": (12.2227042, 45.5132138, "Ospedale dell'Angelo, Mestre (Venezia)",
                      "OpenStreetMap Nominatim: Ospedale dell'Angelo, Via Don Luigi Giussani, Zelarino, Venezia."),
    "san_bortolo": (11.5434513, 45.5575782, "Ospedale San Bortolo, Vicenza",
                    "OpenStreetMap Nominatim: Ospedale Civile di Vicenza \"San Bortolo\", Viale Bartolomeo d'Alviano, Vicenza."),
    "ca_foncello": (12.2607160, 45.6583551, "Ospedale Ca' Foncello, Treviso",
                    "OpenStreetMap Nominatim: Ospedale Regionale \"Ca' Foncello\", Via Cittadella della Salute, Treviso."),
    "negrar": (10.9368751, 45.5297611, "IRCCS Ospedale Sacro Cuore Don Calabria, Negrar di Valpolicella",
               "OpenStreetMap Nominatim: Ospedale Sacro Cuore Don Calabria, Piazza Roma, Negrar di Valpolicella."),
}
ORGANISM = {
    "pubmed_20356715": "Enterobacteriaceae, qnrB19", "pubmed_20956871": "E. coli ESBL da urine",
    "pubmed_21792559": "S. haemolyticus resistente al linezolid", "pubmed_22546764": "K. pneumoniae KPC-3",
    "pubmed_22800501": "K. pneumoniae KPC-3", "pubmed_22830638": "stafilococchi coagulasi-negativi resistenti al linezolid",
    "pubmed_23118475": "K. pneumoniae ST147, blaLAP-2, qnrS1", "pubmed_23659538": "K. pneumoniae OXA-48",
    "pubmed_23962153": "K. pneumoniae resistente ai carbapenemi", "pubmed_24571419": "K. pneumoniae ST512 ed E. coli ST43, KPC-3",
    "pubmed_27301585": "uso di antimicrobici in terapia intensiva", "pubmed_30028474": "Listeria monocytogenes (isolati umani)",
    "pubmed_31924425": "K. pneumoniae ST14 e ST512 resistenti ai carbapenemi", "pubmed_32314259": "batteribilia resistente alla profilassi",
    "pubmed_32575542": "profilassi perioperatoria pediatrica", "pubmed_33925182": "antibiotici nella bronchiolite pediatrica",
    "pubmed_33933164": "uropatogeni pediatrici (WISCA)", "pubmed_35850288": "Gram-negativi MDR ed ESBL",
    "pubmed_36795664": "organismi multiresistenti (MDRO)", "pubmed_37065200": "Mycoplasma genitalium, mutazioni di resistenza",
    "pubmed_37110408": "A. baumannii resistente ai carbapenemi", "pubmed_38360651": "batteri da neutropenia febbrile (WISCA)",
    "pubmed_38433960": "batteri dei sedimenti lagunari (metagenomi)", "pubmed_38481174": "colonizzazioni da Gram-negativi",
    "pubmed_38791647": "Escherichia coli (vitelli)", "pubmed_39316397": "uso di antibiotici (PPS e dati amministrativi)",
    "pubmed_39507942": "antibiotici in area acuta pediatrica", "pubmed_39592720": "antimicrobici in oncoematologia pediatrica",
    "pubmed_39594900": "antibiotici nelle infezioni di cute e tessuti molli", "pubmed_39664895": "E. coli ESBL, stafilococchi MRCP, VRE (cani e gatti)",
    "pubmed_39847160": "E. coli ESBL (camelidi)", "pubmed_40005771": "governance AMS/IPC",
    "pubmed_40032196": "antimicrobici in terapia intensiva pediatrica", "pubmed_40269796": "antibiotici in gravidanza",
    "pubmed_40565484": "K. pneumoniae NDM", "pubmed_40671286": "K. pneumoniae NDM resistente a cefiderocol",
    "pubmed_40723986": "antimicrobici in medicina interna", "pubmed_41274603": "K. pneumoniae ST395, OXA-48, capsula K2",
    "pubmed_41534477": "Streptococcus pneumoniae", "pubmed_41619834": "Enterococcus faecium",
    "pubmed_42650717": "conoscenze e pratiche su AMR del personale", "pubmed_42964188": "organismi multiresistenti (colonizzazione rettale)",
    "pubmed_43004478": "geni di resistenza su microplastiche", "pubmed_21827661": "Enterobacteriaceae, aac(6')-Ib-cr",
    "pubmed_26116560": "K. pneumoniae KPC, resistenza a colistina", "pubmed_42655155": "governance AMS/IPC (Delphi)",
}

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def feature(geometry, place, level, basis, studies, extra_note=""):
    note = NOTE + (" " + extra_note if extra_note else "")
    return {"type": "Feature", "geometry": geometry, "properties": {
        "place": place, "geography_level": level, "geography_basis": basis,
        "study_count": len(studies), "study_ids": "; ".join(s["id"] for s in studies),
        "authors": " | ".join(s["authors"] for s in studies), "year": " | ".join(s["year"] for s in studies),
        "title": " | ".join(s["title"] for s in studies), "sector": " | ".join(s["sector"] for s in studies),
        "organism": " | ".join(s["organism"] for s in studies), "doi": " | ".join(s["doi"] for s in studies),
        "geography_note": note}}

def point(key):
    lon, lat, _l, _s = POINTS[key]
    return {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]}

def place_basis(key, text):
    return f"{text} {POINTS[key][3]}"

def merge(geoms):
    if len(geoms) == 1:
        return geoms[0]
    polys = []
    for g in geoms:
        polys.extend([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"])
    return {"type": "MultiPolygon", "coordinates": polys}

def main():
    catalog = load_json(ROOT / "public/data/literature-catalog.json")
    by_id = {r["id"]: r for r in catalog["records"]}
    miss = set(by_id) - set(ORGANISM)
    if miss:
        raise SystemExit("Organismo mancante: " + ", ".join(sorted(miss)))

    def card(sid):
        r = by_id[sid]; doi = r.get("doi") or ""
        return {"id": sid, "authors": r["authors"], "year": str(r["year"]), "title": r["title"].rstrip("."),
                "sector": SECTOR[r["scope"]], "organism": ORGANISM[sid],
                "doi": f"https://doi.org/{doi}" if doi else r["source_url"]}

    mun = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_municipalities.geojson")["features"]}
    prov = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_provinces.geojson")["features"]}
    region = load_json(ROOT / "public/geography/atlas_region.geojson")["features"][0]["geometry"]
    laguna = load_json(ROOT / "public/geography/atlas_laguna_venezia.geojson")["features"][0]["geometry"]

    layers = {k: [] for k in ["human", "veterinary", "food", "environment", "wildlife", "regional"]}
    placed = {}

    def add(layer, ids, geometry, place, level, basis, extra=""):
        for sid in ids:
            placed[sid] = placed.get(sid, "") + f"{level}: {place}; "
        layers[layer].append(feature(geometry, place, level, basis, [card(s) for s in ids], extra))

    P = lambda *ids: [f"pubmed_{i}" for i in ids]
    add("human", P("20356715", "21827661", "26116560", "33933164", "35850288", "37110408", "38481174", "40671286", "41619834",
                   "38360651", "32575542", "33925182", "39507942", "39592720", "39594900", "40032196"),
        point("aou_padova"), POINTS["aou_padova"][2], "struttura",
        place_basis("aou_padova", "Azienda ospedaliera o reparto padovano nominato nell'abstract o nel testo integrale."))
    add("human", P("21792559", "22546764", "23118475", "24571419", "31924425", "36795664", "37065200", "40565484", "42964188"),
        point("aoui_verona"), POINTS["aoui_verona"][2], "struttura",
        place_basis("aoui_verona", "Ospedale universitario di Verona nominato nell'abstract."))
    add("human", P("20956871", "33933164"), point("angelo_mestre"), POINTS["angelo_mestre"][2], "struttura",
        place_basis("angelo_mestre", "Ospedale nominato nell'abstract."))
    add("human", P("22830638"), point("san_bortolo"), POINTS["san_bortolo"][2], "struttura",
        place_basis("san_bortolo", "Ospedale di Vicenza nominato nell'abstract."))
    add("human", P("32314259"), point("ca_foncello"), POINTS["ca_foncello"][2], "struttura",
        place_basis("ca_foncello", "Ospedale di Treviso nominato nell'abstract."))
    add("human", P("23659538"), point("negrar"), POINTS["negrar"][2], "struttura",
        place_basis("negrar", "Ospedale di Negrar nominato nell'abstract."))
    add("human", P("22800501", "40723986", "42650717"), mun["Padova"], "Padova", "comune",
        "L'abstract colloca lo studio a Padova (ospedale terziario o due ospedali) senza nominare la struttura. Poligono comunale ISTAT 2026.")
    add("human", P("23962153"), mun["Verona"], "Verona", "comune",
        "L'abstract colloca lo studio in due ospedali di Verona non nominati. Poligono comunale ISTAT 2026.")
    add("human", P("41274603"), prov["Venezia"], "Città metropolitana di Venezia", "provincia",
        "Tre ospedali e comunità della provincia di Venezia; ospedali non distinti nel collegamento usato qui. Poligono ISTAT 2026.")
    add("veterinary", P("39847160"), prov["Treviso"], "Provincia di Treviso", "provincia",
        "Due allevamenti di camelidi in provincia di Treviso (tabella del testo integrale). Nessuna azienda è localizzata.")
    names5 = ["Padova", "Rovigo", "Venezia", "Vicenza", "Verona"]
    add("veterinary", P("39664895"), merge([prov[n] for n in names5]), "Province di Padova, Rovigo, Venezia, Vicenza e Verona", "provincia",
        "Cani e gatti di rifugi e colonie in cinque province venete (più Trento e Bolzano, fuori mappa). Nessun rifugio è localizzato.")
    add("environment", P("38433960", "43004478"), laguna, "Laguna di Venezia", "area nominata",
        "Laguna di Venezia nominata nell'abstract o nel testo integrale (sedimenti lagunari; microplastiche davanti a Pellestrina e acqua lagunare). Poligono OpenStreetMap, ODbL.")
    add("regional", P("27301585", "39316397", "40269796", "30028474", "41534477", "38791647", "40005771", "42655155"),
        region, "Veneto", "regione",
        "Gli autori dichiarano il Veneto, più ospedali o aziende non nominati, o una rete regionale. Il contorno regionale non è un punto di misura.")

    if set(placed) != set(by_id):
        raise SystemExit(f"Copertura incompleta. Mancanti: {sorted(set(by_id)-set(placed))}. Extra: {sorted(set(placed)-set(by_id))}")
    names = {"human": "human_amr_evidence.geojson", "veterinary": "veterinary_amr_evidence.geojson",
             "food": "food_chain_amr_evidence.geojson", "environment": "environmental_amr_evidence.geojson",
             "wildlife": "wildlife_amr_evidence.geojson", "regional": "regional_study_outline.geojson"}
    for k, fn in names.items():
        (ROOT / "public/data" / fn).write_text(json.dumps({"type": "FeatureCollection", "features": layers[k]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(fn, len(layers[k]), sum(f["properties"]["study_count"] for f in layers[k]))
    print("studi collocati:", len(placed))

if __name__ == "__main__":
    main()
