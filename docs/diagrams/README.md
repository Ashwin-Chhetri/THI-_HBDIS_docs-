# HMBIS Knowledge Common - Visual Diagrams
## Professional Architecture & Data Flow Diagrams

**Organization**: The Himalayan Initiative  
**Project**: Mountain and Biodiversity Information System (HMBIS)  
**Component**: Knowledge Common for Eastern Himalaya  
**Version**: 1.0  
**Date**: November 6, 2025

---

## 📊 Diagram Suite Overview

This directory contains professional, publication-ready diagrams documenting the technical architecture, data flows, and system design of the HMBIS Knowledge Common platform. All diagrams are created using **Mermaid.js** format and can be exported to **SVG** or **PNG** for inclusion in technical documentation, grant proposals, and publications.

---

## 📑 Diagram Catalog

### 1. [System Architecture Diagram](./01_system_architecture.md)
**Figure 5: System Architecture of the Himalayan Knowledge Common**

**Purpose**: Shows complete system architecture from data sources through visualization

**Layers Visualized**:
- 📊 **Data Sources**: ATREE monitoring data, GBIF API, public geospatial datasets, socioeconomic data
- 🔄 **Ingestion & Standardization**: Darwin Core metadata cataloguing, validation, harmonization
- 💾 **Data Repository & Processing**: PostgreSQL + PostGIS storage, versioning, indicator computation (SMI, SDI, SHI)
- 🎨 **Visualization & API**: REST/GraphQL APIs, MapLibre map services, UI components
- 👤 **User Interaction**: Public interface, admin tools, export modules
- 🔐 **Cross-Cutting Services**: Authentication, logging, monitoring

**Key Features**:
- Clear directional arrows showing data flow
- Color-coded layers (green, blue, orange, purple, pink, gray)
- Standards-compliant (Darwin Core, ISO 19115, OGC)

**Export Sizes**: 2400x1800px recommended

---

### 2. [Data Flow Diagram](./02_data_flow.md)
**Figure 6: Data Flow for the Knowledge Common**

**Purpose**: Visualizes complete data transformation pipeline from input to output

**Flow Stages**:
1. 🔵 **Data Input**: External (GBIF, repositories) + Internal (ATREE, uploads)
2. 🔷 **Metadata Extraction & Validation**: Parsing, registry, error checking, quality flags
3. 🟠 **Database Integration**: Standardization, PostGIS storage, provenance tracking
4. 🔴 **Indicator Computation**: Aggregation, SMI/SDI/SHI calculation
5. 🟣 **Visualization Pipeline**: Database queries, GeoJSON tile generation, frontend rendering
6. 🟢 **User Output**: Downloads, dashboards, change indicators

**Technical Details**:
- Color-coded stages for easy comprehension
- Feedback loops for corrections and updates
- Code examples for each stage
- Performance timing estimates
- SQL and JavaScript implementation snippets

**Export Sizes**: 2400x3000px recommended (vertical layout)

---

### 3. [Database Schema Overview](./03_database_schema.md)
**Entity Relationship Diagram (ERD)**

**Purpose**: Complete database schema showing all tables and relationships

**Core Entities**:
- **Users**: Authentication and authorization
- **Regions**: Geographic boundaries (PostGIS)
- **Taxonomy Cache**: GBIF taxonomy lookup
- **Species**: Extended species information
- **Occurrences**: Primary biodiversity data (partitioned by region)
- **Ecosystems**: Ecosystem type mapping
- **Socioeconomic**: Village-level demographic data
- **Indicators**: SMI/SDI/SHI computed metrics
- **Layers**: User-created custom visualizations
- **Activity Log**: Audit trail

**Technical Specifications**:
- PostgreSQL 15 + PostGIS 3.4
- Spatial indexes (GIST)
- Full-text search (GIN)
- Partitioning strategy
- Foreign key constraints
- Sample queries included

**Export Sizes**: 3000x2400px recommended (wide layout)

---

### 4. [User Interaction Overview](./04_user_interaction.md)
**UI to Data Flow Diagram**

**Purpose**: Shows how user actions flow through the application stack

**Architecture Layers**:
- 🖥️ **User Interface**: Map, search box, filters, layer toggles, charts
- ⚛️ **React Components**: SpeciesView, MapView, FilterPanel, ChartView
- 📦 **Redux State Management**: Species, Map, Filter, UI slices
- 🔌 **API Services**: Species, Occurrence, Region, Indicator services
- 🖥️ **Backend Endpoints**: REST APIs for data retrieval

**User Scenarios Documented**:
1. **Species Search & Visualization**: Type query → API call → Map update
2. **Region Filter & Layer Toggle**: Select region → Filter data → Render layers
3. **Dashboard Data Request**: Navigate to dashboard → Parallel API calls → Charts render

**Performance Insights**:
- Fast interactions (<100ms): Layer toggles, pan/zoom
- Medium interactions (100-500ms): Autocomplete, cached queries
- Slow interactions (500ms-2s): Large dataset loads, computations

**Optimization Strategies**: Debouncing, caching, lazy loading, web workers

**Export Sizes**: 2400x2800px recommended

---

### 5. [Scalability Architecture](./05_scalability.md)
**Regional Expansion Flow Diagram**

**Purpose**: Shows architectural evolution from single region to Himalayan scale

**Phases Visualized**:

**🟢 Current State**: Single Region (Sikkim)
- Single server deployment
- 7,096 km² coverage
- ~500 species, ~10,000 occurrences
- 10-50 concurrent users

**🔵 Phase 1**: Multi-Region (5 Regions)
- Load-balanced application (2-3 servers)
- Database partitioning by region
- Redis caching layer
- 167,382 km² coverage
- ~2,500 species, ~250,000 occurrences
- 100-500 concurrent users

**🟣 Phase 2**: Himalayan Scale (10+ Regions)
- Microservices architecture
- Distributed database (sharding + replicas)
- CDN distribution
- Kubernetes auto-scaling
- 500,000+ km² coverage
- 10,000+ species, 5,000,000+ occurrences
- 1,000-5,000 concurrent users

**Infrastructure Details**:
- Cost breakdowns by phase
- Monitoring strategies (Prometheus, Datadog)
- Migration steps
- Regional data isolation
- Data sovereignty compliance

**Export Sizes**: 2800x2200px recommended

---

## 🎨 Visual Design Standards

### Color Palette (ATREE/THI Branding)

| Layer/Component | Color | Hex Code |
|----------------|-------|----------|
| Data Sources | Green | `#4CAF50` |
| Processing | Blue | `#2196F3` |
| Storage | Orange | `#FF9800` |
| Visualization | Purple | `#9C27B0` |
| User Interface | Pink | `#E91E63` |
| Infrastructure | Gray | `#607D8B` |

### Typography
- **Primary Font**: Arial, Helvetica, sans-serif
- **Code Font**: Consolas, Monaco, monospace
- **Title Size**: 18-24px
- **Label Size**: 12-14px

### Icon Usage
- 📊 Data Sources
- 🔄 Processing/Transformation
- 💾 Storage/Database
- 🎨 Visualization
- 👤 Users
- 🔐 Security
- 📈 Analytics
- 🌍 Geographic

---

## 🛠️ Export Instructions

### Prerequisites
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Or use Docker
docker pull minlag/mermaid-cli
```

### Export to SVG
```bash
# Single diagram
mmdc -i 01_system_architecture.md -o system_architecture.svg -t neutral -b transparent

# All diagrams
for file in *.md; do
    mmdc -i "$file" -o "${file%.md}.svg" -t neutral -b transparent
done
```

### Export to PNG (High Resolution)
```bash
# 300 DPI for print quality
mmdc -i 01_system_architecture.md -o system_architecture.png \
     -t neutral -w 2400 -H 1800 -s 2

# Specific diagram with custom size
mmdc -i 02_data_flow.md -o data_flow.png \
     -t neutral -w 2400 -H 3000 -s 2 -b white
```

### Export All Diagrams (Batch Script)
```bash
#!/bin/bash
# export_all_diagrams.sh

diagrams=(
    "01_system_architecture:2400:1800"
    "02_data_flow:2400:3000"
    "03_database_schema:3000:2400"
    "04_user_interaction:2400:2800"
    "05_scalability:2800:2200"
)

mkdir -p exports/svg exports/png

for diagram in "${diagrams[@]}"; do
    IFS=':' read -r name width height <<< "$diagram"
    
    echo "Exporting $name..."
    
    # SVG
    mmdc -i "${name}.md" -o "exports/svg/${name}.svg" \
         -t neutral -b transparent
    
    # PNG
    mmdc -i "${name}.md" -o "exports/png/${name}.png" \
         -t neutral -w "$width" -H "$height" -s 2 -b white
done

echo "Export complete!"
```

---

## 📐 Diagram Dimensions

| Diagram | Format | Width | Height | Aspect Ratio |
|---------|--------|-------|--------|--------------|
| System Architecture | Landscape | 2400px | 1800px | 4:3 |
| Data Flow | Portrait | 2400px | 3000px | 4:5 |
| Database Schema | Landscape | 3000px | 2400px | 5:4 |
| User Interaction | Portrait | 2400px | 2800px | 6:7 |
| Scalability | Landscape | 2800px | 2200px | 14:11 |

---

## 📄 Usage in Documentation

### Markdown Inclusion
```markdown
## System Architecture

![System Architecture](./diagrams/exports/svg/01_system_architecture.svg)

*Figure 5: Complete system architecture showing data sources through user interaction.*
```

### LaTeX Inclusion
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.9\textwidth]{diagrams/exports/png/01_system_architecture.png}
    \caption{System Architecture of the Himalayan Knowledge Common}
    \label{fig:system_architecture}
\end{figure}
```

### HTML Inclusion
```html
<figure>
    <img src="diagrams/exports/svg/01_system_architecture.svg" 
         alt="System Architecture"
         style="max-width: 100%; height: auto;">
    <figcaption>
        <strong>Figure 5:</strong> System Architecture of the Himalayan Knowledge Common
    </figcaption>
</figure>
```

---

## 🎯 Use Cases

### For Grant Proposals
- Use **Figure 5** (System Architecture) to show comprehensive platform design
- Use **Figure 6** (Data Flow) to demonstrate data quality assurance
- Use **Figure 5.3** (Scalability) to show growth potential

### For Technical Documentation
- Use **Figure 3** (Database Schema) for developer onboarding
- Use **Figure 4** (User Interaction) for frontend architecture explanation
- Use **Figure 6** (Data Flow) for data pipeline documentation

### For Academic Publications
- Use **Figure 5** for system overview in methods section
- Use **Figure 6** for data processing description
- Cite: "The Himalayan Initiative HMBIS Knowledge Common (2025)"

### For Stakeholder Presentations
- Use simplified versions of **Figure 5** for high-level overview
- Use **Figure 4** to show user experience flow
- Use **Figure 5.3** to demonstrate expansion roadmap

---

## 🔧 Customization Guide

### Editing Diagrams

1. **Open source file** (e.g., `01_system_architecture.md`)
2. **Locate Mermaid code block** (between ` ```mermaid` and ` ``` `)
3. **Make changes** following Mermaid syntax
4. **Preview** using [Mermaid Live Editor](https://mermaid.live)
5. **Export** using mmdc command

### Adding New Nodes
```mermaid
NEW_NODE[Node Label<br/>━━━━━━━━━━<br/>Detail Line 1<br/>Detail Line 2]:::styleClass
```

### Adding Connections
```mermaid
NODE_A --> NODE_B  # Solid arrow
NODE_A -.-> NODE_B  # Dotted arrow (optional/async)
NODE_A ==> NODE_B  # Thick arrow (important)
```

### Custom Styling
```mermaid
classDef customStyle fill:#E8F5E9,stroke:#4CAF50,stroke-width:2px,color:#1B5E20

NODE[Label]:::customStyle
```

---

## 📊 Diagram Statistics

| Metric | Count |
|--------|-------|
| **Total Diagrams** | 5 |
| **Total Nodes** | 80+ |
| **Total Connections** | 120+ |
| **Code Examples** | 50+ |
| **Lines of Documentation** | 5,000+ |

---

## 🤝 Contributing

### Diagram Improvement Guidelines

1. **Clarity First**: Ensure diagrams are understandable at a glance
2. **Consistent Styling**: Use established color palette and fonts
3. **Accurate Labels**: All components should be clearly labeled
4. **Updated Documentation**: Keep text descriptions in sync with diagrams
5. **Version Control**: Update version numbers when making significant changes

### Submitting Changes

```bash
# 1. Create feature branch
git checkout -b update-diagrams

# 2. Edit diagram markdown files
vim docs/diagrams/01_system_architecture.md

# 3. Export updated diagrams
./export_all_diagrams.sh

# 4. Commit changes
git add docs/diagrams/
git commit -m "Update system architecture diagram with new API layer"

# 5. Push and create PR
git push origin update-diagrams
```

---

## 📚 Standards & Compliance

### Data Standards Referenced
- **Darwin Core**: Biodiversity data standard (https://dwc.tdwg.org)
- **ISO 19115**: Geographic metadata standard
- **OGC Standards**: WMS, WFS, GeoJSON
- **GeoJSON**: RFC 7946 specification

### Technical Standards
- **REST API**: OpenAPI 3.0
- **GraphQL**: June 2018 specification
- **PostgreSQL**: SQL:2016 standard
- **PostGIS**: OGC Simple Features

---

## 🔗 Related Documentation

- **[Technical Brief](../technical-brief/)**: Comprehensive technical documentation (8 documents)
- **[Architecture Documentation](../ARCHITECTURE.md)**: Current system architecture
- **[Development Guidelines](../DEVELOPMENT_GUIDELINES.md)**: Coding standards and practices
- **[README](../../README.md)**: Project overview

---

## 📧 Contact

**Diagram Queries**: [Contact Technical Team]  
**HMBIS Project**: The Himalayan Initiative  
**GitHub**: https://github.com/Ashwin-Chhetri/THI-Knowledge-Common

---

## 📄 License

These diagrams are part of the HMBIS Knowledge Common project and are licensed under **MIT License**.

```
Copyright (c) 2024-2025 The Himalayan Initiative

Permission is hereby granted to use, modify, and distribute these diagrams
for documentation, educational, and research purposes with attribution.
```

---

## 🙏 Acknowledgments

**Created by**: Technical Documentation Team  
**Review**: Architecture Review Board  
**Tools**: Mermaid.js, Visual Studio Code  
**Inspiration**: GBIF, Map of Life, Global Forest Watch platforms

---

**Last Updated**: November 6, 2025  
**Diagram Suite Version**: 1.0  
**Mermaid Version**: 10.6+

---

**Ready to Export?** Run `./export_all_diagrams.sh` to generate publication-ready diagrams! 🚀
