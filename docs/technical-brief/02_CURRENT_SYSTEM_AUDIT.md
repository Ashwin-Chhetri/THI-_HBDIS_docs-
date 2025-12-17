# Current System Audit
## HMBIS Knowledge Common - Technical Analysis

**Document**: 02 of 08  
**Date**: November 6, 2025  
**Version**: 1.0

---

## Table of Contents

1. [Frontend Technologies](#frontend-technologies)
2. [Backend Architecture](#backend-architecture)
3. [Data Pipeline](#data-pipeline)
4. [Integration Layer](#integration-layer)
5. [System Design Flow](#system-design-flow)
6. [Modularity Analysis](#modularity-analysis)

---

## 1. Frontend Technologies

### 1.1 Core Framework Stack

#### React 19.1.1
- **Purpose**: UI component framework
- **Usage**: All user interface components
- **Key Features Used**:
  - Hooks API (useState, useEffect, useMemo, useCallback)
  - Context API for dependency injection
  - Concurrent rendering capabilities
  - Suspense for lazy loading

**Example Implementation**:
```javascript
// Typical component structure
import React, { useState, useEffect, useMemo } from 'react';
import { useDispatch, useSelector } from 'react-redux';

function SpeciesPanel() {
  const dispatch = useDispatch();
  const species = useSelector(selectSelectedSpecies);
  
  const occurrenceCount = useMemo(() => 
    calculateOccurrences(species), [species]
  );
  
  return (
    <div className={styles.panel}>
      {/* Component JSX */}
    </div>
  );
}
```

#### Redux Toolkit 2.9.2
- **Purpose**: State management
- **Architecture Pattern**: Flux-based unidirectional data flow
- **Key Components**:
  - **Slices**: Feature-based state containers
  - **Reducers**: Pure functions for state updates
  - **Selectors**: Memoized state queries (using Reselect)
  - **Middleware**: Custom logic interceptors

**Store Structure**:
```javascript
{
  layers: {
    byId: {},           // Normalized layer objects
    allIds: [],         // Layer IDs array
    dependencyGraph: {} // DAG structure
  },
  species: {
    searchResults: [],
    selectedSpecies: null,
    occurrenceData: null
  },
  ecosystem: { /* ... */ },
  region: { /* ... */ },
  ioc: { /* ... */ },
  socioeconomic: { /* ... */ },
  repository: { /* ... */ },
  ui: { /* ... */ }
}
```

#### Redux Saga 1.4.2
- **Purpose**: Async operation orchestration
- **Pattern**: Generator-based side effect management
- **Use Cases**:
  - API calls with retry logic
  - Multi-step workflows
  - Dependency cascade updates
  - Background data synchronization

**Saga Example**:
```javascript
export function* handleRegionSelection(action) {
  const { regionId, geometry } = action.payload;
  
  // Step 1: Add region layer
  yield put(addLayer({ id: regionId, geometry }));
  
  // Step 2: Wait for completion
  yield take('layers/addLayer/fulfilled');
  
  // Step 3: Fetch dependent data
  const speciesData = yield call(
    gbifService.getOccurrences, 
    { geometry }
  );
  
  // Step 4: Add species layer
  yield put(addLayer({
    id: 'species',
    data: speciesData,
    dependencies: [regionId]
  }));
}
```

### 1.2 Mapping & Visualization

#### MapLibre GL JS 5.9.0
- **Purpose**: Interactive web mapping
- **Rendering**: WebGL-based vector tile rendering
- **Features Used**:
  - Dynamic style manipulation
  - Custom layer types (raster, vector, heatmap)
  - Geolocation API integration
  - Custom controls and popups

**Layer Management Architecture**:
```
┌──────────────────────────────────────┐
│  React Components                    │
│  (UI Layer)                          │
└──────────┬───────────────────────────┘
           │ dispatch(action)
           ▼
┌──────────────────────────────────────┐
│  Redux Store                         │
│  (State Layer)                       │
└──────────┬───────────────────────────┘
           │ state changes
           ▼
┌──────────────────────────────────────┐
│  EnhancedLayerManager                │
│  (Abstraction Layer)                 │
└──────────┬───────────────────────────┘
           │ MapLibre API calls
           ▼
┌──────────────────────────────────────┐
│  MapLibre GL JS                      │
│  (Rendering Layer)                   │
└──────────────────────────────────────┘
```

**Key Classes**:
1. **EnhancedLayerManager**: Abstracts MapLibre operations
2. **LayerRegistry**: Global layer coordination
3. **LayerState**: Per-panel state tracking
4. **BatchQueue**: Performance optimization

#### Recharts 3.2.1
- **Purpose**: Data visualization (charts, graphs)
- **Usage**: Statistics dashboards, occurrence trends
- **Integration**: React-friendly, responsive

### 1.3 Geospatial Libraries

#### Turf.js 7.2.0
- **Purpose**: Geospatial analysis
- **Operations Used**:
  - `bbox` - Bounding box calculation
  - `booleanPointInPolygon` - Point-in-polygon tests
  - `buffer` - Spatial buffering
  - `intersect` - Geometry intersection
  - `area` - Area calculation

**Example Usage**:
```javascript
import * as turf from '@turf/turf';

// Calculate region bounding box
const bbox = turf.bbox(regionGeometry);

// Filter species within region
const filtered = species.filter(point => 
  turf.booleanPointInPolygon(
    turf.point([point.lng, point.lat]),
    regionGeometry
  )
);
```

### 1.4 Build Tools

#### Vite 7.1.7
- **Purpose**: Development server and build tool
- **Features**:
  - Lightning-fast Hot Module Replacement (HMR)
  - Native ES modules in development
  - Rollup-based production builds
  - Code splitting and lazy loading
  - Tree shaking for minimal bundle size

**Build Configuration**:
```javascript
// vite.config.js highlights
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@app': '/src/app',
      '@features': '/src/features',
      '@services': '/src/services',
      '@shared': '/src/shared'
    }
  },
  build: {
    target: 'es2020',
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom'],
          'vendor-maplibre': ['maplibre-gl'],
          'vendor-charts': ['recharts']
        }
      }
    }
  }
})
```

**Bundle Analysis** (Production):
```
dist/assets/
├── vendor-react-abc123.js      (142 KB)
├── vendor-maplibre-def456.js   (456 KB)
├── vendor-charts-ghi789.js     (234 KB)
├── index-jkl012.js             (89 KB)
└── styles-mno345.css           (23 KB)

Total: ~944 KB (gzipped: ~312 KB)
```

---

## 2. Backend Architecture

### 2.1 Architecture Pattern

**Client-Side Application** (No traditional backend server)
- Static file hosting via CDN
- Direct API calls from browser to external services
- Client-side data processing and caching

### 2.2 Data Storage

#### IndexedDB
- **Purpose**: Client-side persistent storage
- **Capacity**: ~50MB - 1GB (browser-dependent)
- **Usage**:
  - User-uploaded files
  - Cached API responses
  - Large dataset storage (100K+ records)

**Schema**:
```javascript
Database: 'thi-knowledge-common'
├── ObjectStore: 'layers'
│   ├── keyPath: 'id'
│   └── Data: Layer configurations
├── ObjectStore: 'datasets'
│   ├── keyPath: 'key'
│   └── Data: Large occurrence datasets
└── ObjectStore: 'user-uploads'
    ├── keyPath: 'id'
    └── Data: User GeoJSON files
```

#### Local Storage
- **Purpose**: Small configuration data
- **Capacity**: ~5-10MB
- **Usage**:
  - User preferences
  - Last selected region
  - UI state (collapsed panels, etc.)

### 2.3 Hosting Stack

**Current Deployment**:
- **Static Hosting**: GitHub Pages / Netlify / Vercel
- **Map Tiles**: MapTiler CDN
- **API Gateway**: Direct HTTPS calls to GBIF

**Planned Architecture**:
```
┌─────────────────────────────────────┐
│  CDN (Cloudflare/CloudFront)       │
│  - Static assets                    │
│  - Edge caching                     │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  Origin Server (Optional)           │
│  - API Gateway                      │
│  - Authentication                   │
│  - Rate limiting                    │
└─────────────────────────────────────┘
```

---

## 3. Data Pipeline

### 3.1 Data Ingestion Layer

#### Primary Data Sources

**1. GBIF API (api.gbif.org/v1)**
```javascript
// Service: gbifService.js
class GBIFService {
  baseURL = 'https://api.gbif.org/v1';
  
  async getOccurrences(params) {
    const { taxonKey, region, timeRange } = params;
    
    const url = `${this.baseURL}/occurrence/search`;
    const response = await fetch(url, {
      params: {
        taxonKey,
        hasCoordinate: true,
        geometry: region ? toWKT(region) : null,
        eventDate: timeRange ? 
          `${timeRange.start},${timeRange.end}` : null
      }
    });
    
    return this.transform(await response.json());
  }
}
```

**API Endpoints Used**:
- `/species/search` - Species name search
- `/species/{key}` - Species details
- `/occurrence/search` - Occurrence records
- `/occurrence/count` - Count queries
- `/dataset/search` - Dataset discovery

**2. Local Database Integration**
```javascript
// Planned: Regional database adapter
class LocalDatabaseAdapter {
  dbURL = config.localDatabaseURL;
  
  async fetch(request) {
    const query = this.buildQuery(request);
    const response = await fetch(
      `${this.dbURL}/query`,
      { method: 'POST', body: JSON.stringify(query) }
    );
    return this.transform(response.data);
  }
  
  supportsRegion(region) {
    // Only Sikkim data available
    return region === 'sikkim';
  }
}
```

**3. User File Upload**
```javascript
// Service: fileParserService.js
export async function parseGeoJSON(file) {
  const text = await file.text();
  const geojson = JSON.parse(text);
  
  // Validate structure
  if (!geojson.type || !geojson.features) {
    throw new Error('Invalid GeoJSON');
  }
  
  return {
    type: 'geojson',
    geometry: geojson,
    features: geojson.features,
    bounds: turf.bbox(geojson)
  };
}
```

### 3.2 Data Cleaning & Transformation

#### Standardization Process

**Step 1: Data Validation**
```javascript
export function validateOccurrence(record) {
  const errors = [];
  
  // Required fields
  if (!record.decimalLatitude) 
    errors.push('Missing latitude');
  if (!record.decimalLongitude) 
    errors.push('Missing longitude');
  if (!record.scientificName) 
    errors.push('Missing species name');
  
  // Coordinate validation
  if (Math.abs(record.decimalLatitude) > 90)
    errors.push('Invalid latitude');
  if (Math.abs(record.decimalLongitude) > 180)
    errors.push('Invalid longitude');
  
  return { valid: errors.length === 0, errors };
}
```

**Step 2: Format Conversion**
```javascript
// Convert GBIF to Common Format
export function transformGBIFToCommon(gbifData) {
  return {
    type: 'FeatureCollection',
    features: gbifData.results.map(record => ({
      type: 'Feature',
      geometry: {
        type: 'Point',
        coordinates: [
          record.decimalLongitude,
          record.decimalLatitude
        ]
      },
      properties: {
        id: record.key,
        species: record.species,
        scientificName: record.scientificName,
        date: record.eventDate,
        basisOfRecord: record.basisOfRecord,
        source: 'gbif',
        coordinateUncertainty: 
          record.coordinateUncertaintyInMeters,
        ...record
      }
    }))
  };
}
```

**Step 3: Taxonomy Harmonization**
```javascript
// Resolve taxonomy conflicts
export function harmonizeTaxonomy(species) {
  return {
    acceptedName: species.canonicalName || 
                  species.scientificName,
    synonyms: species.synonyms || [],
    kingdom: species.kingdom,
    phylum: species.phylum,
    class: species.class,
    order: species.order,
    family: species.family,
    genus: species.genus,
    specificEpithet: species.species
  };
}
```

### 3.3 Data Storage Strategy

#### Three-Tier Caching

**Tier 1: Redux State (Metadata Only)**
```javascript
// Store only lightweight metadata
{
  layers: {
    'gbif-species': {
      id: 'gbif-species',
      status: 'active',
      recordCount: 104523,
      dataReference: 'indexeddb://datasets/gbif-5218933',
      bounds: [87, 27, 89, 28],
      // NOT storing 104K records here!
    }
  }
}
```

**Tier 2: IndexedDB (Full Datasets)**
```javascript
// Large dataset storage
const db = await openDB('thi-knowledge-common');
await db.put('datasets', {
  key: 'gbif-5218933',
  data: largeGeoJSON, // 104K features
  timestamp: Date.now(),
  size: 45000000 // 45MB
});
```

**Tier 3: Vector Tiles (On-Demand)**
```javascript
// For extremely large datasets
{
  id: 'gbif-species-tiles',
  type: 'vector',
  source: {
    type: 'vector',
    tiles: [
      'https://api.gbif.org/v2/map/occurrence/density/{z}/{x}/{y}.mvt?taxonKey=5218933'
    ],
    minzoom: 0,
    maxzoom: 14
  }
}
```

### 3.4 Data Rendering Pipeline

```
User Action (Select Species)
  ↓
Redux Action Dispatched
  ↓
Saga Intercepts → API Call
  ↓
Data Transformation
  ↓
IndexedDB Storage
  ↓
Redux State Update (metadata only)
  ↓
Component Re-render
  ↓
EnhancedLayerManager.addLayer()
  ↓
MapLibre GL Rendering
  ↓
Visual Update on Map
```

---

## 4. Integration Layer

### 4.1 External Dataset Integration

#### GBIF Integration
- **Standard**: Darwin Core Archive (DwC-A)
- **Protocol**: REST API over HTTPS
- **Authentication**: Not required for read access
- **Rate Limiting**: 100 requests/minute
- **Caching Strategy**: 24-hour TTL for species data

#### India Biodiversity Portal (Planned)
- **Standard**: Darwin Core
- **Integration**: Checklist import
- **Use Case**: Regional species lists

#### mWater (Planned)
- **Type**: Water quality data
- **Integration**: REST API
- **Use Case**: Socioeconomic indicators

### 4.2 Data Source Registry

```javascript
class DataSourceRegistry {
  sources = new Map();
  
  register(id, config) {
    this.sources.set(id, {
      id,
      name: config.name,
      priority: config.priority || 0,
      capabilities: config.capabilities || [],
      adapter: new DataSourceAdapter(config)
    });
  }
  
  selectSource(request) {
    const { dataType, region } = request;
    
    // Filter by capabilities
    const candidates = Array.from(this.sources.values())
      .filter(s => 
        s.capabilities.includes(dataType) &&
        s.adapter.supportsRegion(region)
      );
    
    // Sort by priority
    return candidates.sort((a, b) => 
      b.priority - a.priority
    )[0];
  }
}
```

**Registered Sources**:
```javascript
registry.register('gbif', {
  name: 'GBIF',
  priority: 10,
  capabilities: ['SPECIES', 'OCCURRENCE'],
  adapter: new GBIFAdapter()
});

registry.register('sikkim-local', {
  name: 'Sikkim Database',
  priority: 20, // Higher priority for local data
  capabilities: ['SPECIES', 'ECOSYSTEM'],
  adapter: new LocalDatabaseAdapter()
});

registry.register('user-uploads', {
  name: 'User Files',
  priority: 30, // Highest priority
  capabilities: ['SPECIES', 'REGION', 'ECOSYSTEM'],
  adapter: new UserUploadAdapter()
});
```

---

## 5. System Design Flow

### 5.1 Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                         │
│  • Search Species                                           │
│  • Select Region                                            │
│  • Upload File                                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  REACT COMPONENTS                            │
│  • SpeciesPanel.jsx                                         │
│  • RegionSelector.jsx                                       │
│  • MapContainer.jsx                                         │
└────────────────────┬────────────────────────────────────────┘
                     │ dispatch(action)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   REDUX STORE                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Slices: layers, species, ecosystem, region, etc.    │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Middleware: dependencyOrchestrator, performance     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Sagas: Async workflows, API calls                   │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│   DATA LAYER     │    │   MAP LAYER      │
│                  │    │                  │
│ • Services       │    │ • LayerManager   │
│ • API Clients    │    │ • MapLibre GL    │
│ • Adapters       │    │ • Rendering      │
└────┬─────────────┘    └────┬─────────────┘
     │                       │
     ▼                       ▼
┌─────────────────────────────────────────┐
│        EXTERNAL SYSTEMS                 │
│  • GBIF API                             │
│  • MapTiler                             │
│  • Regional Databases                   │
└─────────────────────────────────────────┘
```

### 5.2 Layer Lifecycle

```
1. USER ACTION
   └─> "Add Species Layer"

2. DISPATCH ACTION
   └─> dispatch(addLayer({ id, type, config }))

3. REDUCER UPDATE
   └─> State: layers.byId[id] = { status: 'pending' }

4. SAGA INTERCEPT
   └─> function* handleAddLayer(action)

5. DEPENDENCY CHECK
   └─> Get dependencies, validate no cycles

6. DATA FETCH
   └─> yield call(dataService.fetch, config)

7. TRANSFORM
   └─> Convert to common GeoJSON format

8. CACHE
   └─> Store in IndexedDB

9. UPDATE STATE
   └─> State: layers.byId[id] = { status: 'active', dataRef }

10. RENDER
    └─> EnhancedLayerManager.addLayer()

11. REFRESH DEPENDENTS
    └─> Trigger dependent layer updates
```

### 5.3 Metadata Management

**Provenance Tracking**:
```javascript
{
  layerId: 'gbif-species-ailurus',
  metadata: {
    source: 'gbif',
    sourceURL: 'https://api.gbif.org/v1/occurrence/search',
    datasetKey: 'gbif-5218933',
    citation: 'GBIF.org (2025) GBIF Occurrence Download',
    license: 'CC-BY 4.0',
    timestamp: '2025-11-06T10:30:00Z',
    recordCount: 1543,
    filters: {
      region: 'sikkim',
      timeRange: { start: '2020', end: '2024' }
    },
    transformations: [
      { type: 'coordinate-validation', passed: 1543, failed: 0 },
      { type: 'taxonomy-harmonization', matched: 1543 },
      { type: 'region-masking', filtered: 47 }
    ]
  }
}
```

---

## 6. Modularity Analysis

### 6.1 Feature Module Structure

Each feature is self-contained:

```
src/features/species/
├── index.js                 # Public API
├── SpeciesView.jsx          # Main container
├── components/              # UI components
│   ├── SpeciesPanel.jsx
│   ├── DataClassSelector.jsx
│   └── SpeciesSearch.jsx
├── hooks/                   # Custom hooks
│   ├── useGBIFLayers.js
│   └── useSpeciesData.js
├── store/                   # Redux logic
│   ├── speciesSlice.js
│   ├── speciesSagas.js
│   └── speciesSelectors.js
├── services/                # Business logic
│   └── speciesService.js
└── styles/                  # CSS modules
    └── SpeciesView.module.css
```

### 6.2 Module Interaction

**Communication Patterns**:

1. **Redux Store** (Shared State)
   ```javascript
   // Species module writes
   dispatch(selectSpecies(species));
   
   // Ecosystem module reads
   const activeSpecies = useSelector(selectSelectedSpecies);
   ```

2. **Event Bus** (Loose Coupling)
   ```javascript
   // Publisher
   eventBus.emit('region:changed', regionId);
   
   // Subscriber
   eventBus.on('region:changed', handleRegionChange);
   ```

3. **Shared Services** (Data Layer)
   ```javascript
   // Both modules use same service
   import { gbifService } from '@services/gbif';
   ```

### 6.3 Data Layer Modules

**Current Modules**:
1. ✅ **Species** - Complete
2. ✅ **Ecosystem** - Complete
3. 🔄 **Region** - 80% complete
4. 🔄 **IoC** (Indicators of Change) - 60% complete
5. 🔄 **Socioeconomic** - 40% complete
6. 🔄 **Repository** - 30% complete

**Module Dependencies**:
```
Region (Core)
  ├─→ Species
  ├─→ Ecosystem
  ├─→ Socioeconomic
  └─→ IoC
       └─→ Species (for trends)
```

---

## Summary

### System Strengths
1. ✅ Modern, performant frontend stack
2. ✅ Scalable architecture with layer dependency management
3. ✅ Multi-source data integration capability
4. ✅ Clean separation of concerns
5. ✅ Comprehensive documentation

### Areas for Enhancement
1. 🔄 Backend API layer for authentication
2. 🔄 Complete module migrations
3. 🔄 Enhanced offline support
4. 🔄 Real-time data streaming
5. 🔄 Machine learning integration

---

**Previous**: [01_EXECUTIVE_SUMMARY.md](./01_EXECUTIVE_SUMMARY.md)  
**Next**: [03_BENCHMARK_COMPARISON.md](./03_BENCHMARK_COMPARISON.md)
