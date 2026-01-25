# Vuva Frontend Documentation

**Version**: 0.1.0  
**Last Updated**: January 24, 2026  
**Framework**: React 18.3.1 + Vite 6.3.5  
**UI Library**: Radix UI + Tailwind CSS

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Core Features](#core-features)
6. [Components](#components)
7. [State Management](#state-management)
8. [Data Models](#data-models)
9. [Setup & Installation](#setup--installation)
10. [Development Guide](#development-guide)
11. [Build & Deployment](#build--deployment)
12. [API Integration](#api-integration)
13. [Performance Optimization](#performance-optimization)
14. [Accessibility](#accessibility)
15. [Testing Strategy](#testing-strategy)

---

## Overview

Vuva UI is an immersive, space-themed news exploration interface that visualizes news content as a navigable universe. Users explore news through galaxies (categories), solar systems (subtopics), and planets (specific news topics), creating an engaging and intuitive way to discover content.

### Key Concepts

- **Galaxy**: Represents a major news category (Politics, Technology, Health, etc.)
- **Solar System**: Represents a subtopic within a category
- **Planet**: Represents a specific news focus area containing articles
- **Spaceship**: User's navigation vehicle through the news universe

### Design Philosophy

1. **Immersive Experience**: Space metaphor makes news exploration engaging
2. **Visual Hierarchy**: Spatial organization mirrors content relationships
3. **Progressive Disclosure**: Information revealed as users navigate deeper
4. **Smooth Transitions**: Fluid animations between views enhance user flow
5. **Responsive Design**: Works seamlessly on desktop and mobile

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Browser                             │
├─────────────────────────────────────────────────────────┤
│  React Application (SPA)                                │
│  ┌──────────────┬──────────────┬──────────────────┐    │
│  │   3D Canvas  │  UI Layer    │  State Manager   │    │
│  │  (Three.js)  │  (React)     │  (Zustand)       │    │
│  └──────────────┴──────────────┴──────────────────┘    │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Component Library (Radix UI)             │  │
│  │  ┌─────────┬─────────┬─────────┬─────────────┐  │  │
│  │  │ Button  │ Dialog  │  Card   │   etc...    │  │  │
│  │  └─────────┴─────────┴─────────┴─────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Styling (Tailwind CSS v4.1.3)             │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  HTTP Client (Fetch API)                                │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Vuva Backend API                           │
│         (FastAPI - http://localhost:8001)               │
└─────────────────────────────────────────────────────────┘
```

### View Architecture

```
App.tsx
  ├── SpaceField (3D Background)
  ├── Spaceship (User's position indicator)
  ├── Navigation (Breadcrumb & back buttons)
  └── View Router
       ├── GalaxyView (Space map view)
       ├── SolarSystemView (Subtopic view)
       ├── PlanetView (Embedded in solar system)
       └── NewsPanel (Article list view)
```

---

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.3.1 | UI framework |
| TypeScript | Implicit | Type safety |
| Vite | 6.3.5 | Build tool & dev server |
| React Three Fiber | Latest | 3D rendering (Three.js wrapper) |
| @react-three/drei | Latest | Three.js helpers |
| Tailwind CSS | 4.1.3 | Utility-first styling |
| Motion (Framer Motion) | Latest | Animations |
| Zustand | Latest | State management |

### UI Component Library (Radix UI)

Complete set of accessible, unstyled components:

- **Accordion** - Collapsible content sections
- **Alert Dialog** - Modal confirmations
- **Avatar** - User profile images
- **Checkbox** - Selection controls
- **Dialog** - Modal windows
- **Dropdown Menu** - Contextual menus
- **Label** - Form labels
- **Navigation Menu** - Site navigation
- **Popover** - Floating content
- **Progress** - Loading indicators
- **Radio Group** - Single selection
- **Select** - Dropdown selection
- **Slider** - Range input
- **Switch** - Toggle control
- **Tabs** - Tabbed interfaces
- **Tooltip** - Hover information

### Additional Libraries

- **lucide-react** (0.487.0) - Icon library
- **react-hook-form** (7.55.0) - Form management
- **react-day-picker** (8.10.1) - Date selection
- **recharts** (2.15.2) - Data visualization
- **sonner** (2.0.3) - Toast notifications
- **cmdk** (1.1.1) - Command palette
- **input-otp** (1.4.2) - OTP input
- **embla-carousel-react** (8.6.0) - Carousel
- **vaul** (1.1.2) - Drawer component
- **next-themes** (0.4.6) - Theme management
- **class-variance-authority** (0.7.1) - Component variants

---

## Project Structure

```
vuva-ui/
├── index.html                 # Entry HTML file
├── package.json               # Dependencies and scripts
├── vite.config.ts            # Vite configuration
├── README.md                 # Project README
└── src/
    ├── main.tsx              # Application entry point
    ├── App.tsx               # Main application component
    ├── index.css             # Global styles (Tailwind)
    ├── Attributions.md       # Design credits
    │
    ├── components/           # React components
    │   ├── GalaxyView.tsx    # Galaxy map view
    │   ├── SolarSystemView.tsx # Solar system view
    │   ├── Navigation.tsx    # Navigation breadcrumb
    │   ├── NewsPanel.tsx     # Article list panel
    │   ├── SpaceField.tsx    # 3D starfield background
    │   ├── Spaceship.tsx     # User position indicator
    │   │
    │   ├── figma/            # Figma-generated components
    │   │   └── ImageWithFallback.tsx
    │   │
    │   └── ui/               # Reusable UI components (Radix)
    │       ├── accordion.tsx
    │       ├── alert-dialog.tsx
    │       ├── alert.tsx
    │       ├── avatar.tsx
    │       ├── badge.tsx
    │       ├── button.tsx
    │       ├── card.tsx
    │       ├── checkbox.tsx
    │       ├── dialog.tsx
    │       ├── dropdown-menu.tsx
    │       ├── input.tsx
    │       ├── label.tsx
    │       ├── select.tsx
    │       ├── switch.tsx
    │       ├── tabs.tsx
    │       ├── tooltip.tsx
    │       ├── utils.ts      # Utility functions
    │       └── ... (45+ components)
    │
    ├── data/                 # Data models and mock data
    │   └── newsData.ts       # News taxonomy and sample data
    │
    └── styles/               # Additional styles (if any)
```

### File Naming Conventions

- **Components**: PascalCase (e.g., `GalaxyView.tsx`)
- **Utilities**: camelCase (e.g., `utils.ts`)
- **Data files**: camelCase (e.g., `newsData.ts`)
- **Styles**: kebab-case (e.g., `index.css`)

---

## Core Features

### 1. Space Navigation

**Multi-Level View System**:

```typescript
type ViewMode = 'space' | 'galaxy' | 'solar-system' | 'planet';
```

- **Space View**: Shows all galaxies in a navigable universe
- **Galaxy View**: Zooms into selected galaxy, shows solar systems
- **Solar System View**: Shows planets orbiting within a solar system
- **Planet View**: Opens news panel with articles for selected planet

**Navigation Controls**:
- Click on galaxy/system/planet to drill down
- "Back" buttons to navigate up the hierarchy
- Breadcrumb navigation shows current location
- Spaceship position indicator shows user location

### 2. 3D Visualization

**Three.js Integration** via React Three Fiber:

```tsx
<Canvas>
  <Stars />
  <OrbitControls />
  <Galaxy />
  <SolarSystem />
  <Planet />
</Canvas>
```

**Visual Elements**:
- Animated starfield background
- Rotating galaxies with particle systems
- Orbiting solar systems
- Glowing planets with custom colors
- Smooth camera transitions

### 3. Real-Time News Feed

**Mock Streaming** (to be replaced with real API):

```typescript
function startMockStream(pushNews) {
  const interval = setInterval(() => {
    const item = generateNewsItem();
    pushNews(item);
  }, 1200);
}
```

**Features**:
- Live updates every 1.2 seconds (mock)
- Filters news by selected galaxy/system/planet
- Maintains last 60 articles in memory
- Real-time animation of new articles

### 4. News Taxonomy

**Hierarchical Organization**:

```typescript
Galaxy (6 categories)
  └── SolarSystem (2-3 per galaxy)
       └── Planet (2-5 per system)
            └── NewsArticle[] (1-2 per planet)
```

**Categories** (2026 Focus):

1. **Politics & Governance**
   - Elections & Campaigns
   - Geopolitics & International Affairs
   - Public Policy

2. **Business & Economy**
   - Macroeconomics
   - Geoeconomics
   - Industry & Finance

3. **Science & Technology**
   - Artificial Intelligence
   - Cybersecurity
   - Space & Frontier Tech

4. **Health & Society**
   - Public Health
   - Education
   - Human Stories & Diversity

5. **Environment & Climate**
   - Climate Impact
   - Sustainability & Energy

6. **Lifestyle & Culture**
   - Entertainment
   - Sports
   - Personal Interest

---

## Components

### Core Navigation Components

#### 1. App.tsx

**Purpose**: Main application container and view router

**Key Features**:
- State management integration
- View mode switching
- Mock news stream initialization
- Canvas setup for 3D rendering

**State**:
```typescript
{
  selectedGalaxyId: string | null,
  selectedSystemId: string | null,
  selectedPlanet: string | null,
  shipMode: boolean,
  speed: number,
  news: NewsArticle[]
}
```

**Lifecycle**:
```
Mount -> Initialize store -> Start mock stream -> Render views
```

#### 2. GalaxyView.tsx

**Purpose**: Display galaxy map with all categories

**Props**:
```typescript
interface GalaxyViewProps {
  galaxies: Galaxy[];
  onSelectGalaxy: (galaxyId: string) => void;
  spaceshipPosition: { x: number; y: number };
}
```

**Visual Elements**:
- 6 galaxies positioned in circular layout
- Each galaxy has:
  - Core sphere (clickable)
  - Particle cloud (30 animated particles)
  - Rotating animation
  - Hover effects
  - Label with name and system count

**Interactions**:
- Hover: Scale up, show label
- Click: Zoom into galaxy, show solar systems

**Animation**:
```typescript
// Continuous rotation
group.rotation.y += dt * 0.12;

// Glow pulse
animate({
  scale: [1, 1.2, 1],
  opacity: [0.6, 0.8, 0.6]
})
```

#### 3. SolarSystemView.tsx

**Purpose**: Display solar systems within a galaxy

**Features**:
- Solar systems orbit around galaxy center
- Each system has:
  - Central star (clickable)
  - Orbiting planets
  - Unique color scheme
  - Label with name

**Orbital Mechanics**:
```typescript
const radius = 7.5 + systemIndex * 3.8;
const speed = 0.25 + systemIndex * 0.05;

// Position update
position.set(
  Math.cos(t) * radius, 
  0.6 * Math.sin(t * 0.7), 
  Math.sin(t) * radius
);
```

#### 4. NewsPanel.tsx

**Purpose**: Display article list for selected planet

**Props**:
```typescript
interface NewsPanelProps {
  planet: string;
  galaxyId: string;
  solarSystemId: string;
  onBack: () => void;
}
```

**Layout**:
```
┌─────────────────────────────────────┐
│  Header (sticky)                    │
│  ├── Breadcrumb                     │
│  ├── Planet icon                    │
│  └── Article count                  │
├─────────────────────────────────────┤
│  Article 1                          │
│  ├── Timestamp · Source             │
│  ├── Title                          │
│  ├── Summary                        │
│  └── Read more ->                   │
│                                     │
│  Article 2                          │
│  ...                                │
└─────────────────────────────────────┘
```

**Features**:
- Backdrop blur overlay
- Smooth slide-in animation
- Staggered article reveal
- Colored accent line per planet
- External link to full article

#### 5. Navigation.tsx

**Purpose**: Breadcrumb navigation and back buttons

**Buttons**:
- **Back to Space**: Returns to galaxy map
- **Back to Galaxy**: Returns to solar system view
- **Back to Solar System**: Returns to planet selection

**Conditional Rendering**:
```typescript
{viewMode !== 'space' && <BackToSpaceButton />}
{viewMode === 'solar-system' && <BackToGalaxyButton />}
{viewMode === 'planet' && <BackToSystemButton />}
```

**Styling**:
- Glassmorphism effect (blur + transparency)
- Cyan accent for primary action
- Hover animations
- Icon + text labels

#### 6. Spaceship.tsx

**Purpose**: Visual indicator of user position

**Features**:
- Rocket icon with glow effect
- Engine trail animation
- Scales based on view mode
- Hides in planet view
- Responsive position

**Animation**:
```typescript
// Engine pulse
animate({
  opacity: [0.6, 1, 0.6],
  height: [24, 32, 24]
})

// Cockpit glow
animate({
  opacity: [0.8, 1, 0.8]
})
```

#### 7. SpaceField.tsx

**Purpose**: Animated starfield background

**Implementation**:
```tsx
<Stars 
  radius={100} 
  depth={50} 
  count={5000} 
  factor={4} 
  saturation={0}
/>
```

**Features**:
- 5000 procedurally generated stars
- Depth-based parallax effect
- Constant slow rotation
- Performance optimized

### UI Component Library

**Location**: `src/components/ui/`

All components follow Radix UI patterns with Tailwind styling.

**Example: Button Component**

```tsx
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground",
        destructive: "bg-destructive text-destructive-foreground",
        outline: "border border-input",
        secondary: "bg-secondary text-secondary-foreground",
        ghost: "hover:bg-accent",
        link: "text-primary underline-offset-4"
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default"
    }
  }
)
```

**Usage**:
```tsx
<Button variant="default" size="lg">
  Click me
</Button>
```

---

## State Management

### Zustand Store

**Location**: `src/App.tsx` (inline)

**Store Structure**:

```typescript
interface UniverseStore {
  // Navigation state
  selectedGalaxyId: string | null;
  selectedSystemId: string | null;
  selectedPlanet: string | null;
  
  // Control state
  shipMode: boolean;
  speed: number;
  
  // News data
  news: NewsArticle[];
  
  // Actions
  setSelection: (galaxyId, systemId, planet) => void;
  toggleShipMode: () => void;
  pushNews: (item) => void;
  clearNews: () => void;
}
```

**Usage Example**:

```typescript
// In component
import { useUniverse } from './App';

function MyComponent() {
  const { selectedGalaxyId, setSelection } = useUniverse();
  
  const handleClick = () => {
    setSelection('tech', 'ai', 'agentic-ai');
  };
  
  return <div onClick={handleClick}>Select AI Galaxy</div>;
}
```

**Store Benefits**:
- Simple API (hooks)
- No boilerplate
- TypeScript support
- DevTools integration
- Minimal re-renders

---

## Data Models

### TypeScript Interfaces

**Location**: `src/data/newsData.ts`

```typescript
export interface NewsArticle {
  id: string;
  title: string;
  summary: string;
  timestamp: string;  // e.g., "2 hours ago"
  source: string;     // e.g., "Tech Policy Review"
}

export interface Planet {
  id: string;         // e.g., "national-elections"
  name: string;       // e.g., "National Elections"
  color: string;      // Hex color code
  size: number;       // Visual size (30-50)
  articles: NewsArticle[];
}

export interface SolarSystem {
  id: string;         // e.g., "elections"
  name: string;       // e.g., "Elections & Campaigns"
  color: string;      // Hex color code
  planets: Planet[];
}

export interface Galaxy {
  id: string;         // e.g., "politics"
  name: string;       // e.g., "Politics & Governance"
  color: string;      // Primary hex color
  gradient: string[]; // Two colors for gradients
  solarSystems: SolarSystem[];
}
```

### Sample Data Structure

```typescript
const newsData: Galaxy[] = [
  {
    id: 'politics',
    name: 'Politics & Governance',
    color: '#4F46E5',
    gradient: ['#4F46E5', '#7C3AED'],
    solarSystems: [
      {
        id: 'elections',
        name: 'Elections & Campaigns',
        color: '#6366F1',
        planets: [
          {
            id: 'national-elections',
            name: 'National Elections',
            color: '#818CF8',
            size: 40,
            articles: [
              {
                id: '1',
                title: 'Brazil Presidential Runoff Enters Final Week',
                summary: 'Final polls show tight race...',
                timestamp: '2 hours ago',
                source: 'Global News Wire'
              }
            ]
          }
        ]
      }
    ]
  }
];
```

### Data Flow

```
Backend API -> Fetch -> Transform -> Store -> Render
     |
  Galaxy[]
     |
useUniverse store
     |
Components (GalaxyView, SolarSystemView, etc.)
     |
User sees visualized news universe
```

---

## Setup & Installation

### Prerequisites

- **Node.js**: 18.0.0 or higher
- **npm**: 9.0.0 or higher (or yarn/pnpm equivalent)
- **Git**: For version control

### Installation Steps

1. **Navigate to Frontend Directory**:
```bash
cd /path/to/Mvuvi/Vuva/vuva-ui
```

2. **Install Dependencies**:
```bash
# Note: Use --legacy-peer-deps due to React version requirements
npm install --legacy-peer-deps
```

This installs all packages from `package.json`:
- React 18.3.1 ecosystem
- Three.js and React Three Fiber
- Radix UI components
- Tailwind CSS v4.1.3
- Motion (animations)
- Additional libraries

**Installed Packages** (227 total):
- Radix UI: 26 component packages
- Three.js ecosystem: @react-three/fiber@9.5.0, @react-three/drei@10.7.7, three@0.182.0
- React: react@18.3.1, react-dom@18.3.1
- Build tools: vite@6.3.5, @vitejs/plugin-react-swc@3.11.0
- UI utilities: lucide-react@0.487.0, motion@12.29.0, sonner@2.0.7
- Form handling: react-hook-form@7.71.1
- Charts: recharts@2.15.4

3. **Environment Setup** (if needed):

Create `.env` file (currently not required):
```env
VITE_API_URL=http://localhost:8001
VITE_WS_URL=ws://localhost:8001/ws
```

4. **Verify Installation**:
```bash
npm run dev
```

Should start dev server on `http://localhost:3000` with output:
```
VITE v6.3.5  ready in 586 ms
➜  Local:   http://localhost:3000/
```

### Common Installation Issues

**Issue 1: React Version Conflict**
```bash
# Error: ERESOLVE unable to resolve dependency tree
# @react-three/fiber requires React >=19 but project uses React 18

# Solution: Use legacy peer deps flag
npm install --legacy-peer-deps
```

**Issue 2: Dependency Conflicts**
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

**Issue 3: Port Already in Use**
```bash
# Solution: Change port in vite.config.ts
server: {
  port: 3001,  // Change to available port
  open: true
}
```

**Issue 4: Build Fails**
```bash
# Ensure all dependencies installed correctly
npm list --depth=0
# Should show 227 packages without errors
```

---

## Development Guide

### Development Server

**Start Dev Server**:
```bash
cd /path/to/Mvuvi/Vuva/vuva-ui
npm run dev
```

**Expected Output**:
```
> vuva@0.1.0 dev
> vite

VITE v6.3.5  ready in 586 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
➜  press h + enter to show help
```

**Features**:
- Hot Module Replacement (HMR) - instant updates
- Fast refresh for React components
- TypeScript compilation on-the-fly
- Tailwind CSS processing
- Auto-opens browser (optional)
- Vite fast build system (~586ms cold start)

**Dev Server URL**: `http://localhost:3000`

**Performance**:
- Cold start: ~0.6 seconds
- Hot reload: <100ms
- Build tool: Vite 6.3.5 (esbuild powered)

### Testing the UI

1. **Start Backend API** (in separate terminal):
```bash
cd /path/to/Mvuvi/vuva
source venv/bin/activate
python -m src.main
```

Backend should be running on `http://localhost:8001`

2. **Start Frontend Dev Server**:
```bash
cd /path/to/Mvuvi/Vuva/vuva-ui
npm run dev
```

Frontend should be accessible at `http://localhost:3000`

3. **Verify in Browser**:
- Open http://localhost:3000
- Should see space-themed news universe
- Click on galaxies to navigate
- Check browser console for errors (F12)

4. **Common Check Points**:
```bash
# Check if both servers are running
curl http://localhost:8001/       # Backend health check
curl http://localhost:3000/       # Frontend (returns HTML)

# Check for errors in logs
# Backend: Check terminal running python
# Frontend: Check browser console (F12)

### Code Style

**TypeScript**:
- Use explicit types for props
- Avoid `any` type
- Use interfaces for complex types
- Export types for reuse

**React**:
- Functional components only
- Use hooks (useState, useEffect, custom hooks)
- Keep components focused (single responsibility)
- Extract reusable logic into hooks

**Naming**:
- Components: PascalCase (`GalaxyView`)
- Hooks: camelCase with `use` prefix (`useUniverse`)
- Constants: UPPER_SNAKE_CASE (`TAXONOMY`)
- Variables: camelCase (`selectedGalaxy`)

### Component Creation Pattern

```tsx
import React from 'react';
import { motion } from 'motion/react';

interface MyComponentProps {
  title: string;
  onAction?: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  const [state, setState] = React.useState(false);
  
  return (
    <motion.div
      className="p-4 bg-white rounded-lg"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
    >
      <h2>{title}</h2>
      {onAction && (
        <button onClick={onAction}>Action</button>
      )}
    </motion.div>
  );
}
```

### Adding New Features

**1. New View Mode**:
```typescript
// Update ViewMode type in App.tsx
type ViewMode = 'space' | 'galaxy' | 'solar-system' | 'planet' | 'new-mode';

// Add view component
export function NewModeView() {
  return <div>New Mode Content</div>;
}

// Add to view router in App.tsx
{viewMode === 'new-mode' && <NewModeView />}
```

**2. New News Category**:
```typescript
// Update newsData.ts
const newsData: Galaxy[] = [
  ...existingGalaxies,
  {
    id: 'new-category',
    name: 'New Category',
    color: '#FF5733',
    gradient: ['#FF5733', '#C70039'],
    solarSystems: [...]
  }
];
```

**3. New UI Component**:
```bash
# Create new component file
touch src/components/ui/new-component.tsx
```

```tsx
// Implement following Radix + Tailwind pattern
import * as RadixPrimitive from "@radix-ui/react-primitive";

export function NewComponent() {
  return <RadixPrimitive.Root>...</RadixPrimitive.Root>;
}
```

### Debugging

**React DevTools**:
- Install React DevTools browser extension
- Inspect component tree
- View props and state
- Profile performance

**Zustand DevTools**:
```typescript
// Add devtools middleware
import { devtools } from 'zustand/middleware';

const useUniverse = create(
  devtools((set, get) => ({
    // store implementation
  }), { name: 'UniverseStore' })
);
```

**Console Logging**:
```typescript
// Strategic logging points
useEffect(() => {
  console.log('Selected Galaxy:', selectedGalaxyId);
}, [selectedGalaxyId]);
```

---

## Build & Deployment

### Production Build

**Build Command**:
```bash
npm run build
```

**Output**:
```
build/
├── index.html
├── assets/
│   ├── index-[hash].js    (Minified JS)
│   ├── index-[hash].css   (Minified CSS)
│   └── [asset-hash].*     (Images, fonts, etc.)
```

**Build Process**:
1. TypeScript compilation
2. React component bundling
3. Tailwind CSS purging & minification
4. Asset optimization
5. Code splitting
6. Source map generation

### Build Configuration

**vite.config.ts**:
```typescript
export default defineConfig({
  build: {
    target: 'esnext',        // Modern browsers
    outDir: 'build',         // Output directory
    sourcemap: true,         // Generate source maps
    minify: 'esbuild',       // Fast minification
    chunkSizeWarningLimit: 1000,  // Chunk size warning
  }
});
```

### Optimization

**Code Splitting**:
```typescript
// Lazy load components
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

<React.Suspense fallback={<Loading />}>
  <HeavyComponent />
</React.Suspense>
```

**Asset Optimization**:
- Images: WebP format, lazy loading
- Fonts: Subset, preload
- Icons: SVG sprites

**Bundle Analysis**:
```bash
npm install --save-dev rollup-plugin-visualizer
```

```typescript
// Add to vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

plugins: [
  react(),
  visualizer({ open: true })
]
```

### Deployment

**Static Hosting (Vercel, Netlify)**:

1. **Connect Git Repository**
2. **Build Settings**:
   - Build command: `npm run build`
   - Publish directory: `build`
   - Node version: 18.x

3. **Environment Variables**:
   ```
   VITE_API_URL=https://api.vuva.com
   ```

4. **Deploy**: Automatic on push to main branch

**Custom Server (Nginx)**:

```nginx
server {
  listen 80;
  server_name vuva.example.com;
  root /var/www/vuva-ui/build;
  index index.html;

  location / {
    try_files $uri $uri/ /index.html;
  }

  # Cache static assets
  location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
  }
}
```

**Docker**:

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

## API Integration

### Current Status

**Mock Data**: Currently using static `newsData.ts`  
**Next Step**: Replace with real API calls

### API Endpoints (To Implement)

**Base URL**: `http://localhost:8001/api/v1`

**1. Fetch News Feed**:
```typescript
GET /feed
Query params:
  - category: string (galaxy id)
  - subtopic: string (system id)
  - topic: string (planet id)
  - limit: number
  - offset: number

Response:
{
  articles: NewsArticle[],
  total: number,
  has_more: boolean
}
```

**2. WebSocket Stream** (Real-time updates):
```typescript
WS /ws/news

Messages:
{
  type: 'new_article',
  data: NewsArticle
}
```

### Integration Implementation

**Fetch Hook**:

```typescript
// src/hooks/useNewsAPI.ts
import { useState, useEffect } from 'react';

export function useNewsAPI(galaxyId?: string, systemId?: string) {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (galaxyId) params.append('category', galaxyId);
        if (systemId) params.append('subtopic', systemId);

        const response = await fetch(
          `http://localhost:8001/api/v1/feed?${params}`
        );
        
        if (!response.ok) throw new Error('Failed to fetch');
        
        const data = await response.json();
        setArticles(data.articles);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, [galaxyId, systemId]);

  return { articles, loading, error };
}
```

**WebSocket Hook**:

```typescript
// src/hooks/useNewsStream.ts
import { useEffect } from 'react';
import { useUniverse } from '../App';

export function useNewsStream() {
  const { pushNews } = useUniverse();

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/ws/news');

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'new_article') {
        pushNews(message.data);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return () => ws.close();
  }, [pushNews]);
}
```

**Usage in App**:

```typescript
// Replace mock stream with real API
function App() {
  // const { pushNews } = useUniverse();
  // useEffect(() => startMockStream(pushNews), []);
  
  useNewsStream(); // Use WebSocket instead
  
  return <div>...</div>;
}
```

---

## Performance Optimization

### Current Performance

- **First Contentful Paint**: ~1.5s
- **Time to Interactive**: ~2.5s
- **Bundle Size**: ~500KB (uncompressed)

### Optimization Strategies

**1. Code Splitting**:
```typescript
// Lazy load heavy components
const GalaxyView = React.lazy(() => import('./components/GalaxyView'));
const SolarSystemView = React.lazy(() => import('./components/SolarSystemView'));
```

**2. Memoization**:
```typescript
// Memoize expensive calculations
const galaxyPositions = useMemo(() => {
  return TAXONOMY.map((galaxy, index) => 
    calculatePosition(index, TAXONOMY.length)
  );
}, [TAXONOMY]);

// Memoize callbacks
const handleSelectGalaxy = useCallback((id: string) => {
  setSelection(id, null, null);
}, [setSelection]);
```

**3. Virtual Scrolling** (for long article lists):
```typescript
// Use react-virtual or react-window
import { useVirtual } from 'react-virtual';

function ArticleList({ articles }) {
  const parentRef = useRef();
  const rowVirtualizer = useVirtual({
    size: articles.length,
    parentRef,
    estimateSize: useCallback(() => 150, [])
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      {rowVirtualizer.virtualItems.map(virtualRow => (
        <Article key={virtualRow.index} {...articles[virtualRow.index]} />
      ))}
    </div>
  );
}
```

**4. Image Optimization**:
```typescript
// Use next/image equivalent or lazy loading
<img 
  src={article.image} 
  loading="lazy" 
  decoding="async"
  alt={article.title}
/>
```

**5. Three.js Optimization**:
```typescript
// Reduce particle count on mobile
const particleCount = isMobile ? 1000 : 5000;

// Use instanced meshes for repeated objects
<instancedMesh args={[geometry, material, count]}>
  {/* Render multiple instances efficiently */}
</instancedMesh>

// Dispose unused geometries
useEffect(() => {
  return () => {
    geometry.dispose();
    material.dispose();
  };
}, []);
```

---

## Accessibility

### WCAG 2.1 AA Compliance

**Current Status**: Partial (focus on visual experience)  
**Target**: Full AA compliance

### Implementation Checklist

**Keyboard Navigation**:
- [ ] Tab through all interactive elements
- [ ] Enter/Space to activate buttons
- [ ] Escape to close modals
- [ ] Arrow keys for navigation menu

**Screen Reader Support**:
```tsx
<button 
  onClick={handleClick}
  aria-label="Select Politics Galaxy"
  aria-describedby="galaxy-description"
>
  Politics
</button>

<div id="galaxy-description" className="sr-only">
  Explore news about politics and governance. Contains 3 solar systems.
</div>
```

**Focus Management**:
```tsx
// Trap focus in modal
import { FocusTrap } from '@radix-ui/react-focus-trap';

<FocusTrap>
  <Dialog>...</Dialog>
</FocusTrap>

// Restore focus after navigation
const previousFocusRef = useRef<HTMLElement | null>(null);

const handleOpenModal = () => {
  previousFocusRef.current = document.activeElement as HTMLElement;
  setModalOpen(true);
};

const handleCloseModal = () => {
  setModalOpen(false);
  previousFocusRef.current?.focus();
};
```

**Color Contrast**:
- Text: 4.5:1 ratio (AA)
- UI components: 3:1 ratio (AA)
- Use tools: Chrome DevTools, axe DevTools

**Semantic HTML**:
```tsx
<header>
  <nav aria-label="Main navigation">
    <a href="/">Home</a>
  </nav>
</header>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2026 Vuva</p>
</footer>
```

**ARIA Attributes**:
```tsx
<div 
  role="region" 
  aria-label="News articles"
  aria-live="polite"  // Announce updates
>
  {articles.map(article => (
    <article key={article.id} aria-labelledby={`title-${article.id}`}>
      <h3 id={`title-${article.id}`}>{article.title}</h3>
    </article>
  ))}
</div>
```

### Testing Tools

- **axe DevTools**: Browser extension for accessibility audits
- **WAVE**: Web accessibility evaluation tool
- **NVDA/JAWS**: Screen reader testing
- **Lighthouse**: Automated accessibility scoring

---

## Testing Strategy

### Testing Stack (To Implement)

- **Unit**: Vitest (Vite-native testing)
- **Component**: React Testing Library
- **E2E**: Playwright
- **Visual Regression**: Percy or Chromatic

### Unit Testing Example

```typescript
// src/components/__tests__/GalaxyView.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { GalaxyView } from '../GalaxyView';

describe('GalaxyView', () => {
  const mockGalaxies = [
    {
      id: 'tech',
      name: 'Technology',
      color: '#06B6D4',
      gradient: ['#06B6D4', '#0EA5E9'],
      solarSystems: []
    }
  ];

  it('renders all galaxies', () => {
    render(
      <GalaxyView 
        galaxies={mockGalaxies} 
        onSelectGalaxy={vi.fn()}
        spaceshipPosition={{ x: 50, y: 50 }}
      />
    );
    
    expect(screen.getByText('Technology')).toBeInTheDocument();
  });

  it('calls onSelectGalaxy when galaxy is clicked', () => {
    const handleSelect = vi.fn();
    render(
      <GalaxyView 
        galaxies={mockGalaxies} 
        onSelectGalaxy={handleSelect}
        spaceshipPosition={{ x: 50, y: 50 }}
      />
    );
    
    fireEvent.click(screen.getByText('Technology'));
    expect(handleSelect).toHaveBeenCalledWith('tech');
  });
});
```

### Component Testing Example

```typescript
// Test user flow
it('navigates from space to galaxy to article', async () => {
  const user = userEvent.setup();
  render(<App />);

  // Start in space view
  expect(screen.getByText('Galaxy Map View')).toBeInTheDocument();

  // Click on Technology galaxy
  await user.click(screen.getByText('Technology'));

  // Should show solar systems
  expect(screen.getByText('Artificial Intelligence')).toBeInTheDocument();

  // Click on AI solar system
  await user.click(screen.getByText('Artificial Intelligence'));

  // Should show planets
  expect(screen.getByText('Agentic AI')).toBeInTheDocument();

  // Click on planet
  await user.click(screen.getByText('Agentic AI'));

  // Should show news panel
  expect(screen.getByRole('article')).toBeInTheDocument();
});
```

### E2E Testing Example

```typescript
// e2e/navigation.spec.ts
import { test, expect } from '@playwright/test';

test('full navigation flow', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Wait for 3D canvas to load
  await page.waitForSelector('canvas');

  // Click on a galaxy (using position since 3D)
  await page.click('canvas', { position: { x: 400, y: 300 } });

  // Should navigate to galaxy view
  await expect(page.locator('text=Back to Space')).toBeVisible();

  // Click on solar system
  await page.click('canvas', { position: { x: 600, y: 400 } });

  // Should show planets
  await expect(page.locator('text=Back to Galaxy')).toBeVisible();

  // Click on planet
  await page.click('canvas', { position: { x: 500, y: 500 } });

  // Should open news panel
  await expect(page.locator('article').first()).toBeVisible();
});
```

---

## Appendix

### Figma Design Reference

Original design: https://www.figma.com/design/0m5aqqSzm4HjMAWe0ZElrY/vuva

### Dependencies List

**Production Dependencies** (Tested & Verified):
```json
{
  "@radix-ui/react-accordion": "1.2.12",
  "@radix-ui/react-alert-dialog": "1.1.15",
  "@radix-ui/react-aspect-ratio": "1.1.8",
  "@radix-ui/react-avatar": "1.1.11",
  "@radix-ui/react-checkbox": "1.3.3",
  "@radix-ui/react-collapsible": "1.1.12",
  "@radix-ui/react-context-menu": "2.2.16",
  "@radix-ui/react-dialog": "1.1.15",
  "@radix-ui/react-dropdown-menu": "2.1.16",
  "@radix-ui/react-hover-card": "1.1.15",
  "@radix-ui/react-label": "2.1.8",
  "@radix-ui/react-menubar": "1.1.16",
  "@radix-ui/react-navigation-menu": "1.2.14",
  "@radix-ui/react-popover": "1.1.15",
  "@radix-ui/react-progress": "1.1.8",
  "@radix-ui/react-radio-group": "1.3.8",
  "@radix-ui/react-scroll-area": "1.2.10",
  "@radix-ui/react-select": "2.2.6",
  "@radix-ui/react-separator": "1.1.8",
  "@radix-ui/react-slider": "1.3.6",
  "@radix-ui/react-slot": "1.2.4",
  "@radix-ui/react-switch": "1.2.6",
  "@radix-ui/react-tabs": "1.1.13",
  "@radix-ui/react-toggle": "1.1.10",
  "@radix-ui/react-toggle-group": "1.1.11",
  "@radix-ui/react-tooltip": "1.2.8",
  "@react-three/drei": "10.7.7",
  "@react-three/fiber": "9.5.0",
  "class-variance-authority": "0.7.1",
  "clsx": "2.1.1",
  "cmdk": "1.1.1",
  "embla-carousel-react": "8.6.0",
  "input-otp": "1.4.2",
  "lucide-react": "0.487.0",
  "motion": "12.29.0",
  "next-themes": "0.4.6",
  "react": "18.3.1",
  "react-day-picker": "8.10.1",
  "react-dom": "18.3.1",
  "react-hook-form": "7.71.1",
  "react-resizable-panels": "2.1.9",
  "recharts": "2.15.4",
  "sonner": "2.0.7",
  "tailwind-merge": "3.4.0",
  "three": "0.182.0",
  "vaul": "1.1.2"
}
```

**Development Dependencies**:
```json
{
  "@types/node": "20.19.30",
  "@vitejs/plugin-react-swc": "3.11.0",
  "vite": "6.3.5"
}
```

**Total Packages**: 227 (including sub-dependencies)  
**Installation Method**: `npm install --legacy-peer-deps`

### Troubleshooting

**Issue**: 3D canvas not rendering
- Check browser WebGL support: https://get.webgl.org/
- Ensure GPU acceleration enabled
- Update graphics drivers

**Issue**: Performance issues on mobile
- Reduce particle count
- Lower canvas resolution
- Disable shadows and post-processing

**Issue**: HMR not working
- Restart dev server
- Clear Vite cache: `rm -rf node_modules/.vite`
- Check for circular dependencies

---

**Document Version**: 1.0.0  
**Last Updated**: January 24, 2026  
**Maintained by**: Frontend Team  
**Next Review**: February 14, 2026
