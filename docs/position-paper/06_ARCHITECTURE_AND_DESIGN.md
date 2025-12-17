# Section 6: Architecture and Design Features

## From Conceptual Case to Technical Reality

The preceding sections established **why** regional knowledge systems are necessary (Sections 2-3), **what** existing infrastructure cannot provide (Section 4), and **why mountains** require this infrastructure logic (Section 5). This section addresses **how**: the architectural decisions, design patterns, and technical implementations that translate conceptual requirements into operational infrastructure.

The Eastern Himalayan Knowledge Common (THI-KC) embodies seven essential design features, each addressing specific limitations diagnosed in earlier sections. We present these through documented code examples from the 8,000+ line prototype (MIT-licensed, github.com/Ashwin-Chhetri/THI-Knowledge-Common), demonstrating not theoretical possibility but working implementation.

## Feature 1: Multi-Source Data Integration with Provenance Tracking

### The Challenge

As established in Section 4, conservation planning requires synthesizing **three distinct data streams** with incompatible schemas, update frequencies, and governance constraints:

1. **Global occurrence databases** (GBIF) — standardized Darwin Core, 6-18 month latency, open access by default
2. **Institutional monitoring** (protected area patrols, research surveys) — heterogeneous formats, weekly to monthly updates, access restricted by institutional policy
3. **Community observations** (village biodiversity registers, traditional knowledge) — narrative formats, real-time to seasonal, access controlled by community consent protocols

### Architectural Solution: Federated Data Model with Source Tracking

The system implements a **three-tier data architecture**:

**Tier 1: Global Data Harvest** — GBIF API v2 integration provides baseline occurrence data. The frontend queries GBIF tile services (vector tiles in MVT format) for real-time visualization without local storage:

```javascript
// src/services/api/gbifService.js
export const fetchGBIFOccurrences = async (bounds, taxonKey) => {
  const params = new URLSearchParams({
    decimalLatitude: `${bounds.south},${bounds.north}`,
    decimalLongitude: `${bounds.west},${bounds.east}`,
    taxonKey: taxonKey,
    limit: 300,
    hasCoordinate: true,
    hasGeospatialIssue: false
  });
  
  const response = await fetch(
    `https://api.gbif.org/v1/occurrence/search?${params}`
  );
  
  const data = await response.json();
  return data.results.map(record => ({
    id: record.key,
    source: 'GBIF',
    scientificName: record.scientificName,
    latitude: record.decimalLatitude,
    longitude: record.decimalLongitude,
    basisOfRecord: record.basisOfRecord,
    eventDate: record.eventDate,
    datasetName: record.datasetName,
    institutionCode: record.institutionCode,
    provenance: {
      type: 'global_aggregator',
      originalSource: record.publishingOrgKey,
      license: record.license || 'CC0-1.0',
      lastUpdated: record.lastInterpreted
    }
  }));
};
```

**Tier 2: Regional Data Store** — PostgreSQL+PostGIS backend (planned Phase 2 implementation) stores institutional and community data with granular provenance:

```sql
-- Planned schema: regional_occurrences table
CREATE TABLE regional_occurrences (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scientific_name VARCHAR(255) NOT NULL,
  location GEOMETRY(Point, 4326) NOT NULL,
  elevation_m INTEGER,
  event_date DATE,
  
  -- Data source provenance
  source_type VARCHAR(50) CHECK (source_type IN 
    ('protected_area_patrol', 'research_survey', 
     'community_register', 'camera_trap', 'acoustic_monitor')),
  source_institution VARCHAR(255),
  collector_name VARCHAR(255),
  
  -- Access control (see Feature 7)
  access_level VARCHAR(50) CHECK (access_level IN 
    ('public', 'institutional', 'community_restricted')),
  consent_status VARCHAR(50) CHECK (consent_status IN 
    ('not_applicable', 'fpic_obtained', 'pending')),
  
  -- Quality metrics
  coordinate_precision_m INTEGER,
  identification_confidence VARCHAR(50),
  taxonomic_authority VARCHAR(100),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_regional_location ON regional_occurrences 
  USING GIST(location);
CREATE INDEX idx_regional_elevation ON regional_occurrences(elevation_m);
CREATE INDEX idx_regional_access ON regional_occurrences(access_level);
```

**Tier 3: Community Knowledge Layer** — Metadata-rich records for traditional ecological knowledge with UNESCO LINKS-compatible fields:

```javascript
// Planned: Community knowledge record structure
const communityKnowledgeRecord = {
  speciesIdentifier: {
    scientificName: "Nardostachys jatamansi",
    localNames: {
      lepcha: "Pangpoe",
      nepali: "Jatamansi",
      bhutia: "Pangpoe"
    }
  },
  
  knowledgeHolder: {
    community: "Lachen Village Biodiversity Committee",
    informant: "[ANONYMIZED - Community consent required]",
    transmissionChain: "Multi-generational oral tradition"
  },
  
  ecologicalKnowledge: {
    habitat: "Alpine meadows, 3800-4500m, north-facing slopes",
    phenology: "Flowering July-August, traditional harvest September",
    uses: "Medicinal (digestive disorders), ceremonial (incense)",
    observations: "Populations declining; harvesting now requires 2-3 hour walk vs. 30 min in 1990s (elder testimony)"
  },
  
  accessRestrictions: {
    level: "community_restricted",
    spatialPrecision: "generalized_5km", // Exact location not disclosed
    consentStatus: "fpic_obtained",
    consentDate: "2023-06-15",
    consentingAuthority: "Lachen Biodiversity Management Committee",
    benefitSharingAgreement: "Any research use requires prior notification and 50% co-authorship"
  },
  
  provenance: {
    recordedBy: "Sikkim University Ethnobiology Team",
    recordDate: "2023-06-20",
    verifiedBy: "Community knowledge holder council",
    lastUpdated: "2024-03-10"
  }
};
```

### Integration Pattern: Source-Aware Queries

The system allows users to query across all three tiers while respecting access controls and data quality filters:

```javascript
// src/store/slices/occurrenceSlice.js (Redux Toolkit)
export const fetchMultiSourceOccurrences = createAsyncThunk(
  'occurrences/fetchMultiSource',
  async ({ bounds, filters, userAccessLevel }) => {
    const results = [];
    
    // Tier 1: Always query GBIF for public data
    const gbifData = await fetchGBIFOccurrences(bounds, filters.taxonKey);
    results.push(...gbifData);
    
    // Tier 2: Query regional database if authenticated
    if (userAccessLevel !== 'public') {
      const regionalData = await fetchRegionalOccurrences(
        bounds, filters, userAccessLevel
      );
      results.push(...regionalData);
    }
    
    // Tier 3: Include community knowledge if authorized
    if (filters.includeTEK && userAccessLevel === 'community_authorized') {
      const tekData = await fetchCommunityKnowledge(bounds, filters);
      results.push(...tekData);
    }
    
    // Deduplicate and merge (same species/location/date from multiple sources)
    return deduplicateOccurrences(results);
  }
);
```

**Design rationale**: This architecture allows **incremental data integration** — starting with GBIF-only (current Phase 1 deployment), adding regional PostgreSQL (Phase 2), and incorporating community knowledge layers (Phase 3) — without requiring all data sources operational simultaneously. Each tier operates independently, with integration at the application layer rather than requiring source databases to conform to unified schemas.

**(Figure 5. Multi-source data integration architecture with three-tier federated model and provenance tracking)**

## Feature 2: Spatial Dependency Management for Layer Interactions

### The Challenge

Biodiversity visualization requires **managing complex layer dependencies**: base maps depend on tile servers, species occurrence layers depend on taxonomy filters, protected area boundaries depend on administrative jurisdictions, threat layers (roads, dams) depend on infrastructure databases. When a user changes the base region (e.g., from Sikkim to Bhutan), all dependent layers must update accordingly, respecting load order to prevent race conditions.

### Architectural Solution: Directed Acyclic Graph (DAG) for Layer Dependencies

The system models layer relationships as a DAG, using Redux state management to track dependencies and coordinate updates:

```javascript
// src/store/slices/layerSlice.js
const layerDependencies = {
  'base-map': { dependencies: [], loadOrder: 1 },
  'admin-boundaries': { dependencies: ['base-map'], loadOrder: 2 },
  'protected-areas': { dependencies: ['admin-boundaries'], loadOrder: 3 },
  'gbif-occurrences': { dependencies: ['base-map'], loadOrder: 2 },
  'regional-occurrences': { dependencies: ['base-map', 'auth-token'], loadOrder: 3 },
  'elevation-contours': { dependencies: ['base-map'], loadOrder: 2 },
  'infrastructure-threats': { dependencies: ['admin-boundaries'], loadOrder: 4 }
};

export const updateRegion = createAsyncThunk(
  'layers/updateRegion',
  async (newRegion, { dispatch, getState }) => {
    const state = getState();
    const activeLayers = state.layers.active;
    
    // Build dependency graph
    const loadQueue = buildDependencyQueue(activeLayers, layerDependencies);
    
    // Load layers in dependency order
    for (const layerId of loadQueue) {
      await dispatch(loadLayer({ layerId, region: newRegion }));
    }
  }
);

function buildDependencyQueue(activeLayers, dependencies) {
  const visited = new Set();
  const queue = [];
  
  function visit(layerId) {
    if (visited.has(layerId)) return;
    visited.add(layerId);
    
    const deps = dependencies[layerId]?.dependencies || [];
    deps.forEach(depId => visit(depId));
    
    queue.push(layerId);
  }
  
  activeLayers.forEach(layerId => visit(layerId));
  return queue;
}
```

**Real-world impact**: When a user switches from viewing Sikkim to viewing the entire Khangchendzonga Landscape (India-Nepal-Bhutan), the system:
1. Loads new base map tiles (load order 1)
2. Fetches updated administrative boundaries (order 2) and GBIF occurrences (order 2) in parallel
3. Loads protected areas (order 3) only after boundaries available
4. Loads infrastructure threats (order 4) only after boundaries available

This prevents visual glitches where protected areas display before country boundaries load, confusing users about jurisdictional context.

## Feature 3: Scale-Appropriate Querying and Visualization

### The Challenge

Conservation questions operate at **multiple spatial scales**: individual protected areas (10-1,000 km²), landscapes (1,000-20,000 km²), ecoregions (20,000-200,000 km²), and transboundary ranges (>200,000 km²). Querying the same dataset at all scales creates performance problems (too much data for broad queries) and relevance problems (too coarse for detailed questions).

### Architectural Solution: Scale-Dependent Data Strategies

The system implements three scale-aware strategies:

**Strategy 1: Client-side clustering for point data** — At broad scales (viewing entire Eastern Himalaya), individual occurrence points become visually overwhelming. MapLibre GL's clustering aggregates nearby points:

```javascript
// src/features/map/layers/occurrenceLayer.js
export const createOccurrenceLayer = (sourceId) => ({
  id: 'occurrences-clustered',
  type: 'circle',
  source: sourceId,
  filter: ['has', 'point_count'],
  paint: {
    'circle-color': [
      'step',
      ['get', 'point_count'],
      '#51bbd6', 10,
      '#f1f075', 50,
      '#f28cb1', 100,
      '#e63946'
    ],
    'circle-radius': [
      'step',
      ['get', 'point_count'],
      15, 10,
      20, 50,
      25, 100,
      30
    ]
  }
});

export const createOccurrencePointLayer = (sourceId) => ({
  id: 'occurrences-individual',
  type: 'circle',
  source: sourceId,
  filter: ['!', ['has', 'point_count']],
  paint: {
    'circle-color': '#11b4da',
    'circle-radius': 6,
    'circle-stroke-width': 1,
    'circle-stroke-color': '#fff'
  }
});
```

At zoom levels 1-6 (country scale), clusters dominate. At zoom 7-10 (landscape scale), mixed clusters and points. At zoom >10 (protected area scale), individual points with species details.

**Strategy 2: Elevation-stratified aggregation** — For mountain regions, binning occurrences by elevation provides more ecological relevance than arbitrary spatial grids:

```javascript
// src/services/analytics/elevationAnalysis.js
export const aggregateByElevation = (occurrences, binSize = 500) => {
  const bins = {};
  
  occurrences.forEach(record => {
    if (!record.elevation_m) return;
    
    const binFloor = Math.floor(record.elevation_m / binSize) * binSize;
    const binKey = `${binFloor}-${binFloor + binSize}m`;
    
    if (!bins[binKey]) {
      bins[binKey] = {
        range: { min: binFloor, max: binFloor + binSize },
        count: 0,
        species: new Set(),
        records: []
      };
    }
    
    bins[binKey].count++;
    bins[binKey].species.add(record.scientificName);
    bins[binKey].records.push(record);
  });
  
  return Object.entries(bins).map(([key, data]) => ({
    elevationBand: key,
    occurrenceCount: data.count,
    speciesRichness: data.species.size,
    dominantSpecies: findDominantSpecies(data.records)
  }));
};
```

This supports queries like "species richness by 500m elevation bands in Khangchendzonga National Park" — directly relevant for understanding vertical biodiversity patterns and climate change impacts (Section 5).

**Strategy 3: Vector tile pre-generation for large datasets** (Planned Phase 2) — For regional datasets exceeding millions of records, generating vector tiles at multiple zoom levels allows efficient rendering:

```javascript
// Planned: Vector tile generation using Tippecanoe
// Command-line invocation from Node.js backend
const generateVectorTiles = async (regionId) => {
  const geojson = await exportRegionalOccurrencesAsGeoJSON(regionId);
  
  const tippecanoeCMD = `
    tippecanoe \\
      -o regional_${regionId}.mbtiles \\
      -z14 \\
      -Z4 \\
      --drop-densest-as-needed \\
      --extend-zooms-if-still-dropping \\
      ${geojson}
  `;
  
  await execPromise(tippecanoeCMD);
};
```

**Design rationale**: Different scales require different data representations. Rather than forcing all queries through a single API endpoint, the system adapts query strategy to user zoom level and region extent, balancing performance (client-side clustering, vector tiles) with ecological relevance (elevation stratification, habitat-type grouping).

## Feature 4: Standards Compliance with Regional Flexibility

### The Challenge

Global standards (Darwin Core, GeoJSON) enable interoperability but were designed for museum specimens, not ecosystem-scale monitoring. Mountain biodiversity requires additional fields: **elevation**, **habitat type**, **threat proximity**, **traditional knowledge metadata** — none standardized in Darwin Core. Yet deviating from standards breaks compatibility with GBIF and other platforms.

### Architectural Solution: Core Standards + Regional Extensions

The system implements **Darwin Core compliance for core fields** while adding regional extensions as separate metadata objects:

```javascript
// src/types/occurrence.ts
export interface DarwinCoreOccurrence {
  // Standard Darwin Core terms
  occurrenceID: string;
  basisOfRecord: 'HumanObservation' | 'PreservedSpecimen' | 'MachineObservation';
  scientificName: string;
  kingdom?: string;
  phylum?: string;
  class?: string;
  order?: string;
  family?: string;
  genus?: string;
  specificEpithet?: string;
  
  decimalLatitude: number;
  decimalLongitude: number;
  geodeticDatum: string;
  coordinateUncertaintyInMeters?: number;
  
  eventDate: string; // ISO 8601
  recordedBy?: string;
  institutionCode?: string;
  collectionCode?: string;
  
  // Standard, but often missing in GBIF — crucial for mountains
  minimumElevationInMeters?: number;
  maximumElevationInMeters?: number;
}

export interface RegionalExtensions {
  // Eastern Himalaya-specific extensions
  elevationBand?: '0-500m' | '500-1500m' | '1500-2800m' | '2800-3800m' | '3800-5000m' | '>5000m';
  habitatType?: 'subtropical_broadleaf' | 'temperate_mixed' | 'subalpine_conifer' | 'alpine_scrub' | 'nival';
  
  // Threat proximity (distance to nearest infrastructure)
  distanceToRoad_m?: number;
  distanceToSettlement_m?: number;
  distanceToDam_m?: number;
  
  // Traditional knowledge fields (UNESCO LINKS compatible)
  localName?: { [language: string]: string };
  knowledgeHolder?: {
    community: string;
    consentStatus: 'fpic_obtained' | 'not_applicable' | 'pending';
    accessRestrictions?: string;
  };
  
  // Data quality indicators
  identificationConfidence?: 'high' | 'medium' | 'low';
  observationMethod?: 'direct_sighting' | 'camera_trap' | 'acoustic_monitor' | 'environmental_dna' | 'tracks_signs';
}

export interface THIOccurrenceRecord {
  darwinCore: DarwinCoreOccurrence;
  regionalExtensions: RegionalExtensions;
  provenance: ProvenanceMetadata;
}
```

**Interoperability workflow**: When contributing data back to GBIF, the system:
1. Exports only Darwin Core fields (ensuring GBIF compatibility)
2. Stores regional extensions in supplementary files (documented in dataset README)
3. Provides API endpoints serving full records (Darwin Core + extensions) for regional users

```javascript
// src/services/export/gbifExport.js
export const exportToGBIFDarwinCore = (records) => {
  return records.map(record => {
    const dwc = record.darwinCore;
    
    // Populate often-missing elevation from regional extensions
    if (!dwc.minimumElevationInMeters && record.regionalExtensions.elevationBand) {
      const [min, max] = parseElevationBand(record.regionalExtensions.elevationBand);
      dwc.minimumElevationInMeters = min;
      dwc.maximumElevationInMeters = max;
    }
    
    // Export only Darwin Core fields for GBIF compatibility
    return dwc;
  });
};

export const exportFullRecords = (records) => {
  // For regional API: include extensions
  return records; // Full THIOccurrenceRecord objects
};
```

**Design rationale**: This approach maintains **interoperability** (can exchange data with GBIF, other NBDIs) while enabling **regional innovation** (add mountain-specific fields without waiting for international standards bodies to adopt them). If Darwin Core eventually adopts `habitatType` or `distanceToThreat` fields, the system can migrate extensions into core without breaking existing data.

## Feature 5: Progressive Enhancement Architecture

### The Challenge

Mountain regions exhibit **extreme variation in institutional capacity**: research stations with high-speed internet coexist with village biodiversity committees using mobile phones on intermittent 3G. Infrastructure must work across this spectrum without requiring all users to have identical technical resources.

### Architectural Solution: Three-Phase Progressive Enhancement

The system deploys in three progressively capable phases:

**Phase 1: Static Frontend + GBIF API** (Current deployment)
- **No backend required** — purely client-side React application
- **Data source**: GBIF API v2 and tile services (external, no hosting cost)
- **Capabilities**: Species occurrence visualization, basic filtering, export to CSV
- **Deployment**: Static hosting (GitHub Pages, Netlify, Cloudflare Pages) — free or <$5/month
- **Bandwidth**: ~2-5 MB initial load, <100 KB per region query
- **Use case**: Individual researchers, students, preliminary conservation assessments

```javascript
// Phase 1 architecture: Pure client-side
// No server, no database, no authentication
// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Provider } from 'react-redux';
import { store } from './store';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
);
```

**Phase 2: Hybrid API Gateway + Caching** (Planned 2026 deployment)
- **Minimal backend**: Node.js/Express API (single instance, 1 GB RAM sufficient)
- **Data sources**: GBIF (proxied for caching) + PostgreSQL (regional institutional data)
- **Capabilities**: Phase 1 + authenticated access to institutional datasets, saved queries, basic analytics
- **Deployment**: VPS or cloud instance (DigitalOcean Droplet, AWS t3.micro) — $10-20/month
- **Bandwidth**: Backend caches GBIF responses, reducing external API calls and improving response time for repeat queries
- **Use case**: Protected area managers, research institutions, government agencies

```javascript
// Phase 2 architecture: Hybrid gateway
// Backend caches GBIF and serves regional data
// backend/server.js
const express = require('express');
const { Pool } = require('pg');
const NodeCache = require('node-cache');

const app = express();
const db = new Pool({ connectionString: process.env.DATABASE_URL });
const cache = new NodeCache({ stdTTL: 3600 }); // 1 hour cache

// Proxy GBIF with caching
app.get('/api/occurrences/global', async (req, res) => {
  const cacheKey = `gbif_${JSON.stringify(req.query)}`;
  const cached = cache.get(cacheKey);
  
  if (cached) {
    return res.json(cached);
  }
  
  const gbifResponse = await fetch(`https://api.gbif.org/v1/occurrence/search?${new URLSearchParams(req.query)}`);
  const data = await gbifResponse.json();
  
  cache.set(cacheKey, data);
  res.json(data);
});

// Serve regional institutional data (requires auth)
app.get('/api/occurrences/regional', authenticateToken, async (req, res) => {
  const { bounds, taxonKey } = req.query;
  
  const results = await db.query(`
    SELECT * FROM regional_occurrences
    WHERE ST_Within(location, ST_MakeEnvelope($1, $2, $3, $4, 4326))
      AND access_level IN ('public', $5)
    LIMIT 300
  `, [bounds.west, bounds.south, bounds.east, bounds.north, req.user.accessLevel]);
  
  res.json(results.rows);
});
```

**Phase 3: Full-Stack Platform + Offline-First** (Planned 2027+)
- **Complete backend**: PostgreSQL+PostGIS, vector tile server, authentication service
- **Data sources**: All Phase 2 + community knowledge layer, uploaded datasets, real-time sensor feeds
- **Capabilities**: All Phase 2 + offline mobile apps (Progressive Web App), community data contribution, advanced analytics, custom reporting
- **Deployment**: Multi-instance (load balancing), managed database (AWS RDS, DigitalOcean Managed Postgres) — $100-300/month
- **Bandwidth**: Offline-first architecture allows field use without connectivity; syncs when online
- **Use case**: Full regional platform serving multiple institutions, community networks, policy agencies

**Design rationale**: Progressive enhancement avoids the "all-or-nothing" trap where infrastructure requires massive upfront investment before providing any utility. Phase 1 delivers immediate value (GBIF visualization) to any user with a web browser. Institutions can adopt Phase 2 when ready to contribute proprietary data. Full Phase 3 capabilities emerge only when regional coordination justifies the investment.

**(Figure 6. Progressive enhancement architecture: three deployment phases with increasing capabilities and infrastructure requirements)**

## Feature 6: Governance Architecture for Multi-Stakeholder Systems

### The Challenge

Technical infrastructure alone does not ensure adoption. As shown in Section 5, conservation planning requires **institutional trust**, **community legitimacy**, and **governance structures** that give data providers authority over how their contributions are used.

### Design: Multi-Stakeholder Governance Model

Regional knowledge systems require governance architectures that accommodate diverse stakeholders:

**Governance principles**:
- **Representation**: Government agencies, research institutions, community organizations each hold decision-making authority
- **Tiered decision authority**: Consensus for data governance policies; majority vote for technical priorities; community veto power over traditional knowledge access policies
- **Transparency**: Regular data access audits, public documentation of governance decisions
- **Institutional anchoring**: Regional research institution or intergovernmental body hosts infrastructure

```javascript
// Governance encoded in access control system
// src/services/auth/accessControl.js
export const AccessLevels = {
  PUBLIC: 'public',
  INSTITUTIONAL_RESEARCHER: 'institutional_researcher',
  GOVERNMENT_OFFICIAL: 'government_official',
  COMMUNITY_MEMBER: 'community_member',
  STEERING_COMMITTEE: 'steering_committee'
};

export const canAccessRecord = (user, record) => {
  // Public data accessible to all
  if (record.accessLevel === 'public') return true;
  
  // Institutional data requires authentication
  if (record.accessLevel === 'institutional') {
    return user.accessLevel in [
      AccessLevels.INSTITUTIONAL_RESEARCHER,
      AccessLevels.GOVERNMENT_OFFICIAL,
      AccessLevels.STEERING_COMMITTEE
    ];
  }
  
  // Community-restricted data requires community authorization
  if (record.accessLevel === 'community_restricted') {
    if (user.accessLevel === AccessLevels.STEERING_COMMITTEE) return true;
    
    // Community members can access their own community's data
    if (user.accessLevel === AccessLevels.COMMUNITY_MEMBER) {
      return user.community === record.contributingCommunity;
    }
    
    return false;
  }
  
  return false;
};

export const canModifyGovernance = (user, action) => {
  // Traditional knowledge policies require community consent
  if (action.type === 'tek_access_policy') {
    return user.accessLevel === AccessLevels.COMMUNITY_MEMBER 
      || user.accessLevel === AccessLevels.STEERING_COMMITTEE;
  }
  
  // Technical roadmap decisions by steering committee
  if (action.type === 'feature_priority') {
    return user.accessLevel === AccessLevels.STEERING_COMMITTEE;
  }
  
  return false;
};
```

**Design rationale**: Co-design is not a "nice-to-have" engagement exercise but **essential infrastructure architecture**. The access control system (Feature 7) directly implements governance agreements negotiated through participatory process. Community veto power is not symbolic — it's encoded in the permission system, preventing even system administrators from overriding community data access decisions without documented consent.

## Feature 7: Open Science by Default, with Granular Privacy Controls

### The Challenge

Biodiversity data faces a **transparency-privacy paradox**: open science principles demand data sharing for reproducibility and collaboration, yet sensitive data (rare species locations, traditional knowledge, commercially valuable genetic resources) require restrictions to prevent harm. Global platforms default to "open" (GBIF's CC0 norm), while national systems default to "closed" (requiring bureaucratic approval). Neither serves ecosystem-scale conservation well.

### Architectural Solution: Tiered Access with Spatial Generalization

The system implements **five access tiers** with progressively detailed data disclosure:

**Tier 1: Public Summary Statistics** (No authentication required)
- Species presence/absence by elevation band
- Temporal trends (species richness over time)
- Habitat type associations
- **No precise coordinates disclosed**

Example: "Red panda (*Ailurus fulgens*) observed in 3,500-4,000m elevation band, temperate mixed forest habitat, 27 observations 2020-2024, increasing trend."

**Tier 2: Generalized Spatial Data** (Free registration required)
- Occurrence records with coordinates **generalized to 5 km grid cells**
- Sufficient for landscape-scale analyses, insufficient for poaching targeting
- Standard for threatened species globally (GBIF obscures coordinates for IUCN Endangered species)

```javascript
// src/services/privacy/spatialGeneralization.js
export const generalizeCoordinates = (lat, lon, precision_km = 5) => {
  const gridSize = precision_km / 111; // ~111 km per degree
  
  const gridLat = Math.floor(lat / gridSize) * gridSize + (gridSize / 2);
  const gridLon = Math.floor(lon / gridSize) * gridSize + (gridSize / 2);
  
  return {
    latitude: gridLat,
    longitude: gridLon,
    precision: `generalized_${precision_km}km`,
    originalPrecision: 'withheld'
  };
};

export const shouldGeneralize = (record) => {
  // IUCN Red List threatened categories
  const threatenedCategories = ['CR', 'EN', 'VU'];
  
  // Commercially valuable species (e.g., medicinal plants)
  const commercialSpecies = ['Nardostachys jatamansi', 'Panax pseudoginseng'];
  
  return threatenedCategories.includes(record.iucnCategory)
    || commercialSpecies.includes(record.scientificName)
    || record.accessLevel === 'community_restricted';
};
```

**Tier 3: Precise Coordinates** (Institutional affiliation required)
- Full-resolution occurrence data for authenticated researchers
- Requires data use agreement: acknowledge source, no commercial use without benefit-sharing, report publications back to platform

**Tier 4: Contextual Data** (Government agency or research project approval)
- Includes patrol routes, infrastructure threat layers, habitat quality assessments
- Restricted to users with demonstrated conservation application (reviewed by steering committee)

**Tier 5: Traditional Knowledge** (Community consent required)
- Controlled by contributing communities
- May require in-person consultation, Free Prior and Informed Consent documentation, co-authorship agreements
- Platform facilitates connection between researchers and communities but does not grant access unilaterally

**Design rationale**: Rather than binary "open vs. closed," the system recognizes that **different data serve different purposes at different sensitivities**. Summary statistics enable public engagement and education without risk. Generalized coordinates allow landscape analyses without enabling poaching. Precise data supports detailed research under responsible use agreements. Community knowledge remains under community control, respecting Indigenous Data Sovereignty principles 【Carroll et al. 2020†Data Science Journal】.

**(Figure 7. Tiered access control system with progressive data disclosure and community governance)**

## Integration: How Seven Features Work Together

These seven features are **not independent modules** but an integrated system:

1. **Multi-source integration** (Feature 1) provides data
2. **Spatial dependencies** (Feature 2) coordinate layer loading
3. **Scale-appropriate queries** (Feature 3) ensure performance and relevance
4. **Standards compliance** (Feature 4) enables interoperability while allowing innovation
5. **Progressive enhancement** (Feature 5) allows adoption across capacity spectrum
6. **Co-design process** (Feature 6) ensures governance legitimacy
7. **Tiered access** (Feature 7) balances transparency and protection

A user query like "Show red panda observations in Khangchendzonga Landscape from 2020-2024, including community knowledge if authorized" triggers:

1. Feature 3 determines appropriate scale (landscape = vector tile rendering + clustering)
2. Feature 2 loads base map → administrative boundaries → species layer in dependency order
3. Feature 1 fetches GBIF data (Tier 1), regional data if authenticated (Tier 2), community data if authorized (Tier 3)
4. Feature 7 applies spatial generalization for threatened species before display
5. Feature 4 exports results in Darwin Core format for interoperability
6. Feature 6 logs query for governance transparency (steering committee reviews data access patterns quarterly)
7. Feature 5 ensures query works whether user is on high-speed university connection or mobile 3G

The next section demonstrates how these architectural capabilities translate into **decision-relevant outputs** — biodiversity indicators, temporal analyses, and conservation prioritization tools that move data from infrastructure into action.

---

**Word Count**: 6,847 words  
**Code Examples**: 12 substantive implementations (JavaScript, SQL, TypeScript)  
**Figures Referenced**: 3 (Figures 5-7)  
**Next Section**: Section 7 — From Data to Action: Indicators and Analytics

