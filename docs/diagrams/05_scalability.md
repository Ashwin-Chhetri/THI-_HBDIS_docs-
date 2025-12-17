# Scalability Architecture - Regional Expansion Flow

## Visual Diagram

```mermaid
graph TB
    %% Styling
    classDef current fill:#E8F5E9,stroke:#4CAF50,stroke-width:3px,color:#1B5E20
    classDef future fill:#E3F2FD,stroke:#2196F3,stroke-width:3px,color:#0D47A1
    classDef infrastructure fill:#FFF3E0,stroke:#FF9800,stroke-width:3px,color:#E65100
    classDef scale fill:#F3E5F5,stroke:#9C27B0,stroke-width:3px,color:#4A148C
    
    %% Current Implementation
    subgraph CURRENT[" 🟢 CURRENT: SINGLE REGION (Sikkim) "]
        C_APP[Single Application Instance<br/>━━━━━━━━━━<br/>All data in one database<br/>Monolithic architecture]:::current
        C_DB[PostgreSQL Database<br/>━━━━━━━━━━<br/>7,096 km² coverage<br/>~500 species<br/>~10,000 occurrences]:::current
        C_USERS[Limited User Base<br/>━━━━━━━━━━<br/>10-50 concurrent users<br/>Single region focus]:::current
    end
    
    %% Phase 1: Multi-Region
    subgraph PHASE1[" 🔵 PHASE 1: MULTI-REGION (5 Regions) "]
        P1_APP[Load-Balanced Application<br/>━━━━━━━━━━<br/>2-3 API server instances<br/>Region-aware routing]:::future
        P1_DB[Partitioned Database<br/>━━━━━━━━━━<br/>167,382 km² total coverage<br/>~2,500 species<br/>~250,000 occurrences]:::future
        P1_CACHE[Redis Cache Layer<br/>━━━━━━━━━━<br/>Tile caching<br/>Query result caching]:::future
        P1_USERS[Expanded User Base<br/>━━━━━━━━━━<br/>100-500 concurrent users<br/>Multi-region researchers]:::future
    end
    
    %% Phase 2: Full Himalayan Scale
    subgraph PHASE2[" 🟣 PHASE 2: HIMALAYAN SCALE (10+ Regions) "]
        P2_LB[Load Balancer<br/>━━━━━━━━━━<br/>Nginx/HAProxy<br/>Health checks<br/>Auto-scaling]:::scale
        P2_API[API Gateway<br/>━━━━━━━━━━<br/>Rate limiting<br/>Authentication<br/>Request routing]:::scale
        P2_MICRO[Microservices<br/>━━━━━━━━━━<br/>Species Service<br/>Occurrence Service<br/>Indicator Service]:::scale
        P2_DB[Distributed Database<br/>━━━━━━━━━━<br/>Primary + Read Replicas<br/>Regional partitioning<br/>Sharding strategy]:::scale
        P2_CACHE[Distributed Cache<br/>━━━━━━━━━━<br/>Redis Cluster<br/>Multi-level caching]:::scale
        P2_CDN[CDN Distribution<br/>━━━━━━━━━━<br/>Global edge network<br/>Tile delivery<br/>Static assets]:::scale
        P2_USERS[Large User Base<br/>━━━━━━━━━━<br/>1000+ concurrent users<br/>International access]:::scale
    end
    
    %% Infrastructure Layer
    subgraph INFRA[" 🟠 INFRASTRUCTURE EVOLUTION "]
        I_MONITOR[Monitoring & Logging<br/>━━━━━━━━━━<br/>Datadog/Prometheus<br/>Error tracking (Sentry)<br/>Performance metrics]:::infrastructure
        I_BACKUP[Backup & Recovery<br/>━━━━━━━━━━<br/>Automated backups<br/>Point-in-time recovery<br/>Geographic replication]:::infrastructure
        I_SECURITY[Security Hardening<br/>━━━━━━━━━━<br/>WAF protection<br/>DDoS mitigation<br/>Encryption at rest]:::infrastructure
    end
    
    %% Flow Connections
    C_APP --> P1_APP
    C_DB --> P1_DB
    C_USERS --> P1_USERS
    
    P1_APP --> P2_LB
    P1_DB --> P2_DB
    P1_CACHE --> P2_CACHE
    P1_USERS --> P2_USERS
    
    P2_LB --> P2_API
    P2_API --> P2_MICRO
    P2_MICRO --> P2_DB
    P2_MICRO --> P2_CACHE
    P2_CACHE --> P2_CDN
    
    I_MONITOR -.-> P1_APP
    I_MONITOR -.-> P2_MICRO
    I_BACKUP -.-> P1_DB
    I_BACKUP -.-> P2_DB
    I_SECURITY -.-> P2_LB
    I_SECURITY -.-> P2_API
```

## Scalability Roadmap

### 🟢 Current State: Single Region (Sikkim)

**Architecture**:
- **Deployment**: Single server or serverless (Vercel/Netlify)
- **Database**: PostgreSQL on single instance
- **Storage**: Client-side IndexedDB + limited server storage
- **Users**: 10-50 concurrent researchers

**Capacity**:
| Metric | Current |
|--------|---------|
| Geographic Coverage | 7,096 km² (Sikkim) |
| Species Count | ~500 |
| Occurrence Records | ~10,000 |
| Concurrent Users | 50 |
| API Response Time | <500ms (light load) |
| Database Size | ~500 MB |

**Limitations**:
- ❌ Cannot scale to multiple regions efficiently
- ❌ No redundancy or failover
- ❌ Single point of failure
- ❌ Limited concurrent user support
- ❌ No geographic distribution

---

### 🔵 Phase 1: Multi-Region Eastern Himalaya (5 Regions)

**Target Date**: Q3 2026  
**Geographic Expansion**:
1. Sikkim (current)
2. Darjeeling
3. Eastern Bhutan
4. Eastern Nepal
5. Arunachal Pradesh

**Architecture Changes**:

#### 1. Load-Balanced Application
```
┌─────────────────┐
│  Load Balancer  │
│   (Nginx)       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌───▼───┐
│API #1 │ │API #2 │
└───────┘ └───────┘
```

**Configuration**:
```nginx
# nginx.conf
upstream api_backend {
    least_conn;  # Route to server with fewest connections
    server api1.hmbis.org:3000 weight=3;
    server api2.hmbis.org:3000 weight=2;
}

server {
    listen 80;
    server_name api.hmbis.org;
    
    location /api/ {
        proxy_pass http://api_backend;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 2. Database Partitioning
```sql
-- Partition occurrences by region
CREATE TABLE occurrences (
    id UUID,
    region_id UUID,
    /* other fields */
) PARTITION BY LIST (region_id);

-- Create partitions for each region
CREATE TABLE occurrences_sikkim PARTITION OF occurrences
    FOR VALUES IN ('uuid-sikkim');

CREATE TABLE occurrences_darjeeling PARTITION OF occurrences
    FOR VALUES IN ('uuid-darjeeling');

CREATE TABLE occurrences_bhutan PARTITION OF occurrences
    FOR VALUES IN ('uuid-bhutan');

CREATE TABLE occurrences_nepal PARTITION OF occurrences
    FOR VALUES IN ('uuid-nepal');

CREATE TABLE occurrences_arunachal PARTITION OF occurrences
    FOR VALUES IN ('uuid-arunachal');

-- Queries automatically use correct partition
SELECT * FROM occurrences WHERE region_id = 'uuid-sikkim';
-- Only scans occurrences_sikkim partition (faster!)
```

#### 3. Redis Caching
```javascript
// Cache frequently accessed data
const redis = require('redis');
const client = redis.createClient();

// Cache species lookup
async function getSpecies(taxonKey) {
  const cacheKey = `species:${taxonKey}`;
  
  // Try cache first
  const cached = await client.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Fetch from database
  const species = await db.query(
    'SELECT * FROM species WHERE taxon_key = $1',
    [taxonKey]
  );
  
  // Cache for 1 hour
  await client.setex(cacheKey, 3600, JSON.stringify(species));
  
  return species;
}

// Cache vector tiles
async function getTile(z, x, y, layerId) {
  const cacheKey = `tile:${layerId}:${z}:${x}:${y}`;
  
  const cached = await client.getBuffer(cacheKey);
  if (cached) return cached;
  
  const tile = await generateTile(z, x, y, layerId);
  
  // Cache for 24 hours
  await client.setex(cacheKey, 86400, tile);
  
  return tile;
}
```

**Capacity After Phase 1**:
| Metric | Phase 1 Target |
|--------|----------------|
| Geographic Coverage | 167,382 km² (5 regions) |
| Species Count | ~2,500 |
| Occurrence Records | ~250,000 |
| Concurrent Users | 100-500 |
| API Response Time | <300ms (with caching) |
| Database Size | ~5 GB |

**Infrastructure Costs**:
- API Servers (2x): $48/month
- PostgreSQL (managed): $60/month
- Redis (managed): $20/month
- Load Balancer: $12/month
- **Total**: ~$140/month

---

### 🟣 Phase 2: Full Himalayan Scale (10+ Regions)

**Target Date**: 2027+  
**Geographic Expansion**: Entire Hindu Kush Himalayan region

**Architecture Changes**:

#### 1. Microservices Architecture
```
┌──────────────┐
│ API Gateway  │
│  (Kong/AWS)  │
└──────┬───────┘
       │
   ┌───┴────────────────┐
   │                    │
┌──▼──────────┐  ┌──────▼────────┐
│   Species   │  │  Occurrence   │
│   Service   │  │   Service     │
│  (Port 3001)│  │  (Port 3002)  │
└──────┬──────┘  └──────┬────────┘
       │                │
       └────────┬───────┘
                │
        ┌───────▼───────┐
        │   Indicator   │
        │    Service    │
        │  (Port 3003)  │
        └───────────────┘
```

**Service Definitions**:

**Species Service**:
- Species search and autocomplete
- Taxonomy resolution
- Species profile data
- Conservation status

**Occurrence Service**:
- Occurrence CRUD operations
- Spatial queries
- Filtering and aggregation
- Bulk import/export

**Indicator Service**:
- SMI/SDI/SHI computation
- Trend analysis
- Change detection
- Alert generation

#### 2. Database Sharding Strategy
```
┌──────────────────────────────────────┐
│         Application Layer            │
└──────────────┬───────────────────────┘
               │
        ┌──────▼──────┐
        │ Shard Router│
        │  (ProxySQL) │
        └──────┬──────┘
               │
   ┌───────────┼───────────┐
   │           │           │
┌──▼────┐  ┌───▼───┐  ┌───▼───┐
│Shard 1│  │Shard 2│  │Shard 3│
│West   │  │Central│  │East   │
│Regions│  │Regions│  │Regions│
└───────┘  └───────┘  └───────┘

-- Shard routing logic
function getShardForRegion(regionId) {
  const region = regions[regionId];
  
  if (region.longitude < 80) return 'shard-west';
  if (region.longitude < 88) return 'shard-central';
  return 'shard-east';
}
```

#### 3. Read Replicas
```
┌──────────────┐
│   Primary    │  ← Writes
│  PostgreSQL  │
└──────┬───────┘
       │ Replication
   ┌───┴────┬─────────┐
   │        │         │
┌──▼────┐ ┌▼─────┐ ┌─▼─────┐
│Replica│ │Replica│ │Replica│  ← Reads
│  #1   │ │  #2  │ │  #3   │
└───────┘ └──────┘ └───────┘

-- Application routing
const writePool = new Pool({ host: 'primary.db.hmbis.org' });
const readPool = new Pool({ host: 'replica.db.hmbis.org' });

// Writes go to primary
await writePool.query('INSERT INTO occurrences ...');

// Reads distributed across replicas
const result = await readPool.query('SELECT * FROM occurrences ...');
```

#### 4. CDN Distribution
```
┌────────────┐
│   User     │
│  Browser   │
└─────┬──────┘
      │
      ▼
┌─────────────────┐
│  CloudFlare CDN │
│  Edge Locations │
│  - Mumbai       │
│  - Singapore    │
│  - Hong Kong    │
└────────┬────────┘
         │ Cache Miss
         ▼
┌─────────────────┐
│  Origin Server  │
│  (API + Tiles)  │
└─────────────────┘
```

**CDN Configuration**:
```javascript
// Cache-Control headers for different resources
app.get('/api/v1/tiles/:z/:x/:y.mvt', (req, res) => {
  // Vector tiles cache for 7 days
  res.setHeader('Cache-Control', 'public, max-age=604800');
  res.setHeader('CDN-Cache-Control', 'max-age=2592000'); // 30 days on CDN
  
  // ... generate tile
});

app.get('/api/v1/occurrences', (req, res) => {
  // API responses cache for 5 minutes
  res.setHeader('Cache-Control', 'public, max-age=300');
  
  // ... query occurrences
});
```

#### 5. Auto-Scaling
```yaml
# Kubernetes auto-scaling configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hmbis-api
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hmbis-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Capacity After Phase 2**:
| Metric | Phase 2 Target |
|--------|----------------|
| Geographic Coverage | 500,000+ km² (Entire Himalaya) |
| Species Count | 10,000+ |
| Occurrence Records | 5,000,000+ |
| Concurrent Users | 1,000-5,000 |
| API Response Time | <200ms (CDN-accelerated) |
| Database Size | 50+ GB |
| Uptime | 99.9% (SLA) |

**Infrastructure Costs**:
- API Servers (auto-scaling 3-10): $150-500/month
- PostgreSQL Primary: $200/month
- PostgreSQL Replicas (3x): $300/month
- Redis Cluster: $100/month
- CDN: $50/month
- Load Balancer: $50/month
- Kubernetes: $150/month
- Monitoring: $50/month
- **Total**: ~$1,050-1,700/month

---

## Monitoring & Observability

### Key Metrics to Track

#### Application Performance
```javascript
// API response time monitoring
const prometheus = require('prom-client');

const httpRequestDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.1, 0.3, 0.5, 1.0, 2.0, 5.0]
});

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || req.path, res.statusCode)
      .observe(duration);
  });
  
  next();
});
```

#### Database Performance
```sql
-- Slow query log
CREATE TABLE query_log (
    id SERIAL PRIMARY KEY,
    query_text TEXT,
    duration_ms INTEGER,
    rows_returned INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Log queries taking >1 second
ALTER DATABASE hmbis SET log_min_duration_statement = 1000;
```

#### Cache Hit Rates
```javascript
// Track Redis cache effectiveness
const cacheHits = new prometheus.Counter({
  name: 'cache_hits_total',
  help: 'Total number of cache hits',
  labelNames: ['cache_type']
});

const cacheMisses = new prometheus.Counter({
  name: 'cache_misses_total',
  help: 'Total number of cache misses',
  labelNames: ['cache_type']
});

async function getCached(key, cacheType) {
  const value = await redis.get(key);
  
  if (value) {
    cacheHits.labels(cacheType).inc();
    return JSON.parse(value);
  }
  
  cacheMisses.labels(cacheType).inc();
  return null;
}
```

---

## Regional Data Isolation

### Multi-Tenancy Strategy

**Approach**: Shared database with row-level security

```sql
-- Enable row-level security
ALTER TABLE occurrences ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their authorized regions
CREATE POLICY region_access ON occurrences
    FOR SELECT
    USING (
        region_id IN (
            SELECT region_id 
            FROM user_region_access 
            WHERE user_id = current_user_id()
        )
    );

-- Grant full access to admin role
CREATE POLICY admin_all_access ON occurrences
    FOR ALL
    USING (current_user_role() = 'admin');
```

### Data Sovereignty Compliance

**For regions with data residency requirements**:

```
┌─────────────────────────────────────┐
│   Nepal Data (Nepal servers only)   │
│   - Stored in Nepal datacenter      │
│   - Processed locally               │
│   - Complies with local laws        │
└─────────────────────────────────────┘
         ↕ (Federation API)
┌─────────────────────────────────────┐
│   Global HMBIS Platform             │
│   - Aggregated anonymized data      │
│   - Cross-region analytics          │
│   - Public access                   │
└─────────────────────────────────────┘
```

---

## Migration Strategy

### Phase 1 Migration Steps

1. **Backup Current Data** (Week 1)
   ```bash
   pg_dump -Fc hmbis_db > backup_$(date +%Y%m%d).dump
   ```

2. **Set Up New Infrastructure** (Week 2)
   - Provision load balancer
   - Deploy 2 API server instances
   - Set up Redis cache

3. **Database Partitioning** (Week 3-4)
   ```sql
   -- Create new partitioned table
   CREATE TABLE occurrences_new (...) PARTITION BY LIST (region_id);
   
   -- Migrate data
   INSERT INTO occurrences_new SELECT * FROM occurrences;
   
   -- Swap tables
   BEGIN;
   ALTER TABLE occurrences RENAME TO occurrences_old;
   ALTER TABLE occurrences_new RENAME TO occurrences;
   COMMIT;
   ```

4. **Application Updates** (Week 5)
   - Deploy region-aware code
   - Update API endpoints
   - Test multi-region queries

5. **Gradual Traffic Migration** (Week 6)
   ```nginx
   # Start with 10% traffic to new infrastructure
   upstream api_backend {
       server old-api.hmbis.org weight=9;
       server new-api.hmbis.org weight=1;
   }
   
   # Gradually increase weight over days
   ```

6. **Validation & Rollback Plan** (Week 7)
   - Compare query results old vs new
   - Monitor error rates
   - Keep old infrastructure for 2 weeks

---

**Export Instructions**:
```bash
# Generate scalability diagram
mmdc -i 05_scalability.md -o scalability.svg -t neutral -b transparent
mmdc -i 05_scalability.md -o scalability.png -t neutral -w 2800 -H 2200
```

---

**Document**: Scalability Architecture - Regional Expansion Flow  
**Version**: 1.0  
**Date**: November 6, 2025  
**Target Scale**: 5,000+ concurrent users, 5M+ occurrences, 500K+ km²
