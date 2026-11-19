# Ambito pubblico del Veneto One Health AMR Atlas

Edizione `ven_amr_atlas`, pubblicata da Codex Vitae ETS. Il runtime carica soltanto le fonti `public_approved`.

La base pubblica comprende:

- confini ISTAT generalizzati al 1 gennaio 2026, già in UTF-8: 560 comuni, 7 province (la Venezia è Città metropolitana) e la regione;
- sei indicatori AR-ISS 2024 aggregati per il Veneto (sangue e liquor), con numerosità, percentuale, IC 95% e copertura regionale del 71,6%; nessun downscaling;
- consumo e spesa di antibiotici del rapporto regionale OsMed Anno 2024, Tabella 13 (13,6 DDD/1.000 abitanti/die): consumo, non resistenza;
- sintesi PPS-3 2022 della Regione del Veneto / SER (21 presidi, 6.266 pazienti; pazienti non COVID: ICA 8,2%, almeno un antimicrobico 43,7%);
- poligono della Laguna di Venezia da OpenStreetMap (relation 3049430), ODbL 1.0, © OpenStreetMap contributors;
- sei strutture sanitarie nominate, georiferite con Nominatim (ODbL);
- 46 studi con collegamento territoriale esplicito al Veneto (19 novembre 2026), nei sei layer di evidenza. Il segnaposto indica dove è stato condotto lo studio, non una prevalenza. Le aree senza segnaposto sono nessuna evidenza pubblicata, non resistenza zero.

Non sono pubblicati il cruscotto MIC dell'IZSVe né i report ReSolVe/ULSS sul consumo veterinario: vedi `EXCLUDED_SOURCES.md`. Non ci sono record individuali, identificativi di paziente o campione, né coordinate di aziende, canili o rifugi.
