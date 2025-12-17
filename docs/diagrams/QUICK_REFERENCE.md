# Quick Reference Guide - HMBIS Diagrams

## 🎯 One-Page Cheat Sheet

### Diagram Files

| # | Diagram | File | Purpose | Size |
|---|---------|------|---------|------|
| 5 | **System Architecture** | `01_system_architecture.md` | Complete platform architecture | 2400x1800 |
| 6 | **Data Flow** | `02_data_flow.md` | Data transformation pipeline | 2400x3000 |
| - | **Database Schema** | `03_database_schema.md` | Entity relationships | 3000x2400 |
| - | **User Interaction** | `04_user_interaction.md` | UI to backend flow | 2400x2800 |
| - | **Scalability** | `05_scalability.md` | Growth architecture | 2800x2200 |

---

## ⚡ Quick Commands

### Install Tools
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Or use Yarn
yarn global add @mermaid-js/mermaid-cli
```

### Export Single Diagram
```bash
# SVG (vector, scalable)
mmdc -i 01_system_architecture.md -o system_architecture.svg -t neutral -b transparent

# PNG (raster, high-res)
mmdc -i 01_system_architecture.md -o system_architecture.png -t neutral -w 2400 -H 1800
```

### Export All Diagrams
```bash
cd docs/diagrams
./export_all_diagrams.sh
```

### Preview Online
Visit https://mermaid.live and paste code from ` ```mermaid` blocks

---

## 🎨 Color Reference

```
Data Sources:    #4CAF50 (Green)
Processing:      #2196F3 (Blue)
Storage:         #FF9800 (Orange)
Visualization:   #9C27B0 (Purple)
User Interface:  #E91E63 (Pink)
Infrastructure:  #607D8B (Gray)
```

---

## 📊 Diagram Contents At-a-Glance

### Figure 5: System Architecture
**Layers**: Data Sources → Ingestion → Repository → Visualization → Users  
**Standards**: Darwin Core, ISO 19115, OGC  
**Key Components**: GBIF API, PostGIS, MapLibre, REST API

### Figure 6: Data Flow
**Stages**: Input → Validation → Storage → Computation → Rendering → Output  
**Indicators**: SMI, SDI, SHI  
**Technologies**: PostgreSQL, Redis, Vector Tiles

### Database Schema
**Tables**: 15 core tables  
**Entities**: Users, Regions, Occurrences, Species, Indicators  
**Features**: Partitioning, Spatial indexes, Full-text search

### User Interaction
**Layers**: UI → Components → State → API → Backend  
**Framework**: React 19 + Redux + MapLibre  
**Flows**: Search, Filter, Visualize

### Scalability
**Phases**:  
- Current: 1 region, 50 users  
- Phase 1: 5 regions, 500 users  
- Phase 2: 10+ regions, 5000 users

**Tech**: Load balancing, Sharding, CDN, Auto-scaling

---

## 🔧 Common Edits

### Change Node Label
```mermaid
OLD_NODE[Old Label]:::styleClass
# Change to:
NEW_NODE[New Label<br/>With Details]:::styleClass
```

### Add Connection
```mermaid
NODE_A --> NODE_B  # Solid arrow
NODE_A -.-> NODE_B  # Dotted arrow
```

### Change Color
```mermaid
classDef newStyle fill:#NEW_COLOR,stroke:#BORDER_COLOR,stroke-width:2px

NODE[Label]:::newStyle
```

---

## 📤 Export Options

### For Web/Documentation
```bash
mmdc -i diagram.md -o diagram.svg -t neutral -b transparent
```
**Use**: Markdown, HTML, web pages

### For Print/Publications
```bash
mmdc -i diagram.md -o diagram.png -t neutral -w 2400 -H 1800 -s 2 -b white
```
**Use**: PDF, LaTeX, printed materials

### For Presentations
```bash
mmdc -i diagram.md -o diagram.png -t dark -w 1920 -H 1080 -b #1e1e1e
```
**Use**: PowerPoint, Google Slides (dark theme)

---

## 📝 Usage Examples

### Markdown
```markdown
![System Architecture](./diagrams/exports/svg/01_system_architecture.svg)
```

### HTML
```html
<img src="diagrams/exports/svg/01_system_architecture.svg" alt="Architecture">
```

### LaTeX
```latex
\includegraphics[width=\textwidth]{diagrams/exports/png/01_system_architecture.png}
```

---

## 🐛 Troubleshooting

### mmdc: command not found
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Export fails / Blank output
```bash
# Use Docker instead
docker run --rm -v $(pwd):/data minlag/mermaid-cli \
  -i /data/diagram.md -o /data/diagram.svg
```

### Syntax error in diagram
1. Copy code block (between ` ```mermaid` and ` ``` `)
2. Paste in https://mermaid.live
3. Fix errors shown in preview
4. Copy corrected code back

### Low quality PNG
```bash
# Increase scale factor (-s) and dimensions
mmdc -i diagram.md -o diagram.png -s 3 -w 3600 -H 2700
```

---

## 📋 Checklist Before Publication

- [ ] All diagrams export without errors
- [ ] SVG files open correctly in browser
- [ ] PNG files are high resolution (300 DPI)
- [ ] Labels are clear and readable
- [ ] Colors match ATREE/THI branding
- [ ] Documentation text matches diagrams
- [ ] Version numbers updated
- [ ] File sizes reasonable (<5 MB per diagram)

---

## 🔗 Quick Links

- **Mermaid Live Editor**: https://mermaid.live
- **Mermaid Documentation**: https://mermaid.js.org
- **HMBIS Repository**: https://github.com/Ashwin-Chhetri/THI-Knowledge-Common
- **Technical Brief**: `docs/technical-brief/README.md`
- **Full Documentation**: `docs/diagrams/README.md`

---

## 💡 Tips

1. **Always preview** in Mermaid Live before committing
2. **Use descriptive labels** - avoid abbreviations
3. **Keep it simple** - complex diagrams are hard to read
4. **Test exports** - verify output before sharing
5. **Version control** - commit source `.md` files, not just exports
6. **Document changes** - update README when modifying diagrams

---

**Last Updated**: November 6, 2025  
**Quick Ref Version**: 1.0

For complete documentation, see `README.md` in this directory.
