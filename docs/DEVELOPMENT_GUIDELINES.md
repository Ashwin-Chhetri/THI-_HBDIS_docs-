# Development Guidelines for AI Assistants

**Project**: THI Knowledge Common  
**Version**: 1.0  
**Last Updated**: November 3, 2025  
**Target Audience**: AI Coding Assistants (Copilot, Claude, GPT-4, etc.)

---

## Table of Contents

1. [Purpose & Scope](#purpose--scope)
2. [Mandatory Architecture Adherence](#mandatory-architecture-adherence)
3. [Code Generation Rules](#code-generation-rules)
4. [Redux State Management Guidelines](#redux-state-management-guidelines)
5. [Layer Management Guidelines](#layer-management-guidelines)
6. [Component Development Guidelines](#component-development-guidelines)
7. [Data Service Guidelines](#data-service-guidelines)
8. [File Organization](#file-organization)
9. [Testing Requirements](#testing-requirements)
10. [Common Patterns & Anti-Patterns](#common-patterns--anti-patterns)
11. [Review Checklist](#review-checklist)

---

## Purpose & Scope

This document provides **strict guidelines** for AI coding assistants working on the THI Knowledge Common project. All generated code MUST adhere to these guidelines to maintain architectural consistency and code quality.

### When to Use This Document

- ✅ Creating new features
- ✅ Modifying existing features
- ✅ Refactoring code
- ✅ Adding new layers or data sources
- ✅ Implementing UI components
- ✅ Writing tests

### Core Principle

> **Every code change must maintain the established architecture.** 
> If the architecture doesn't support a use case, propose architectural changes rather than working around them.

---

## Mandatory Architecture Adherence

### 1. Redux as Single Source of Truth

**RULE**: All layer state MUST be stored in Redux, never in component state.

```javascript
// ✅ CORRECT: Layer state in Redux
const layers = useSelector(state => state.layers.byId);
const dispatch = useDispatch();

function addSpeciesLayer() {
  dispatch(addLayer({
    id: 'gbif-species',
    type: 'SPECIES',
    category: 'BIODIVERSITY'
  }));
}

// ❌ WRONG: Layer state in component
const [layers, setLayers] = useState({});

function addSpeciesLayer() {
  setLayers({
    ...layers,
    'gbif-species': { /* ... */ }
  });
}
```

### 2. Layer Dependency Graph

**RULE**: Always update the dependency graph when creating layers with dependencies.

```javascript
// ✅ CORRECT: Specify dependencies
dispatch(addLayer({
  id: 'gbif-species',
  type: 'SPECIES',
  category: 'BIODIVERSITY',
  dependencies: ['region-sikkim'], // Explicit dependency
  filters: {
    region: 'region-sikkim'
  }
}));

// ❌ WRONG: Missing dependency declaration
dispatch(addLayer({
  id: 'gbif-species',
  type: 'SPECIES',
  category: 'BIODIVERSITY',
  // Missing dependencies array
  filters: {
    region: 'region-sikkim' // Filter without dependency tracking
  }
}));
```

### 3. EnhancedLayerManager for MapLibre Operations

**RULE**: NEVER call MapLibre API directly from components. Always use EnhancedLayerManager.

```javascript
// ✅ CORRECT: Use EnhancedLayerManager
const layerManager = useContext(LayerManagerContext);

function addLayer() {
  layerManager.addLayer({
    id: 'my-layer',
    type: 'raster',
    source: 'my-source'
  }, 'BIODIVERSITY');
}

// ❌ WRONG: Direct MapLibre API call
function addLayer() {
  map.addLayer({
    id: 'my-layer',
    type: 'raster',
    source: 'my-source'
  });
}
```

### 4. Layer Categories

**RULE**: Every layer MUST be assigned to a category.

```javascript
// ✅ CORRECT: Category specified
dispatch(addLayer({
  id: 'boundary-layer',
  category: 'BOUNDARIES', // Required
  type: 'REGION'
}));

// ❌ WRONG: No category
dispatch(addLayer({
  id: 'boundary-layer',
  type: 'REGION'
  // Missing category
}));
```

**Valid Categories**:
- `BASE` - Base maps (satellite, terrain)
- `BOUNDARIES` - Administrative boundaries
- `BIODIVERSITY` - Species data
- `ANALYSIS` - Computed layers
- `OVERLAYS` - UI elements
- `CONTROLS` - Map controls

### 5. Async Operations with Redux Saga

**RULE**: Complex async operations MUST use Redux Saga, not component useEffect.

```javascript
// ✅ CORRECT: Redux Saga for async flow
// In saga file
export function* handleRegionSelection(action) {
  const { regionId, geometry } = action.payload;
  
  yield put(addLayer({
    id: regionId,
    type: 'REGION',
    geometry
  }));

  yield take('layers/addLayer/fulfilled');

  const speciesData = yield call(gbifService.getOccurrences, { geometry });
  
  yield put(addLayer({
    id: 'species',
    data: speciesData,
    dependencies: [regionId]
  }));
}

// ❌ WRONG: Complex async in component
function RegionSelector() {
  useEffect(() => {
    async function loadRegionAndSpecies() {
      await dispatch(addLayer({ id: 'region' }));
      const species = await fetchSpecies();
      await dispatch(addLayer({ id: 'species', data: species }));
    }
    loadRegionAndSpecies();
  }, [region]);
}
```

---

## Code Generation Rules

### File Creation

**RULE**: When creating new files, follow the project structure exactly.

```
src/
├── features/          # Feature modules (species, ecosystem, etc.)
│   └── [feature]/
│       ├── index.js
│       ├── [Feature]View.jsx
│       ├── components/
│       ├── hooks/
│       ├── store/     # Redux slice, sagas, selectors
│       ├── services/  # API calls
│       └── types/     # TypeScript definitions
├── services/          # Shared services
│   ├── map/           # Map-related services
│   ├── data/          # Data source adapters
│   └── cache/         # Caching utilities
├── store/             # Redux store configuration
│   ├── slices/
│   ├── sagas/
│   └── middleware/
└── shared/            # Shared components and utilities
    ├── components/
    └── utils/
```

### Naming Conventions

```javascript
// ✅ CORRECT naming
const layersSlice = createSlice({ name: 'layers' });  // camelCase for variables
function LayerPanel() { }                              // PascalCase for components
export const LAYER_CATEGORIES = { };                   // UPPER_SNAKE_CASE for constants
function handleLayerAdd() { }                          // camelCase, verb prefix for functions

// ❌ WRONG naming
const LayersSlice = createSlice({ name: 'layers' });  // Wrong: PascalCase for variable
function layerPanel() { }                              // Wrong: camelCase for component
export const layerCategories = { };                    // Wrong: camelCase for constant
function LayerAdd() { }                                // Wrong: PascalCase for function
```

### Import Order

**RULE**: Organize imports in the following order:

```javascript
// 1. React and external libraries
import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { createSelector } from '@reduxjs/toolkit';

// 2. Internal services and utilities
import { gbifService } from '@/services/gbif/gbifService';
import { LayerDependencyResolver } from '@/services/layer/layerDependencyResolver';

// 3. Redux actions and selectors
import { addLayer, removeLayer } from '@/store/slices/layersSlice';
import { selectLayersByCategory } from '@/store/selectors/layersSelectors';

// 4. Components
import { LayerPanel } from './components/LayerPanel';
import { SpeciesSearch } from './components/SpeciesSearch';

// 5. Types
import type { Layer, LayerCategory } from '@/types';

// 6. Styles
import styles from './SpeciesView.module.css';
```

---

## Redux State Management Guidelines

### Creating a Redux Slice

**TEMPLATE**: Use this exact structure for new slices:

```javascript
// src/store/slices/[feature]Slice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunks
export const fetch[Feature]Data = createAsyncThunk(
  '[feature]/fetchData',
  async (params, { dispatch, getState }) => {
    // Async logic here
    const data = await api.fetchData(params);
    return data;
  }
);

// Slice
const [feature]Slice = createSlice({
  name: '[feature]',
  initialState: {
    // Define initial state
    data: null,
    status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null
  },
  reducers: {
    // Synchronous actions
    set[Feature]Data: (state, action) => {
      state.data = action.payload;
    },
    reset[Feature]: (state) => {
      state.data = null;
      state.status = 'idle';
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    // Async action handlers
    builder
      .addCase(fetch[Feature]Data.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetch[Feature]Data.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.data = action.payload;
      })
      .addCase(fetch[Feature]Data.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  }
});

export const { set[Feature]Data, reset[Feature] } = [feature]Slice.actions;
export default [feature]Slice.reducer;
```

### Creating Selectors

**RULE**: Use memoized selectors for derived state.

```javascript
// src/store/selectors/[feature]Selectors.js
import { createSelector } from '@reduxjs/toolkit';

// Basic selector
export const select[Feature]Data = state => state.[feature].data;
export const select[Feature]Status = state => state.[feature].status;

// Memoized selector
export const select[Feature]Computed = createSelector(
  [select[Feature]Data, (state, arg) => arg],
  (data, arg) => {
    // Expensive computation here
    return data?.filter(item => item.type === arg);
  }
);

// ✅ CORRECT: Use in component
const filteredData = useSelector(state => 
  select[Feature]Computed(state, 'SPECIES')
);

// ❌ WRONG: Inline selector (no memoization)
const filteredData = useSelector(state => 
  state.[feature].data?.filter(item => item.type === 'SPECIES')
);
```

### Creating Sagas

**TEMPLATE**: Use this structure for sagas:

```javascript
// src/store/sagas/[feature]Sagas.js
import { call, put, select, take, takeLatest, all } from 'redux-saga/effects';
import { [feature]Actions } from '@/store/slices/[feature]Slice';
import { [feature]Service } from '@/services/[feature]/[feature]Service';

// Worker saga
export function* handle[Action](action) {
  try {
    // 1. Show loading state
    yield put([feature]Actions.setLoading(true));

    // 2. Perform async operation
    const data = yield call([feature]Service.fetchData, action.payload);

    // 3. Update state
    yield put([feature]Actions.setData(data));

    // 4. Handle side effects
    yield put(showNotification({ message: 'Success!' }));

  } catch (error) {
    // Error handling
    yield put([feature]Actions.setError(error.message));
    yield put(showNotification({ 
      type: 'error', 
      message: error.message 
    }));
  } finally {
    // Cleanup
    yield put([feature]Actions.setLoading(false));
  }
}

// Watcher saga
export function* watch[Feature]Actions() {
  yield takeLatest('[feature]/[action]', handle[Action]);
}

// Root saga
export function* [feature]Saga() {
  yield all([
    watch[Feature]Actions(),
    // Add more watchers here
  ]);
}
```

### Middleware Creation

**RULE**: Middleware should be pure and handle cross-cutting concerns.

```javascript
// src/store/middleware/[feature]Middleware.js

export const [feature]Middleware = ({ getState, dispatch }) => next => action => {
  // 1. Execute action first
  const result = next(action);

  // 2. Handle side effects based on action type
  if (action.type === 'layers/addLayer') {
    const state = getState();
    
    // Perform side effects
    // Example: Log analytics
    analytics.track('layer_added', {
      layerId: action.payload.id,
      category: action.payload.category
    });
  }

  // 3. Return result
  return result;
};
```

---

## Layer Management Guidelines

### Adding a Layer

**RULE**: Always follow this complete flow:

```javascript
// Step 1: Define layer configuration
const layerConfig = {
  id: 'unique-layer-id',
  type: 'SPECIES',              // Layer type
  category: 'BIODIVERSITY',      // Required: One of LAYER_CATEGORIES
  source: 'gbif-api',            // Data source identifier
  dependencies: [],              // Array of layer IDs this depends on
  dependents: [],                // Auto-populated by middleware
  filters: {                     // Active filters
    region: 'sikkim',
    timeRange: { start: '2020', end: '2024' }
  },
  metadata: {                    // Additional metadata
    taxonKey: 5218933,
    scientificName: 'Ailurus fulgens'
  },
  status: 'pending'              // 'pending' | 'loading' | 'active' | 'error'
};

// Step 2: Dispatch action
dispatch(addLayer(layerConfig));

// Step 3: Middleware automatically handles:
// - Dependency graph update
// - Dependent layer refresh
// - Performance tracking
```

### Removing a Layer

**RULE**: Check for dependents before removal:

```javascript
// ✅ CORRECT: Check dependents
function removeLayerSafely(layerId) {
  const dependents = useSelector(state => 
    selectDependentLayers(state, layerId)
  );

  if (dependents.length > 0) {
    // Warn user
    showConfirmation({
      message: `Layer has ${dependents.length} dependent layers. Remove all?`,
      onConfirm: () => {
        // Remove dependents first
        dependents.forEach(depId => dispatch(removeLayer({ layerId: depId })));
        // Then remove main layer
        dispatch(removeLayer({ layerId }));
      }
    });
  } else {
    // Safe to remove
    dispatch(removeLayer({ layerId }));
  }
}

// ❌ WRONG: Direct removal without checking
function removeLayer(layerId) {
  dispatch(removeLayer({ layerId })); // Might break dependent layers!
}
```

### Updating Layer Filters

**RULE**: Filter updates should trigger dependent layer refresh:

```javascript
// ✅ CORRECT: Update filter with dependency handling
dispatch(updateLayerFilters({
  layerId: 'region-sikkim',
  filters: {
    timeRange: { start: '2021', end: '2024' }
  }
}));
// Middleware automatically refreshes dependent species layers

// ❌ WRONG: Direct state mutation
const layer = state.layers.byId['region-sikkim'];
layer.filters.timeRange = { start: '2021', end: '2024' }; // Mutation!
```

### Layer Lifecycle

```javascript
// Complete layer lifecycle example
export function* layerLifecycleSaga(action) {
  const { layerId, config } = action.payload;

  try {
    // 1. PENDING state
    yield put(updateLayerStatus({ layerId, status: 'pending' }));

    // 2. Add to dependency graph
    yield put(updateDependencyGraph({ layerId, dependencies: config.dependencies }));

    // 3. LOADING state
    yield put(updateLayerStatus({ layerId, status: 'loading' }));

    // 4. Fetch data
    const data = yield call(dataService.fetch, config);

    // 5. Store data
    yield call(cacheService.store, layerId, data);

    // 6. Add to map via LayerManager
    const layerManager = yield select(selectLayerManager);
    yield call([layerManager, 'addLayer'], {
      id: layerId,
      ...config,
      data
    }, config.category);

    // 7. ACTIVE state
    yield put(updateLayerStatus({ layerId, status: 'active' }));

    // 8. Trigger dependent layer refresh
    const dependents = yield select(state => 
      selectDependentLayers(state, layerId)
    );
    for (const depId of dependents) {
      yield put(refreshLayer({ layerId: depId }));
    }

  } catch (error) {
    // ERROR state
    yield put(updateLayerStatus({ layerId, status: 'error' }));
    yield put(setLayerError({ layerId, error: error.message }));
  }
}
```

---

## Component Development Guidelines

### Component Structure

**TEMPLATE**: Use this structure for all components:

```javascript
// src/features/[feature]/components/[Component].jsx
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import PropTypes from 'prop-types';

// Redux actions and selectors
import { someAction } from '@/store/slices/someSlice';
import { selectSomeData } from '@/store/selectors/someSelectors';

// Child components
import { ChildComponent } from './ChildComponent';

// Styles
import styles from './[Component].module.css';

/**
 * [Component] - Brief description
 * 
 * @param {Object} props
 * @param {string} props.id - Component ID
 * @param {Function} props.onAction - Callback for action
 */
export function [Component]({ id, onAction }) {
  // 1. Hooks (in this order)
  const dispatch = useDispatch();
  
  // Redux state
  const data = useSelector(selectSomeData);
  
  // Local state
  const [localState, setLocalState] = useState(null);
  
  // Refs (if needed)
  const ref = useRef(null);
  
  // Memoized values
  const computedValue = useMemo(() => {
    return expensiveComputation(data);
  }, [data]);
  
  // Callbacks
  const handleClick = useCallback(() => {
    dispatch(someAction());
    onAction?.();
  }, [dispatch, onAction]);

  // 2. Effects
  useEffect(() => {
    // Effect logic
    return () => {
      // Cleanup
    };
  }, []);

  // 3. Render
  return (
    <div className={styles.container}>
      <h2>{computedValue}</h2>
      <button onClick={handleClick}>Action</button>
      <ChildComponent data={data} />
    </div>
  );
}

// 4. PropTypes
[Component].propTypes = {
  id: PropTypes.string.isRequired,
  onAction: PropTypes.func
};

// 5. Default props (if needed)
[Component].defaultProps = {
  onAction: () => {}
};
```

### Hooks Best Practices

**RULE**: Create custom hooks for reusable logic:

```javascript
// src/features/[feature]/hooks/use[Feature].js

import { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

/**
 * Custom hook for [feature] functionality
 */
export function use[Feature](params) {
  const dispatch = useDispatch();
  const state = useSelector(selectState);
  
  const [localState, setLocalState] = useState(null);

  useEffect(() => {
    // Hook logic
  }, [params]);

  return {
    data: state.data,
    loading: state.loading,
    error: state.error,
    actions: {
      doSomething: () => dispatch(someAction())
    }
  };
}

// ✅ CORRECT: Use in component
function MyComponent() {
  const { data, loading, actions } = use[Feature](params);
  
  if (loading) return <Spinner />;
  
  return <div onClick={actions.doSomething}>{data}</div>;
}

// ❌ WRONG: Duplicate logic in component
function MyComponent() {
  const dispatch = useDispatch();
  const data = useSelector(selectState);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // Duplicate logic that should be in hook
  }, []);
}
```

### Context Usage

**RULE**: Use Context for dependency injection, not for global state.

```javascript
// ✅ CORRECT: Context for LayerManager instance
export const LayerManagerContext = createContext(null);

export function LayerManagerProvider({ children, map, panelId }) {
  const layerManager = useMemo(() => 
    new EnhancedLayerManager(map, panelId),
    [map, panelId]
  );

  useEffect(() => {
    layerManager.initialize();
    return () => layerManager.cleanup();
  }, [layerManager]);

  return (
    <LayerManagerContext.Provider value={layerManager}>
      {children}
    </LayerManagerContext.Provider>
  );
}

// Use in component
function MyComponent() {
  const layerManager = useContext(LayerManagerContext);
  // ...
}

// ❌ WRONG: Context for state (use Redux instead)
export const LayersContext = createContext({ layers: {} });

function LayersProvider({ children }) {
  const [layers, setLayers] = useState({}); // Should be in Redux!
  return (
    <LayersContext.Provider value={{ layers, setLayers }}>
      {children}
    </LayersContext.Provider>
  );
}
```

---

## Data Service Guidelines

### Service Structure

**TEMPLATE**: Use this structure for all services:

```javascript
// src/services/[service]/[service]Service.js

class [Service]Service {
  constructor(config = {}) {
    this.baseURL = config.baseURL;
    this.cache = new Map();
    this.timeout = config.timeout || 5000;
  }

  /**
   * Fetch data with caching
   */
  async fetch(params) {
    // 1. Check cache
    const cacheKey = this.getCacheKey(params);
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // 2. Build request
    const url = this.buildURL(params);
    const options = this.buildRequestOptions(params);

    // 3. Fetch with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // 4. Transform to common format
      const transformed = this.transform(data);

      // 5. Cache result
      this.cache.set(cacheKey, transformed);

      return transformed;

    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error(`Request timeout after ${this.timeout}ms`);
      }
      throw error;
    } finally {
      clearTimeout(timeoutId);
    }
  }

  /**
   * Transform response to common format
   */
  transform(data) {
    return {
      type: 'FeatureCollection',
      features: data.results.map(item => ({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [item.lon, item.lat]
        },
        properties: { ...item }
      }))
    };
  }

  /**
   * Clear cache
   */
  clearCache() {
    this.cache.clear();
  }

  /**
   * Generate cache key from params
   */
  getCacheKey(params) {
    return JSON.stringify(params);
  }

  /**
   * Build URL from params
   */
  buildURL(params) {
    const queryString = new URLSearchParams(params).toString();
    return `${this.baseURL}?${queryString}`;
  }

  /**
   * Build request options
   */
  buildRequestOptions(params) {
    return {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    };
  }
}

// Export singleton instance
export const [service]Service = new [Service]Service({
  baseURL: process.env.VITE_[SERVICE]_API_URL
});
```

### Error Handling

**RULE**: Always handle errors consistently:

```javascript
// ✅ CORRECT: Comprehensive error handling
async function fetchData(params) {
  try {
    const data = await service.fetch(params);
    return { success: true, data };
  } catch (error) {
    // Log error
    console.error('[Service] Fetch failed:', error);

    // Transform to app error format
    const appError = {
      success: false,
      error: {
        message: error.message,
        code: error.code || 'UNKNOWN',
        timestamp: Date.now()
      }
    };

    // Dispatch error action
    dispatch(setError(appError));

    // Return error (don't throw)
    return appError;
  }
}

// ❌ WRONG: Unhandled errors
async function fetchData(params) {
  const data = await service.fetch(params); // Might throw!
  return data;
}
```

---

## File Organization

### Feature Module Structure

```
src/features/species/
├── index.js                    # Public exports only
├── SpeciesView.jsx             # Main view component
├── components/
│   ├── SpeciesPanel.jsx        # Main panel
│   ├── DataClassSelector.jsx  # Sub-components
│   ├── SpeciesSearch.jsx
│   └── LayerControls.jsx
├── hooks/
│   ├── useGBIFLayers.js        # Layer management hook
│   ├── useSpeciesData.js       # Data fetching hook
│   └── useSpeciesFilters.js    # Filter management hook
├── store/
│   ├── speciesSlice.js         # Redux slice
│   ├── speciesSagas.js         # Async operations
│   └── speciesSelectors.js     # Memoized selectors
├── services/
│   └── speciesService.js       # API integration
├── types/
│   └── species.types.js        # TypeScript definitions
└── styles/
    └── SpeciesView.module.css  # Component styles
```

### Shared Services Structure

```
src/services/
├── map/
│   ├── enhancedLayerManager.js      # Layer manager class
│   ├── layerRegistry.js             # Global registry
│   └── mapService.js                # Map utilities
├── data/
│   ├── dataSourceRegistry.js        # Multi-source coordinator
│   └── adapters/
│       ├── gbifAdapter.js           # GBIF integration
│       ├── localAdapter.js          # Local DB integration
│       └── userUploadAdapter.js     # User file handling
├── cache/
│   ├── indexedDBCache.js            # IndexedDB wrapper
│   └── memoryCache.js               # In-memory cache
└── layer/
    ├── layerDependencyResolver.js   # Dependency graph
    └── batchOperationQueue.js       # Batch processor
```

---

## Testing Requirements

### Unit Test Template

```javascript
// src/features/[feature]/__tests__/[feature].test.js

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';

import { use[Feature] } from '../hooks/use[Feature]';
import [feature]Reducer from '../store/[feature]Slice';

describe('[Feature] Hook', () => {
  let store;

  beforeEach(() => {
    // Create fresh store for each test
    store = configureStore({
      reducer: {
        [feature]: [feature]Reducer
      }
    });
  });

  afterEach(() => {
    // Cleanup
  });

  it('should initialize with default state', () => {
    const { result } = renderHook(() => use[Feature](), {
      wrapper: ({ children }) => (
        <Provider store={store}>{children}</Provider>
      )
    });

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
  });

  it('should fetch data successfully', async () => {
    const { result } = renderHook(() => use[Feature](), {
      wrapper: ({ children }) => (
        <Provider store={store}>{children}</Provider>
      )
    });

    await act(async () => {
      await result.current.actions.fetchData();
    });

    expect(result.current.data).not.toBeNull();
    expect(result.current.loading).toBe(false);
  });
});
```

### Integration Test Template

```javascript
// src/features/[feature]/__tests__/[feature].integration.test.js

import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { createTestStore } from '@/test/utils';

import { [Feature]View } from '../[Feature]View';

describe('[Feature] Integration', () => {
  it('should handle complete user flow', async () => {
    const store = createTestStore();

    render(
      <Provider store={store}>
        <[Feature]View />
      </Provider>
    );

    // 1. User interaction
    const button = screen.getByRole('button', { name: /add layer/i });
    fireEvent.click(button);

    // 2. Wait for async operation
    await waitFor(() => {
      expect(screen.getByText(/layer added/i)).toBeInTheDocument();
    });

    // 3. Verify state
    const state = store.getState();
    expect(state.layers.allIds).toHaveLength(1);
  });
});
```

---

## Common Patterns & Anti-Patterns

### Pattern: Dependency Management

```javascript
// ✅ CORRECT: Explicit dependency declaration
dispatch(addLayer({
  id: 'analysis-richness',
  type: 'ANALYSIS',
  dependencies: ['gbif-species', 'local-species'], // Clear dependencies
  compute: (deps) => {
    const gbifData = deps['gbif-species'];
    const localData = deps['local-species'];
    return calculateRichness(gbifData, localData);
  }
}));

// ❌ WRONG: Implicit dependencies
dispatch(addLayer({
  id: 'analysis-richness',
  type: 'ANALYSIS',
  compute: () => {
    // Accessing other layers without declaring dependency
    const gbifData = store.getState().layers.byId['gbif-species'];
    return calculateRichness(gbifData);
  }
}));
```

### Pattern: Async Data Fetching

```javascript
// ✅ CORRECT: Redux Saga for complex async
export function* fetchSpeciesDataSaga(action) {
  const { region, taxonKey } = action.payload;

  try {
    // Parallel fetching
    const [gbifData, localData] = yield all([
      call(gbifService.fetch, { region, taxonKey }),
      call(localService.fetch, { region, taxonKey })
    ]);

    // Merge results
    const merged = mergeData(gbifData, localData);

    yield put(setSpeciesData(merged));
  } catch (error) {
    yield put(setError(error.message));
  }
}

// ❌ WRONG: useEffect for complex async
function SpeciesPanel() {
  useEffect(() => {
    async function fetchData() {
      const gbif = await gbifService.fetch(params);
      const local = await localService.fetch(params);
      const merged = mergeData(gbif, local);
      dispatch(setSpeciesData(merged));
    }
    fetchData();
  }, [region, taxonKey]);
}
```

### Pattern: Memoization

```javascript
// ✅ CORRECT: Memoized selector
export const selectFilteredLayers = createSelector(
  [selectAllLayers, (state, filter) => filter],
  (layers, filter) => {
    // Expensive filtering only runs when inputs change
    return layers.filter(layer => layer.type === filter);
  }
);

// Use in component
const filteredLayers = useSelector(state => 
  selectFilteredLayers(state, 'SPECIES')
);

// ❌ WRONG: Inline selector (runs on every render)
const filteredLayers = useSelector(state => 
  Object.values(state.layers.byId).filter(l => l.type === 'SPECIES')
);
```

### Anti-Pattern: Direct State Mutation

```javascript
// ❌ WRONG: Mutating Redux state
function someReducer(state, action) {
  state.layers.byId[action.payload.id] = action.payload; // Mutation!
  return state;
}

// ✅ CORRECT: Immutable update (Redux Toolkit does this automatically)
const someSlice = createSlice({
  name: 'some',
  initialState: {},
  reducers: {
    addLayer: (state, action) => {
      // Redux Toolkit uses Immer, so this is safe
      state.layers.byId[action.payload.id] = action.payload;
    }
  }
});
```

### Anti-Pattern: Props Drilling

```javascript
// ❌ WRONG: Passing props through many levels
<GrandParent>
  <Parent data={data}>
    <Child data={data}>
      <GrandChild data={data} />
    </Child>
  </Parent>
</GrandParent>

// ✅ CORRECT: Use Redux or Context
function GrandChild() {
  const data = useSelector(selectData); // Direct access
  return <div>{data}</div>;
}
```

---

## Review Checklist

Before submitting code, verify:

### Architecture Compliance
- [ ] Layer state is in Redux, not component state
- [ ] Dependencies are declared in dependency graph
- [ ] Layer categories are specified
- [ ] Complex async uses Redux Saga
- [ ] EnhancedLayerManager is used for MapLibre operations

### Code Quality
- [ ] Imports are organized correctly
- [ ] Naming conventions are followed
- [ ] PropTypes are defined for components
- [ ] Error handling is comprehensive
- [ ] No console.logs in production code
- [ ] Comments explain "why", not "what"

### Performance
- [ ] Selectors are memoized
- [ ] useCallback for event handlers
- [ ] useMemo for expensive computations
- [ ] No unnecessary re-renders
- [ ] Large data uses IndexedDB, not Redux

### Testing
- [ ] Unit tests for logic
- [ ] Integration tests for flows
- [ ] Edge cases are covered
- [ ] Test names are descriptive

### Documentation
- [ ] JSDoc comments for functions
- [ ] README updated if needed
- [ ] Architecture diagrams updated if structure changed

---

## Emergency Override

If the architecture prevents a critical feature:

1. **Document the issue**: Explain why current architecture doesn't work
2. **Propose architectural change**: Don't work around, fix the root cause
3. **Get approval**: Discuss with team before implementing workaround
4. **Update documentation**: If architectural change is approved, update ARCHITECTURE.md

**Example**:
```javascript
// ❌ NEVER DO THIS:
// Workaround: Storing layer state in component because Redux "too slow"
const [layers, setLayers] = useState({});

// ✅ INSTEAD: Propose performance optimization to Redux architecture
// Create GitHub issue: "Optimize Redux layer updates for 100K+ features"
// Propose solution: Use virtual layers + IndexedDB
```

---

## Conclusion

These guidelines ensure:
- **Consistency**: All code follows same patterns
- **Maintainability**: Easy to understand and modify
- **Scalability**: Architecture supports growth
- **Quality**: Best practices are enforced

**Remember**: The architecture exists to solve real problems. Follow it strictly, and propose changes when it falls short.

---

**Document Version**: 1.0  
**Last Updated**: November 3, 2025  
**Next Review**: When major architectural changes are made