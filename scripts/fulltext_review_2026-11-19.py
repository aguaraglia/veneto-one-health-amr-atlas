import json,csv
from collections import Counter
rows=json.load(open('rows_pre_ft.json')); st=json.load(open('ft/status.json'))
H='healthcare_amr'; S='stewardship'; V='veterinaria_amr'; E='ambientale_amr'; C='animali_compagnia'
PROM={
'21827661':(H,'struttura','AOU Padova (teaching Hospital of Padua)',"Testo integrale: 'clinical isolates ... collected at the teaching Hospital of Padua'."),
'26116560':(H,'struttura','AOU Padova (Padua Teaching Hospital)',"Testo integrale: 'The Padua Teaching Hospital is a highly accessed tertiary care hospital with 1400 ... beds'."),
'38360651':(H,'struttura','AOU Padova, Oncoematologia pediatrica (Ospedale pediatrico di Padova); coorte di Genova fuori mappa',"Testo integrale: coorti separate 'Paediatric Hospital of Padua' e Gaslini Genova; si mappa solo Padova."),
'39847160':(V,'provincia','Provincia di Treviso (2 allevamenti di camelidi, non localizzati)',"Testo integrale, tabella aziende: 'Veneto Treviso' per le 2 aziende venete; si mappa la provincia, non le aziende."),
'39664895':(C,'provincia','Province di Padova, Rovigo, Venezia, Vicenza, Verona (rifugi non mappati); Trento/Bolzano fuori mappa',"Testo integrale: campioni per provincia (Padova, Rovigo, Venezia, Vicenza, Verona); ESBL/MRCPS/VRE tra i target; rifugi non mappati."),
'42655155':(S,'regione','Veneto (consenso Delphi interregionale ARCO II con FVG e Trentino-Alto Adige)',"Testo integrale: panel da Veneto, FVG, Trentino-AA; modello di governance AMS del Veneto; workshop a Padova."),
'43004478':(E,'area_nominata','Laguna di Venezia e costa di Pellestrina',"Testo integrale: microplastiche raccolte davanti all'isola di Pellestrina (Venezia); invecchiamento con acqua della Laguna di Venezia (Stazione idrobiologica di Chioggia)."),
}
KEEP={
'22475657':'Testo integrale non disponibile (nessun PMCID, nessun DOI). Resta dubbio: ambito antifungino.',
'29951378':"Testo integrale PMC6019954 (HTML PMC; XML Europe PMC errore 500): luogo confermato Ospedale San Camillo Treviso; resta dubbio solo per ambito antifungino (Lombardia non include antifungini).",
'39452659':"Testo integrale PMC11508697: luogo confermato AOU Padova ('Padova University Hospital', 2019-2023); resta dubbio solo per ambito antifungino.",
'40134816':"Testo integrale PMC11934064: luogo confermato AULSS 3 Serenissima (SS. Giovanni e Paolo, dell'Angelo, Chioggia, Mirano, Dolo); resta dubbio solo per ambito antifungino.",
'36902700':"Testo integrale PMC10003924: 1 caso in 1 ospedale veneto (giugno 2022), ospedale non nominato; ambito antifungino. Resta dubbio.",
'27807430':"Testo integrale PMC5069283: stabilimenti alimentari del Veneto (scala regione); resta dubbio solo per ambito biocidi (non antibiotici).",
'34680820':"Testo integrale PMC8532857: 'our Diabetic Foot Unit' senza nome di luogo nel testo (solo afferenza). Resta dubbio.",
'32131557':"Testo integrale PMC7143824: 36 allevamenti in Emilia-Romagna, Lombardia e Veneto senza quota veneta. Resta dubbio.",
'23237371':'Nessun testo OA in PMC; copia editore (Taylor & Francis) risponde 403, non aggirata. Resta dubbio.',
'25011666':'Nessun testo OA in PMC; copia editore (Taylor & Francis) risponde 403, non aggirata. Resta dubbio.',
'28412407':'Nessun testo in PMC; copia editore (IJID/Elsevier) non scaricabile (500/redirect JS). Resta dubbio.',
'31935535':'Nessun testo in PMC; copia editore (IJID/Elsevier) non scaricabile (500/redirect JS). Resta dubbio.',
'23433443':'Nessun testo OA (Unpaywall: chiuso). Resta dubbio.',
'24320689':'Nessun testo OA (Unpaywall: chiuso). Resta dubbio.',
'31225744':'Nessun testo OA (Unpaywall: chiuso). Resta dubbio.',
'32777624':'Nessun testo OA (Unpaywall: chiuso). Resta dubbio.',
}
EXC={'41901757':"Testo integrale PMC13029290: unico luogo veneto e il servizio di sequenziamento (BMR Genomics, Padova); nessuna area di studio veneta. Escluso."}
assert set(PROM)|set(KEEP)|set(EXC)==set(st), set(st)-(set(PROM)|set(KEEP)|set(EXC))
for r in rows:
    p=r['pmid']; r['fulltext_check']=''
    if p in PROM:
        s,sc,pl,n=PROM[p]; r.update(sector=s,scale=sc,place=pl,decision='include',reason='Promosso dopo verifica testo integrale.'); r['fulltext_check']=n
    elif p in KEEP: r['fulltext_check']=KEEP[p]
    elif p in EXC: r.update(decision='exclude'); r['fulltext_check']=EXC[p]
json.dump(rows,open('rows.json','w'),ensure_ascii=False)
cols=['pmid','doi','year','first_author','title','sector','scale','place','decision','reason','fulltext_check','pmid_verified','doi_verified']
with open('2026-11-19-atlante-amr-veneto-studi.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader(); [w.writerow(r) for r in rows]
inc=[r for r in rows if r['decision']=='include']
print(Counter(r['decision'] for r in rows)); print(Counter(r['sector'] for r in inc)); print(Counter(r['scale'] for r in inc))
