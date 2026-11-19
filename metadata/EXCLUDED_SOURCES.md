# Fonti escluse dall'atlante Veneto (verifica riuso 2026-11-19, grok-05dev)

## IZSVe, report pubblico MIC (antibiotico-sensibilità veterinaria)
- Pagina: https://www.izsvenezie.it/temi/altri-temi/antibiotico-resistenza-sensibilita/report-pubblico/
- Contenuto: 10 riquadri Qlik Sense incorporati da https://sense2.izsvenezie.it/pub/single/?appid=7cf4b904-87fd-4681-a917-1a3ad903d417 ; nessuna funzione di esportazione dati, nessuna licenza indicata sul report.
- Note legali del sito (https://www.izsvenezie.it/note-legali/): "Testi e tabelle presenti in questo sito web sono distribuiti, dove non diversamente indicato, con Licenza Creative Commons 4.0 / Attribuzione – Non Commerciale (CC BY NC)". Sono esclusi "immagini, fotografie, video ed elaborazioni grafiche" non accompagnati da esplicito riferimento alla licenza e i contenuti non prodotti da IZSVe; per questi serve autorizzazione preventiva (comunicazione@izsvenezie.it).
- Esito: i grafici MIC sono elaborazioni grafiche senza riferimento esplicito alla licenza, quindi fuori dalla CC BY-NC. ESCLUSO come layer. Nessuna richiesta inviata (decisione di Alex: "altrimenti non usiamolo").

## ReSolVe Veneto, report consumo antibiotici veterinari per ULSS
- Pagina: https://www.resolveveneto.it/report-consumo-antibiotici/ (footer "Copyright 2024"; /credits/ risponde 404). Copia AULSS 3: https://www.aulss3.veneto.it/myportal/AU12VE/api/content/download?id=6797a017de90ce008caa80e1
- I PDF ULSS non riportano licenza; i dati derivano da ClassyFarm (Ministero della Salute).
- Esito: nessuna licenza esplicita. ESCLUSO come layer.

## Rapporto OsMed Regione Veneto 2024 (PDF)
- Pagina: https://www.aifa.gov.it/documents/20142/3610201/Veneto_Osmed_2024.pdf
- Contenuto valutato: Tabella 13, antibiotici 13,6 DDD/1.000 abitanti/die e 9,7 euro pro capite.
- Esito: il PDF non ha una licenza di riuso esplicita; è coperto dal copyright del sito AIFA, non dalla licenza open data. ESCLUSO. Il consumo regionale pubblicato nell'atlante è l'estratto J01 di AIFA Open Data 2024 (CC BY 4.0).

## Sintesi PPS-3 Veneto 2022 (SER)
- Pagina: https://www.ser-veneto.it/public/SintesiPPS3Veneto.pdf
- Contenuto valutato: 21 presidi, 6.266 pazienti; pazienti non COVID: ICA 8,2%, almeno un antimicrobico 43,7%.
- Esito: nessuna licenza di riuso esplicita. ESCLUSO per intero. Nessun dato di questa sintesi resta nel sito.

## Cataloghi open data
- dati.gov.it (CKAN): 0 dataset per "izsvenezie", "Venezie", "antimicrobico" (2026-11-19).
- dati.veneto.it: l'endpoint API restituisce HTML, non CKAN; nessun dataset AMR veterinario trovato.

Gli articoli scientifici con autori IZSVe restano nel catalogo della letteratura (citazione bibliografica, nessun dato ridistribuito).
