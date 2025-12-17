# Appendices & References
## HMBIS Knowledge Common - Supporting Materials

**Document**: 08 of 08  
**Date**: November 6, 2025  
**Version**: 1.0

---

## Table of Contents

1. [Figure-Ready Diagrams](#1-figure-ready-diagrams)
2. [Technology Stack Reference](#2-technology-stack-reference)
3. [API Reference](#3-api-reference)
4. [Database Schema Reference](#4-database-schema-reference)
5. [Glossary](#5-glossary)
6. [References & Citations](#6-references--citations)
7. [Contributing Guidelines](#7-contributing-guidelines)
8. [License Information](#8-license-information)

---

## 1. Figure-Ready Diagrams

### 1.1 System Architecture Overview

**Figure A.1: High-Level System Architecture**

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   React UI   │  │ MapLibre GL  │  │   Charts     │            │
│  │  Components  │  │     Map      │  │  (D3/Plotly) │            │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘            │
└─────────┼──────────────────┼──────────────────┼────────────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────────┐
│                       STATE MANAGEMENT LAYER                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                      Redux Store                             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │  │
│  │  │ Species  │  │ Regions  │  │   Map    │  │   User   │   │  │
│  │  │  Slice   │  │  Slice   │  │  Slice   │  │  Slice   │   │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                               │                                      │
│                    ┌──────────┴──────────┐                         │
│                    │                     │                          │
│            ┌───────▼──────┐    ┌────────▼────────┐                │
│            │  Redux Saga  │    │  Redux Thunk    │                 │
│            │ (Side Effects)│   │   (Async)       │                 │
│            └───────┬──────┘    └────────┬────────┘                │
└────────────────────┼──────────────────────┼─────────────────────────┘
                     │                      │
                     └──────────┬───────────┘
                                │
┌─────────────────────────────────────────────────────────────────────┐
│                         SERVICE LAYER                                │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │  GBIF Service  │  │  Data Service  │  │  Layer Service │       │
│  │   - Fetch      │  │  - Transform   │  │  - Lifecycle   │       │
│  │   - Search     │  │  - Validate    │  │  - Dependencies│       │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘       │
└───────────┼──────────────────────┼──────────────────┼──────────────┘
            │                      │                  │
            └──────────────────────┼──────────────────┘
                                   │
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐       │
│  │   IndexedDB    │  │  LocalStorage  │  │  SessionStorage│       │
│  │  (Structured)  │  │   (Config)     │  │    (Temp)      │       │
│  └────────┬───────┘  └────────────────┘  └────────────────┘       │
└───────────┼──────────────────────────────────────────────────────────┘
            │
┌───────────▼──────────────────────────────────────────────────────────┐
│                      EXTERNAL DATA SOURCES                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ GBIF API   │  │  MapTiler  │  │  User File │  │   Future   │   │
│  │  (REST)    │  │  (Tiles)   │  │  (Upload)  │  │   (API)    │   │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

**Description**: Complete system architecture showing all layers from presentation to data sources. Arrows indicate data flow direction.

**Export Instructions**: 
- Format: SVG or PNG at 300 DPI
- Dimensions: 1200x1400px
- Background: White
- Fonts: Arial/Helvetica
- Colors: Use organizational brand colors

---

### 1.2 Data Flow - GBIF Occurrence Fetch

**Figure A.2: GBIF Data Fetch & Processing Pipeline**

```
┌─────────────┐
│    User     │
│   Action    │
│ (Click Map) │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│  Dispatch Action                │
│  fetchOccurrences({             │
│    taxonKey: "5218933",         │
│    geometry: polygon            │
│  })                             │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Redux Saga Middleware          │
│  - Intercept action             │
│  - Call API service             │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  GBIF Service                   │
│  1. Build query params          │
│  2. Add geometry filter         │
│  3. Fetch from GBIF API         │
│  4. Handle pagination           │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Network Request                │
│  GET https://api.gbif.org/v1/   │
│      occurrence/search          │
│  ?taxonKey=5218933              │
│  &geometry=POLYGON(...)         │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Response (JSON)                │
│  {                              │
│    results: [...],              │
│    count: 1250,                 │
│    endOfRecords: false          │
│  }                              │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Data Transformation            │
│  - Convert to GeoJSON           │
│  - Normalize date formats       │
│  - Add quality flags            │
│  - Calculate statistics         │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Data Validation                │
│  - Check required fields        │
│  - Validate coordinates         │
│  - Filter invalid records       │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  IndexedDB Storage              │
│  - Store in "occurrences" table │
│  - Create spatial index         │
│  - Update metadata              │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  Redux State Update             │
│  dispatch({                     │
│    type: 'SET_OCCURRENCES',     │
│    payload: processedData       │
│  })                             │
└─────────┬───────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  React Component Re-render      │
│  - Map updates with markers     │
│  - Stats panel shows count      │
│  - Loading indicator hides      │
└─────────────────────────────────┘
```

**Description**: Complete flow from user interaction to visual update, showing all transformation and storage steps.

---

### 1.3 Proposed Backend Architecture

**Figure A.3: Three-Tier Backend Architecture (Proposed)**

```
┌──────────────────────────────────────────────────────────────┐
│                       CLIENT TIER                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Browser  │  │  Mobile  │  │   API    │  │  Admin   │    │
│  │   App    │  │   App    │  │  Client  │  │  Portal  │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
└───────┼─────────────┼─────────────┼─────────────┼───────────┘
        │             │             │             │
        │  HTTPS      │  HTTPS      │  HTTPS      │  HTTPS
        └─────────────┴─────────────┴─────────────┘
                            │
                ┌───────────▼───────────┐
                │   Load Balancer       │
                │   (nginx/HAProxy)     │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼───────┐  ┌────────▼────────┐  ┌──────▼──────┐
│  API Server 1 │  │  API Server 2   │  │API Server N │
│               │  │                 │  │             │
│  ┌─────────┐  │  │  ┌─────────┐   │  │ ┌─────────┐ │
│  │Express  │  │  │  │Express  │   │  │ │Express  │ │
│  │Node.js  │  │  │  │Node.js  │   │  │ │Node.js  │ │
│  └────┬────┘  │  │  └────┬────┘   │  │ └────┬────┘ │
└───────┼───────┘  └────────┼────────┘  └──────┼──────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
┌───────────────────────────────────────────────────────────────┐
│                  APPLICATION TIER                              │
│                                                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   REST API   │  │  WebSocket   │  │   GraphQL    │       │
│  │  Controllers │  │    Server    │  │  (Optional)  │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│  ┌──────┴─────────────────┴─────────────────┴──────┐        │
│  │              Business Logic Layer                │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │        │
│  │  │ Species  │  │  Data    │  │  User    │      │        │
│  │  │ Service  │  │ Adapter  │  │ Service  │      │        │
│  │  └──────────┘  └──────────┘  └──────────┘      │        │
│  └───────────────────────┬──────────────────────────┘        │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   ORM/Query  │  │  Cache Layer │  │  File Storage│       │
│  │   Builder    │  │   (Redis)    │  │    (S3)      │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌───────────────────────────────────────────────────────────────┐
│                      DATA TIER                                 │
│                                                                │
│  ┌──────────────────────┐       ┌──────────────────────┐     │
│  │ PostgreSQL (Primary) │◄─────►│PostgreSQL (Replica)  │     │
│  │     + PostGIS        │       │     + PostGIS        │     │
│  │                      │       │     (Read-only)      │     │
│  │  ┌────────────────┐  │       └──────────────────────┘     │
│  │  │  occurrences   │  │                                     │
│  │  │  species       │  │       ┌──────────────────────┐     │
│  │  │  regions       │  │       │  Redis Cache         │     │
│  │  │  users         │  │       │  - Session store     │     │
│  │  │  layers        │  │       │  - Query cache       │     │
│  │  └────────────────┘  │       │  - Rate limiting     │     │
│  └──────────────────────┘       └──────────────────────┘     │
└───────────────────────────────────────────────────────────────┘
```

**Description**: Proposed production-ready three-tier architecture with load balancing, caching, and database replication.

---

### 1.4 Layer Dependency Graph

**Figure A.4: Layer Lifecycle & Dependencies**

```
                    ┌─────────────────┐
                    │  Base Map       │
                    │  (Always Active)│
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
         ┌──────────▼─────────┐   ┌──▼──────────────┐
         │  Region Boundary   │   │  Terrain Layer  │
         │  (Load on select)  │   │  (Optional)     │
         └──────────┬─────────┘   └─────────────────┘
                    │
         ┌──────────┴──────────┐
         │                     │
    ┌────▼──────────┐   ┌──────▼─────────┐
    │ Protected     │   │  Land Cover    │
    │ Areas         │   │  (Optional)    │
    └────┬──────────┘   └────────────────┘
         │
         │ [User selects species]
         │
    ┌────▼──────────────────────┐
    │  Species Occurrences      │
    │  (Depends on region)      │
    └────┬──────────────────────┘
         │
         ├───► Heatmap (Optional)
         │
         ├───► Cluster (Auto if >1000 points)
         │
         └───► Individual Markers
         
         
Dependency Rules:
─────────────────
1. Base Map must load first
2. Region boundary required before occurrences
3. Heatmap/Cluster mutually exclusive
4. Cluster auto-activates at high density
5. Layers cleanup when dependencies removed
```

**Description**: Visual representation of layer dependencies and loading order. Critical for understanding rendering sequence.

---

### 1.5 Technology Stack Comparison

**Figure A.5: Technology Comparison Matrix**

```
┌─────────────────────────────────────────────────────────────────────┐
│               Frontend Framework Comparison                          │
├──────────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│   Feature    │  React   │   Vue    │ Angular  │  Svelte  │ Current │
├──────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│ Learning     │    ★★★   │   ★★★★   │   ★★     │   ★★★★   │  React  │
│ Ecosystem    │   ★★★★★  │   ★★★★   │   ★★★★   │   ★★★    │    ✓    │
│ Performance  │   ★★★★   │   ★★★★   │   ★★★    │  ★★★★★   │    ✓    │
│ Map Support  │   ★★★★★  │   ★★★★   │   ★★★    │   ★★★    │    ✓    │
│ Community    │   ★★★★★  │   ★★★★   │   ★★★★   │   ★★★    │    ✓    │
│ GIS Libraries│   ★★★★★  │   ★★★    │   ★★★    │   ★★     │    ✓    │
└──────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                 Mapping Library Comparison                           │
├──────────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│   Feature    │ MapLibre │  Leaflet │ Mapbox   │  Cesium  │ Current │
├──────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│ Performance  │  ★★★★★   │   ★★★    │  ★★★★★   │   ★★     │MapLibre │
│ 3D Support   │   ★★★★   │    ★     │   ★★★★   │  ★★★★★   │   N/A   │
│ Vector Tiles │  ★★★★★   │   ★★★    │  ★★★★★   │   ★★★    │    ✓    │
│ Open Source  │  ★★★★★   │  ★★★★★   │    ★     │  ★★★★★   │    ✓    │
│ Documentation│   ★★★★   │  ★★★★★   │  ★★★★★   │   ★★★    │    ✓    │
│ License      │   Free   │   Free   │  Paid*   │   Free   │    ✓    │
└──────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
* Mapbox requires paid account for production use

┌─────────────────────────────────────────────────────────────────────┐
│             State Management Comparison                              │
├──────────────┬──────────┬──────────┬──────────┬──────────┬─────────┤
│   Feature    │  Redux   │  Zustand │  Recoil  │ Context  │ Current │
├──────────────┼──────────┼──────────┼──────────┼──────────┼─────────┤
│ Complexity   │   ★★     │   ★★★★   │   ★★★    │  ★★★★★   │  Redux  │
│ DevTools     │  ★★★★★   │   ★★★    │   ★★★★   │    ★     │    ✓    │
│ Middleware   │  ★★★★★   │   ★★★    │   ★★     │    ★     │    ✓    │
│ Async        │  ★★★★★   │   ★★★★   │   ★★★★   │   ★★     │    ✓    │
│ TypeScript   │  ★★★★★   │  ★★★★★   │   ★★★★   │   ★★★★   │    ✓    │
│ Bundle Size  │   ★★     │  ★★★★★   │   ★★★    │  ★★★★★   │    -    │
└──────────────┴──────────┴──────────┴──────────┴──────────┴─────────┘
```

**Description**: Comparative analysis of technology choices with ratings. Shows why current stack was selected.

---

### 1.6 Performance Benchmarks

**Figure A.6: Load Time & Performance Metrics**

```
Performance Comparison: Current vs. Optimized

Load Time (seconds)
────────────────────────────────────────────────────────────
Current    ████████████████ 3.2s
Optimized  ████████ 1.6s    (↓ 50%)
Target     ██████ 1.2s

Time to Interactive (seconds)
────────────────────────────────────────────────────────────
Current    ██████████████████████ 4.5s
Optimized  ████████████ 2.4s      (↓ 47%)
Target     ████████ 1.8s

First Contentful Paint (seconds)
────────────────────────────────────────────────────────────
Current    ████████ 1.6s
Optimized  ████ 0.8s              (↓ 50%)
Target     ███ 0.6s

Bundle Size (MB)
────────────────────────────────────────────────────────────
Current    ██████████ 2.5 MB
Optimized  ████ 1.0 MB            (↓ 60%)
Target     ███ 0.8 MB

Memory Usage - 10K Records (MB)
────────────────────────────────────────────────────────────
Current    ██████████████████ 280 MB
Optimized  ██████████ 150 MB      (↓ 46%)
Target     ████████ 120 MB

Rendering Time - 10K Points (ms)
────────────────────────────────────────────────────────────
Current    ████████████████ 800ms
Optimized  ████ 200ms             (↓ 75%)
Target     ██ 100ms
```

**Description**: Before/after performance metrics showing optimization impact. Includes targets for Phase 1-2.

---

## 2. Technology Stack Reference

### 2.1 Frontend Dependencies

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| **Core** |
| react | 19.1.1 | UI framework | MIT |
| react-dom | 19.1.1 | React renderer | MIT |
| react-router-dom | 7.5.2 | Routing | MIT |
| **State Management** |
| @reduxjs/toolkit | 2.9.2 | State container | MIT |
| react-redux | 9.2.0 | React bindings | MIT |
| redux-saga | 1.4.2 | Side effects | MIT |
| **Mapping** |
| maplibre-gl | 5.9.0 | Map rendering | BSD-3 |
| @turf/turf | 7.2.0 | Spatial analysis | MIT |
| **Data Visualization** |
| recharts | 2.15.2 | Charts | MIT |
| d3 | 7.9.0 | Data viz | ISC |
| **Storage** |
| dexie | 4.0.10 | IndexedDB wrapper | Apache-2.0 |
| **HTTP Client** |
| axios | 1.8.0 | HTTP requests | MIT |
| **UI Components** |
| @mui/material | 6.3.1 | Component library | MIT |
| **Build Tools** |
| vite | 7.1.7 | Build tool | MIT |
| **Testing** |
| vitest | 3.1.0 | Test framework | MIT |
| @testing-library/react | 16.2.0 | Testing utilities | MIT |

### 2.2 Backend Dependencies (Proposed)

| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| **Runtime** |
| node.js | 20 LTS | JavaScript runtime | MIT |
| **Framework** |
| express | 5.x | Web framework | MIT |
| cors | 2.x | CORS middleware | MIT |
| helmet | 8.x | Security headers | MIT |
| **Database** |
| pg | 8.x | PostgreSQL client | MIT |
| postgis | (extension) | Spatial database | GPL-2.0 |
| **ORM** |
| prisma | 7.x | Database ORM | Apache-2.0 |
| **Caching** |
| redis | 5.x (client) | Cache client | MIT |
| ioredis | 6.x | Redis client | MIT |
| **Authentication** |
| jsonwebtoken | 9.x | JWT auth | MIT |
| bcrypt | 5.x | Password hashing | MIT |
| **Validation** |
| joi | 17.x | Schema validation | BSD-3 |
| **Logging** |
| winston | 3.x | Logging | MIT |
| **Task Queue** |
| bull | 4.x | Job queue | MIT |

### 2.3 Infrastructure

| Service | Provider | Purpose | Cost Tier |
|---------|----------|---------|-----------|
| **Hosting** |
| Frontend | Vercel/Netlify | Static hosting | Free |
| API | DigitalOcean | API servers | $12-48/mo |
| **Database** |
| PostgreSQL | DigitalOcean | Primary DB | $15-200/mo |
| Redis | Upstash/DO | Caching | $10-50/mo |
| **Storage** |
| Object Storage | S3/Spaces | File storage | $5-20/mo |
| **CDN** |
| CDN | CloudFlare | Content delivery | Free-$20/mo |
| **Monitoring** |
| Error Tracking | Sentry | Error monitoring | Free |
| APM | Datadog | Performance | $0-50/mo |
| **CI/CD** |
| Build | GitHub Actions | Automation | Free |

---

## 3. API Reference

### 3.1 Current External APIs

#### GBIF Occurrence Search API

**Endpoint**: `https://api.gbif.org/v1/occurrence/search`

**Method**: `GET`

**Query Parameters**:
```
taxonKey       - GBIF species identifier (integer)
geometry       - WKT polygon or bbox
limit          - Results per page (max 300, default 20)
offset         - Pagination offset
year           - Year filter (e.g., "2020,2024")
basisOfRecord  - Record type (HUMAN_OBSERVATION, etc.)
hasCoordinate  - Boolean (true/false)
hasGeospatialIssue - Boolean (true/false)
```

**Example Request**:
```bash
curl "https://api.gbif.org/v1/occurrence/search?\
taxonKey=5218933&\
geometry=POLYGON((88.0 27.0, 89.0 27.0, 89.0 28.0, 88.0 28.0, 88.0 27.0))&\
limit=100"
```

**Example Response**:
```json
{
  "offset": 0,
  "limit": 100,
  "endOfRecords": false,
  "count": 1250,
  "results": [
    {
      "key": 4019920123,
      "scientificName": "Ailurus fulgens F.Cuvier, 1825",
      "decimalLatitude": 27.3389,
      "decimalLongitude": 88.6138,
      "coordinateUncertaintyInMeters": 30,
      "eventDate": "2024-01-15T10:30:00",
      "basisOfRecord": "HUMAN_OBSERVATION",
      "countryCode": "IN",
      "stateProvince": "Sikkim",
      "locality": "Kanchenjunga National Park",
      "recordedBy": "John Doe",
      "identifiedBy": "Jane Smith",
      "taxonKey": 5218933,
      "kingdom": "Animalia",
      "phylum": "Chordata",
      "class": "Mammalia",
      "order": "Carnivora",
      "family": "Ailuridae",
      "genus": "Ailurus",
      "species": "Ailurus fulgens"
    }
  ]
}
```

**Rate Limit**: 100 requests/minute

**Documentation**: https://www.gbif.org/developer/occurrence

---

#### GBIF Species Matching API

**Endpoint**: `https://api.gbif.org/v1/species/match`

**Method**: `GET`

**Query Parameters**:
```
name     - Scientific name to match
kingdom  - Kingdom filter (optional)
strict   - Strict matching (true/false)
verbose  - Include alternatives (true/false)
```

**Example**:
```bash
curl "https://api.gbif.org/v1/species/match?name=Ailurus%20fulgens"
```

**Response**:
```json
{
  "usageKey": 5218933,
  "scientificName": "Ailurus fulgens F.Cuvier, 1825",
  "canonicalName": "Ailurus fulgens",
  "rank": "SPECIES",
  "status": "ACCEPTED",
  "confidence": 97,
  "matchType": "EXACT",
  "kingdom": "Animalia",
  "phylum": "Chordata",
  "order": "Carnivora",
  "family": "Ailuridae",
  "genus": "Ailurus",
  "species": "Ailurus fulgens",
  "kingdomKey": 1,
  "phylumKey": 44,
  "classKey": 359,
  "orderKey": 732,
  "familyKey": 9673,
  "genusKey": 2435194,
  "speciesKey": 5218933,
  "synonym": false,
  "class": "Mammalia"
}
```

---

### 3.2 Proposed Internal API

#### Authentication

**POST** `/api/v1/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "researcher"
  }
}
```

---

#### Occurrences

**GET** `/api/v1/occurrences`

Query Parameters:
- `regionId` (UUID) - Filter by region
- `taxonKey` (integer) - Filter by species
- `startDate` (ISO 8601) - Filter by date range start
- `endDate` (ISO 8601) - Filter by date range end
- `limit` (integer, max 1000) - Results per page
- `offset` (integer) - Pagination offset

Response:
```json
{
  "total": 1250,
  "limit": 100,
  "offset": 0,
  "data": [
    {
      "id": "uuid",
      "regionId": "uuid",
      "taxonKey": 5218933,
      "scientificName": "Ailurus fulgens",
      "acceptedName": "Ailurus fulgens",
      "location": {
        "type": "Point",
        "coordinates": [88.6138, 27.3389]
      },
      "coordinatePrecision": 0.0001,
      "eventDate": "2024-01-15",
      "source": "GBIF",
      "qualityScore": 85,
      "metadata": {
        "recordedBy": "John Doe",
        "basisOfRecord": "HUMAN_OBSERVATION"
      },
      "createdAt": "2024-01-16T00:00:00Z",
      "updatedAt": "2024-01-16T00:00:00Z"
    }
  ]
}
```

**POST** `/api/v1/occurrences`

Create new occurrence record (requires authentication).

Request:
```json
{
  "regionId": "uuid",
  "taxonKey": 5218933,
  "scientificName": "Ailurus fulgens",
  "location": {
    "latitude": 27.3389,
    "longitude": 88.6138
  },
  "eventDate": "2024-01-15",
  "source": "USER_UPLOAD",
  "metadata": {
    "recordedBy": "Jane Smith",
    "notes": "Observed near forest edge"
  }
}
```

---

#### Regions

**GET** `/api/v1/regions`

Response:
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Sikkim",
      "code": "SKM",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[...]]]
      },
      "bbox": [88.0, 27.0, 89.0, 28.5],
      "area": 7096,
      "statistics": {
        "speciesCount": 500,
        "occurrenceCount": 12500
      }
    }
  ]
}
```

**GET** `/api/v1/regions/:id`

Get single region with detailed statistics.

---

#### Statistics

**GET** `/api/v1/statistics/summary`

Query Parameters:
- `regionId` (UUID, optional)
- `startDate` (ISO 8601, optional)
- `endDate` (ISO 8601, optional)

Response:
```json
{
  "totalSpecies": 500,
  "totalOccurrences": 12500,
  "recentObservations": 45,
  "topSpecies": [
    {
      "taxonKey": 5218933,
      "scientificName": "Ailurus fulgens",
      "count": 125
    }
  ],
  "temporalDistribution": [
    {"month": "2024-01", "count": 450},
    {"month": "2024-02", "count": 520}
  ]
}
```

---

## 4. Database Schema Reference

### 4.1 Proposed PostgreSQL Schema

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm; -- For fuzzy text search

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    organization VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Regions table
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    geometry GEOMETRY(Polygon, 4326) NOT NULL,
    bbox GEOMETRY(Polygon, 4326) NOT NULL,
    area DECIMAL(12, 2), -- Square kilometers
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Taxonomy cache
CREATE TABLE taxonomy_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    input_name VARCHAR(255) NOT NULL,
    taxon_key BIGINT UNIQUE NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    canonical_name VARCHAR(255),
    rank VARCHAR(50),
    status VARCHAR(50),
    kingdom VARCHAR(100),
    phylum VARCHAR(100),
    class VARCHAR(100),
    "order" VARCHAR(100),
    family VARCHAR(100),
    genus VARCHAR(100),
    species VARCHAR(100),
    confidence INTEGER,
    synonyms JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Occurrences table (partitioned by region)
CREATE TABLE occurrences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    taxon_key BIGINT NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    accepted_name VARCHAR(255),
    location GEOMETRY(Point, 4326) NOT NULL,
    coordinate_precision DECIMAL(10, 8),
    coordinate_uncertainty DECIMAL(10, 2),
    event_date DATE,
    event_time TIME,
    basis_of_record VARCHAR(100),
    source VARCHAR(50) NOT NULL,
    source_id VARCHAR(255),
    quality_score INTEGER,
    recorded_by VARCHAR(255),
    identified_by VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
) PARTITION BY LIST (region_id);

-- Create partitions (example for Sikkim)
-- CREATE TABLE occurrences_sikkim PARTITION OF occurrences
--     FOR VALUES IN ('sikkim-region-uuid');

-- Spatial indexes
CREATE INDEX idx_occurrences_location 
    ON occurrences USING GIST(location);

CREATE INDEX idx_occurrences_region 
    ON occurrences(region_id);

CREATE INDEX idx_occurrences_taxon 
    ON occurrences(taxon_key);

CREATE INDEX idx_occurrences_date 
    ON occurrences(event_date);

CREATE INDEX idx_occurrences_quality 
    ON occurrences(quality_score);

-- Full-text search index
CREATE INDEX idx_occurrences_scientific_name 
    ON occurrences USING GIN(scientific_name gin_trgm_ops);

-- Layers table (for custom user layers)
CREATE TABLE layers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    region_id UUID REFERENCES regions(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    data JSONB NOT NULL,
    style JSONB,
    visible BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Activity log
CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Materialized view for statistics (fast aggregates)
CREATE MATERIALIZED VIEW region_statistics AS
SELECT 
    r.id as region_id,
    r.name as region_name,
    COUNT(DISTINCT o.taxon_key) as species_count,
    COUNT(o.id) as occurrence_count,
    AVG(o.quality_score) as avg_quality,
    MAX(o.updated_at) as last_updated
FROM regions r
LEFT JOIN occurrences o ON r.id = o.region_id
GROUP BY r.id, r.name;

-- Create index on materialized view
CREATE UNIQUE INDEX idx_region_stats_region 
    ON region_statistics(region_id);

-- Refresh function for statistics
CREATE OR REPLACE FUNCTION refresh_statistics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY region_statistics;
END;
$$ LANGUAGE plpgsql;
```

### 4.2 IndexedDB Schema (Current)

```javascript
// Current client-side database schema
const db = new Dexie('HMBISDatabase');

db.version(1).stores({
  // Species data
  species: '++id, taxonKey, scientificName, acceptedName',
  
  // Occurrence records
  occurrences: '++id, taxonKey, regionId, [taxonKey+regionId], eventDate',
  
  // Region geometries
  regions: '++id, code, name',
  
  // Layer configurations
  layers: '++id, type, regionId, visible',
  
  // User preferences
  preferences: '++id, key',
  
  // Cache metadata
  cache: '++id, key, timestamp'
});

// Compound indexes for efficient queries
db.version(2).stores({
  occurrences: '++id, taxonKey, regionId, [taxonKey+regionId], eventDate, [regionId+eventDate]'
});
```

---

## 5. Glossary

**Darwin Core**: A standard for biodiversity data sharing, defining fields like scientificName, eventDate, decimalLatitude, etc.

**GeoJSON**: A format for encoding geographic data structures using JSON. Used for vector geometries.

**GBIF (Global Biodiversity Information Facility)**: International network providing open access to biodiversity data.

**IndexedDB**: Browser API for client-side storage of structured data, including files/blobs.

**MapLibre GL JS**: Open-source library for rendering interactive maps from vector tiles.

**OGC (Open Geospatial Consortium)**: International organization developing standards for geospatial content.

**PostGIS**: Spatial database extension for PostgreSQL, enabling geographic queries.

**Redux Saga**: Middleware library for managing side effects in Redux applications.

**Taxon Key**: Unique identifier for a species or taxonomic group in GBIF.

**Vector Tiles**: Map tiles that contain vector data rather than rendered images, allowing client-side styling.

**Web Workers**: JavaScript running in background threads, preventing UI blocking.

**WKT (Well-Known Text)**: Text markup language for representing vector geometry (e.g., POLYGON(...)).

---

## 6. References & Citations

### Academic & Standards

1. **Darwin Core Standard**
   - Darwin Core Task Group. (2021). *Darwin Core Quick Reference Guide*.
   - URL: https://dwc.tdwg.org/terms/
   - Last accessed: 2025-11-06

2. **GBIF Data Quality Requirements**
   - Chapman, A. D. (2005). *Principles of Data Quality*.
   - GBIF: Copenhagen. ISBN: 87-92020-03-8
   - URL: https://www.gbif.org/document/80509

3. **Spatial Data Infrastructure Best Practices**
   - OGC. (2024). *OGC Standards and Supporting Documents*.
   - URL: https://www.ogc.org/standards/

### Platform Documentation

4. **GBIF API Documentation**
   - URL: https://www.gbif.org/developer/summary
   - Version: v1
   - Last accessed: 2025-11-06

5. **MapLibre GL JS Documentation**
   - URL: https://maplibre.org/maplibre-gl-js/docs/
   - Version: 5.9.0
   - Last accessed: 2025-11-06

6. **React Documentation**
   - URL: https://react.dev
   - Version: 19.x
   - Last accessed: 2025-11-06

7. **Redux Toolkit Documentation**
   - URL: https://redux-toolkit.js.org
   - Version: 2.x
   - Last accessed: 2025-11-06

### Comparable Platforms

8. **Map of Life Technical Architecture**
   - URL: https://mol.org
   - Jetz, W., et al. (2012). *Integrating biodiversity distribution knowledge*.

9. **Global Forest Watch Platform**
   - URL: https://www.globalforestwatch.org
   - World Resources Institute. (2024).

10. **India Biodiversity Portal**
    - URL: https://indiabiodiversity.org
    - Karthik, R., et al. (2021). *India Biodiversity Portal: A case study*.

11. **Atlas of Living Australia**
    - URL: https://www.ala.org.au
    - Belbin, L., et al. (2021). *The Atlas of Living Australia*.

### Conservation & Biodiversity

12. **The Himalayan Initiative Overview**
    - Organization website
    - Mission and objectives documentation

13. **Eastern Himalaya Biodiversity Hotspot**
    - Myers, N., et al. (2000). *Biodiversity hotspots for conservation priorities*.
    - Nature, 403, 853-858.

14. **IUCN Red List Categories**
    - URL: https://www.iucnredlist.org
    - Version: 2024-1

---

## 7. Contributing Guidelines

### Code Contributions

**Branch Naming**:
```
feature/<short-description>    - New features
bugfix/<issue-number>          - Bug fixes
refactor/<module-name>         - Code refactoring
docs/<topic>                   - Documentation updates
```

**Commit Messages**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(species): add fuzzy search for species names

Implement Fuse.js-based fuzzy matching to handle misspellings
and partial names in species search.

Closes #123
```

**Pull Request Process**:
1. Create feature branch from `develop`
2. Write tests for new functionality
3. Ensure all tests pass (`npm test`)
4. Update documentation
5. Submit PR with clear description
6. Request review from 2+ team members
7. Address review feedback
8. Squash commits before merge

**Code Style**:
- Follow ESLint configuration
- Use Prettier for formatting
- Write JSDoc comments for public APIs
- Keep functions small (<50 lines)
- Prefer functional components and hooks

---

### Documentation Contributions

**Structure**:
- Use Markdown for all documentation
- Include code examples
- Add diagrams where helpful
- Link to related docs

**Required Sections**:
1. Overview
2. Prerequisites
3. Step-by-step instructions
4. Examples
5. Troubleshooting
6. Related resources

---

### Testing Requirements

**Coverage Targets**:
- Unit tests: >80%
- Integration tests: >60%
- E2E tests: >40%

**Test Structure**:
```javascript
describe('FeatureName', () => {
  describe('functionName', () => {
    it('should handle normal case', () => {
      // Test
    });
    
    it('should handle edge case', () => {
      // Test
    });
    
    it('should throw error for invalid input', () => {
      // Test
    });
  });
});
```

---

## 8. License Information

### Project License

**MIT License**

Copyright (c) 2024-2025 The Himalayan Initiative

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

### Third-Party Licenses

#### Core Dependencies

**React** (MIT License)
- Copyright (c) Meta Platforms, Inc. and affiliates.
- https://github.com/facebook/react/blob/main/LICENSE

**MapLibre GL JS** (BSD-3-Clause)
- Copyright (c) 2020-2024 MapLibre contributors
- https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt

**Redux** (MIT License)
- Copyright (c) 2015-present Dan Abramov and the Redux documentation authors.
- https://github.com/reduxjs/redux/blob/master/LICENSE.md

**Turf.js** (MIT License)
- Copyright (c) 2019 Morgan Herlocker
- https://github.com/Turfjs/turf/blob/master/LICENSE

#### Data Sources

**GBIF Data License**
- Data accessed through GBIF follows CC0 1.0 or CC-BY 4.0
- Must cite data publishers
- URL: https://www.gbif.org/terms

**MapTiler**
- Free tier for development
- Requires attribution: "© MapTiler © OpenStreetMap contributors"
- URL: https://www.maptiler.com/copyright/

---

### Data Attribution

When using occurrence data from GBIF, include:

```
Data provided by [Dataset Name] via GBIF.org (accessed [date])
GBIF Occurrence Download [DOI]
```

Example:
```
Data provided by iNaturalist Research-grade Observations via GBIF.org
(accessed 2024-11-06)
GBIF Occurrence Download https://doi.org/10.15468/dl.abcdef
```

---

## Document Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-06 | Initial comprehensive technical brief | Documentation Team |
| 0.9 | 2025-10-28 | Draft version for internal review | Development Team |

---

## Contact Information

**Project Team**:
- Technical Lead: [Contact]
- Project Manager: [Contact]
- Data Manager: [Contact]

**Organization**:
- The Himalayan Initiative
- Website: [URL]
- Email: [Contact Email]

**Repository**:
- GitHub: https://github.com/[organization]/THIKnowledgeCommon
- Issues: https://github.com/[organization]/THIKnowledgeCommon/issues

---

## Acknowledgments

This project builds on the open-source contributions of:
- GBIF and its data publishers
- MapLibre community
- React and Redux communities
- PostGIS developers
- OpenStreetMap contributors

Special thanks to:
- The Himalayan Initiative team
- Eastern Himalaya biodiversity researchers
- Open-source maintainers
- Technical advisors

---

**Previous**: [07_IMPLEMENTATION_ROADMAP.md](./07_IMPLEMENTATION_ROADMAP.md)  
**Index**: [01_EXECUTIVE_SUMMARY.md](./01_EXECUTIVE_SUMMARY.md)

---

**End of Technical Brief Series**

---

This completes the 8-document comprehensive technical brief for HMBIS Knowledge Common. All documents are designed to be publication-ready with proper formatting, diagrams, and references suitable for technical documentation, grant proposals, and architectural planning.
