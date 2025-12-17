# AI INSTRUCTION MANUAL: THI Knowledge Common Architecture
## Complete Rules for AI Agents Working on This Codebase

> **⚠️ CRITICAL**: This document is **THE SOURCE OF TRUTH** for any AI instance working on THI Knowledge Common. Read this FIRST before making ANY code changes. Failure to follow these rules WILL break the system.

**Version**: 2.0  
**Last Updated**: November 19, 2025  
**Audience**: GitHub Copilot, Claude, GPT-4, and future AI coding assistants  
**Purpose**: Prevent breaking changes when adding features, especially new region types or data sources

---

## 🚨 ABSOLUTE RULES (NEVER VIOLATE)

### Rule #1: NO DIRECT DEPENDENCIES BETWEEN FEATURES
```
❌ FORBIDDEN:
features/species/components/SpeciesPanel.jsx
  ↓ (import)
features/region/store/regionSlice.js

✅ CORRECT:
features/species/components/SpeciesPanel.jsx
  ↓ (subscribe)
EventBus → 'region:changed' event
  ↑ (publish)
features/region/services/RegionService.ts
```

**Enforcement**: ESLint rule `no-restricted-imports`
```javascript
// .eslintrc.js
rules: {
  'no-restricted-imports': ['error', {
    patterns: ['**/features/*/..', '../features/']
  }]
}
```

---

### Rule #2: ALWAYS USE ENTITY REGISTRY (NEVER HARDCODE)

**❌ FORBIDDEN PATTERN**:
```javascript
// RegionPanel.jsx
const isAtreeSiteSelected = 
  selectedRegion?.name === 'Khangchendzonga Landscape' ||
  selectedRegion?.name === 'Trans-himalyan Landscape' ||
  selectedRegion?.name === 'Arunachal Pradesh Landscape';

if (isAtreeSiteSelected) {
  // Special logic
}
```

**✅ CORRECT PATTERN**:
```typescript
// infrastructure/plugins/region-plugins/ATREERegionPlugin.ts
export class ATREERegionPlugin implements RegionPlugin {
  async discover(): Promise<RegionDescriptor[]> {
    // Auto-scan /atree-repository-data/region/ folder
    const files = await scanDirectory('/atree-repository-data/region/');
    
    return files.map(file => ({
      id: generateId(file.name),
      name: extractName(file.name),  // ← Automatic
      type: 'atree-site' as RegionType,
      source: file.path
    }));
  }
}

// domain/regions/entities/Region.ts
export class Region {
  isAtreeSite(): boolean {
    return this.type.equals(RegionType.ATREE_SITE);
  }
}

// Usage (generic for ALL region types):
if (region.isAtreeSite()) {
  // Special logic
}
```

**Why**: New ATREE sites can be added by **dropping a file in a folder**. No code changes.

---

### Rule #3: ALL IMPORTS MUST USE PATH ALIASES

**❌ FORBIDDEN**:
```javascript
import { Region } from '../../../domain/regions/entities/Region';
import { EventBus } from '../../../../core/events/EventBus';
```

**✅ CORRECT**:
```javascript
import { Region } from '@domain/regions';
import { EventBus } from '@core/events';
```

**Path Aliases** (tsconfig.json):
```json
{
  "compilerOptions": {
    "paths": {
      "@core/*": ["src/core/*"],
      "@domain/*": ["src/domain/*"],
      "@application/*": ["src/application/*"],
      "@infrastructure/*": ["src/infrastructure/*"],
      "@presentation/*": ["src/presentation/*"]
    }
  }
}
```

**Enforcement**: ESLint rule
```javascript
// .eslintrc.js
rules: {
  'no-restricted-imports': ['error', {
    patterns: ['../*', '../../*', '../../../*']  // No relative imports
  }]
}
```

---

### Rule #4: NEVER MODIFY DOMAIN ENTITIES DIRECTLY

**❌ FORBIDDEN**:
```javascript
const region = await regionRepository.findById('sikkim');
region.geometry = newGeometry;  // ❌ Direct mutation
await regionRepository.save(region);
```

**✅ CORRECT**:
```typescript
const region = await regionRepository.findById('sikkim');

// Use domain method (validates invariants)
const result = region.updateGeometry(newGeometry);

if (result.isFailure) {
  throw result.error;  // Validation failed
}

await regionRepository.save(region);

// Publish event (automatic in repository)
await eventBus.publish(new RegionGeometryChangedEvent(region.getId(), oldGeometry, newGeometry));
```

**Why**: Domain entities enforce business rules. Direct mutation bypasses validation.

---

### Rule #5: ALWAYS PUBLISH DOMAIN EVENTS

**When to publish**:
- Entity created
- Entity updated
- Entity deleted
- Significant state change

**Pattern**:
```typescript
// ✅ CORRECT: Repository publishes events automatically
export class RegionRepositoryImpl implements RegionRepository {
  async save(region: Region): Promise<void> {
    // 1. Persist to storage
    await this.db.regions.put(region.toDTO());
    
    // 2. Publish event (automatic)
    await this.eventBus.publish(new RegionAddedEvent(region, this.currentUserId));
    
    // 3. Log (automatic)
    this.logger.info('Region saved', { regionId: region.getId().value });
  }
}

// ❌ FORBIDDEN: Manual event publishing in application code
class AddRegionUseCase {
  async execute(command: AddRegionCommand): Promise<void> {
    const region = Region.create(command.data);
    await this.repository.save(region);
    // ❌ DON'T DO THIS (repository already published event)
    await this.eventBus.publish(new RegionAddedEvent(region));
  }
}
```

---

## 📐 ARCHITECTURAL LAYERS (STRICT HIERARCHY)

### Layer Dependency Rules

```
┌─────────────────────────────────────────────────────────┐
│  PRESENTATION (React Components, Hooks)                 │
│  ↓ CAN DEPEND ON: application, domain, core            │
├─────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE (Repositories, APIs, Caching)           │
│  ↓ CAN DEPEND ON: application, domain, core            │
├─────────────────────────────────────────────────────────┤
│  APPLICATION (Use Cases, Commands, Queries)             │
│  ↓ CAN DEPEND ON: domain, core                         │
├─────────────────────────────────────────────────────────┤
│  DOMAIN (Entities, Value Objects, Domain Services)      │
│  ↓ CAN DEPEND ON: core ONLY                            │
├─────────────────────────────────────────────────────────┤
│  CORE (EventBus, Logger, Result, Validation)           │
│  ↓ CAN DEPEND ON: NOTHING                              │
└─────────────────────────────────────────────────────────┘
```

**Enforcement**: `dependency-cruiser` (checks at build time)
```javascript
// .dependency-cruiser.js
module.exports = {
  forbidden: [
    {
      name: 'core-depends-on-nothing',
      from: { path: '^src/core' },
      to: { path: '^src/(domain|application|infrastructure|presentation)' }
    },
    {
      name: 'domain-only-depends-on-core',
      from: { path: '^src/domain' },
      to: { path: '^src/(application|infrastructure|presentation)' }
    },
    {
      name: 'no-cross-feature-imports',
      from: { path: '^src/presentation/features/([^/]+)' },
      to: { path: '^src/presentation/features/(?!\\1)' }
    }
  ]
};
```

---

## 🏗️ HOW TO ADD NEW FEATURES (STEP-BY-STEP)

### Adding a New Region Type (Example: Protected Areas)

**Scenario**: You need to add "Protected Areas" as a new region type.

**❌ WRONG APPROACH** (will break things):
```javascript
// 1. Hardcode in RegionPanel.jsx
const handleProtectedAreaToggle = (checked) => {
  // Copy-paste 100 lines from ATREE toggle handler
};

// 2. Add to regionSlice.js
const [protectedAreaEnabled, setProtectedAreaEnabled] = useState(false);

// 3. Update GBIF filtering logic
if (selectedRegion.name === 'Kaziranga National Park' || ...) {
  // Special logic
}

// ❌ RESULT: Modified 8 files, duplicated 300 lines, fragile
```

**✅ CORRECT APPROACH** (follows architecture):

**Step 1: Create Plugin** (infrastructure/plugins/region-plugins/)
```typescript
// ProtectedAreasRegionPlugin.ts
export class ProtectedAreasRegionPlugin implements RegionPlugin {
  private readonly source = 'https://api.protectedplanet.net/v3/';
  
  async discover(): Promise<RegionDescriptor[]> {
    // Fetch from WDPA (World Database on Protected Areas) API
    const response = await fetch(`${this.source}protected_areas?country=IN,NP,BT,CN`);
    const data = await response.json();
    
    return data.protected_areas.map(pa => ({
      id: `pa-${pa.wdpa_id}`,
      name: pa.name,
      type: 'protected-area' as RegionType,  // ← New type
      source: `${this.source}protected_areas/${pa.wdpa_id}`,
      format: 'geojson',
      metadata: {
        wdpaId: pa.wdpa_id,
        iucnCategory: pa.iucn_category,
        designation: pa.designation
      }
    }));
  }
  
  async load(descriptor: RegionDescriptor): Promise<Region> {
    const response = await fetch(descriptor.source);
    const geojson = await response.json();
    
    return Region.create({
      id: descriptor.id,
      name: descriptor.name,
      type: 'protected-area',
      geometry: Geometry.fromGeoJSON(geojson),
      metadata: descriptor.metadata
    }).unwrap();
  }
  
  async validate(region: Region): Promise<ValidationResult> {
    // Custom validation for protected areas
    if (!region.getMetadata().wdpaId) {
      return ValidationResult.fail('Missing WDPA ID');
    }
    return ValidationResult.ok();
  }
}
```

**Step 2: Register Plugin** (config/dependency-injection.ts)
```typescript
// dependency-injection.ts
export function bootstrapApplication(): Container {
  const container = new Container();
  
  // Register region plugins
  const regionRegistry = new RegionRegistry();
  await regionRegistry.registerPlugin(new ATREERegionPlugin());
  await regionRegistry.registerPlugin(new CountryRegionPlugin());
  await regionRegistry.registerPlugin(new StateRegionPlugin());
  await regionRegistry.registerPlugin(new ProtectedAreasRegionPlugin());  // ← Add one line
  
  container.bind(RegionRegistry).toConstantValue(regionRegistry);
  return container;
}
```

**Step 3: Update Domain Types** (domain/regions/value-objects/RegionType.ts)
```typescript
export class RegionType extends ValueObject<string> {
  static readonly COUNTRY = new RegionType('country');
  static readonly STATE = new RegionType('state');
  static readonly CUSTOM = new RegionType('custom');
  static readonly ATREE_SITE = new RegionType('atree-site');
  static readonly PROTECTED_AREA = new RegionType('protected-area');  // ← Add one line
  
  private constructor(value: string) {
    super(value);
  }
}
```

**Step 4: DONE! No other changes needed**

The existing code **automatically**:
- ✅ Discovers all protected areas via plugin
- ✅ Renders them in UI (generic `RegionSelector` component)
- ✅ Handles toggle logic (generic `useRegionToggle` hook)
- ✅ Publishes events when selected
- ✅ Updates species panel (event subscription)
- ✅ Updates map highlights (event subscription)

**Total changes**: 3 files, ~50 lines of code
**No existing code modified**: ✅

---

### Adding Time-Series Climate Data

**Step 1: Create Climate Domain** (domain/climate/)

```typescript
// domain/climate/entities/ClimateDataPoint.ts
export class ClimateDataPoint {
  constructor(
    private readonly id: string,
    private readonly location: Coordinates,
    private readonly timestamp: Timestamp,
    private readonly variable: ClimateVariable,
    private readonly value: number,
    private readonly unit: string
  ) {}
  
  // Getters
  getId(): string { return this.id; }
  getLocation(): Coordinates { return this.location; }
  getTimestamp(): Timestamp { return this.timestamp; }
  getValue(): number { return this.value; }
}

// domain/climate/entities/ClimateTimeSeries.ts
export class ClimateTimeSeries {
  constructor(
    private readonly id: string,
    private readonly location: Coordinates,
    private readonly variable: ClimateVariable,
    private readonly timeRange: TimeRange,
    private readonly dataPoints: ClimateDataPoint[]
  ) {}
  
  getValueAt(timestamp: Timestamp): number | null {
    // Find exact or interpolate
    return this.interpolate(timestamp);
  }
}
```

**Step 2: Create Repository Interface** (domain/climate/repositories/)
```typescript
// ClimateRepository.ts (INTERFACE, no implementation)
export interface ClimateRepository {
  findByRegion(
    region: Region,
    variable: ClimateVariable,
    timeRange: TimeRange
  ): Promise<ClimateTimeSeries[]>;
  
  streamByRegion(
    region: Region,
    variable: ClimateVariable,
    timeRange: TimeRange
  ): AsyncIterable<ClimateDataPoint>;
}
```

**Step 3: Implement Repository** (infrastructure/persistence/repositories/)
```typescript
// ClimateRepositoryImpl.ts (CONCRETE implementation)
export class ClimateRepositoryImpl implements ClimateRepository {
  constructor(
    private readonly climateAPI: ClimateAPIAdapter,
    private readonly cache: TemporalCache,
    private readonly eventBus: EventBus
  ) {}
  
  async findByRegion(
    region: Region,
    variable: ClimateVariable,
    timeRange: TimeRange
  ): Promise<ClimateTimeSeries[]> {
    // 1. Check cache
    const cached = await this.cache.get(region.getId(), variable, timeRange);
    if (cached) return [cached];
    
    // 2. Fetch from API
    const data = await this.climateAPI.fetchTimeSeries({
      bounds: region.getBounds(),
      variable: variable.getValue(),
      startDate: timeRange.getStart(),
      endDate: timeRange.getEnd()
    });
    
    // 3. Convert to domain model
    const timeSeries = ClimateTimeSeries.fromDTO(data);
    
    // 4. Cache
    await this.cache.set(region.getId(), variable, timeSeries);
    
    // 5. Publish event
    await this.eventBus.publish(
      new ClimateDataLoadedEvent(region.getId(), variable, timeRange)
    );
    
    return [timeSeries];
  }
}
```

**Step 4: Create Use Case** (application/climate/queries/)
```typescript
// get-climate-time-series/GetClimateTimeSeriesQuery.ts
export class GetClimateTimeSeriesQuery {
  constructor(
    public readonly regionId: RegionId,
    public readonly variable: ClimateVariable,
    public readonly timeRange: TimeRange
  ) {}
}

// get-climate-time-series/GetClimateTimeSeriesQueryHandler.ts
export class GetClimateTimeSeriesQueryHandler {
  constructor(
    private readonly regionRepository: RegionRepository,
    private readonly climateRepository: ClimateRepository,
    private readonly logger: Logger
  ) {}
  
  async handle(query: GetClimateTimeSeriesQuery): Promise<Result<ClimateTimeSeries[], Error>> {
    // 1. Get region
    const region = await this.regionRepository.findById(query.regionId);
    if (!region) {
      return Result.fail(new RegionNotFoundError(query.regionId));
    }
    
    // 2. Get climate data
    try {
      const timeSeries = await this.climateRepository.findByRegion(
        region,
        query.variable,
        query.timeRange
      );
      
      this.logger.info('Climate time-series retrieved', {
        regionId: query.regionId.value,
        variable: query.variable.getValue(),
        dataPoints: timeSeries[0].getDataPoints().length
      });
      
      return Result.ok(timeSeries);
    } catch (error) {
      this.logger.error('Failed to retrieve climate data', { error });
      return Result.fail(error);
    }
  }
}
```

**Step 5: Create React Hook** (presentation/features/climate/hooks/)
```typescript
// useClimateData.ts
export function useClimateData(
  regionId: RegionId | null,
  variable: ClimateVariable,
  timeRange: TimeRange
) {
  const [timeSeries, setTimeSeries] = useState<ClimateTimeSeries | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  const queryHandler = useQueryHandler(GetClimateTimeSeriesQueryHandler);
  
  useEffect(() => {
    if (!regionId) return;
    
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      const result = await queryHandler.handle(
        new GetClimateTimeSeriesQuery(regionId, variable, timeRange)
      );
      
      if (result.isSuccess) {
        setTimeSeries(result.value[0]);
      } else {
        setError(result.error);
      }
      
      setLoading(false);
    };
    
    fetchData();
  }, [regionId, variable, timeRange]);
  
  return { timeSeries, loading, error };
}
```

**Step 6: Create UI Component** (presentation/features/climate/components/)
```typescript
// ClimatePanel.tsx
export function ClimatePanel() {
  const selectedRegion = useSelectedRegion();
  const [variable, setVariable] = useState(ClimateVariable.TEMPERATURE);
  const [timeRange, setTimeRange] = useState(
    TimeRange.create(
      Timestamp.create('2000-01-01'),
      Timestamp.create('2024-12-31')
    ).unwrap()
  );
  
  const { timeSeries, loading, error } = useClimateData(
    selectedRegion?.getId(),
    variable,
    timeRange
  );
  
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!timeSeries) return <EmptyState message="Select a region to view climate data" />;
  
  return (
    <div className="climate-panel">
      <ClimateVariableSelector value={variable} onChange={setVariable} />
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />
      <ClimateChart timeSeries={timeSeries} />
    </div>
  );
}
```

**Result**: Fully functional climate time-series feature with:
- ✅ Clean separation of concerns
- ✅ Testable at every layer
- ✅ No coupling to existing features
- ✅ Event-driven updates
- ✅ Automatic caching

---

## 🧪 TESTING REQUIREMENTS

### Test Coverage Targets

| Layer | Unit Tests | Integration Tests | E2E Tests |
|-------|-----------|-------------------|-----------|
| **Domain** | 100% | N/A | N/A |
| **Application** | 90%+ | 100% (use cases) | N/A |
| **Infrastructure** | 70%+ | 100% (repositories) | N/A |
| **Presentation** | 80%+ | N/A | Critical flows only |

### Test Patterns

**Domain Entity Tests**:
```typescript
// domain/regions/entities/Region.spec.ts
describe('Region', () => {
  describe('create', () => {
    it('should create valid region', () => {
      const result = Region.create({
        name: 'Test Region',
        type: 'custom',
        geometry: validGeometry
      });
      
      expect(result.isSuccess).toBe(true);
      expect(result.value.getName()).toBe('Test Region');
    });
    
    it('should reject invalid geometry', () => {
      const result = Region.create({
        name: 'Test Region',
        type: 'custom',
        geometry: invalidGeometry
      });
      
      expect(result.isFailure).toBe(true);
      expect(result.error).toBeInstanceOf(ValidationError);
    });
  });
  
  describe('updateGeometry', () => {
    it('should update valid geometry', () => {
      const region = createValidRegion();
      const result = region.updateGeometry(newValidGeometry);
      
      expect(result.isSuccess).toBe(true);
      expect(region.getGeometry()).toBe(newValidGeometry);
    });
  });
});
```

**Use Case Tests**:
```typescript
// application/regions/commands/add-region/AddRegionCommandHandler.spec.ts
describe('AddRegionCommandHandler', () => {
  let handler: AddRegionCommandHandler;
  let mockRepository: jest.Mocked<RegionRepository>;
  let mockEventBus: jest.Mocked<EventBus>;
  
  beforeEach(() => {
    mockRepository = {
      save: jest.fn(),
      findById: jest.fn()
    };
    mockEventBus = {
      publish: jest.fn()
    };
    handler = new AddRegionCommandHandler(mockRepository, mockEventBus);
  });
  
  it('should add region successfully', async () => {
    const command = new AddRegionCommand({
      name: 'Test Region',
      type: 'custom',
      geometry: validGeometry
    });
    
    const result = await handler.handle(command);
    
    expect(result.isSuccess).toBe(true);
    expect(mockRepository.save).toHaveBeenCalledTimes(1);
    expect(mockEventBus.publish).toHaveBeenCalledWith(
      expect.any(RegionAddedEvent)
    );
  });
});
```

---

## 🚫 COMMON MISTAKES (AND HOW TO AVOID)

### Mistake #1: Skipping the Registry

**❌ WRONG**:
```javascript
// Adding new ATREE site by hardcoding
const newSite = {
  name: 'New ATREE Site',
  type: 'custom',
  // ...
};
dispatch(addRegion(newSite));
```

**✅ CORRECT**:
```javascript
// 1. Add file to /atree-repository-data/region/New_Site.zip
// 2. Plugin auto-discovers it
// 3. Done!
```

---

### Mistake #2: Direct State Mutation

**❌ WRONG**:
```javascript
const region = state.regions.find(r => r.id === 'sikkim');
region.geometry = newGeometry;  // ❌ Mutating Redux state
```

**✅ CORRECT**:
```javascript
dispatch(updateRegionGeometry({ regionId: 'sikkim', geometry: newGeometry }));
```

---

### Mistake #3: Forgetting Events

**❌ WRONG**:
```javascript
async function addRegion(region: Region) {
  await repository.save(region);
  // ❌ Forgot to notify other features!
}
```

**✅ CORRECT**:
```javascript
async function addRegion(region: Region) {
  await repository.save(region);
  await eventBus.publish(new RegionAddedEvent(region));  // ✅ Notify subscribers
}
```

---

### Mistake #4: Coupling to UI Framework

**❌ WRONG** (business logic in React component):
```javascript
function SpeciesPanel() {
  const [occurrences, setOccurrences] = useState([]);
  
  useEffect(() => {
    // ❌ Business logic in component
    const filtered = occurrences.filter(o => 
      turf.booleanPointInPolygon([o.lon, o.lat], regionGeometry)
    );
    const count = filtered.length;
    // ...
  }, [occurrences, regionGeometry]);
}
```

**✅ CORRECT** (business logic in domain/application):
```javascript
// application/species/queries/count-occurrences/CountOccurrencesQueryHandler.ts
class CountOccurrencesQueryHandler {
  async handle(query: CountOccurrencesQuery): Promise<number> {
    const occurrences = await this.repository.findByRegion(query.region);
    return occurrences.length;
  }
}

// presentation/features/species/hooks/useOccurrenceCount.ts
function useOccurrenceCount(region: Region | null) {
  const queryHandler = useQueryHandler(CountOccurrencesQueryHandler);
  
  const [count, setCount] = useState(0);
  
  useEffect(() => {
    if (!region) return;
    const result = await queryHandler.handle(new CountOccurrencesQuery(region));
    setCount(result);
  }, [region]);
  
  return count;
}

// presentation/features/species/components/SpeciesPanel.tsx
function SpeciesPanel() {
  const region = useSelectedRegion();
  const count = useOccurrenceCount(region);  // ✅ Clean, testable
  
  return <div>Occurrences: {count}</div>;
}
```

---

## 📋 CHECKLIST: Before Committing Code

**EVERY commit must pass**:

- [ ] **No relative imports** (`../`, `../../`)
- [ ] **No cross-feature imports** (features don't import from other features)
- [ ] **No hardcoded region names** (use registry)
- [ ] **No hardcoded types** (use enums/value objects)
- [ ] **All domain events published** (when state changes)
- [ ] **Tests written** (unit tests for domain/application)
- [ ] **Types defined** (TypeScript or JSDoc)
- [ ] **Dependency cruiser passes** (`npm run check:deps`)
- [ ] **ESLint passes** (`npm run lint`)
- [ ] **Tests pass** (`npm test`)
- [ ] **No console.logs** (use logger)
- [ ] **Error handling** (use Result type, no uncaught exceptions)

---

## 🔧 CODE GENERATION TEMPLATES

### Template: New Entity

```typescript
// domain/{domain}/entities/{EntityName}.ts
import { ValueObject } from '@core/value-objects';
import { Result } from '@core/result';
import { ValidationError } from '@core/errors';

export class {EntityName} {
  private constructor(
    private readonly id: {EntityName}Id,
    private name: string,
    // Add other fields
  ) {
    this.validate();
  }
  
  static create(data: {EntityName}Data): Result<{EntityName}, ValidationError> {
    // Validation
    if (!data.name || data.name.length < 1) {
      return Result.fail(new ValidationError('{EntityName} name required'));
    }
    
    return Result.ok(new {EntityName}(
      {EntityName}Id.generate(),
      data.name
    ));
  }
  
  private validate(): void {
    if (this.name.length < 1) {
      throw new Error('Invalid {EntityName}');
    }
  }
  
  // Getters
  getId(): {EntityName}Id { return this.id; }
  getName(): string { return this.name; }
  
  // Business methods
  updateName(newName: string): Result<void, ValidationError> {
    if (newName.length < 1) {
      return Result.fail(new ValidationError('Name required'));
    }
    this.name = newName;
    return Result.ok();
  }
  
  // Equality
  equals(other: {EntityName}): boolean {
    return this.id.equals(other.id);
  }
}
```

### Template: New Use Case

```typescript
// application/{domain}/commands/{action}/{Action}Command.ts
export class {Action}Command {
  constructor(
    public readonly entityId: {Entity}Id,
    public readonly data: {Action}Data
  ) {}
}

// application/{domain}/commands/{action}/{Action}CommandHandler.ts
export class {Action}CommandHandler {
  constructor(
    private readonly repository: {Entity}Repository,
    private readonly eventBus: EventBus,
    private readonly logger: Logger
  ) {}
  
  async handle(command: {Action}Command): Promise<Result<void, Error>> {
    try {
      // 1. Get entity
      const entity = await this.repository.findById(command.entityId);
      if (!entity) {
        return Result.fail(new {Entity}NotFoundError(command.entityId));
      }
      
      // 2. Perform action
      const result = entity.{action}(command.data);
      if (result.isFailure) {
        return Result.fail(result.error);
      }
      
      // 3. Save
      await this.repository.save(entity);
      
      // 4. Publish event
      await this.eventBus.publish(new {Entity}{Action}Event(entity));
      
      // 5. Log
      this.logger.info('{Entity} {action}', {
        entityId: entity.getId().value
      });
      
      return Result.ok();
    } catch (error) {
      this.logger.error('{Action} failed', { error });
      return Result.fail(error);
    }
  }
}
```

### Template: New React Hook

```typescript
// presentation/features/{feature}/hooks/use{EntityAction}.ts
import { useState, useEffect } from 'react';
import { {Action}CommandHandler } from '@application/{domain}/commands';
import { useCommandHandler } from '@presentation/shared/hooks';

export function use{Entity}{Action}() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  
  const commandHandler = useCommandHandler({Action}CommandHandler);
  
  const {action} = async (entityId: {Entity}Id, data: {Action}Data) => {
    setLoading(true);
    setError(null);
    
    const result = await commandHandler.handle(
      new {Action}Command(entityId, data)
    );
    
    if (result.isFailure) {
      setError(result.error);
    }
    
    setLoading(false);
    return result;
  };
  
  return { {action}, loading, error };
}
```

---

## 🎯 FINAL REMINDERS

1. **Read this document FIRST** before touching code
2. **Use the templates** above for consistency
3. **Follow the layer rules** (no upward dependencies)
4. **Publish events** for all state changes
5. **Use the registry** (never hardcode entity data)
6. **Test at every layer** (domain → application → infrastructure)
7. **Path aliases always** (no relative imports)
8. **Ask before breaking rules** (there might be a good reason)

---

**Last Updated**: November 19, 2025  
**Maintainer**: THI Knowledge Common Team  
**Questions**: File an issue or ask in team chat

**THIS IS THE SOURCE OF TRUTH. FOLLOW IT.**
