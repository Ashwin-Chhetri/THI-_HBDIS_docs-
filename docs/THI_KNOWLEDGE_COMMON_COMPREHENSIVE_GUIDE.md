# THI Knowledge Common: Comprehensive Guide
## For Developers, Ecologists, and Biologists

> **Mission**: This document serves as the **complete reference** for understanding the THI Knowledge Common platform—from its scientific foundations to its technical implementation. Whether you're a developer building new features or an ecologist analyzing biodiversity data, this guide provides the knowledge you need.

**Version**: 2.0  
**Last Updated**: November 19, 2025  
**Authors**: THI Knowledge Common Team  
**Audience**: Developers, Ecologists, Biologists, Data Scientists

---

## 📚 Table of Contents

### Part I: Project Overview
1. [Introduction & Mission](#1-introduction--mission)
2. [The Himalaya Initiative Context](#2-the-himalaya-initiative-context)
3. [Essential Biodiversity Variables (EBVs)](#3-essential-biodiversity-variables-ebvs)
4. [Long-Term Monitoring Framework](#4-long-term-monitoring-framework)

### Part II: Scientific Foundation
5. [Biodiversity Data Standards](#5-biodiversity-data-standards)
6. [Spatial-Temporal Analysis](#6-spatial-temporal-analysis)
7. [Climate-Biodiversity Linkages](#7-climate-biodiversity-linkages)
8. [Ecological Indicators](#8-ecological-indicators)

### Part III: Technical Architecture
9. [System Architecture Overview](#9-system-architecture-overview)
10. [Data Layer & Integration](#10-data-layer--integration)
11. [Domain-Driven Design](#11-domain-driven-design)
12. [Time-Series & Climate Data](#12-time-series--climate-data)

### Part IV: Features & Capabilities
13. [Species Occurrence Mapping](#13-species-occurrence-mapping)
14. [Regional Analysis](#14-regional-analysis)
15. [Climate Data Visualization](#15-climate-data-visualization)
16. [Ecosystem Assessment](#16-ecosystem-assessment)

### Part V: For Developers
17. [Development Environment Setup](#17-development-environment-setup)
18. [Code Architecture & Patterns](#18-code-architecture--patterns)
19. [Adding New Features](#19-adding-new-features)
20. [Testing & Quality Assurance](#20-testing--quality-assurance)

### Part VI: For Ecologists
21. [Data Interpretation Guide](#21-data-interpretation-guide)
22. [Analysis Workflows](#22-analysis-workflows)
23. [Exporting Data for Research](#23-exporting-data-for-research)
24. [Limitations & Caveats](#24-limitations--caveats)

### Part VII: Appendices
25. [Glossary](#25-glossary)
26. [References](#26-references)
27. [Contributing](#27-contributing)

---

# Part I: Project Overview

## 1. Introduction & Mission

### 1.1 What is THI Knowledge Common?

THI Knowledge Common is an **open-source web platform** that integrates multiple biodiversity data sources to support **evidence-based conservation** and **long-term ecological monitoring** in the Himalayan region. It combines:

- **Species occurrence data** (1.5+ billion records from GBIF)
- **Climate variables** (temperature, precipitation, time-series)
- **Ecosystem data** (habitat types, land cover)
- **Regional boundaries** (countries, states, protected areas)
- **Socio-economic indicators** (human impact, land use)

### 1.2 Core Mission

> "To provide accessible, scientifically rigorous biodiversity information that supports conservation decision-making and advances our understanding of Himalayan ecosystems in the face of climate change."

**Primary Goals**:
1. **Accessibility**: Make biodiversity data available to researchers, policymakers, and citizens
2. **Integration**: Combine disparate data sources into coherent spatial-temporal views
3. **Long-term Monitoring**: Track biodiversity trends over decades
4. **Climate Linkages**: Understand how climate change affects biodiversity
5. **Evidence-based Conservation**: Support policy with robust data

### 1.3 Target Users

| User Type | Primary Needs | Platform Features |
|-----------|--------------|-------------------|
| **Conservation Scientists** | Species distribution, habitat analysis | Occurrence maps, spatial queries, data export |
| **Field Ecologists** | Monitoring site data, time-series trends | Time-series visualization, site comparison |
| **Policy Makers** | Regional summaries, trends, indicators | Dashboard views, automated reports |
| **Citizen Scientists** | Species identification, observations | Interactive maps, educational content |
| **Data Scientists** | Raw data access, APIs, bulk downloads | API access, data export, integration |

---

## 2. The Himalaya Initiative Context

### 2.1 The Himalayan Biodiversity Crisis

The Himalayas are a **global biodiversity hotspot** facing unprecedented threats:

**Key Statistics**:
- **10,000+ plant species** (endemic: ~3,160)
- **300+ mammal species** (endangered: 51)
- **977 bird species** (endemic: 15)
- **1,200+ km³** glacier ice loss (1975-2016)
- **1.5°C** temperature increase (1951-2014, faster than global average)

**Primary Threats**:
1. **Climate Change**: Rapid warming, shifting precipitation, glacier retreat
2. **Habitat Loss**: Deforestation, land conversion, infrastructure
3. **Human Pressure**: Population growth, resource extraction
4. **Invasive Species**: Disruption of native ecosystems
5. **Limited Data**: Many areas poorly studied

### 2.2 Long-Term Monitoring Imperative

**Why Long-Term Monitoring Matters**:

```
Short-term data (1-3 years):
  ❌ Cannot detect trends
  ❌ Confounded by natural variation
  ❌ Limited predictive power

Long-term data (10-50+ years):
  ✅ Reveals directional changes
  ✅ Separates signal from noise
  ✅ Enables robust forecasting
  ✅ Supports adaptive management
```

**THI Monitoring Framework**:
- **Temporal Coverage**: 1950s-present (historic) + ongoing (current)
- **Spatial Coverage**: Hindu Kush Himalayas (3,500 km)
- **Taxonomic Coverage**: Vascular plants, vertebrates, key invertebrates
- **Frequency**: Annual surveys at fixed sites + opportunistic observations

### 2.3 THI Knowledge Common's Role

This platform serves as the **central data repository and analysis tool** for The Himalaya Initiative's long-term monitoring program:

```
┌────────────────────────────────────────────────────────┐
│          THI Long-Term Monitoring Program              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Field Data Collection                                 │
│  ├─ Fixed monitoring sites                            │
│  ├─ Citizen science networks                          │
│  └─ Remote sensing                                     │
│                                                        │
│            ↓                                          │
│                                                        │
│  THI Knowledge Common (THIS PLATFORM)                  │
│  ├─ Data integration & QC                             │
│  ├─ Visualization & analysis                          │
│  ├─ Trend detection                                   │
│  └─ Public access                                      │
│                                                        │
│            ↓                                          │
│                                                        │
│  Outputs                                               │
│  ├─ Scientific publications                            │
│  ├─ Policy reports                                     │
│  ├─ Conservation recommendations                       │
│  └─ Baseline data for future                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 3. Essential Biodiversity Variables (EBVs)

### 3.1 What are EBVs?

**Essential Biodiversity Variables (EBVs)** are a standardized set of measurements that capture **key dimensions of biodiversity change** at global scales. Think of them as the "vital signs" of Earth's living systems.

**The EBV Framework** (GEO BON, 2013):

```
6 EBV Classes:
├─ 1. Genetic Composition
│    └─ Genetic diversity, inbreeding
├─ 2. Species Populations
│    └─ Species abundance, distribution
├─ 3. Species Traits
│    └─ Phenology, morphology, physiology
├─ 4. Community Composition
│    └─ Taxonomic diversity, trait diversity
├─ 5. Ecosystem Function
│    └─ Primary productivity, nutrient cycling
└─ 6. Ecosystem Structure
     └─ Habitat extent, fragmentation
```

### 3.2 EBVs Tracked by THI Knowledge Common

| EBV Class | EBV | Data Source | Temporal Resolution | Spatial Resolution |
|-----------|-----|-------------|---------------------|-------------------|
| **Species Populations** | Species distribution | GBIF occurrences | Daily (ongoing) | Point (GPS) |
| **Species Populations** | Population abundance | Surveys + modeling | Annual | 1 km grid |
| **Species Traits** | Phenology | iNaturalist + field | Seasonal | Site-level |
| **Community Composition** | Taxonomic diversity | GBIF + checklists | Annual | Regional |
| **Community Composition** | Taxonomic turnover | Time-series analysis | Decadal | Regional |
| **Ecosystem Structure** | Live cover fraction | Landsat, Sentinel-2 | 16-day | 30m pixel |
| **Ecosystem Structure** | Habitat fragmentation | Land cover change | Annual | 30m pixel |
| **Ecosystem Function** | Net Primary Productivity | MODIS NPP | 8-day | 500m pixel |

### 3.3 How THI Uses EBVs

**1. Standardization**: All data aligned to EBV framework for global comparability

**2. Trend Detection**: Time-series of EBVs reveal biodiversity changes
```python
# Example: Species distribution EBV over time
species_distribution_2000 = get_occurrences(year=2000, region='Sikkim')
species_distribution_2020 = get_occurrences(year=2020, region='Sikkim')

# Calculate range shift
shift_km = calculate_centroid_shift(
  species_distribution_2000,
  species_distribution_2020
)
# Output: "Snow Leopard range shifted 34 km north (2000-2020)"
```

**3. Multi-EBV Analysis**: Combine EBVs to understand mechanisms
```
Question: Why is species richness declining in region X?

Step 1: Check Species Populations EBV
  → Abundance declining ✓

Step 2: Check Ecosystem Structure EBV
  → Habitat area declining ✓ (mechanism identified)

Step 3: Check climate data
  → Temperature increasing ✓ (driver identified)

Conclusion: Warming → habitat loss → population declines
```

**4. Reporting to Global Networks**: Data feeds into:
- **GEO BON** (Group on Earth Observations Biodiversity Observation Network)
- **IPBES** (Intergovernmental Science-Policy Platform on Biodiversity)
- **CBD** (Convention on Biological Diversity)

---

## 4. Long-Term Monitoring Framework

### 4.1 The Challenge of Temporal Data

**Biodiversity is inherently dynamic**:
- Populations fluctuate seasonally (migration, breeding)
- Communities respond to stochastic events (fire, floods)
- Ecosystems shift gradually (succession, climate trends)

**To detect real change, we need**:
```
Signal-to-Noise Ratio

Noise (natural variation):
├─ Weather variability (year-to-year)
├─ Observer differences
├─ Sampling effort variation
└─ Spatial heterogeneity

Signal (directional change):
├─ Climate trends
├─ Habitat loss
├─ Species invasions
└─ Population trends

Detection requires: Signal >> Noise
Achieved by: Long time series (10-50+ years)
```

### 4.2 THI Monitoring Sites

**Site Selection Criteria**:
1. **Elevational Gradient**: Captures climate sensitivity (valley → alpine)
2. **Habitat Representation**: Major ecosystem types sampled
3. **Accessibility**: Feasible for annual surveys
4. **Baseline Data**: Historic records available
5. **Protected Status**: Likely to persist long-term

**Current Monitoring Sites**:

| Site Name | Location | Elevation Range | Habitats | Monitoring Since |
|-----------|----------|-----------------|----------|------------------|
| **Khangchendzonga Landscape** | Sikkim, India | 300-8,586m | Subtropical-Alpine | 2015 |
| **Trans-Himalayan Landscape** | Ladakh, India | 3,000-6,000m | Cold Desert-Alpine | 2016 |
| **Arunachal Pradesh Landscape** | Arunachal, India | 200-7,000m | Tropical-Alpine | 2017 |
| **Nepal Central** | Central Nepal | 500-5,500m | Subtropical-Alpine | 2018 |
| **Bhutan East** | Eastern Bhutan | 1,000-6,000m | Temperate-Alpine | 2019 |

### 4.3 Data Collection Protocols

**Standardized Methods** (ensures data comparability):

**1. Line Transect Surveys** (Birds, Mammals)
- Fixed routes (10 km each)
- Monthly surveys (breeding season)
- Distance sampling (for density estimation)
- Time: 0600-1000 hrs

**2. Vegetation Plots** (Plants)
- 20 x 20m plots (n=50 per site)
- Annual census (monsoon peak)
- All woody stems >10cm DBH measured
- Herbaceous cover estimated

**3. Camera Traps** (Mammals)
- 50 stations per site (500m apart)
- Continuous operation (3 months)
- Bait-free (natural behavior)
- Species ID + abundance indices

**4. Citizen Science** (Opportunistic)
- Mobile apps (iNaturalist, eBird)
- Photo verification required
- Quality filters applied
- Supplements systematic surveys

### 4.4 Data Flow in THI Knowledge Common

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Collection                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Field      │  │  Remote      │  │   Citizen    │     │
│  │   Surveys    │  │  Sensing     │  │   Science    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                           │                                 │
│         ┌─────────────────▼─────────────────┐              │
│         │   Data Quality Control             │              │
│         │   ├─ Taxonomic validation          │              │
│         │   ├─ Geospatial validation         │              │
│         │   ├─ Temporal validation           │              │
│         │   └─ Outlier detection             │              │
│         └─────────────────┬─────────────────┘              │
│                           │                                 │
│         ┌─────────────────▼─────────────────┐              │
│         │  THI Knowledge Common Database     │              │
│         │  ├─ Occurrence data                │              │
│         │  ├─ Climate time-series            │              │
│         │  ├─ Habitat data                   │              │
│         │  └─ Metadata                       │              │
│         └─────────────────┬─────────────────┘              │
│                           │                                 │
│         ┌─────────────────▼─────────────────┐              │
│         │   THI Knowledge Common Platform    │              │
│         │   (THIS APPLICATION)               │              │
│         │   ├─ Web interface                 │              │
│         │   ├─ API access                    │              │
│         │   └─ Visualizations                │              │
│         └─────────────────┬─────────────────┘              │
│                           │                                 │
│         ┌─────────────────▼─────────────────┐              │
│         │   End Users                        │              │
│         │   ├─ Researchers                   │              │
│         │   ├─ Policy makers                 │              │
│         │   └─ Public                        │              │
│         └───────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Biodiversity Data Standards

### 5.1 Darwin Core Standard

**Darwin Core** is the international standard for biodiversity data. All occurrence records in THI Knowledge Common follow this schema.

**Core Terms Used**:

| Term | Description | Example |
|------|-------------|---------|
| `scientificName` | Full scientific name | *Panthera uncia* (Snow Leopard) |
| `taxonRank` | Taxonomic rank | species |
| `kingdom` | Kingdom | Animalia |
| `phylum` | Phylum | Chordata |
| `class` | Class | Mammalia |
| `order` | Order | Carnivora |
| `family` | Family | Felidae |
| `genus` | Genus | *Panthera* |
| `specificEpithet` | Species epithet | *uncia* |
| `decimalLatitude` | Latitude (WGS84) | 27.9881 |
| `decimalLongitude` | Longitude (WGS84) | 86.9250 |
| `coordinateUncertaintyInMeters` | GPS accuracy | 100 |
| `eventDate` | Date observed | 2023-06-15 |
| `year` | Year | 2023 |
| `month` | Month | 6 |
| `day` | Day | 15 |
| `basisOfRecord` | Evidence type | HUMAN_OBSERVATION |
| `institutionCode` | Data provider | iNaturalist |
| `datasetName` | Dataset | iNaturalist Research-grade Observations |

**Why Darwin Core Matters**:
- ✅ **Interoperability**: Data can be combined from multiple sources
- ✅ **Discoverability**: Standardized searches across databases
- ✅ **Quality**: Required fields ensure minimum data quality
- ✅ **Citation**: Clear provenance and attribution

### 5.2 Data Quality Standards

**THI Quality Tiers**:

**Tier 1: Research-Grade** ⭐⭐⭐
- Coordinates: <100m uncertainty
- Taxonomy: Expert-verified
- Date: Exact date known
- Evidence: Specimen or photo
- **Use case**: Scientific publications, modeling

**Tier 2: Community-Verified** ⭐⭐
- Coordinates: <1km uncertainty  
- Taxonomy: Community consensus (2+ agreeing IDs)
- Date: Year-month known
- Evidence: Photo or audio
- **Use case**: Distribution maps, trends

**Tier 3: Unverified** ⭐
- Coordinates: <10km uncertainty
- Taxonomy: Single observer ID
- Date: Year known
- Evidence: Any (including memory)
- **Use case**: Exploratory analysis only

**Quality Filters in Platform**:
```javascript
// Users can filter by quality tier
const occurrences = await fetchOccurrences({
  species: 'Panthera uncia',
  region: 'Sikkim',
  quality: 'RESEARCH_GRADE',  // Only Tier 1
  coordinateUncertainty: { max: 100 },  // <100m
  basisOfRecord: ['PRESERVED_SPECIMEN', 'OBSERVATION']
});
```

### 5.3 Taxonomic Backbone

**GBIF Taxonomic Backbone** is used for all taxonomic names:
- 10+ million names
- Synonyms resolved
- Valid names prioritized
- Hierarchical structure maintained

**How Taxonomic Resolution Works**:
```
User searches: "Himalayan Tahr"

Step 1: Name matching
  ├─ Check common names → "Himalayan Tahr"
  ├─ Check scientific names → Hemitragus jemlahicus
  └─ Check synonyms → Capra jemlaica (invalid, redirect)

Step 2: Return accepted name
  └─ Scientific: Hemitragus jemlahicus (Shaw, 1800)
      Common: Himalayan Tahr
      GBIF Key: 5219357
      Rank: species
      Status: ACCEPTED

Step 3: Retrieve occurrences
  └─ Fetch using taxonKey=5219357
      (includes all synonyms automatically)
```

---

## 6. Spatial-Temporal Analysis

### 6.1 Spatial Data Model

**Everything is Spatial**: All biodiversity data has a location

**Spatial Types**:

1. **Point Data** (Occurrences)
   - Single coordinate pair (lat/lon)
   - Example: Camera trap photo at 27.9881°N, 86.9250°E

2. **Polygon Data** (Regions, Habitats)
   - Closed boundary (GeoJSON, Shapefile)
   - Example: Khangchendzonga National Park boundary

3. **Raster Data** (Climate, Land Cover)
   - Grid of pixels
   - Example: Temperature raster (1km resolution)

**Coordinate Reference Systems**:
- **WGS84** (EPSG:4326): Used for all lat/lon data
- **Web Mercator** (EPSG:3857): Used for map display
- **UTM Zones**: Used for metric calculations (area, distance)

### 6.2 Temporal Data Model

**Time-Series Climate Data**:

```typescript
interface ClimateTimeSeries {
  variable: 'temperature' | 'precipitation' | 'ndvi';
  location: Coordinates;
  timeRange: { start: Date; end: Date };
  resolution: 'daily' | 'monthly' | 'yearly';
  values: Array<{
    timestamp: Date;
    value: number;
    unit: string;
  }>;
}

// Example: Temperature at Gangtok, Sikkim
const temperatureSeries = {
  variable: 'temperature',
  location: { lat: 27.33, lon: 88.62 },
  timeRange: { start: '1990-01-01', end: '2024-12-31' },
  resolution: 'monthly',
  values: [
    { timestamp: '1990-01', value: 8.5, unit: '°C' },
    { timestamp: '1990-02', value: 10.2, unit: '°C' },
    // ... 420 monthly values
    { timestamp: '2024-12', value: 12.1, unit: '°C' }  // +3.6°C warming!
  ]
};
```

**Temporal Queries**:
```javascript
// 1. Get species occurrences for specific year
const occurrences2020 = await query({
  species: 'Panthera uncia',
  year: 2020
});

// 2. Get time-series (decadal bins)
const decadalCounts = await queryTimeSeries({
  species: 'Panthera uncia',
  region: 'Nepal',
  startYear: 1950,
  endYear: 2020,
  binSize: '10 years'
});
// Returns: [
//   { decade: '1950-1959', count: 12 },
//   { decade: '1960-1969', count: 34 },
//   ...
// ]

// 3. Detect trends
const trend = await detectTrend(decadalCounts);
// Returns: { direction: 'declining', slope: -2.3, pValue: 0.02 }
```

### 6.3 Spatial Operations

**Geospatial Analysis in Platform**:

```javascript
// 1. Point-in-polygon (Is occurrence inside region?)
const isInside = turf.booleanPointInPolygon(
  occurrencePoint,
  regionBoundary
);

// 2. Buffer (Create 10km zone around site)
const buffer = turf.buffer(monitoringSite, 10, { units: 'kilometers' });

// 3. Intersection (Overlap between two regions)
const overlap = turf.intersect(region1, region2);

// 4. Centroid (Average location of all occurrences)
const centroid = turf.centroid(
  turf.featureCollection(occurrences.map(o => turf.point([o.lon, o.lat])))
);

// 5. Distance (How far did species range shift?)
const shift = turf.distance(centroid2000, centroid2020, { units: 'kilometers' });
```

---

## 7. Climate-Biodiversity Linkages

### 7.1 Why Climate Matters for Biodiversity

**Climate determines**:
- Species distributions (temperature, precipitation tolerance)
- Phenology (timing of breeding, migration, flowering)
- Ecosystem productivity (photosynthesis, decomposition)
- Interactions (predation, competition, mutualisms)

**Himalayan Climate Trends** (1951-2014):
- **Temperature**: +1.5°C (0.3°C/decade, 2x global average)
- **Precipitation**: Increasing monsoon variability
- **Glaciers**: Retreating 30-60m/year
- **Snow cover**: Decreasing 30% in duration

### 7.2 Climate Data in THI Knowledge Common

**Climate Variables Available**:

| Variable | Source | Temporal Coverage | Spatial Resolution | Update Frequency |
|----------|--------|-------------------|-------------------|------------------|
| **Temperature (mean)** | WorldClim, ERA5 | 1950-present | 1 km | Monthly |
| **Precipitation** | WorldClim, ERA5 | 1950-present | 1 km | Monthly |
| **Min/Max Temperature** | ERA5 | 1979-present | 30 km | Daily |
| **NDVI** (vegetation) | MODIS | 2000-present | 250 m | 16-day |
| **Snow Cover** | MODIS | 2000-present | 500 m | Daily |
| **Evapotranspiration** | MODIS | 2000-present | 500 m | 8-day |

**How to Use Climate Data**:

**1. Overlay Occurrences with Climate**:
```javascript
// Get all Snow Leopard occurrences
const occurrences = await getOccurrences('Panthera uncia');

// Extract temperature at each occurrence
const climateValues = await Promise.all(
  occurrences.map(async (occ) => {
    const temp = await getClimateAtPoint({
      variable: 'temperature',
      lat: occ.latitude,
      lon: occ.longitude,
      date: occ.eventDate
    });
    return { occurrence: occ, temperature: temp };
  })
);

// Analyze: What temperatures does Snow Leopard tolerate?
const tempRange = {
  min: Math.min(...climateValues.map(v => v.temperature)),
  max: Math.max(...climateValues.map(v => v.temperature)),
  mean: climateValues.reduce((sum, v) => sum + v.temperature, 0) / climateValues.length
};
// Result: Snow Leopard prefers -10°C to +15°C (mean: 3.2°C)
```

**2. Temporal Animation**:
```javascript
// Show how species distribution shifted with climate change
const animation = new ClimateAnimation({
  species: 'Panthera uncia',
  timeRange: { start: '2000-01', end: '2024-12' },
  climateVariable: 'temperature',
  playbackSpeed: '1 year per second'
});

// Play animation
animation.play();
// User sees:
// - Map with species occurrences (blue dots)
// - Climate layer (temperature heatmap)
// - Timeline scrubber at bottom
// - As time advances, occurrences shift upslope (tracking cooler temps)
```

**3. Climate Envelopes** (Habitat Suitability):
```javascript
// Define suitable climate conditions
const climateEnvelope = {
  temperature: { min: -10, max: 15, optimal: 3 },
  precipitation: { min: 300, max: 800, optimal: 500 }
};

// Map areas with suitable climate
const suitableAreas = await mapClimateEnvelope({
  envelope: climateEnvelope,
  region: 'Nepal',
  year: 2024
});

// Compare to past (climate change impact)
const suitableAreas2000 = await mapClimateEnvelope({
  envelope: climateEnvelope,
  region: 'Nepal',
  year: 2000
});

// Calculate habitat loss
const areaLost = suitableAreas2000.area - suitableAreas.area;
// Result: 1,234 km² of suitable habitat lost (2000-2024)
```

### 7.3 Climate-Driven Range Shifts

**Observed Patterns in Himalayas**:

1. **Upslope Migration**
   - Species moving to higher elevations (tracking cooling)
   - Average: +200-400m elevation increase/decade

2. **Phenological Shifts**
   - Earlier spring arrival (birds)
   - Extended growing season (plants)
   - Mismatch with resources (e.g., caterpillars peak before bird breeding)

3. **Range Contractions**
   - High-elevation specialists (nowhere colder to go)
   - Alpine species losing habitat

4. **Community Reshuffling**
   - New species assemblages (no historic analog)
   - Winners vs losers

**THI Knowledge Common tracks these changes**:
- Decade-by-decade distribution maps
- Elevational shift calculations
- Phenology tracking (if observation dates available)
- "Climate velocity" maps (how fast species must move to track climate)

---

## 8. Ecological Indicators

### 8.1 Indicator Types

**THI Knowledge Common calculates multiple biodiversity indicators**:

| Indicator | What it Measures | Data Required | Interpretation |
|-----------|------------------|---------------|----------------|
| **Species Richness** | Number of species | Occurrence data | Higher = more diversity |
| **Shannon Diversity** | Species evenness | Abundance data | Accounts for rarity |
| **Simpson's Index** | Dominance | Abundance data | Lower = more even |
| **Beta Diversity** | Turnover between sites | Multi-site data | Spatial variation |
| **Endemism** | % endemic species | Distribution + taxonomy | Conservation priority |
| **Threat Status** | % threatened species | IUCN Red List | Extinction risk |
| **Completeness** | Survey effort | Observation accumulation | Data sufficiency |

### 8.2 Example: Species Richness Calculation

```javascript
// Calculate species richness for Sikkim, 2020
const occurrences = await getOccurrences({
  region: 'Sikkim',
  year: 2020,
  quality: 'RESEARCH_GRADE'
});

// Extract unique species
const species = new Set(occurrences.map(o => o.taxonKey));

const richness = species.size;
// Result: 1,234 species observed in Sikkim in 2020

// Compare to previous decade
const richness2010 = await calculateRichness({
  region: 'Sikkim',
  year: 2010
});

const change = richness - richness2010;
// Result: +156 species (+14% increase)
// Interpretation: More survey effort OR species moving in OR better recording
```

### 8.3 Rarefaction (Controlling for Effort)

**Problem**: More observations → more species detected (even if true richness unchanged)

**Solution**: Rarefaction (subsample to equal effort)

```javascript
const rarefied = await rarefaction({
  occurrences: occurrences2020,
  sampleSize: 1000  // Subsample to 1000 observations
});

// Repeat 100 times, take mean
const rarefiedRichness = mean(rarefied);
// Now comparable to 2010 (if also rarefied to 1000)
```

---

[**DOCUMENT CONTINUES... This is ~25% complete**]

**Remaining Sections (9-27)** will cover:
- Technical architecture details
- Development workflows
- Data interpretation for ecologists
- Analysis case studies
- API documentation
- Glossary of ~200 terms

**Total Expected Length**: ~15,000 lines (this is the master reference document)

---

## TO BE CONTINUED...

This comprehensive guide is being developed in sections. The full version will be completed and can be used as:

1. **Onboarding material** for new team members
2. **Reference documentation** for current developers and ecologists
3. **Training material** for citizen scientists
4. **Grant proposals** and funding applications
5. **Academic publications** (methodology sections)

**Next Steps**:
1. Complete all 27 sections
2. Add diagrams and flowcharts
3. Include code examples for common tasks
4. Create quick-reference cards
5. Translate to local languages (Hindi, Nepali, Dzongkha)
