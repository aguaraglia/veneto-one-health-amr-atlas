(() => {
  'use strict';

  const config = window.AMR_ATLAS_CONFIG;
  if (!config) {
    document.body.innerHTML = '<main><h1>Configurazione mancante</h1><p>Impossibile avviare l\'atlante.</p></main>';
    return;
  }

  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));

  const setText = (id, value) => {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
  };

  const fetchJson = async path => {
    const response = await fetch(path, { cache: 'no-store' });
    if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
    return response.json();
  };

  const publicRecords = catalog => (catalog.records || catalog.layers || [])
    .filter(record => record.publication_status === 'public_approved');

  const featureColor = (feature, layerConfig) => {
    const scale = Array.isArray(layerConfig.colorScale) ? layerConfig.colorScale : [];
    const property = layerConfig.valueProperty;
    const value = property ? Number((feature.properties || {})[property]) : NaN;
    if (!scale.length || !Number.isFinite(value)) return layerConfig.fillColor || layerConfig.color || '#2d7d61';
    const ordered = scale.slice().sort((a, b) => Number(a.max) - Number(b.max));
    const match = ordered.find(item => value <= Number(item.max));
    return (match || ordered[ordered.length - 1]).color;
  };

  const popupLabel = (field, layerConfig) => {
    const labels = layerConfig.popupLabels || {};
    return labels[field] || field;
  };

  const splitParts = value => String(value ?? '').split(/\s+\|\s+/).map(part => part.trim()).filter(Boolean);

  const doiLink = value => {
    const raw = String(value || '').trim();
    if (!raw) return 'DOI non assegnato in PubMed';
    const href = /^10\.\d+\//.test(raw) ? `https://doi.org/${raw}` : raw;
    if (!/^https?:\/\//.test(href)) return escapeHtml(raw);
    const label = /pubmed\.ncbi\.nlm\.nih\.gov/.test(href)
      ? 'PubMed (DOI non assegnato)'
      : href.replace(/^https?:\/\/(?:dx\.)?doi\.org\//, '');
    return `<a href="${escapeHtml(href)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`;
  };

  const studyPopup = (props, layerConfig) => {
    const titles = splitParts(props.title);
    const dois = splitParts(props.doi);
    const authors = splitParts(props.authors);
    const years = splitParts(props.year);
    const caveat = props.geography_note || 'Il segnaposto indica dove è stato condotto lo studio, non una prevalenza.';
    const studyCount = Math.max(titles.length, dois.length, 1);
    const studies = [];
    for (let index = 0; index < studyCount; index += 1) {
      const title = titles[index] || titles[0] || 'Studio pubblicato';
      const doi = dois[index] || (dois.length === 1 ? dois[0] : '');
      const meta = [authors[index] || '', years[index] || ''].filter(Boolean).join(' · ');
      studies.push(`<li><strong>${escapeHtml(title)}</strong>${meta ? `<br><small>${escapeHtml(meta)}</small>` : ''}<br>${doiLink(doi)}</li>`);
    }
    const contextFields = ['geography_level', 'geography_basis', 'sector', 'organism']
      .filter(field => props[field] !== undefined && props[field] !== null && props[field] !== '')
      .map(field => `<div><strong>${escapeHtml(popupLabel(field, layerConfig))}</strong><br>${escapeHtml(props[field])}</div>`)
      .join('');
    const heading = props[layerConfig.labelProperty] || layerConfig.label;
    return `<div class="map-popup"><h3>${escapeHtml(heading)}</h3><p class="map-caveat">${escapeHtml(caveat)}</p><div><strong>Studi</strong><ol class="map-studies">${studies.join('')}</ol></div>${contextFields}</div>`;
  };

  document.title = `${config.title} · AMR Atlas`;
  setText('atlas-region-name', config.regionName);
  setText('atlas-title', config.title);
  setText('atlas-short-name', config.shortName);
  setText('atlas-status-label', config.dataStatusLabel);

  async function renderEvidenceDirectory() {
    const root = document.getElementById('evidence-root');
    if (!root) return;
    try {
      const catalog = await fetchJson(config.catalogs.evidence);
      const approved = publicRecords(catalog);
      const candidates = (catalog.records || []).filter(item => item.publication_status !== 'public_approved');
      const approvedHtml = approved.length
        ? approved.map(record => `<article class="directory-row"><span><strong>${escapeHtml(record.title)}</strong><small>${escapeHtml(record.period || 'Periodo non indicato')} · ${escapeHtml(record.geography || config.regionName)}</small></span><span>${escapeHtml(record.evidence_type || 'evidenza')}</span></article>`).join('')
        : '<p class="empty-filter">Nessun dataset AMR è ancora approvato per la pubblicazione.</p>';
      const candidateHtml = candidates.length
        ? candidates.map(record => `<article class="directory-row"><span><strong>${escapeHtml(record.title)}</strong><small>${escapeHtml(record.publisher || '')}</small></span><span>non pubblicato · ${escapeHtml(record.publication_status)}</span></article>`).join('')
        : '<p class="empty-filter">Nessuna fonte candidata registrata.</p>';
      root.innerHTML = `<div class="directory-layout"><section><h2>Evidenze pubbliche</h2><div class="directory-list">${approvedHtml}</div></section><section><h2>Registro di preparazione</h2><p>Le voci seguenti sono piste di lavoro e non dati dell\'atlante.</p><div class="directory-list">${candidateHtml}</div></section></div>`;
    } catch (error) {
      root.innerHTML = `<p class="empty-filter">Catalogo non disponibile: ${escapeHtml(error.message)}</p>`;
    }
  }

  async function initMap() {
    const mapNode = document.getElementById('map');
    if (!mapNode || typeof L === 'undefined') return;

    const map = L.map(mapNode, { zoomControl: true }).setView(config.map.center, config.map.zoom);
    const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors · Laguna di Venezia &copy; <a href="https://www.openstreetmap.org/relation/3049430">OpenStreetMap</a> contributors, ODbL'
    }).addTo(map);
    const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri'
    });

    const overlayControl = L.control.layers({ OpenStreetMap: osm, Satellite: satellite }, {}, { collapsed: false }).addTo(map);
    const reading = L.control({ position: 'bottomright' });
    reading.onAdd = () => {
      const div = L.DomUtil.create('div', 'map-reading-control');
      div.innerHTML = 'Aree vuote: <strong>nessuna evidenza pubblicata</strong>, non resistenza zero.';
      return div;
    };
    reading.addTo(map);
    const loaded = [];
    const errors = [];
    const studyPanes = [
      ['amr-region', 410],
      ['amr-province', 420],
      ['amr-area', 430],
      ['amr-point', 450]
    ];
    studyPanes.forEach(([name, zIndex]) => {
      map.createPane(name);
      map.getPane(name).style.zIndex = String(zIndex);
    });
    const paneForFeature = feature => {
      const type = feature.geometry && feature.geometry.type;
      if (type === 'Point' || type === 'MultiPoint') return 'amr-point';
      const level = String((feature.properties || {}).geography_level || '');
      if (level === 'regione') return 'amr-region';
      if (level === 'provincia') return 'amr-province';
      return 'amr-area';
    };

    try {
      const catalog = await fetchJson(config.catalogs.layers);
      const approvedLayers = publicRecords(catalog).filter(layer => layer.overviewCount === 'evidence');
      for (const layerConfig of approvedLayers) {
        try {
          const geojson = await fetchJson(layerConfig.file);
          if (geojson.type !== 'FeatureCollection') throw new Error('non e\' un FeatureCollection');
          const buckets = { 'amr-region': [], 'amr-province': [], 'amr-area': [], 'amr-point': [] };
          (geojson.features || []).forEach(feature => buckets[paneForFeature(feature)].push(feature));
          const parts = studyPanes.map(([pane]) => {
            if (!buckets[pane].length) return null;
            return L.geoJSON({ type: 'FeatureCollection', features: buckets[pane] }, {
              pane,
              style: feature => ({
                color: layerConfig.color || '#2d7d61',
                weight: Number(layerConfig.weight || 1.2),
                fillColor: featureColor(feature, layerConfig),
                fillOpacity: Number(layerConfig.fillOpacity ?? 0.12)
              }),
              pointToLayer: (feature, latlng) => L.circleMarker(latlng, {
                pane: 'amr-point',
                radius: Number(layerConfig.radius || 6),
                color: layerConfig.color || '#2d7d61',
                fillColor: layerConfig.fillColor || layerConfig.color || '#2d7d61',
                fillOpacity: 0.9,
                weight: 1
              }),
              onEachFeature: (feature, featureLayer) => {
                featureLayer.bindPopup(studyPopup(feature.properties || {}, layerConfig), { maxWidth: 360 });
              }
            });
          }).filter(Boolean);
          const layer = L.featureGroup(parts);
          overlayControl.addOverlay(layer, layerConfig.label);
          if (layerConfig.defaultVisible) layer.addTo(map);
          loaded.push({ config: layerConfig, layer, count: (geojson.features || []).length });
        } catch (error) {
          errors.push(`${layerConfig.id}: ${error.message}`);
        }
      }
    } catch (error) {
      errors.push(error.message);
    }

    const explicitEvidence = loaded.some(item => item.config.overviewCount === 'evidence');
    const countsInOverview = (layerConfig) => {
      if (layerConfig.overviewCount === 'evidence') return true;
      if (explicitEvidence || layerConfig.overviewCount === 'context') return false;
      const id = String(layerConfig.id || '').toLowerCase();
      return !/municipalit|provinces|region_istat|hydro|wastewater|sira_|sire_/.test(id);
    };
    const refreshLocalized = () => {
      const total = loaded.reduce((sum, item) => (
        map.hasLayer(item.layer) && countsInOverview(item.config) ? sum + item.count : sum
      ), 0);
      const visible = loaded.filter(item => map.hasLayer(item.layer)).length;
      setText('metric-visible', total.toLocaleString('it-IT'));
      setText('metric-sources', visible.toLocaleString('it-IT'));
      setText('overview-localized', total.toLocaleString('it-IT'));
    };
    map.on('overlayadd', refreshLocalized);
    map.on('overlayremove', refreshLocalized);
    refreshLocalized();
    const polygons = [];
    loaded.forEach(item => item.layer.eachLayer(group => group.eachLayer(featureLayer => {
      if (!featureLayer.getBounds || featureLayer.getLatLng) return;
      try {
        const bounds = featureLayer.getBounds();
        if (!bounds || !bounds.isValid()) return;
        const area = Math.abs(bounds.getNorth() - bounds.getSouth()) * Math.abs(bounds.getEast() - bounds.getWest());
        polygons.push({ featureLayer, area });
      } catch (error) { /* skip layers without bounds */ }
    })));
    polygons.sort((a, b) => b.area - a.area);
    polygons.forEach(item => item.featureLayer.bringToFront());
    const framed = loaded.map(item => item.layer).filter(layer => {
      try { return layer.getBounds && layer.getBounds().isValid(); } catch (error) { return false; }
    });
    if (framed.length) map.fitBounds(L.featureGroup(framed).getBounds(), { padding: [28, 28] });
    setText('overview-layers', loaded.length.toLocaleString('it-IT'));
    setText('status', errors.length ? `${loaded.length} layer caricati · ${errors.length} non disponibili` : `${loaded.length} layer pubblici caricati`);

    const empty = document.getElementById('map-empty-state');
    if (empty) empty.hidden = loaded.length > 0;
  }

  async function renderDashboardEvidence() {
    const root = document.getElementById('dashboard-evidence');
    if (!root) return;
    try {
      const catalog = await fetchJson(config.catalogs.evidence);
      const approved = publicRecords(catalog);
      root.innerHTML = approved.length
        ? approved.map(record => `<article class="evidence-card"><strong>${escapeHtml(record.title)}</strong><br><small>${escapeHtml(record.period || '')} · ${escapeHtml(record.geography || config.regionName)}</small><p>${escapeHtml(record.summary || record.note || '')}</p></article>`).join('')
        : '<div class="evidence-card"><strong>Dati in preparazione</strong><p>Nessuna evidenza regionale e\' pubblicata finche\' fonte, licenza, granularita\' e limiti non risultano verificati.</p></div>';
    } catch (error) {
      root.innerHTML = `<div class="evidence-card"><strong>Catalogo non disponibile</strong><p>${escapeHtml(error.message)}</p></div>`;
    }
  }

  renderEvidenceDirectory();
  renderDashboardEvidence();
  initMap();
})();
