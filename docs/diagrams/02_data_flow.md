# Figure 6. Data Flow for the Knowledge Common

## Visual Diagram

```mermaid
graph TB
    %% Styling
    classDef input fill:#E8F5E9,stroke:#4CAF50,stroke-width:3px,color:#1B5E20
    classDef metadata fill:#E3F2FD,stroke:#2196F3,stroke-width:3px,color:#0D47A1
    classDef database fill:#FFF3E0,stroke:#FF9800,stroke-width:3px,color:#E65100
    classDef compute fill:#FCE4EC,stroke:#E91E63,stroke-width:3px,color:#880E4F
    classDef visualize fill:#F3E5F5,stroke:#9C27B0,stroke-width:3px,color:#4A148C
    classDef output fill:#C8E6C9,stroke:#388E3C,stroke-width:3px,color:#1B5E20
    
    %% Stage 1: Data Input
    subgraph S1[" 🔵 STAGE 1: DATA INPUT "]
        EXT[External Sources<br/>━━━━━━━━━━<br/>• GBIF API<br/>• Open Repositories<br/>• Remote Sensing]:::input
        INT[Internal Sources<br/>━━━━━━━━━━<br/>• ATREE Datasets<br/>• CSV Uploads<br/>• Field Observations]:::input
    end
    
    %% Stage 2: Metadata & Validation
    subgraph S2[" 🔷 STAGE 2: METADATA EXTRACTION & VALIDATION "]
        PARSE[Automated Parsing<br/>━━━━━━━━━━<br/>• File format detection<br/>• Column mapping<br/>• Encoding normalization]:::metadata
        REGISTRY[Metadata Registry<br/>━━━━━━━━━━<br/>• Darwin Core fields<br/>• ISO 19115 spatial metadata<br/>• Provenance tracking]:::metadata
        ERROR[Error Checking<br/>━━━━━━━━━━<br/>• Schema validation<br/>• Coordinate verification<br/>• Taxonomy matching]:::metadata
        FLAGS[Validation Flags<br/>━━━━━━━━━━<br/>• Quality score (0-100)<br/>• Issue categories<br/>• Manual review queue]:::metadata
    end
    
    %% Stage 3: Database Integration
    subgraph S3[" 🟠 STAGE 3: DATABASE INTEGRATION "]
        STANDARD[Standardized Datasets<br/>━━━━━━━━━━<br/>• Normalized schema<br/>• Unified coordinate system<br/>• Consistent taxonomy]:::database
        POSTGIS[PostgreSQL + PostGIS<br/>━━━━━━━━━━<br/>• Spatial tables<br/>• Indexed queries<br/>• Partitioned by region]:::database
        PROV[Provenance Tracking<br/>━━━━━━━━━━<br/>• Source attribution<br/>• Update timestamps<br/>• Version history]:::database
    end
    
    %% Stage 4: Indicator Computation
    subgraph S4[" 🔴 STAGE 4: INDICATOR COMPUTATION "]
        AGG[Aggregate Metrics<br/>━━━━━━━━━━<br/>• Species counts<br/>• Spatial distributions<br/>• Temporal trends]:::compute
        SMI[Species Monitoring Index<br/>━━━━━━━━━━<br/>• Observation frequency<br/>• Population trends<br/>• Range changes]:::compute
        SDI[Species Distribution Index<br/>━━━━━━━━━━<br/>• Habitat occupancy<br/>• Elevation ranges<br/>• Ecosystem presence]:::compute
        SHI[Species Health Index<br/>━━━━━━━━━━<br/>• Conservation status<br/>• Threat assessment<br/>• Ecological integrity]:::compute
    end
    
    %% Stage 5: Visualization Pipeline
    subgraph S5[" 🟣 STAGE 5: VISUALIZATION PIPELINE "]
        QUERY[Database Query<br/>━━━━━━━━━━<br/>• Spatial filters<br/>• Attribute filters<br/>• Pagination]:::visualize
        TILE[GeoJSON Tile Generation<br/>━━━━━━━━━━<br/>• Vector tiles (MVT)<br/>• Zoom-level optimization<br/>• Tile caching]:::visualize
        RENDER[Frontend Rendering<br/>━━━━━━━━━━<br/>• MapLibre GL JS<br/>• Interactive layers<br/>• Chart libraries (D3)]:::visualize
    end
    
    %% Stage 6: User Output
    subgraph S6[" 🟢 STAGE 6: USER OUTPUT "]
        DOWNLOAD[Download/Export Tools<br/>━━━━━━━━━━<br/>• CSV export<br/>• GeoJSON/Shapefile<br/>• PDF reports]:::output
        DASH[Interactive Dashboards<br/>━━━━━━━━━━<br/>• Species profiles<br/>• Regional summaries<br/>• Temporal comparisons]:::output
        CHANGE[Change Indicators<br/>━━━━━━━━━━<br/>• Trend visualizations<br/>• Before/after maps<br/>• Alert notifications]:::output
    end
    
    %% Flow Connections
    EXT --> PARSE
    INT --> PARSE
    
    PARSE --> REGISTRY
    REGISTRY --> ERROR
    ERROR --> FLAGS
    
    FLAGS --> STANDARD
    STANDARD --> POSTGIS
    POSTGIS --> PROV
    
    PROV --> AGG
    AGG --> SMI
    AGG --> SDI
    AGG --> SHI
    
    SMI --> QUERY
    SDI --> QUERY
    SHI --> QUERY
    POSTGIS --> QUERY
    
    QUERY --> TILE
    TILE --> RENDER
    
    RENDER --> DOWNLOAD
    RENDER --> DASH
    RENDER --> CHANGE
    
    %% Feedback loops
    FLAGS -.->|Manual Corrections| INT
    ERROR -.->|Rejected Records| INT
    PROV -.->|Update Notifications| RENDER
```

## Data Flow Description

### 🔵 Stage 1: Data Input

**External Sources** (Blue Box)
- **GBIF API**: Real-time species occurrence data via REST API
- **Open Repositories**: Public datasets (WorldClim, SRTM, OpenStreetMap)
- **Remote Sensing**: Satellite imagery, land cover classifications

**Internal Sources** (Blue Box)
- **ATREE Datasets**: Research project data, long-term monitoring records
- **CSV Uploads**: User-contributed spreadsheets via web interface
- **Field Observations**: GPS-tagged observations, photos, field notes

**Flow**: Raw data enters the system from multiple channels → Automated processing begins

---

### 🔷 Stage 2: Metadata Extraction & Validation

**Automated Parsing** (Light Blue)
1. Detect file format (CSV, Excel, JSON, XML, Shapefile)
2. Map columns to standard fields (e.g., "Species Name" → `scientificName`)
3. Normalize text encoding (UTF-8) and date formats (ISO 8601)

**Metadata Registry** (Light Blue)
1. Extract Darwin Core fields:
   - `scientificName`, `decimalLatitude`, `decimalLongitude`
   - `eventDate`, `basisOfRecord`, `recordedBy`
2. ISO 19115 spatial metadata:
   - Coordinate reference system (CRS)
   - Spatial extent (bounding box)
   - Data lineage
3. Provenance information:
   - Dataset source and citation
   - Collection date and collector
   - Data license (CC0, CC-BY, etc.)

**Error Checking** (Light Blue)
1. **Schema Validation**:
   - Required fields present
   - Data types correct (numeric coordinates, valid dates)
2. **Coordinate Verification**:
   - Within Eastern Himalaya bounds (lat: 26-29°N, lon: 87-95°E)
   - Precision assessment (decimal places)
   - Swap detection (lat/lon reversed)
3. **Taxonomy Matching**:
   - Match against GBIF backbone taxonomy
   - Flag unmatched or ambiguous names
   - Resolve synonyms to accepted names

**Validation Flags** (Light Blue)
1. **Quality Score** (0-100):
   - 90-100: High quality (complete metadata, precise coordinates)
   - 70-89: Medium quality (minor issues, acceptable)
   - <70: Low quality (requires review)
2. **Issue Categories**:
   - 🟢 Green: No issues
   - 🟡 Yellow: Minor warnings
   - 🔴 Red: Critical errors
3. **Manual Review Queue**:
   - Records flagged for expert review
   - Curator dashboard for approval/rejection

**Flow**: Raw data → Parsed and validated → Tagged with quality flags

---

### 🟠 Stage 3: Database Integration

**Standardized Datasets** (Orange)
- **Normalized Schema**: All records conform to common structure
- **Unified Coordinate System**: WGS84 (EPSG:4326)
- **Consistent Taxonomy**: Accepted names from GBIF backbone

**PostgreSQL + PostGIS** (Orange)
- **Spatial Tables**:
  ```sql
  CREATE TABLE occurrences (
      id UUID PRIMARY KEY,
      scientific_name VARCHAR(255),
      location GEOMETRY(Point, 4326),
      event_date DATE,
      quality_score INTEGER
  );
  ```
- **Indexed Queries**: Fast spatial and attribute searches
- **Partitioned by Region**: Optimized for Eastern Himalaya sub-regions

**Provenance Tracking** (Orange)
- **Source Attribution**: Link back to original dataset
- **Update Timestamps**: Track when records added/modified
- **Version History**: Maintain audit trail of changes

**Flow**: Validated data → Stored in spatial database → Ready for analysis

---

### 🔴 Stage 4: Indicator Computation

**Aggregate Metrics** (Pink)
- **Species Counts**: Total species per region/ecosystem
- **Spatial Distributions**: Density maps, range polygons
- **Temporal Trends**: Observations over time

**Species Monitoring Index (SMI)** (Pink)
$$\text{SMI} = \frac{\text{Recent Observations}}{\text{Historical Baseline}} \times 100$$

- Tracks observation frequency changes
- Detects population trend signals
- Alerts on range contractions

**Species Distribution Index (SDI)** (Pink)
$$\text{SDI} = \frac{\text{Occupied Grid Cells}}{\text{Total Suitable Cells}} \times 100$$

- Measures habitat occupancy
- Elevation range analysis
- Ecosystem-specific presence

**Species Health Index (SHI)** (Pink)
$$\text{SHI} = w_1 \cdot \text{IUCN Status} + w_2 \cdot \text{Population Trend} + w_3 \cdot \text{Habitat Quality}$$

- Integrates conservation status
- Assesses threat levels
- Ecological integrity scoring

**Flow**: Raw occurrence data → Aggregated and analyzed → Indicators computed

---

### 🟣 Stage 5: Visualization Pipeline

**Database Query** (Purple)
1. **Spatial Filters**: Bounding box, polygon, buffer zones
2. **Attribute Filters**: Species, date range, quality threshold
3. **Pagination**: Handle large result sets (>100K records)

**GeoJSON Tile Generation** (Purple)
1. **Vector Tiles (MVT)**:
   - Mapbox Vector Tile format
   - Pre-rendered at zoom levels 0-14
2. **Zoom-level Optimization**:
   - Level 0-5: Clustered points
   - Level 6-10: Simplified geometries
   - Level 11-14: Full detail
3. **Tile Caching**:
   - Redis cache for frequently accessed tiles
   - CDN distribution for global access

**Frontend Rendering** (Purple)
1. **MapLibre GL JS**:
   - Hardware-accelerated rendering
   - Smooth pan/zoom interactions
   - Dynamic layer styling
2. **Interactive Layers**:
   - Species occurrence points
   - Protected area boundaries
   - Elevation contours
3. **Chart Libraries**:
   - D3.js for custom visualizations
   - Recharts for standard charts
   - Plotly for 3D plots

**Flow**: Database queries → Efficient tile generation → Beautiful map display

---

### 🟢 Stage 6: User Output

**Download/Export Tools** (Green)
- **CSV Export**: Filtered occurrence records with all attributes
- **GeoJSON/Shapefile**: Spatial data for GIS software
- **PDF Reports**: Formatted summaries with maps and charts
- **Metadata Bundling**: Include data dictionary and citations

**Interactive Dashboards** (Green)
- **Species Profiles**:
  - Distribution maps
  - Observation timeline
  - Conservation status
- **Regional Summaries**:
  - Species richness
  - Ecosystem health
  - Land use changes
- **Temporal Comparisons**:
  - Before/after analysis
  - Seasonal patterns
  - Long-term trends

**Change Indicators** (Green)
- **Trend Visualizations**:
  - Line charts showing SMI/SDI/SHI over time
  - Heat maps of changing distributions
- **Before/After Maps**:
  - Side-by-side comparisons
  - Slider for temporal navigation
- **Alert Notifications**:
  - Email alerts for significant changes
  - Dashboard warnings for declining species
  - Export for reports and publications

**Flow**: Processed data → User-friendly visualizations → Actionable insights

---

## Color-Coded Flow Legend

| Color | Stage | Purpose |
|-------|-------|---------|
| 🔵 **Blue** | Data Input | Raw data entry points |
| 🔷 **Light Blue** | Metadata & Validation | Quality assurance |
| 🟠 **Orange** | Database Integration | Persistent storage |
| 🔴 **Pink** | Indicator Computation | Analytical processing |
| 🟣 **Purple** | Visualization Pipeline | User interface preparation |
| 🟢 **Green** | User Output | Final deliverables |

---

## Technical Implementation Details

### Stage 1-2: Data Ingestion Service
```javascript
// Automated data parser
class DataIngestionService {
  async processUpload(file) {
    // 1. Parse file
    const parsed = await this.parseFile(file);
    
    // 2. Extract metadata
    const metadata = this.extractMetadata(parsed);
    
    // 3. Validate
    const validation = await this.validate(parsed);
    
    // 4. Store with flags
    return this.store(parsed, metadata, validation);
  }
}
```

### Stage 3: Database Storage
```sql
-- Insert with provenance
INSERT INTO occurrences (
  id, scientific_name, location, event_date,
  quality_score, source_id, created_at
) VALUES (
  gen_random_uuid(),
  'Ailurus fulgens',
  ST_SetSRID(ST_MakePoint(88.6138, 27.3389), 4326),
  '2024-01-15',
  92,
  'atree-sikkim-2024',
  NOW()
);
```

### Stage 4: Indicator Calculation
```javascript
// SMI computation
async function calculateSMI(taxonKey, regionId) {
  const recent = await countOccurrences(taxonKey, regionId, recentPeriod);
  const baseline = await countOccurrences(taxonKey, regionId, baselinePeriod);
  
  return (recent / baseline) * 100;
}
```

### Stage 5: Vector Tile Generation
```javascript
// Tile endpoint
app.get('/tiles/:z/:x/:y.mvt', async (req, res) => {
  const { z, x, y } = req.params;
  
  // Query occurrences within tile bounds
  const features = await db.query(`
    SELECT ST_AsMVT(q, 'occurrences', 4096, 'geom')
    FROM (
      SELECT id, scientific_name,
             ST_AsMVTGeom(location, TileBBox(${z}, ${x}, ${y}), 4096, 0, false) AS geom
      FROM occurrences
      WHERE location && TileBBox(${z}, ${x}, ${y})
    ) q
  `);
  
  res.setHeader('Content-Type', 'application/x-protobuf');
  res.send(features);
});
```

---

## Feedback Loops (Dotted Lines)

1. **Manual Corrections** (Validation → Input):
   - Rejected records returned to data providers
   - Correction instructions provided
   - Re-upload mechanism

2. **Rejected Records** (Error Checking → Input):
   - Critical errors prevent storage
   - Error reports generated
   - Resubmission required

3. **Update Notifications** (Provenance → Rendering):
   - Real-time updates when data changes
   - WebSocket notifications to frontend
   - Automatic map refresh

---

**Export Instructions**:
```bash
# Generate SVG
mmdc -i 02_data_flow.md -o data_flow.svg -t neutral -b transparent

# Generate high-res PNG
mmdc -i 02_data_flow.md -o data_flow.png -t neutral -w 2400 -H 3000 -s 2
```

---

**Document**: Figure 6 - Data Flow Diagram  
**Version**: 1.0  
**Date**: November 6, 2025  
**Organization**: The Himalayan Initiative  
**Standards**: Darwin Core, ISO 19115, OGC WMS/WFS
