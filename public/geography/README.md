# Geografia pubblica

La cartografia pubblica dell'edizione Veneto comprende:

- `atlas_region.geojson`: confine regionale ISTAT 2026;
- `atlas_provinces.geojson`: 7 province/città metropolitana ISTAT 2026;
- `atlas_municipalities.geojson`: 560 comuni ISTAT al 1/1/2026 (la fusione Castegnero-Nanto del 21/02/2026 non è ancora nel file);
- `atlas_laguna_venezia.geojson`: poligono della Laguna di Venezia da OpenStreetMap (relation 3049430), ODbL 1.0, semplificato.

Gli studi della letteratura curata sono in layer distinti sotto `public/data/`,
non in questi confini di base. Un punto è una struttura nominata. Un poligono
è un comune, una provincia o un'area nominata (Laguna). Il contorno regionale
è riservato agli studi che non dichiarano una scala più fine. Nessuna azienda,
canile o rifugio è localizzato.
