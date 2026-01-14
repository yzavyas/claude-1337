# Component Patterns

Composition patterns for scalable frontend architecture.

## Core Principle

**Composition over inheritance.** Modern frontend favors combining smaller, focused components rather than inheritance hierarchies.

Facebook's thousands of React components use zero inheritance. Svelte follows the same philosophy.

## Pattern Decision Tree

```
What problem are you solving?
├── Multiple layout regions → Compound Components
├── Deep prop passing → Context API
├── Modal/overlay → Portal pattern
├── Complex logic, custom UI → Headless UI
├── Repeating structure → Render props / Snippets
└── Simple data flow → Props (don't over-engineer)
```

## 1. Compound Components

Components that work together by sharing implicit state. Like HTML's `<select>` and `<option>`.

### When to Use

- Component has 3+ props for layout/content
- Multiple related subcomponents
- Flexible declarative API needed

### React Implementation

```jsx
import { createContext, useContext, useState } from 'react';

const TabsContext = createContext(null);

function Tabs({ children, defaultValue }) {
  const [activeTab, setActiveTab] = useState(defaultValue);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

function TabList({ children }) {
  return <div className="tab-list">{children}</div>;
}

function Tab({ value, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext);
  return (
    <button
      className={activeTab === value ? 'active' : ''}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  );
}

function TabPanel({ value, children }) {
  const { activeTab } = useContext(TabsContext);
  if (activeTab !== value) return null;
  return <div className="tab-panel">{children}</div>;
}

// Usage
<Tabs defaultValue="tab1">
  <TabList>
    <Tab value="tab1">First</Tab>
    <Tab value="tab2">Second</Tab>
  </TabList>
  <TabPanel value="tab1">Content 1</TabPanel>
  <TabPanel value="tab2">Content 2</TabPanel>
</Tabs>
```

### Svelte 5 Implementation

```svelte
<!-- Tabs.svelte -->
<script lang="ts">
  import { setContext } from 'svelte';
  import type { Snippet } from 'svelte';

  let { children, defaultValue }: {
    children: Snippet;
    defaultValue: string;
  } = $props();

  let activeTab = $state(defaultValue);

  setContext('tabs', {
    get activeTab() { return activeTab; },
    setActiveTab: (value: string) => activeTab = value
  });
</script>

<div class="tabs">
  {@render children()}
</div>
```

```svelte
<!-- Tab.svelte -->
<script lang="ts">
  import { getContext } from 'svelte';
  import type { Snippet } from 'svelte';

  let { value, children }: {
    value: string;
    children: Snippet;
  } = $props();

  const tabs = getContext('tabs');
</script>

<button
  class:active={tabs.activeTab === value}
  onclick={() => tabs.setActiveTab(value)}
>
  {@render children()}
</button>
```

## 2. Context API

Share data across component trees without prop drilling.

### When to Use

- Theme, auth state, language
- Data needed at multiple tree levels
- Avoiding 3+ levels of prop passing

### When NOT to Use

- Simple parent-child data (just use props)
- Data needed by 1-2 components
- High-frequency updates (performance issue)

### React

```jsx
const ThemeContext = createContext({ theme: 'light', setTheme: () => {} });

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useTheme() {
  return useContext(ThemeContext);
}
```

### Svelte 5

```svelte
<!-- Parent -->
<script>
  import { setContext } from 'svelte';

  let theme = $state('light');

  setContext('theme', {
    get theme() { return theme; },  // Getter for reactivity
    toggle: () => theme = theme === 'light' ? 'dark' : 'light'
  });
</script>
```

```svelte
<!-- Child (any depth) -->
<script>
  import { getContext } from 'svelte';
  const { theme, toggle } = getContext('theme');
</script>

<button onclick={toggle}>
  Current: {theme}
</button>
```

**Critical**: Use getters for reactive context values in Svelte 5.

## 3. Headless UI

Components that provide logic without prescribing UI.

### Popular Libraries

| Library | Framework | Focus |
|---------|-----------|-------|
| Headless UI | React/Vue | Tailwind-oriented |
| React ARIA | React | Accessibility |
| Radix UI | React | Unstyled primitives |
| Melt UI | Svelte | Builders pattern |
| Bits UI | Svelte | Headless primitives |

### Pattern

```jsx
// Headless hook
function useToggle(initial = false) {
  const [isOpen, setIsOpen] = useState(initial);
  return {
    isOpen,
    toggle: () => setIsOpen(!isOpen),
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
  };
}

// Usage - complete control over UI
function Dropdown() {
  const { isOpen, toggle } = useToggle();

  return (
    <div>
      <button onClick={toggle}>Menu</button>
      {isOpen && <div className="my-custom-dropdown">...</div>}
    </div>
  );
}
```

## 4. Render Props / Snippets

Pass rendering logic as a function/prop.

### React Render Props

```jsx
function List({ items, renderItem }) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
/>
```

### Svelte 5 Snippets

```svelte
<!-- List.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  let { items, row }: {
    items: T[];
    row: Snippet<[T]>;
  } = $props();
</script>

<ul>
  {#each items as item}
    <li>{@render row(item)}</li>
  {/each}
</ul>
```

```svelte
<!-- Usage -->
<List items={users}>
  {#snippet row(user)}
    <UserCard {user} />
  {/snippet}
</List>
```

## 5. Portal Pattern

Render content outside the component tree (for modals, tooltips).

### React

```jsx
import { createPortal } from 'react-dom';

function Modal({ children, isOpen }) {
  if (!isOpen) return null;

  return createPortal(
    <div className="modal-overlay">
      <div className="modal">{children}</div>
    </div>,
    document.body
  );
}
```

### Svelte

```svelte
<script>
  import { browser } from '$app/environment';
  let { isOpen, children } = $props();
</script>

{#if isOpen && browser}
  <svelte:element this="div" {...$$props}>
    <div class="modal-overlay">
      <div class="modal">
        {@render children()}
      </div>
    </div>
  </svelte:element>
{/if}

<!-- Or use a portal library like svelte-portal -->
```

## 6. State Machine Pattern

For complex UI with multiple states and transitions.

### When to Use

- Loading → Success → Error flows
- Multi-step wizards
- Animation sequences (warp → intro → content)

### Implementation

```typescript
type State = 'idle' | 'loading' | 'success' | 'error';
type Event = 'FETCH' | 'SUCCESS' | 'ERROR' | 'RESET';

const machine = {
  idle: { FETCH: 'loading' },
  loading: { SUCCESS: 'success', ERROR: 'error' },
  success: { RESET: 'idle' },
  error: { RESET: 'idle', FETCH: 'loading' },
};

function transition(state: State, event: Event): State {
  return machine[state]?.[event] || state;
}
```

### Libraries

- **XState**: Full state machine library
- **Zag**: Headless components as state machines
- **Robot**: Lightweight finite state machines

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|------------|-----|
| Global store for UI state | Local state | Coupling, testing |
| Prop drilling 3+ levels | Context API | Maintenance |
| 15+ props | Compound components | Readability |
| Inheritance hierarchy | Composition | Flexibility |
| Premature abstraction | Wait for pattern | YAGNI |

## Composition Guidelines

### When to Extract

- Same 3+ elements repeated
- Logic shared across components
- Testing in isolation needed

### When NOT to Extract

- Used only once
- Extraction adds complexity
- Breaking natural component boundaries

### File Organization

```
components/
├── ui/              # Generic (Button, Card, Modal)
│   └── Button/
│       ├── Button.tsx
│       ├── Button.test.tsx
│       └── index.ts
├── features/        # Domain-specific (UserCard, ProductList)
│   └── checkout/
│       └── CartItem.tsx
└── layout/          # Structural (Header, Sidebar)
    └── MainLayout.tsx
```

## Sources

- [React Composition vs Inheritance](https://reactjs.org/docs/composition-vs-inheritance.html)
- [Svelte 5 Snippets](https://svelte.dev/docs/svelte/snippet)
- [Patterns.dev](https://www.patterns.dev/)
- [Kent C. Dodds - Compound Components](https://kentcdodds.com/blog/compound-components-with-react-hooks)
