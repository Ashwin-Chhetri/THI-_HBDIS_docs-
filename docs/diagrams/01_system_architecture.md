# Figure 5. System Architecture of the Himalayan Knowledge Common

## Visual Diagram

```mermaid
graph LR
    %% Styling
    classDef dataSource fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20
    classDef ingestion fill:#E3F2FD,stroke:#2196F3,stroke-width:2px,color:#0D47A1
    classDef repository fill:#FFF3E0,stroke:#FF9800,stroke-width:2px,color:#E65100
    classDef visualization fill:#F3E5F5,stroke:#9C27B0,stroke-width:2px,color:#4A148C
    classDef user fill:#FCE4EC,stroke:#E91E63,stroke-width:2px,color:#880E4F
    classDef crosscutting fill:#ECEFF1,stroke:#607D8B,stroke-width:2px,color:#263238
    
    %% Data Sources Layer
    subgraph DS[" 📊 DATA SOURCES "]
        ATREE[ATREE Long-term<br/>Monitoring Data]:::dataSource
        GBIF[GBIF & India<br/>Biodiversity Portal]:::dataSource
        GEO[Public Geospatial<br/>Datasets<br/>Land Use | Elevation | Climate]:::dataSource
        SOCIO[Socio-Economic<br/>Datasets<br/>Census | Village-level]:::dataSource
    end
    
    %% Ingestion Layer
    subgraph IL[" 🔄 INGESTION & STANDARDIZATION "]
        META[Metadata Cataloguing<br/>Darwin Core | ISO 19115]:::ingestion
        VALID[Data Validation<br/>Cleaning | Harmonization]:::ingestion
    end
    
    %% Repository Layer
    subgraph RL[" 💾 DATA REPOSITORY & PROCESSING "]
        STORAGE[Central Storage<br/>PostgreSQL + PostGIS]:::repository
        VERSION[Data Versioning &<br/>Provenance System]:::repository
        COMPUTE[Indicator Computation<br/>SMI | SDI | SHI Calculators]:::repository
    end
    
    %% Visualization Layer
    subgraph VL[" 🎨 VISUALIZATION & API "]
        API[REST/GraphQL APIs<br/>Clean & Aggregated Data]:::visualization
        MAP[Map & Dashboard<br/>Services<br/>MapLibre GL JS]:::visualization
        UI[UI Components<br/>Filters | Search | Layers]:::visualization
    end
    
    %% User Interaction Layer
    subgraph UL[" 👤 USER INTERACTION "]
        PUBLIC[Public Interface<br/>Explore Map | Data Pathways]:::user
        ADMIN[Administrative Tools<br/>Upload | Curation Dashboard]:::user
        EXPORT[Export & Download<br/>CSV | GeoJSON | Shapefile]:::user
    end
    
    %% Cross-cutting Concerns
    subgraph CC[" 🔐 CROSS-CUTTING SERVICES "]
        AUTH[Authentication &<br/>Access Control<br/>Sensitive Data Tiers]:::crosscutting
        LOG[Logging & Monitoring<br/>Update Cycles | Usage Stats]:::crosscutting
    end
    
    %% Data Flow Arrows
    ATREE --> META
    GBIF --> META
    GEO --> META
    SOCIO --> META
    
    META --> VALID
    VALID --> STORAGE
    
    STORAGE --> VERSION
    STORAGE --> COMPUTE
    VERSION --> COMPUTE
    
    COMPUTE --> API
    STORAGE --> API
    
    API --> MAP
    API --> UI
    MAP --> PUBLIC
    UI --> PUBLIC
    
    API --> ADMIN
    API --> EXPORT
    
    %% Cross-cutting connections
    AUTH -.->|Controls Access| API
    AUTH -.->|Manages| ADMIN
    LOG -.->|Monitors| STORAGE
    LOG -.->|Tracks| API
    LOG -.->|Records| PUBLIC
```

## Architecture Description

### Layer 1: Data Sources (Left Side)
**Purpose**: External and internal data inputs feeding the Knowledge Common

- **ATREE Long-term Monitoring Data**: Field observations, ecological surveys, and research datasets
- **GBIF & India Biodiversity Portal**: Species occurrence records via APIs
- **Public Geospatial Datasets**: Land use, elevation models (SRTM), climate data (WorldClim)
- **Socio-Economic Datasets**: Census data, village-level statistics, household surveys

### Layer 2: Ingestion & Standardization
**Purpose**: Ensure data quality and interoperability

- **Metadata Cataloguing**: 
  - Darwin Core standard for biodiversity data
  - ISO 19115 for spatial metadata
  - Automated metadata extraction

- **Data Validation**:
  - Schema validation against defined standards
  - Coordinate verification and precision flagging
  - Taxonomy matching against GBIF backbone
  - Duplicate detection and conflict resolution

### Layer 3: Data Repository & Processing
**Purpose**: Central storage and analytical processing

- **Central Storage**: 
  - PostgreSQL for structured data
  - PostGIS extension for spatial data
  - Optimized with spatial indexes

- **Data Versioning & Provenance**:
  - Track data lineage and transformations
  - Maintain update history
  - Enable rollback capabilities

- **Indicator Computation**:
  - **SMI**: Species Monitoring Index
  - **SDI**: Species Distribution Index  
  - **SHI**: Species Health Index
  - Automated recalculation on data updates

### Layer 4: Visualization & API
**Purpose**: Serve processed data to applications

- **REST/GraphQL APIs**:
  - RESTful endpoints for occurrence data, regions, species
  - GraphQL for complex nested queries
  - Rate limiting and caching (Redis)

- **Map & Dashboard Services**:
  - Vector tile generation for performance
  - MapLibre GL JS rendering engine
  - Real-time layer updates

- **UI Components**:
  - Species search and autocomplete
  - Region/polygon selection tools
  - Date range and attribute filters
  - Layer visibility toggles

### Layer 5: User Interaction (Right Side)
**Purpose**: End-user interfaces and tools

- **Public Interface**:
  - Interactive map exploration
  - Data pathways and stories
  - Species profiles and occurrence maps

- **Administrative Tools**:
  - Bulk data upload interface
  - Curation and review dashboard
  - Data quality monitoring

- **Export & Download**:
  - Multiple format support (CSV, GeoJSON, Shapefile)
  - Metadata bundling
  - Citation generation

### Cross-Cutting Services
**Purpose**: System-wide concerns

- **Authentication & Access Control**:
  - JWT-based authentication
  - Role-based access (Public, Researcher, Administrator)
  - Sensitive data tier management

- **Logging & Monitoring**:
  - API usage tracking
  - Database performance metrics
  - User interaction analytics
  - Update cycle monitoring

## Technical Standards

### Data Standards
- **Darwin Core**: Species occurrence data standardization
- **ISO 19115**: Geographic metadata standard
- **OGC Standards**: WMS, WFS for spatial data services
- **GeoJSON**: Vector data exchange format

### API Standards
- **REST**: Richardson Maturity Model Level 2+
- **OpenAPI 3.0**: API documentation
- **JSON:API**: Resource relationship specification
- **GraphQL**: Flexible query interface

### Security Standards
- **OAuth 2.0**: Authorization framework
- **JWT**: Token-based authentication
- **HTTPS/TLS 1.3**: Encrypted communication
- **CORS**: Cross-origin resource sharing policies

## Scalability Considerations

### Horizontal Scaling
- Load-balanced API servers
- Database read replicas
- CDN for static assets
- Redis cache cluster

### Regional Expansion
- Database partitioning by region
- Microservices for region-specific processing
- Multi-region deployment support

### Performance Optimization
- Vector tiles for map rendering (handles millions of points)
- Materialized views for pre-computed aggregations
- Lazy loading for UI components
- Service worker caching

## Color Legend
- 🟢 **Green** (Data Sources): External inputs and datasets
- 🔵 **Blue** (Ingestion): Data processing and standardization
- 🟠 **Orange** (Repository): Storage and computation
- 🟣 **Purple** (Visualization): APIs and rendering
- 🔴 **Pink** (User): Interactive interfaces
- ⚫ **Gray** (Cross-cutting): System-wide services

---

**Export Instructions**:
- **For SVG**: Use Mermaid Live Editor (https://mermaid.live) or mermaid-cli
- **For PNG**: Export at 300 DPI, 2400x1800px minimum
- **Color Palette**: Compatible with ATREE/THI branding (greens, teals, neutrals)

**Rendering Command**:
```bash
# Using mermaid-cli
mmdc -i 01_system_architecture.md -o system_architecture.svg -t neutral -b transparent
mmdc -i 01_system_architecture.md -o system_architecture.png -t neutral -w 2400 -H 1800
```

---

**Document**: Figure 5 - System Architecture  
**Version**: 1.0  
**Date**: November 6, 2025  
**Organization**: The Himalayan Initiative
