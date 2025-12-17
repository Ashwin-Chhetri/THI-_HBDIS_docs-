# Proposed System Architecture
## Enhanced Architecture for HMBIS Knowledge Common

**Document**: 04 of 08  
**Date**: November 6, 2025  
**Version**: 1.0

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Proposed System Diagram](#2-proposed-system-diagram)
3. [Data Layer Architecture](#3-data-layer-architecture)
4. [Database Structure](#4-database-structure)
5. [API Services Layer](#5-api-services-layer)
6. [Visualization & Frontend](#6-visualization--frontend)
7. [Infrastructure & Hosting](#7-infrastructure--hosting)
8. [Quality Control & Validation](#8-quality-control--validation)
9. [Indicator Computation](#9-indicator-computation)
10. [Scalability Strategy](#10-scalability-strategy)

---

## 1. Architecture Overview

### 1.1 Architectural Principles

**1. Progressive Enhancement**
- Start with current static architecture
- Add backend services incrementally
- Maintain backward compatibility

**2. Microservices Approach**
- Independent, deployable services
- Loose coupling between components
- Technology diversity where beneficial

**3. API-First Design**
- Public API for all functionality
- Versioned endpoints (v1, v2)
- Comprehensive documentation

**4. Cloud-Native**
- Containerized services (Docker)
- Orchestration ready (Kubernetes)
- Auto-scaling capabilities

### 1.2 Three-Tier Evolution

```
CURRENT (v1.0) - Static Client
┌────────────────────┐
│   React Client     │
│   - IndexedDB      │
│   - Direct API     │
└────────────────────┘

NEXT (v2.0) - Hybrid
┌────────────────────┐
│   React Client     │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│   API Gateway      │
│   - Auth           │
│   - Cache          │
│   - Rate Limit     │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│   External APIs    │
└────────────────────┘

FUTURE (v3.0) - Full Stack
┌────────────────────┐
│   React Client     │
└─────────┬──────────┘
          │
┌─────────▼──────────┐
│  GraphQL Gateway   │
└─────────┬──────────┘
          │
    ┌─────┴─────┐
    │           │
┌───▼───┐  ┌───▼────┐
│  Data │  │Analysis│
│Service│  │Service │
└───┬───┘  └───┬────┘
    │          │
┌───▼──────────▼────┐
│   PostgreSQL      │
│   + PostGIS       │
└───────────────────┘
```

---

## 2. Proposed System Diagram

### 2.1 Complete Architecture (v2.0 Target)

```
┌──────────────────────────────────────────────────────────────┐
│                      CLIENT TIER                              │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Web Application (React)                   │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │ Species  │  │Ecosystem │  │   IoC    │            │ │
│  │  │  Module  │  │  Module  │  │  Module  │            │ │
│  │  └──────────┘  └──────────┘  └──────────┘            │ │
│  │                                                        │ │
│  │  Redux Store + Layer Management + MapLibre GL         │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           Progressive Web App (PWA)                    │ │
│  │  - Service Worker                                      │ │
│  │  - Offline Support                                     │ │
│  │  - Push Notifications                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ HTTPS / WebSocket
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                    API GATEWAY TIER                           │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │               NGINX / Kong API Gateway                 │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐      │ │
│  │  │   Auth     │  │   Rate     │  │   Cache    │      │ │
│  │  │  (OAuth)   │  │  Limiting  │  │  (Redis)   │      │ │
│  │  └────────────┘  └────────────┘  └────────────┘      │ │
│  │                                                        │ │
│  │  Load Balancing • SSL Termination • Request Routing   │ │
│  └────────────────────────────────────────────────────────┘ │
└────────────────────────┬─────────────────────────────────────┘
                         │ Internal Network
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   SERVICES TIER                               │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Data      │  │  Analysis   │  │   Export    │         │
│  │  Service    │  │  Service    │  │  Service    │         │
│  │             │  │             │  │             │         │
│  │ • GBIF API  │  │ • SDM       │  │ • CSV       │         │
│  │ • Local DB  │  │ • Metrics   │  │ • GeoJSON   │         │
│  │ • Upload    │  │ • Trends    │  │ • PDF       │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│  ┌──────▼────────────────▼────────────────▼──────┐         │
│  │          Message Queue (RabbitMQ)             │         │
│  └───────────────────────┬───────────────────────┘         │
│                          │                                  │
│  ┌─────────────┐  ┌─────▼──────┐  ┌─────────────┐         │
│  │   User      │  │  Compute   │  │   Search    │         │
│  │  Service    │  │  Service   │  │  Service    │         │
│  │             │  │            │  │             │         │
│  │ • Auth      │  │ • ML       │  │ • Full-text │         │
│  │ • Profiles  │  │ • Spatial  │  │ • Spatial   │         │
│  │ • Uploads   │  │ • Batch    │  │ • Facets    │         │
│  └──────┬──────┘  └──────┬─────┘  └──────┬──────┘         │
│         │                │               │                 │
└─────────┼────────────────┼───────────────┼─────────────────┘
          │                │               │
          ▼                ▼               ▼
┌──────────────────────────────────────────────────────────────┐
│                    DATA TIER                                  │
│                                                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│
│  │  PostgreSQL    │  │   Redis        │  │  Elasticsearch ││
│  │  + PostGIS     │  │                │  │                ││
│  │                │  │  • Cache       │  │  • Full-text   ││
│  │  • Biodiversity│  │  • Sessions    │  │  • Spatial     ││
│  │  • Users       │  │  • Job Queue   │  │  • Aggregation ││
│  │  • Metadata    │  │                │  │                ││
│  └────────┬───────┘  └────────────────┘  └────────────────┘│
│           │                                                  │
│  ┌────────▼───────┐  ┌────────────────┐                    │
│  │   TimescaleDB  │  │  S3 / MinIO    │                    │
│  │                │  │                │                    │
│  │  • Time-series │  │  • Files       │                    │
│  │  • Indicators  │  │  • Backups     │                    │
│  │  • Metrics     │  │  • Exports     │                    │
│  └────────────────┘  └────────────────┘                    │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 External Integrations

```
┌──────────────────────────────────────────────────────────────┐
│              EXTERNAL DATA SOURCES                            │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    GBIF     │  │     IBP     │  │   mWater    │         │
│  │  API v1/v2  │  │   (Planned) │  │  (Planned)  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  MapTiler   │  │ OpenStreetM │  │  Sentinel   │         │
│  │   Tiles     │  │    aps      │  │   Hub       │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Data Layer Architecture

### 3.1 Data Ingestion Pipeline

```
┌─────────────────────────────────────────────────────────┐
│               DATA INGESTION FLOW                        │
└─────────────────────────────────────────────────────────┘

Step 1: SOURCE IDENTIFICATION
├── GBIF API
├── Local Database
├── User Upload (GeoJSON, Shapefile, KML)
└── Third-party APIs

Step 2: DATA EXTRACTION
├── HTTP Request / File Parse
├── Pagination Handling
├── Error Recovery
└── Progress Tracking

Step 3: VALIDATION
├── Schema Validation (Darwin Core)
├── Coordinate Validation
├── Taxonomy Verification
├── Date Format Checking
└── Quality Flagging

Step 4: TRANSFORMATION
├── Format Standardization (→ GeoJSON)
├── Taxonomy Harmonization
├── Coordinate Projection (→ WGS84)
├── Unit Conversion
└── Metadata Enrichment

Step 5: ENRICHMENT
├── Reverse Geocoding
├── Elevation Data
├── Climate Variables
├── Protected Area Status
└── Threat Assessment

Step 6: STORAGE
├── PostgreSQL (Metadata)
├── PostGIS (Spatial Data)
├── TimescaleDB (Time-series)
├── S3/MinIO (Large Files)
└── Elasticsearch (Search Index)

Step 7: INDEXING
├── Spatial Index (R-tree)
├── Temporal Index (B-tree)
├── Full-text Index (GiST)
└── Facet Index (Aggregations)

Step 8: CACHE
├── Redis (Hot Data)
├── CDN (Static Assets)
└── Browser (Service Worker)
```

### 3.2 Data Validation Module

**Implementation**:
```javascript
// src/services/validation/dataValidator.js

export class DataValidator {
  /**
   * Validate occurrence record
   */
  validateOccurrence(record) {
    const errors = [];
    const warnings = [];
    
    // Required fields
    if (!record.scientificName) {
      errors.push({
        field: 'scientificName',
        message: 'Scientific name is required',
        severity: 'error'
      });
    }
    
    // Coordinate validation
    if (record.decimalLatitude) {
      if (Math.abs(record.decimalLatitude) > 90) {
        errors.push({
          field: 'decimalLatitude',
          message: 'Latitude must be between -90 and 90',
          severity: 'error'
        });
      }
    }
    
    // Coordinate precision
    if (record.coordinateUncertaintyInMeters > 10000) {
      warnings.push({
        field: 'coordinateUncertaintyInMeters',
        message: 'Low coordinate precision (>10km)',
        severity: 'warning'
      });
    }
    
    // Taxonomy check
    const taxonomyMatch = this.verifyTaxonomy(
      record.scientificName
    );
    if (!taxonomyMatch.found) {
      warnings.push({
        field: 'scientificName',
        message: 'Taxonomy not found in GBIF backbone',
        severity: 'warning',
        suggestions: taxonomyMatch.suggestions
      });
    }
    
    // Date validation
    if (record.eventDate) {
      const date = new Date(record.eventDate);
      if (date > new Date()) {
        errors.push({
          field: 'eventDate',
          message: 'Date cannot be in the future',
          severity: 'error'
        });
      }
    }
    
    return {
      valid: errors.length === 0,
      errors,
      warnings,
      qualityScore: this.calculateQualityScore(record)
    };
  }
  
  /**
   * Calculate data quality score (0-100)
   */
  calculateQualityScore(record) {
    let score = 100;
    
    // Deduct points for missing fields
    const importantFields = [
      'scientificName', 'decimalLatitude', 
      'decimalLongitude', 'eventDate', 'basisOfRecord'
    ];
    importantFields.forEach(field => {
      if (!record[field]) score -= 10;
    });
    
    // Deduct for low precision
    if (record.coordinateUncertaintyInMeters > 1000) {
      score -= 5;
    }
    if (record.coordinateUncertaintyInMeters > 10000) {
      score -= 10;
    }
    
    // Bonus for additional data
    if (record.identifiedBy) score += 2;
    if (record.recordedBy) score += 2;
    if (record.associatedMedia) score += 3;
    
    return Math.max(0, Math.min(100, score));
  }
}
```

---

## 4. Database Structure

### 4.1 PostgreSQL Schema

```sql
-- Core biodiversity tables

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Species table
CREATE TABLE species (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    taxon_key BIGINT UNIQUE NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    canonical_name VARCHAR(255),
    kingdom VARCHAR(100),
    phylum VARCHAR(100),
    class VARCHAR(100),
    "order" VARCHAR(100),
    family VARCHAR(100),
    genus VARCHAR(100),
    taxonomic_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Full-text search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', 
            coalesce(scientific_name, '') || ' ' ||
            coalesce(canonical_name, '') || ' ' ||
            coalesce(genus, '') || ' ' ||
            coalesce(family, '')
        )
    ) STORED
);

CREATE INDEX idx_species_taxon_key ON species(taxon_key);
CREATE INDEX idx_species_search ON species USING GIN(search_vector);
CREATE INDEX idx_species_family ON species(family);

-- Occurrences table
CREATE TABLE occurrences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gbif_id BIGINT UNIQUE,
    species_id UUID REFERENCES species(id),
    
    -- Spatial
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    coordinate_uncertainty_meters REAL,
    elevation REAL,
    
    -- Temporal
    event_date DATE,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    
    -- Record details
    basis_of_record VARCHAR(50),
    recorded_by VARCHAR(255),
    identified_by VARCHAR(255),
    dataset_key UUID,
    
    -- Data quality
    quality_score INTEGER CHECK (quality_score BETWEEN 0 AND 100),
    validation_flags JSONB,
    
    -- Metadata
    source VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Spatial index (critical for performance)
CREATE INDEX idx_occurrences_location ON occurrences 
    USING GIST(location);

-- Temporal indices
CREATE INDEX idx_occurrences_year ON occurrences(year);
CREATE INDEX idx_occurrences_date ON occurrences(event_date);

-- Species FK index
CREATE INDEX idx_occurrences_species ON occurrences(species_id);

-- Data quality index
CREATE INDEX idx_occurrences_quality ON occurrences(quality_score);

-- Composite index for common queries
CREATE INDEX idx_occurrences_species_year ON occurrences(species_id, year);

-- Regions table
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- 'country', 'state', 'protected_area', etc.
    geometry GEOGRAPHY(MULTIPOLYGON, 4326) NOT NULL,
    area_km2 REAL,
    properties JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_regions_geometry ON regions USING GIST(geometry);
CREATE INDEX idx_regions_type ON regions(type);

-- Datasets table
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    publisher VARCHAR(255),
    license VARCHAR(100),
    citation TEXT,
    doi VARCHAR(100),
    record_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Users table (for future auth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    affiliation VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- User uploads table
CREATE TABLE user_uploads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    size_bytes BIGINT,
    geometry GEOGRAPHY(GEOMETRY, 4326),
    properties JSONB,
    validation_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_uploads_user ON user_uploads(user_id);
CREATE INDEX idx_user_uploads_geometry ON user_uploads USING GIST(geometry);
```

### 4.2 TimescaleDB for Time-Series

```sql
-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Biodiversity indicators time-series
CREATE TABLE biodiversity_indicators (
    time TIMESTAMPTZ NOT NULL,
    region_id UUID REFERENCES regions(id),
    indicator_type VARCHAR(50) NOT NULL,
    
    -- Metrics
    species_count INTEGER,
    occurrence_count INTEGER,
    richness_index REAL,
    evenness_index REAL,
    diversity_index REAL,
    
    -- Metadata
    data_quality VARCHAR(20),
    computation_method VARCHAR(100),
    
    PRIMARY KEY (time, region_id, indicator_type)
);

-- Convert to hypertable
SELECT create_hypertable(
    'biodiversity_indicators',
    'time',
    chunk_time_interval => INTERVAL '1 month'
);

-- Create continuous aggregate for monthly summaries
CREATE MATERIALIZED VIEW biodiversity_monthly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 month', time) AS month,
    region_id,
    indicator_type,
    AVG(species_count) AS avg_species_count,
    AVG(diversity_index) AS avg_diversity_index
FROM biodiversity_indicators
GROUP BY month, region_id, indicator_type;

-- Refresh policy
SELECT add_continuous_aggregate_policy(
    'biodiversity_monthly',
    start_offset => INTERVAL '2 months',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 day'
);
```

---

## 5. API Services Layer

### 5.1 RESTful API Design

**Base URL**: `https://api.hmbis.org/v1`

**Core Endpoints**:

```yaml
# Species Endpoints
GET    /species/search                # Search species
GET    /species/{taxonKey}            # Species details
GET    /species/{taxonKey}/occurrences # Occurrences for species

# Occurrence Endpoints
GET    /occurrences/search            # Search occurrences
GET    /occurrences/count             # Count query
POST   /occurrences/batch             # Batch fetch
GET    /occurrences/grid              # Grid aggregation

# Region Endpoints
GET    /regions                       # List regions
GET    /regions/{id}                  # Region details
POST   /regions/analyze               # Spatial analysis
GET    /regions/{id}/species          # Species in region

# Analysis Endpoints
POST   /analysis/richness             # Species richness
POST   /analysis/trends               # Temporal trends
POST   /analysis/comparison           # Region comparison

# Export Endpoints
POST   /export/csv                    # Export to CSV
POST   /export/geojson                # Export to GeoJSON
POST   /export/report                 # Generate PDF report

# User Endpoints
POST   /auth/login                    # User login
POST   /auth/register                 # User registration
GET    /users/me                      # Current user
POST   /uploads                       # File upload
GET    /uploads/{id}                  # Upload details
```

### 5.2 API Implementation (Node.js + Express)

```javascript
// src/api/server.js
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import { Pool } from 'pg';
import Redis from 'ioredis';

const app = express();
const db = new Pool({ connectionString: process.env.DATABASE_URL });
const redis = new Redis(process.env.REDIS_URL);

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// Routes
app.get('/v1/species/search', async (req, res) => {
  const { q, limit = 20, offset = 0 } = req.query;
  
  try {
    // Check cache
    const cacheKey = `species:search:${q}:${limit}:${offset}`;
    const cached = await redis.get(cacheKey);
    if (cached) {
      return res.json(JSON.parse(cached));
    }
    
    // Query database
    const query = `
      SELECT 
        taxon_key,
        scientific_name,
        canonical_name,
        family,
        ts_rank(search_vector, plainto_tsquery('english', $1)) as rank
      FROM species
      WHERE search_vector @@ plainto_tsquery('english', $1)
      ORDER BY rank DESC
      LIMIT $2 OFFSET $3
    `;
    
    const result = await db.query(query, [q, limit, offset]);
    
    const response = {
      results: result.rows,
      count: result.rowCount,
      limit,
      offset
    };
    
    // Cache for 1 hour
    await redis.setex(cacheKey, 3600, JSON.stringify(response));
    
    res.json(response);
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/v1/occurrences/search', async (req, res) => {
  const { 
    taxonKey, 
    bounds, // "west,south,east,north"
    year,
    limit = 100,
    offset = 0
  } = req.query;
  
  try {
    let query = `
      SELECT 
        o.id,
        o.gbif_id,
        ST_X(o.location::geometry) as longitude,
        ST_Y(o.location::geometry) as latitude,
        o.event_date,
        o.year,
        o.basis_of_record,
        o.quality_score,
        s.scientific_name
      FROM occurrences o
      JOIN species s ON o.species_id = s.id
      WHERE 1=1
    `;
    
    const params = [];
    let paramCount = 1;
    
    if (taxonKey) {
      query += ` AND s.taxon_key = $${paramCount}`;
      params.push(taxonKey);
      paramCount++;
    }
    
    if (bounds) {
      const [west, south, east, north] = bounds.split(',').map(Number);
      query += ` AND ST_Within(
        o.location,
        ST_MakeEnvelope($${paramCount}, $${paramCount+1}, $${paramCount+2}, $${paramCount+3}, 4326)
      )`;
      params.push(west, south, east, north);
      paramCount += 4;
    }
    
    if (year) {
      query += ` AND o.year = $${paramCount}`;
      params.push(year);
      paramCount++;
    }
    
    query += ` LIMIT $${paramCount} OFFSET $${paramCount+1}`;
    params.push(limit, offset);
    
    const result = await db.query(query, params);
    
    // Transform to GeoJSON
    const geojson = {
      type: 'FeatureCollection',
      features: result.rows.map(row => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [row.longitude, row.latitude]
        },
        properties: {
          id: row.id,
          gbifId: row.gbif_id,
          scientificName: row.scientific_name,
          date: row.event_date,
          year: row.year,
          basisOfRecord: row.basis_of_record,
          qualityScore: row.quality_score
        }
      }))
    };
    
    res.json(geojson);
  } catch (error) {
    console.error('Occurrence search error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API server running on port ${PORT}`);
});
```

---

## 6. Visualization & Frontend

### 6.1 Enhanced Frontend Architecture

**No major changes to current React architecture**, but add:

1. **Service Worker** for offline support
2. **Web Workers** for heavy computation
3. **IndexedDB** enhancements
4. **GraphQL** client (future)

### 6.2 Performance Optimizations

```javascript
// src/services/optimization/dataOptimizer.js

export class DataOptimizer {
  /**
   * Reduce point density for better performance
   */
  simplifyPoints(points, tolerance = 0.001) {
    if (points.length < 1000) return points;
    
    // Grid-based simplification
    const grid = new Map();
    const gridSize = tolerance;
    
    points.forEach(point => {
      const gridX = Math.floor(point.lng / gridSize);
      const gridY = Math.floor(point.lat / gridSize);
      const key = `${gridX},${gridY}`;
      
      if (!grid.has(key)) {
        grid.set(key, point);
      }
    });
    
    return Array.from(grid.values());
  }
  
  /**
   * Cluster points for visualization
   */
  clusterPoints(points, zoom) {
    const radius = this.getClusterRadius(zoom);
    const clusters = [];
    const processed = new Set();
    
    points.forEach((point, index) => {
      if (processed.has(index)) return;
      
      const cluster = {
        center: point,
        points: [point],
        count: 1
      };
      
      // Find nearby points
      points.forEach((other, otherIndex) => {
        if (processed.has(otherIndex)) return;
        if (index === otherIndex) return;
        
        const distance = this.distance(point, other);
        if (distance < radius) {
          cluster.points.push(other);
          cluster.count++;
          processed.add(otherIndex);
        }
      });
      
      processed.add(index);
      clusters.push(cluster);
    });
    
    return clusters;
  }
  
  getClusterRadius(zoom) {
    // More clustering at lower zoom levels
    return 50 / Math.pow(2, zoom);
  }
}
```

---

## 7. Infrastructure & Hosting

### 7.1 Deployment Architecture

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Frontend
  client:
    build: ./client
    ports:
      - "80:80"
    environment:
      - API_URL=http://api:3000
  
  # API Gateway
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
  
  # API Server
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/hmbis
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  # Database
  db:
    image: timescale/timescaledb-ha:latest-pg15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=hmbis
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres-data:/var/lib/postgresql/data
  
  # Cache
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
  
  # Search
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
    volumes:
      - es-data:/usr/share/elasticsearch/data

volumes:
  postgres-data:
  redis-data:
  es-data:
```

### 7.2 Cloud Deployment Strategy

**Option 1: AWS**
```
Route 53 (DNS)
  ↓
CloudFront (CDN)
  ↓
S3 (Static Assets)

ALB (Load Balancer)
  ↓
ECS Fargate (API Containers)
  ↓
RDS PostgreSQL + ElastiCache Redis
```

**Option 2: DigitalOcean** (Cost-effective)
```
Spaces (CDN + Storage)
  ↓
Load Balancer
  ↓
Droplets (Kubernetes)
  ↓
Managed PostgreSQL + Redis
```

**Option 3: Self-hosted** (Maximum control)
```
University Server / VPS
  ↓
Docker Compose / Kubernetes
  ↓
All services containerized
```

---

## 8. Quality Control & Validation

### 8.1 Automated Quality Checks

```javascript
export const qualityChecks = {
  /**
   * Check 1: Coordinate validity
   */
  checkCoordinates(lat, lng) {
    return {
      valid: Math.abs(lat) <= 90 && Math.abs(lng) <= 180,
      flag: 'COORDINATE_OUT_OF_RANGE'
    };
  },
  
  /**
   * Check 2: Coordinate-country mismatch
   */
  async checkCountryMatch(lat, lng, country) {
    const actualCountry = await reverseGeocode(lat, lng);
    return {
      valid: actualCountry === country,
      flag: 'COORDINATE_COUNTRY_MISMATCH'
    };
  },
  
  /**
   * Check 3: Temporal validity
   */
  checkDate(date) {
    const d = new Date(date);
    const now = new Date();
    return {
      valid: d <= now && d > new Date('1700-01-01'),
      flag: 'INVALID_DATE'
    };
  },
  
  /**
   * Check 4: Taxonomy match
   */
  async checkTaxonomy(scientificName) {
    const match = await gbifService.matchName(scientificName);
    return {
      valid: match.confidence > 90,
      flag: 'TAXONOMY_UNCERTAIN',
      suggestion: match.acceptedName
    };
  }
};
```

---

## 9. Indicator Computation

### 9.1 Biodiversity Indices

```javascript
export class BiodiversityIndicators {
  /**
   * Shannon Diversity Index
   * H' = -Σ(pi * ln(pi))
   */
  shannonIndex(occurrences) {
    const speciesCounts = this.countBySpecies(occurrences);
    const total = occurrences.length;
    
    let index = 0;
    for (const count of Object.values(speciesCounts)) {
      const p = count / total;
      index -= p * Math.log(p);
    }
    
    return index;
  }
  
  /**
   * Simpson's Index
   * D = Σ(n(n-1)) / (N(N-1))
   */
  simpsonIndex(occurrences) {
    const speciesCounts = this.countBySpecies(occurrences);
    const N = occurrences.length;
    
    let sum = 0;
    for (const n of Object.values(speciesCounts)) {
      sum += n * (n - 1);
    }
    
    return sum / (N * (N - 1));
  }
  
  /**
   * Species Richness
   */
  richness(occurrences) {
    return new Set(
      occurrences.map(o => o.taxonKey)
    ).size;
  }
  
  /**
   * Temporal trend
   */
  temporalTrend(occurrencesByYear) {
    // Linear regression
    const years = Object.keys(occurrencesByYear).map(Number);
    const counts = Object.values(occurrencesByYear);
    
    const n = years.length;
    const sumX = years.reduce((a, b) => a + b, 0);
    const sumY = counts.reduce((a, b) => a + b, 0);
    const sumXY = years.reduce((sum, x, i) => sum + x * counts[i], 0);
    const sumX2 = years.reduce((sum, x) => sum + x * x, 0);
    
    const slope = (n * sumXY - sumX * sumY) / 
                  (n * sumX2 - sumX * sumX);
    
    return {
      slope,
      trend: slope > 0 ? 'increasing' : 
             slope < 0 ? 'decreasing' : 'stable'
    };
  }
}
```

---

## 10. Scalability Strategy

### 10.1 Horizontal Scaling

```
Single Server (Current)
  ↓
Multiple API Servers + Load Balancer
  ↓
Microservices + Message Queue
  ↓
Kubernetes Cluster with Auto-scaling
```

### 10.2 Database Scaling

```
PostgreSQL Primary (Write)
  ↓
PostgreSQL Replicas (Read)
  ↓
Sharding by Region
  ↓
Distributed Database (CockroachDB/Citus)
```

### 10.3 Caching Strategy

```
L1: Browser Cache (Service Worker)
  ↓ Miss
L2: CDN Cache (CloudFlare)
  ↓ Miss
L3: Redis Cache (API Layer)
  ↓ Miss
L4: Database Query
```

---

## Summary

This proposed architecture provides:

1. ✅ **Scalability** - From static to full-stack
2. ✅ **Performance** - Multi-tier caching
3. ✅ **Quality** - Automated validation
4. ✅ **Standards** - Darwin Core, OGC compliant
5. ✅ **Flexibility** - Microservices ready
6. ✅ **Cost-effective** - Progressive enhancement

**Implementation Priority**:
1. Phase 1 (Q4 2025): API Gateway + Auth
2. Phase 2 (Q1 2026): Database Layer
3. Phase 3 (Q2 2026): Advanced Features
4. Phase 4 (Q3 2026): ML & Analytics

---

**Previous**: [03_BENCHMARK_COMPARISON.md](./03_BENCHMARK_COMPARISON.md)  
**Next**: [05_DATA_FLOW_DOCUMENTATION.md](./05_DATA_FLOW_DOCUMENTATION.md)
