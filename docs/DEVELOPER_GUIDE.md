# Developer Guide - THI Knowledge Common

**Version**: 1.0  
**Last Updated**: November 24, 2025  
**For**: New and existing developers

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Key Concepts](#key-concepts)
4. [Development Workflow](#development-workflow)
5. [Common Tasks](#common-tasks)
6. [Debugging Guide](#debugging-guide)
7. [Testing Guide](#testing-guide)
8. [Performance Tips](#performance-tips)
9. [FAQs](#faqs)

---

## Quick Start

### Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher
- Git

### Setup

```bash
# 1. Clone repository
git clone https://github.com/Ashwin-Chhetri/THI-Knowledge-Common.git
cd THI-Knowledge-Common

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Open browser
# Navigate to http://localhost:5173
```

### First Contribution Checklist

- [ ] Read this guide
- [ ] Review [ARCHITECTURE.md](./ARCHITECTURE.md)
- [ ] Review [REDUX_PATTERNS.md](./REDUX_PATTERNS.md)
- [ ] Run app locally and explore features
- [ ] Read existing code in feature you'll work on
- [ ] Create feature branch: `git checkout -b feature/your-feature-name`

---

## Project Structure

### Directory Layout

```
src/
├── app/                    # Application core
│   ├── store.js           # Redux store configuration
│   ├── hooks.js           # Typed Redux hooks
│   └── providers/         # Context providers
│
├── features/              # Feature modules (feature-first architecture)
│   ├── species/          # Species search & visualization
│   │   ├── store/        # Redux (slice, selectors, sagas)
│   │   ├── hooks/        # React hooks
│   │   ├── components/   # UI components
│   │   └── styles/       # Feature-specific styles
│   │
│   ├── region/           # Region selection & management
│   ├── ecosystem/        # Ecosystem data
│   ├── map/             # Map rendering
│   └── ...              # Other features
│
├── services/             # Business logic & API clients
│   ├── region/          # Region services
│   ├── gbif/            # GBIF API client
│   └── ...
│
├── infrastructure/       # Infrastructure layer
│   └── cache/           # Caching (IndexedDB)
│
├── shared/              # Shared resources
│   ├── components/      # Reusable UI components
│   └── utils/          # Utility functions
│
├── store/               # Global Redux
│   ├── slices/         # Global slices
│   └── sagas/          # Root sagas
│
├── types/               # Type definitions
│   └── regionLoadState.types.js
│
└── styles/              # Global styles
```

### Feature Module Structure

Each feature follows this pattern:

```
features/species/
├── index.js              # Public exports
├── SpeciesView.jsx       # Main component
├── hooks/
│   ├── useGBIFLayers.js
│   └── useSpeciesData.js
├── components/
│   ├── SpeciesPanel.jsx
│   └── SpeciesSearch.jsx
├── store/
│   ├── speciesSlice.js   # Redux state
│   ├── speciesSelectors.js # Memoized selectors
│   └── speciesSagas.js   # Async operations
└── styles/
    └── SpeciesPanel.module.css
```

---

## Key Concepts

### 1. State Machine Pattern

**Always check state before operations**:

```javascript
import { REGION_LOAD_STATE } from '@types/regionLoadState.types';
import { selectRegionLoadState } from '@features/region/store/regionSelectors';

function MyComponent() {
  const loadState = useSelector(selectRegionLoadState);
  
  // Check explicit state
  if (loadState === REGION_LOAD_STATE.LOADING_GEOMETRY) {
    return <Loading />;
  }
  
  if (loadState === REGION_LOAD_STATE.READY) {
    return <Map />; // Geometry guaranteed to exist
  }
  
  return <Welcome />;
}
```

**States**:
- `IDLE` - No region selected
- `LOADING_BOUNDS` - Fetching metadata
- `LOADING_GEOMETRY` - Fetching full geometry (300-2000ms)
- `READY` - Geometry loaded and ready
- `ERROR` - Load failed

### 2. Memoized Selectors

**Always use selectors, never direct state access**:

```javascript
// ❌ WRONG
const region = useSelector(state => state.region.selectedRegion);

// ✅ CORRECT
import { selectRegionUIData } from '@features/region/store/regionSelectors';
const { regionName, isReady } = useSelector(selectRegionUIData);
```

**Why?**
- Prevents infinite render loops
- Better performance (memoization)
- Stable references for useEffect

### 3. Saga Patterns

**Use race() for cancellation**:

```javascript
function* handleLoad() {
  const { data, cancelled } = yield race({
    data: call(fetchData),
    cancelled: take('CANCEL_ACTION')
  });
  
  if (cancelled) return; // Don't apply stale data
  
  yield put(setData(data));
}
```

### 4. Version Tokens

**For long-running async operations**:

```javascript
function* handleUpdate() {
  // 1. Start operation
  const operationId = `update-${Date.now()}`;
  yield put(startGeometryOperation({ operationId, ... }));
  
  // 2. Get version
  const expectedVersion = yield select(selectGeometryVersion);
  
  // 3. Do async work
  const result = yield call(fetchData);
  
  // 4. Validate not stale
  const { valid } = yield put(completeGeometryOperation({ 
    operationId, 
    expectedVersion 
  }));
  
  // 5. Apply only if valid
  if (valid) {
    yield put(setData(result));
  }
}
```

---

## Development Workflow

### Step-by-Step Process

#### 1. Pick a Task

Check the issue tracker or project board for assigned tasks.

#### 2. Create Feature Branch

```bash
git checkout -b feature/add-species-filter
```

**Branch Naming**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates

#### 3. Implement Changes

**a. State Changes (Redux)**

If adding/modifying state:

```javascript
// 1. Update slice
// src/features/species/store/speciesSlice.js
const speciesSlice = createSlice({
  name: 'species',
  initialState: {
    filters: {},
    results: []
  },
  reducers: {
    setFilter: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    }
  }
});

// 2. Create selector
// src/features/species/store/speciesSelectors.js
export const selectActiveFilters = state => state.species.filters;

// 3. Create saga (if async)
// src/features/species/store/speciesSagas.js
function* handleFilterChange(action) {
  // Async logic
}
```

**b. UI Components**

```javascript
// src/features/species/components/FilterPanel.jsx
import { useSelector, useDispatch } from 'react-redux';
import { selectActiveFilters } from '../store/speciesSelectors';
import { setFilter } from '../store/speciesSlice';

function FilterPanel() {
  const dispatch = useDispatch();
  const filters = useSelector(selectActiveFilters);
  
  const handleChange = (key, value) => {
    dispatch(setFilter({ [key]: value }));
  };
  
  return (
    <div>
      {/* Filter UI */}
    </div>
  );
}
```

#### 4. Test Changes

```bash
# Run tests
npm test

# Manual testing in browser
npm run dev
# Test your feature thoroughly
```

#### 5. Commit Changes

```bash
git add .
git commit -m "feat: add species filter panel

- Add filter state to speciesSlice
- Create FilterPanel component
- Add filter selectors
- Update SpeciesView to include FilterPanel"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `docs` - Documentation
- `test` - Tests
- `style` - Formatting
- `perf` - Performance improvement

#### 6. Push and Create PR

```bash
git push origin feature/add-species-filter
```

Then create pull request on GitHub.

---

## Common Tasks

### Task 1: Add New Redux State

**Example**: Add `selectedTaxon` to species state

```javascript
// 1. Update slice
const speciesSlice = createSlice({
  name: 'species',
  initialState: {
    selectedTaxon: null, // Add field
    // ... existing fields
  },
  reducers: {
    // Add action
    setSelectedTaxon: (state, action) => {
      state.selectedTaxon = action.payload;
    }
  }
});

// 2. Export action
export const { setSelectedTaxon } = speciesSlice.actions;

// 3. Create selector
export const selectSelectedTaxon = state => state.species.selectedTaxon;

// 4. Use in component
function SpeciesPanel() {
  const dispatch = useDispatch();
  const selectedTaxon = useSelector(selectSelectedTaxon);
  
  const handleSelect = (taxon) => {
    dispatch(setSelectedTaxon(taxon));
  };
  
  return <div>{selectedTaxon?.scientificName}</div>;
}
```

### Task 2: Add Async Operation (Saga)

**Example**: Fetch species details

```javascript
// 1. Create saga
// src/features/species/store/speciesSagas.js

function* handleFetchSpeciesDetails(action) {
  const { taxonKey } = action.payload;
  
  try {
    // Set loading
    yield put(setSpeciesLoading(true));
    
    // Fetch data
    const response = yield call(gbifAPI.fetchSpecies, taxonKey);
    
    // Update state
    yield put(setSpeciesDetails(response.data));
    
  } catch (error) {
    yield put(setSpeciesError(error.message));
  } finally {
    yield put(setSpeciesLoading(false));
  }
}

// 2. Watch for action
function* watchSpecies() {
  yield takeEvery('species/fetchSpeciesDetails', handleFetchSpeciesDetails);
}

// 3. Dispatch from component
function SpeciesDetails({ taxonKey }) {
  const dispatch = useDispatch();
  
  useEffect(() => {
    dispatch({ type: 'species/fetchSpeciesDetails', payload: { taxonKey } });
  }, [taxonKey, dispatch]);
  
  return <div>...</div>;
}
```

### Task 3: Add New Component

```javascript
// 1. Create component file
// src/features/species/components/TaxonCard.jsx

import React from 'react';
import PropTypes from 'prop-types';
import styles from './TaxonCard.module.css';

function TaxonCard({ taxon, onSelect }) {
  return (
    <div className={styles.card} onClick={() => onSelect(taxon)}>
      <h3>{taxon.scientificName}</h3>
      <p>{taxon.commonName}</p>
    </div>
  );
}

TaxonCard.propTypes = {
  taxon: PropTypes.shape({
    scientificName: PropTypes.string.isRequired,
    commonName: PropTypes.string
  }).isRequired,
  onSelect: PropTypes.func.isRequired
};

export default TaxonCard;

// 2. Create styles
// src/features/species/components/TaxonCard.module.css

.card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.card:hover {
  background: #f5f5f5;
}

// 3. Use in parent
import TaxonCard from './components/TaxonCard';

function TaxonList({ taxa }) {
  const dispatch = useDispatch();
  
  const handleSelect = (taxon) => {
    dispatch(setSelectedTaxon(taxon));
  };
  
  return (
    <div>
      {taxa.map(taxon => (
        <TaxonCard 
          key={taxon.key}
          taxon={taxon}
          onSelect={handleSelect}
        />
      ))}
    </div>
  );
}
```

### Task 4: Add Caching

**Example**: Cache species search results

```javascript
// Use existing GeometryCacheService pattern

import { geometryCacheService } from '@infrastructure/cache/GeometryCacheService';

function* handleSearchSpecies(action) {
  const { query } = action.payload;
  const cacheKey = `species-search-${query}`;
  
  try {
    // 1. Check cache
    const cached = yield call([geometryCacheService, 'get'], cacheKey);
    if (cached) {
      console.log('🎯 Cache hit!');
      yield put(setSearchResults(cached));
      return;
    }
    
    // 2. Fetch from API
    console.log('❌ Cache miss - fetching from API');
    const results = yield call(gbifAPI.search, query);
    
    // 3. Cache results
    yield call([geometryCacheService, 'set'], cacheKey, results);
    
    // 4. Update state
    yield put(setSearchResults(results));
    
  } catch (error) {
    yield put(setSearchError(error.message));
  }
}
```

---

## Debugging Guide

### Redux DevTools

**Installation**:
```bash
# Browser extension
# Chrome: Redux DevTools
# Firefox: Redux DevTools
```

**Usage**:
1. Open DevTools (F12)
2. Click "Redux" tab
3. See all state changes in real-time
4. Time-travel debugging (go back/forward in state history)

**Useful Features**:
- **Action Log**: See every dispatched action
- **State Diff**: See what changed
- **Time Travel**: Jump to any previous state
- **Trace**: See which component dispatched action

### Console Logging

**Structured Logging**:

```javascript
// ✅ GOOD: Structured with context
console.log('[RegionSaga] Loading geometry for:', {
  regionName,
  regionType,
  loadState: REGION_LOAD_STATE.LOADING_GEOMETRY
});

// ❌ BAD: Unstructured
console.log('loading', regionName);
```

**Log Levels**:
```javascript
console.log('[Component] Info message');      // General info
console.warn('[Saga] ⚠️ Warning message');    // Warnings
console.error('[Service] ❌ Error:', error);  // Errors
```

### Common Issues

#### Issue 1: Infinite Render Loop

**Symptoms**: Component re-renders 50+ times, browser freezes

**Cause**: Unstable useEffect dependency

**Solution**:
```javascript
// ❌ WRONG
const region = useSelector(state => state.region.selectedRegion);
useEffect(() => { /* ... */ }, [region]); // Object reference changes!

// ✅ CORRECT
const { regionName, isReady } = useSelector(selectRegionUIData);
useEffect(() => { /* ... */ }, [regionName, isReady]); // Primitives
```

#### Issue 2: Null Reference Error

**Symptoms**: `Cannot read property 'X' of null`

**Cause**: Accessing data before state machine is ready

**Solution**:
```javascript
// ❌ WRONG
const geometry = useSelector(state => state.region.selectedRegion.geometry);
return <Map geometry={geometry} />; // Crashes if null!

// ✅ CORRECT
const isReady = useSelector(selectIsGeometryReady);
const geometry = useSelector(selectSelectedRegionGeometry);

if (!isReady) return <Loading />;
return <Map geometry={geometry} />;
```

#### Issue 3: Stale Data Displayed

**Symptoms**: UI shows old data after user action

**Cause**: Race condition - no saga cancellation

**Solution**:
```javascript
// ❌ WRONG
function* handleLoad() {
  const data = yield call(fetchData);
  yield put(setData(data)); // Might be stale!
}

// ✅ CORRECT
function* handleLoad() {
  const { data, cancelled } = yield race({
    data: call(fetchData),
    cancelled: take('CANCEL_ACTION')
  });
  
  if (cancelled) return;
  yield put(setData(data));
}
```

---

## Testing Guide

### Unit Tests

**Location**: Place tests next to source files in `__tests__/` folder

```
src/features/species/
├── hooks/
│   ├── useSpeciesData.js
│   └── __tests__/
│       └── useSpeciesData.test.js
```

**Example Test**:

```javascript
// src/features/species/store/__tests__/speciesSlice.test.js

import { describe, it, expect } from 'vitest';
import speciesReducer, { setSelectedTaxon } from '../speciesSlice';

describe('speciesSlice', () => {
  it('should set selected taxon', () => {
    const initialState = { selectedTaxon: null };
    const taxon = { key: 123, scientificName: 'Panthera tigris' };
    
    const nextState = speciesReducer(
      initialState,
      setSelectedTaxon(taxon)
    );
    
    expect(nextState.selectedTaxon).toEqual(taxon);
  });
});
```

### Integration Tests

**Test full user flows**:

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '@app/store';
import SpeciesPanel from '../SpeciesPanel';

describe('SpeciesPanel', () => {
  it('should allow species search and selection', async () => {
    render(
      <Provider store={store}>
        <SpeciesPanel />
      </Provider>
    );
    
    // Type in search
    const searchInput = screen.getByPlaceholderText('Search species...');
    fireEvent.change(searchInput, { target: { value: 'tiger' } });
    
    // Wait for results
    const result = await screen.findByText('Panthera tigris');
    
    // Click result
    fireEvent.click(result);
    
    // Verify selection
    expect(screen.getByText('Selected: Panthera tigris')).toBeInTheDocument();
  });
});
```

### Running Tests

```bash
# Run all tests
npm test

# Watch mode (re-run on changes)
npm test -- --watch

# Coverage report
npm test -- --coverage

# Specific test file
npm test speciesSlice.test
```

---

## Performance Tips

### 1. Use Memoized Selectors

```javascript
// ✅ GOOD: Memoized with createSelector
export const selectFilteredSpecies = createSelector(
  [selectAllSpecies, selectFilters],
  (species, filters) => {
    return species.filter(s => matchesFilters(s, filters));
  }
);
```

### 2. Memoize Components

```javascript
// ✅ GOOD: Only re-renders when props change
export default React.memo(SpeciesCard, (prevProps, nextProps) => {
  return prevProps.taxon.key === nextProps.taxon.key;
});
```

### 3. Use useCallback

```javascript
// ✅ GOOD: Stable function reference
const handleClick = useCallback(() => {
  dispatch(setSelectedTaxon(taxon));
}, [dispatch, taxon]);
```

### 4. Batch Redux Updates

```javascript
// ❌ BAD: Multiple dispatches
dispatch(setLoading(true));
dispatch(setData(data));
dispatch(setLoading(false));

// ✅ GOOD: Batch in saga
function* handleLoad() {
  yield put(setLoading(true));
  const data = yield call(fetchData);
  
  // Batch updates
  yield put({ 
    type: 'BATCH_UPDATE',
    payload: { 
      loading: false,
      data 
    }
  });
}
```

### 5. Lazy Load Components

```javascript
// ✅ GOOD: Lazy load heavy components
const HeavyMapComponent = React.lazy(() => import('./HeavyMapComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyMapComponent />
    </Suspense>
  );
}
```

---

## FAQs

### Q: When should I create a new Redux slice?

**A**: Create a new slice when:
- Feature is independent
- State doesn't fit in existing slices
- Feature has unique lifecycle

**Example**: Species, Region, Ecosystem each have their own slices.

### Q: Should I use local state or Redux?

**A**: Use Redux when:
- Multiple components need the data
- Data survives component unmount
- Need to persist across page refresh (with persistence middleware)

Use local state when:
- Only one component needs it
- UI-only state (dropdowns, modals)
- Temporary data

### Q: How do I add a new API endpoint?

```javascript
// 1. Add to service
// src/services/gbif/gbifAPI.js

export const gbifAPI = {
  fetchSpecies: async (taxonKey) => {
    const response = await axios.get(`${GBIF_BASE_URL}/species/${taxonKey}`);
    return response.data;
  }
};

// 2. Use in saga
function* handleFetchSpecies(action) {
  const data = yield call(gbifAPI.fetchSpecies, action.payload.taxonKey);
  yield put(setSpeciesDetails(data));
}
```

### Q: How do I debug Redux state?

**A**: Use Redux DevTools:
1. Open DevTools → Redux tab
2. See all actions and state changes
3. Use time-travel to go back/forward
4. Inspect state tree

Also add console.log in reducers:
```javascript
reducers: {
  setSelectedTaxon: (state, action) => {
    console.log('[Slice] Setting taxon:', action.payload);
    state.selectedTaxon = action.payload;
  }
}
```

### Q: How do I fix "Cannot read property of undefined"?

**A**: Add defensive checks:
```javascript
// ❌ WRONG
const name = species.scientificName;

// ✅ CORRECT
const name = species?.scientificName || 'Unknown';
```

Or check state machine:
```javascript
if (isReady && species) {
  const name = species.scientificName;
}
```

### Q: Where should business logic go?

**A**: 
- **Simple logic**: Redux slice reducers
- **Async logic**: Redux Sagas
- **Complex logic**: Service layer (src/services/)
- **UI logic**: React components

### Q: How do I handle errors?

```javascript
function* handleFetch() {
  try {
    const data = yield call(fetchData);
    yield put(setData(data));
  } catch (error) {
    console.error('[Saga] Error:', error);
    yield put(setError(error.message));
  }
}
```

---

## Summary

**Key Takeaways**:
1. ✅ Always use memoized selectors
2. ✅ Check state machine before operations
3. ✅ Use race() for saga cancellation
4. ✅ Add version tokens for long operations
5. ✅ Use Redux DevTools for debugging
6. ✅ Write tests for new features
7. ✅ Follow coding standards

**Essential Reading**:
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [REDUX_PATTERNS.md](./REDUX_PATTERNS.md) - Redux patterns
- [DEVELOPMENT_GUIDELINES.md](./DEVELOPMENT_GUIDELINES.md) - Coding standards

**Get Help**:
- Check existing code examples
- Review phase documentation (PHASE_*.md)
- Ask team members
- Check GitHub issues

---

**Happy Coding! 🚀**

---

**Document Version**: 1.0  
**Last Updated**: November 24, 2025  
**Maintained By**: THI Knowledge Common Team
