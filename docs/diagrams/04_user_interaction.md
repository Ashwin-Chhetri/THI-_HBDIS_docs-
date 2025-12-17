# User Interaction Overview - UI to Data Flow

## Visual Diagram

```mermaid
graph TB
    %% Styling
    classDef ui fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20
    classDef component fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#0D47A1
    classDef state fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100
    classDef api fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
    classDef backend fill:#FCE4EC,stroke:#E91E63,stroke-width:2px,color:#880E4F
    
    %% User Interface Layer
    subgraph UI[" 🖥️ USER INTERFACE LAYER "]
        MAP[Interactive Map<br/>━━━━━━━━━━<br/>MapLibre GL JS<br/>Pan, Zoom, Click]:::ui
        SEARCH[Species Search Box<br/>━━━━━━━━━━<br/>Autocomplete<br/>Fuzzy Matching]:::ui
        FILTERS[Filter Panel<br/>━━━━━━━━━━<br/>Date Range<br/>Region Selector<br/>Quality Threshold]:::ui
        LAYERS[Layer Toggle<br/>━━━━━━━━━━<br/>Protected Areas<br/>Ecosystems<br/>Occurrences]:::ui
        CHARTS[Dashboard Charts<br/>━━━━━━━━━━<br/>Species Trends<br/>Distribution Graphs]:::ui
    end
    
    %% Component Layer
    subgraph COMP[" ⚛️ REACT COMPONENT LAYER "]
        SPECIES_VIEW[SpeciesView<br/>Component]:::component
        MAP_VIEW[MapView<br/>Component]:::component
        FILTER_VIEW[FilterPanel<br/>Component]:::component
        CHART_VIEW[ChartView<br/>Component]:::component
    end
    
    %% State Management Layer
    subgraph STATE[" 📦 STATE MANAGEMENT (Redux) "]
        SPECIES_SLICE[Species Slice<br/>━━━━━━━━━━<br/>selectedSpecies<br/>occurrenceData<br/>isLoading]:::state
        MAP_SLICE[Map Slice<br/>━━━━━━━━━━<br/>viewport<br/>activeLayers<br/>mapStyle]:::state
        FILTER_SLICE[Filter Slice<br/>━━━━━━━━━━<br/>dateRange<br/>regionId<br/>qualityMin]:::state
        UI_SLICE[UI Slice<br/>━━━━━━━━━━<br/>panelOpen<br/>selectedTab<br/>notifications]:::state
    end
    
    %% API Service Layer
    subgraph API_LAYER[" 🔌 API SERVICE LAYER "]
        SPECIES_API[Species Service<br/>━━━━━━━━━━<br/>searchSpecies()<br/>getSpeciesDetails()]:::api
        OCC_API[Occurrence Service<br/>━━━━━━━━━━<br/>fetchOccurrences()<br/>getOccurrenceById()]:::api
        REGION_API[Region Service<br/>━━━━━━━━━━<br/>getRegions()<br/>getRegionBoundary()]:::api
        IND_API[Indicator Service<br/>━━━━━━━━━━<br/>calculateSMI()<br/>getIndicatorHistory()]:::api
    end
    
    %% Backend Layer
    subgraph BACKEND[" 🖥️ BACKEND API ENDPOINTS "]
        SPECIES_EP[GET /api/v1/species<br/>━━━━━━━━━━<br/>Search & Autocomplete]:::backend
        OCC_EP[GET /api/v1/occurrences<br/>━━━━━━━━━━<br/>Filtered Query]:::backend
        REGION_EP[GET /api/v1/regions<br/>━━━━━━━━━━<br/>Boundary Data]:::backend
        IND_EP[GET /api/v1/indicators<br/>━━━━━━━━━━<br/>Computed Metrics]:::backend
        TILES_EP[GET /api/v1/tiles/{z}/{x}/{y}<br/>━━━━━━━━━━<br/>Vector Tiles]:::backend
    end
    
    %% User Interactions
    MAP -->|User clicks region| MAP_VIEW
    SEARCH -->|User types query| SPECIES_VIEW
    FILTERS -->|User adjusts filters| FILTER_VIEW
    LAYERS -->|User toggles layer| MAP_VIEW
    CHARTS -->|User requests data| CHART_VIEW
    
    %% Component to State
    SPECIES_VIEW -->|dispatch(setSelectedSpecies)| SPECIES_SLICE
    MAP_VIEW -->|dispatch(setViewport)| MAP_SLICE
    FILTER_VIEW -->|dispatch(updateFilters)| FILTER_SLICE
    CHART_VIEW -->|dispatch(requestData)| SPECIES_SLICE
    
    %% State to API
    SPECIES_SLICE -->|Triggers API call| SPECIES_API
    SPECIES_SLICE -->|Triggers API call| OCC_API
    MAP_SLICE -->|Triggers tile request| TILES_EP
    FILTER_SLICE -->|Updates query params| OCC_API
    
    %% API to Backend
    SPECIES_API -->|HTTP GET| SPECIES_EP
    OCC_API -->|HTTP GET| OCC_EP
    REGION_API -->|HTTP GET| REGION_EP
    IND_API -->|HTTP GET| IND_EP
    
    %% Backend Response
    SPECIES_EP -.->|Response| SPECIES_API
    OCC_EP -.->|Response| OCC_API
    REGION_EP -.->|Response| REGION_API
    IND_EP -.->|Response| IND_API
    TILES_EP -.->|Vector Tile| MAP_VIEW
    
    %% API to State (Response)
    SPECIES_API -.->|dispatch(setSpeciesData)| SPECIES_SLICE
    OCC_API -.->|dispatch(setOccurrences)| SPECIES_SLICE
    REGION_API -.->|dispatch(setRegionData)| MAP_SLICE
    IND_API -.->|dispatch(setIndicators)| SPECIES_SLICE
    
    %% State to Component (Re-render)
    SPECIES_SLICE -.->|useSelector| SPECIES_VIEW
    MAP_SLICE -.->|useSelector| MAP_VIEW
    FILTER_SLICE -.->|useSelector| FILTER_VIEW
    SPECIES_SLICE -.->|useSelector| CHART_VIEW
    
    %% Component to UI (Update)
    SPECIES_VIEW -.->|Render| SEARCH
    MAP_VIEW -.->|Render| MAP
    MAP_VIEW -.->|Render| LAYERS
    FILTER_VIEW -.->|Render| FILTERS
    CHART_VIEW -.->|Render| CHARTS
```

## User Interaction Flow

### 🔍 Scenario 1: Species Search & Visualization

**Step-by-Step Flow**:

1. **User Action**: Types "red panda" in search box
   ```
   User Input → SEARCH Component
   ```

2. **Component Handler**:
   ```javascript
   // SpeciesView.jsx
   const handleSearch = (query) => {
     dispatch(searchSpecies(query));
   };
   ```

3. **Redux Action Dispatched**:
   ```javascript
   // speciesSlice.js
   dispatch({
     type: 'species/searchSpecies',
     payload: 'red panda'
   });
   ```

4. **Redux Saga Middleware**:
   ```javascript
   // speciesSaga.js
   function* handleSearchSpecies(action) {
     try {
       const results = yield call(speciesService.search, action.payload);
       yield put(setSpeciesResults(results));
     } catch (error) {
       yield put(setError(error.message));
     }
   }
   ```

5. **API Service Call**:
   ```javascript
   // speciesService.js
   async search(query) {
     const response = await axios.get('/api/v1/species', {
       params: { q: query, limit: 20 }
     });
     return response.data;
   }
   ```

6. **Backend API**:
   ```javascript
   // GET /api/v1/species?q=red panda
   app.get('/api/v1/species', async (req, res) => {
     const { q } = req.query;
     
     const results = await db.query(`
       SELECT taxon_key, scientific_name, common_name
       FROM species
       WHERE common_name ILIKE $1
       OR scientific_name ILIKE $1
       LIMIT 20
     `, [`%${q}%`]);
     
     res.json(results.rows);
   });
   ```

7. **Response Flows Back**:
   ```
   Backend → API Service → Redux State → Component → UI
   ```

8. **UI Updates**:
   ```javascript
   // Species dropdown appears with:
   // - Ailurus fulgens (Red Panda)
   // - Ailurus styani (Styan's Red Panda)
   ```

9. **User Selects Species**: Clicks "Ailurus fulgens"

10. **Map Updates**:
    ```javascript
    dispatch(fetchOccurrences({ taxonKey: 5218933 }));
    ```

11. **Occurrence Data Loaded**:
    ```
    API → Redux → MapView Component → MapLibre Renders Markers
    ```

---

### 🗺️ Scenario 2: Region Filter & Layer Toggle

**Step-by-Step Flow**:

1. **User Action**: Selects "Sikkim" from region dropdown
   ```
   User Input → FILTERS Component
   ```

2. **Filter Update**:
   ```javascript
   // FilterPanel.jsx
   const handleRegionChange = (regionId) => {
     dispatch(setActiveRegion(regionId));
     dispatch(fetchOccurrences({ regionId }));
   };
   ```

3. **Redux State Updates**:
   ```javascript
   // filterSlice.js
   state.activeRegion = 'region-sikkim-uuid';
   state.needsRefresh = true;
   ```

4. **Map Auto-Zooms**:
   ```javascript
   // MapView.jsx
   useEffect(() => {
     if (activeRegion) {
       const bounds = getRegionBounds(activeRegion);
       mapRef.current.fitBounds(bounds, { padding: 50 });
     }
   }, [activeRegion]);
   ```

5. **User Toggles "Protected Areas" Layer**:
   ```javascript
   dispatch(toggleLayer({ layerId: 'protected-areas', visible: true }));
   ```

6. **Map Layer Added**:
   ```javascript
   // mapSlice.js saga
   function* handleToggleLayer(action) {
     const { layerId, visible } = action.payload;
     
     if (visible) {
       yield call(mapService.addLayer, {
         id: layerId,
         type: 'fill',
         source: 'protected-areas-source',
         paint: {
           'fill-color': '#4CAF50',
           'fill-opacity': 0.3
         }
       });
     }
   }
   ```

7. **Result**: Map shows Sikkim region with protected area boundaries overlay

---

### 📊 Scenario 3: Dashboard Data Request

**Step-by-Step Flow**:

1. **User Action**: Navigates to "Species Dashboard" tab
   ```
   Route Change → /species/:taxonKey/dashboard
   ```

2. **Component Mounts**:
   ```javascript
   // SpeciesDashboard.jsx
   useEffect(() => {
     dispatch(fetchIndicators({ taxonKey }));
     dispatch(fetchOccurrenceTrends({ taxonKey }));
   }, [taxonKey]);
   ```

3. **Parallel API Calls**:
   ```javascript
   // Redux Saga
   function* handleFetchDashboard(action) {
     const [indicators, trends] = yield all([
       call(indicatorService.get, action.payload),
       call(occurrenceService.getTrends, action.payload)
     ]);
     
     yield put(setDashboardData({ indicators, trends }));
   }
   ```

4. **Backend Queries**:
   ```sql
   -- Indicators query
   SELECT indicator_type, value, year
   FROM indicators
   WHERE taxon_key = $1
   ORDER BY year DESC;
   
   -- Trends query
   SELECT 
     DATE_TRUNC('month', event_date) AS month,
     COUNT(*) AS count
   FROM occurrences
   WHERE taxon_key = $1
   GROUP BY month
   ORDER BY month;
   ```

5. **Charts Render**:
   ```javascript
   // ChartView.jsx
   <LineChart data={trends}>
     <XAxis dataKey="month" />
     <YAxis />
     <Line type="monotone" dataKey="count" stroke="#4CAF50" />
   </LineChart>
   ```

---

## Component-to-Data Mapping

### 1. Species Search Box
```
UI Component: <SpeciesSearchInput />
              ↓
State: speciesSlice.searchQuery
              ↓
API: GET /api/v1/species?q={query}
              ↓
Backend: Full-text search on species table
              ↓
Response: Array of species matches
              ↓
UI Update: Dropdown with autocomplete results
```

### 2. Map Region Selector
```
UI Component: <RegionSelector />
              ↓
State: filterSlice.activeRegion
              ↓
API: GET /api/v1/regions/{id}/boundary
              ↓
Backend: PostGIS boundary query
              ↓
Response: GeoJSON polygon
              ↓
Map Update: Fit bounds to region, apply filter
```

### 3. Date Range Filter
```
UI Component: <DateRangePicker />
              ↓
State: filterSlice.dateRange {start, end}
              ↓
API: GET /api/v1/occurrences?startDate={start}&endDate={end}
              ↓
Backend: Date filter in WHERE clause
              ↓
Response: Filtered occurrences
              ↓
Map Update: Re-render markers, update count
```

### 4. Layer Toggle Switches
```
UI Component: <LayerToggle layerId="ecosystems" />
              ↓
State: mapSlice.activeLayers[] array
              ↓
Map Action: Add/remove layer from map
              ↓
Tile Source: GET /api/v1/tiles/ecosystems/{z}/{x}/{y}.mvt
              ↓
Backend: Generate vector tile from PostGIS
              ↓
Map Render: Display ecosystem boundaries
```

### 5. Quality Threshold Slider
```
UI Component: <QualitySlider min={0} max={100} />
              ↓
State: filterSlice.qualityThreshold
              ↓
API: GET /api/v1/occurrences?qualityMin={threshold}
              ↓
Backend: WHERE quality_score >= threshold
              ↓
Response: High-quality occurrences only
              ↓
Map Update: Remove low-quality markers
```

---

## Data Flow Timing

### Fast Interactions (<100ms)
- Toggle layer visibility (client-side)
- Pan/zoom map (GPU-accelerated)
- Switch between tabs (React routing)
- Open/close panels (state change only)

### Medium Interactions (100-500ms)
- Species autocomplete search (cached)
- Region boundary loading (from cache)
- Occurrence count updates (indexed query)
- Chart data refresh (materialized views)

### Slow Interactions (500ms-2s)
- Initial occurrence fetch (large dataset)
- Indicator computation (complex aggregation)
- Tile generation (first load, no cache)
- Export large datasets (streaming response)

---

## Optimization Strategies

### 1. Debounced Search
```javascript
// Prevent API spam during typing
const debouncedSearch = useMemo(
  () => debounce((query) => {
    dispatch(searchSpecies(query));
  }, 300),
  [dispatch]
);
```

### 2. Request Caching
```javascript
// Cache API responses
const cachedFetch = async (url) => {
  const cached = cache.get(url);
  if (cached && !isExpired(cached)) {
    return cached.data;
  }
  
  const data = await fetch(url).then(r => r.json());
  cache.set(url, { data, timestamp: Date.now() });
  return data;
};
```

### 3. Lazy Loading
```javascript
// Load components only when needed
const Dashboard = lazy(() => import('./features/dashboard/Dashboard'));
const Export = lazy(() => import('./features/export/Export'));
```

### 4. Virtual Scrolling
```javascript
// Render only visible list items
<VirtualList
  items={occurrences}
  itemHeight={60}
  visibleCount={20}
/>
```

### 5. Web Workers
```javascript
// Process large datasets off main thread
const worker = new Worker('dataProcessor.worker.js');
worker.postMessage({ action: 'processOccurrences', data });
worker.onmessage = (e) => setProcessedData(e.data);
```

---

## Error Handling Flow

### Network Error
```
API Call Fails → Redux Error Action → UI Error Boundary
                                     ↓
                           Show Error Message
                                     ↓
                           "Retry" Button → Re-attempt API Call
```

### Validation Error
```
User Input → Client-side Validation Fails
                     ↓
           Show Inline Error Message
                     ↓
           Disable Submit Button
```

### Backend Error (500)
```
Backend Error → API Returns Error → Redux Error State
                                          ↓
                              Log to Sentry (monitoring)
                                          ↓
                              Show User-friendly Message
```

---

## Real-Time Updates

### WebSocket Connection
```javascript
// Establish WebSocket for live updates
const ws = new WebSocket('wss://api.hmbis.org/ws');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  
  switch (update.type) {
    case 'NEW_OCCURRENCE':
      dispatch(addOccurrence(update.data));
      showNotification('New observation added!');
      break;
      
    case 'INDICATOR_UPDATED':
      dispatch(updateIndicator(update.data));
      break;
  }
};
```

### Auto-Refresh Strategy
```javascript
// Poll for updates every 5 minutes
useEffect(() => {
  const interval = setInterval(() => {
    if (document.visibilityState === 'visible') {
      dispatch(refreshData());
    }
  }, 300000); // 5 minutes
  
  return () => clearInterval(interval);
}, []);
```

---

## Accessibility Features

### Keyboard Navigation
```javascript
// Map controls accessible via keyboard
<button
  onClick={handleZoomIn}
  onKeyPress={(e) => e.key === 'Enter' && handleZoomIn()}
  aria-label="Zoom in"
>
  +
</button>
```

### Screen Reader Support
```javascript
// Announce map updates
<div role="status" aria-live="polite" aria-atomic="true">
  {occurrenceCount} observations loaded
</div>
```

### Focus Management
```javascript
// Trap focus in modal dialogs
<Modal onClose={handleClose}>
  <FocusTrap>
    <DialogContent />
  </FocusTrap>
</Modal>
```

---

**Export Instructions**:
```bash
# Generate interaction diagram
mmdc -i 04_user_interaction.md -o user_interaction.svg -t neutral -b transparent
mmdc -i 04_user_interaction.md -o user_interaction.png -t neutral -w 2400 -H 2800
```

---

**Document**: User Interaction Overview - UI to Data Flow  
**Version**: 1.0  
**Date**: November 6, 2025  
**Framework**: React 19 + Redux Toolkit + MapLibre GL JS
