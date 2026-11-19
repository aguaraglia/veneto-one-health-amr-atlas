# Veneto One Health AMR Atlas

Edizione regionale `ven_amr_atlas`, pubblicata da Codex Vitae ETS sulla stessa
base dell'edizione Lombardia.

Sito pubblico: <https://aguaraglia.github.io/veneto-one-health-amr-atlas/>

## Stato

Letteratura scientifica del 19 novembre 2026: 46 studi con collegamento
territoriale esplicito al Veneto, in sei layer (AMR umana, veterinaria,
alimentare, ambientale, fauna selvatica, studi a scala regionale). I layer
alimentare e fauna selvatica sono vuoti: l'area senza segnaposto è nessuna
evidenza pubblicata, non resistenza zero. Ogni popup cita lo studio e il DOI
(o il record PubMed se il DOI non è assegnato) e ricorda che il segnaposto è
il luogo dello studio, non una prevalenza.

Fonti istituzionali pubbliche: AR-ISS 2024, OsMed Veneto 2024 (Tabella 13) e
PPS-3 2022. Confini ISTAT 2026 (560 comuni, 7 province, regione). Laguna di
Venezia © OpenStreetMap contributors, ODbL. Il cruscotto MIC IZSVe e i report
ReSolVe/ULSS sono esclusi: vedi `metadata/EXCLUDED_SOURCES.md`.

Il conteggio in homepage legge `public/data/literature-catalog.json` (46).

## Pagine

Sorgente su `main`. Il sito statico è pubblicato dal branch `gh-pages`
(GitHub Pages, cartella `/`). Nessun file `CNAME`. Analitica: GoatCounter
`https://atlanteamr.goatcounter.com/count`, come l'edizione Lombardia.

## Build locale

```bash
python3 -m http.server 8000
```

Aprire `http://localhost:8000/`.

Per rigenerare i dati pubblici servono gli input in `raw/` e, per i confini,
l'archivio ISTAT indicato in `metadata/SNAPSHOTS.tsv`:

```bash
pip install -r requirements-geodata.txt
python3 scripts/build_istat_geography.py --source-root <Limiti01012026_g> --output-root public/geography
python3 scripts/build_laguna_polygon.py
python3 scripts/build_literature_catalog.py
python3 scripts/build_study_evidence_layers.py
```

## Directory

- `public/`: dati e asset approvati per il sito;
- `metadata/`: fonti, snapshot e fonti escluse;
- `raw/`: curatela, esummary e risposte Nominatim;
- `scripts/`: ricostruzione del catalogo e dei layer;
- `private/`: nessun dato riservato in questa edizione.
