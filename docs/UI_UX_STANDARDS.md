# Vuva UI/UX Standards & Design System

**Version**: 1.0.0  
**Last Updated**: January 24, 2026  
**Status**: Foundation Phase

## Overview

This document defines the UI/UX standards, design principles, and implementation guidelines for the Vuva frontend application. It ensures consistency, accessibility, and an exceptional user experience across all interfaces.

## Design Philosophy

### Core Principles

1. **Simplicity First** - Clean, uncluttered interfaces that focus on user tasks
2. **Speed & Performance** - Fast loading, responsive interactions, optimistic UI updates
3. **Accessibility** - WCAG 2.1 AA compliance, keyboard navigation, screen reader support
4. **Mobile-First** - Designed for mobile, enhanced for desktop
5. **Data Transparency** - Clear feedback on processing status, confidence scores visible
6. **Progressive Disclosure** - Show basic features first, advanced options on demand

### Brand Identity

**Name**: Vuva (Swahili for "discover/harvest")  
**Tagline**: "Discover News, Your Way"  
**Mission**: Democratize news access through AI-powered OCR and personalization

---

## Visual Design System

### Color Palette

#### Primary Colors
```css
--primary-blue: #2563EB;        /* Primary actions, links */
--primary-blue-dark: #1E40AF;   /* Hover states */
--primary-blue-light: #DBEAFE;  /* Backgrounds, badges */
```

#### Secondary Colors
```css
--secondary-teal: #14B8A6;      /* Success states, positive feedback */
--secondary-orange: #F59E0B;    /* Warnings, pending states */
--secondary-red: #EF4444;       /* Errors, destructive actions */
```

#### Neutral Colors
```css
--gray-50: #F9FAFB;             /* Page backgrounds */
--gray-100: #F3F4F6;            /* Card backgrounds */
--gray-200: #E5E7EB;            /* Borders */
--gray-300: #D1D5DB;            /* Disabled elements */
--gray-600: #4B5563;            /* Secondary text */
--gray-900: #111827;            /* Primary text */
--white: #FFFFFF;
--black: #000000;
```

#### Semantic Colors
```css
--success: var(--secondary-teal);
--warning: var(--secondary-orange);
--error: var(--secondary-red);
--info: var(--primary-blue);
```

### Typography

#### Font Families
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
```

#### Font Sizes
```css
--text-xs: 0.75rem;      /* 12px - Captions, labels */
--text-sm: 0.875rem;     /* 14px - Body text (small) */
--text-base: 1rem;       /* 16px - Body text */
--text-lg: 1.125rem;     /* 18px - Emphasized text */
--text-xl: 1.25rem;      /* 20px - Section headings */
--text-2xl: 1.5rem;      /* 24px - Page headings */
--text-3xl: 1.875rem;    /* 30px - Hero headings */
--text-4xl: 2.25rem;     /* 36px - Large hero text */
```

#### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Line Heights
```css
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

### Spacing Scale

```css
--space-1: 0.25rem;     /* 4px */
--space-2: 0.5rem;      /* 8px */
--space-3: 0.75rem;     /* 12px */
--space-4: 1rem;        /* 16px */
--space-5: 1.25rem;     /* 20px */
--space-6: 1.5rem;      /* 24px */
--space-8: 2rem;        /* 32px */
--space-10: 2.5rem;     /* 40px */
--space-12: 3rem;       /* 48px */
--space-16: 4rem;       /* 64px */
--space-20: 5rem;       /* 80px */
```

### Border Radius

```css
--radius-sm: 0.25rem;   /* 4px - Small elements */
--radius-md: 0.5rem;    /* 8px - Buttons, inputs */
--radius-lg: 0.75rem;   /* 12px - Cards */
--radius-xl: 1rem;      /* 16px - Modals */
--radius-full: 9999px;  /* Circular */
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
--shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
```

### Animations

```css
--transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Component Standards

### Buttons

#### Primary Button
```html
<button class="btn btn-primary">
  Upload Document
</button>
```

**Specifications**:
- Height: 40px (desktop), 48px (mobile)
- Padding: 12px 24px
- Font: 14px, medium weight
- Border radius: var(--radius-md)
- Transition: background 150ms

**States**:
- Default: Blue background, white text
- Hover: Darker blue, slight scale (1.02)
- Active: Even darker, scale (0.98)
- Disabled: Gray background, gray text, cursor not-allowed
- Loading: Spinner + "Processing..." text

#### Secondary Button
```html
<button class="btn btn-secondary">
  Cancel
</button>
```

**Specifications**:
- Same as primary but with border and transparent background
- Border: 1px solid gray-300
- Text color: gray-900
- Hover: gray-100 background

#### Icon Button
```html
<button class="btn btn-icon">
  <svg>...</svg>
</button>
```

**Specifications**:
- Size: 40x40px
- Icon size: 20x20px
- Border radius: var(--radius-md)

### Input Fields

#### Text Input
```html
<div class="input-group">
  <label for="email" class="input-label">Email Address</label>
  <input 
    type="email" 
    id="email" 
    class="input-field"
    placeholder="you@example.com"
  />
  <span class="input-hint">We'll never share your email</span>
</div>
```

**Specifications**:
- Height: 40px
- Padding: 10px 12px
- Border: 1px solid gray-300
- Border radius: var(--radius-md)
- Font size: 14px

**States**:
- Focus: Blue border, blue ring shadow
- Error: Red border, red text below
- Disabled: Gray background, not-allowed cursor
- Success: Green border (after validation)

#### File Upload
```html
<div class="file-upload">
  <input type="file" id="file" class="file-input" />
  <label for="file" class="file-label">
    <svg>Upload icon</svg>
    <span>Drop file here or click to upload</span>
    <span class="text-sm text-gray-500">PNG, JPG, PDF up to 10MB</span>
  </label>
</div>
```

**Specifications**:
- Dashed border for drop zone
- Height: 200px (desktop), 150px (mobile)
- Drag & drop support with visual feedback
- Preview thumbnail after upload

### Cards

```html
<div class="card">
  <div class="card-header">
    <h3 class="card-title">Article Title</h3>
    <span class="badge badge-info">Technology</span>
  </div>
  <div class="card-body">
    <p class="card-text">Article summary...</p>
  </div>
  <div class="card-footer">
    <button class="btn btn-text">Read More</button>
  </div>
</div>
```

**Specifications**:
- Background: white
- Border radius: var(--radius-lg)
- Shadow: var(--shadow-md)
- Padding: 20px
- Hover: Slight shadow increase

### Badges

```html
<span class="badge badge-success">Completed</span>
<span class="badge badge-warning">Processing</span>
<span class="badge badge-error">Failed</span>
```

**Specifications**:
- Height: 24px
- Padding: 4px 12px
- Font size: 12px, medium weight
- Border radius: var(--radius-full)

### Modals

```html
<div class="modal">
  <div class="modal-overlay" />
  <div class="modal-content">
    <div class="modal-header">
      <h2 class="modal-title">Confirm Action</h2>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <p>Are you sure you want to proceed?</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">Confirm</button>
    </div>
  </div>
</div>
```

**Specifications**:
- Overlay: rgba(0, 0, 0, 0.5)
- Content: Max width 500px, centered
- Animation: Fade in + scale up
- Dismiss: Click overlay, ESC key, close button

### Navigation

#### Top Navigation
```html
<nav class="navbar">
  <div class="navbar-brand">
    <img src="logo.svg" alt="Vuva" />
  </div>
  <div class="navbar-menu">
    <a href="/feed" class="navbar-item">Feed</a>
    <a href="/upload" class="navbar-item">Upload</a>
    <a href="/history" class="navbar-item">History</a>
  </div>
  <div class="navbar-actions">
    <button class="btn btn-icon">
      <svg>Notifications</svg>
    </button>
    <div class="user-menu">
      <img src="avatar.jpg" alt="User" class="avatar" />
    </div>
  </div>
</nav>
```

**Specifications**:
- Height: 64px
- Background: white
- Shadow: var(--shadow-sm)
- Sticky positioning
- Mobile: Hamburger menu

### Loading States

#### Spinner
```html
<div class="spinner">
  <svg class="spinner-icon">...</svg>
</div>
```

#### Skeleton Loader
```html
<div class="skeleton">
  <div class="skeleton-line w-full"></div>
  <div class="skeleton-line w-3/4"></div>
  <div class="skeleton-line w-1/2"></div>
</div>
```

#### Progress Bar
```html
<div class="progress">
  <div class="progress-bar" style="width: 45%"></div>
</div>
```

---

## Responsive Design

### Breakpoints

```css
--breakpoint-sm: 640px;   /* Mobile landscape */
--breakpoint-md: 768px;   /* Tablet */
--breakpoint-lg: 1024px;  /* Desktop */
--breakpoint-xl: 1280px;  /* Large desktop */
--breakpoint-2xl: 1536px; /* Extra large */
```

### Grid System

```css
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}

@media (min-width: 768px) {
  .container {
    padding: 0 24px;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 32px;
  }
}
```

### Mobile Considerations

- **Touch Targets**: Minimum 48x48px
- **Font Sizes**: Minimum 16px for body text (prevent zoom on iOS)
- **Navigation**: Bottom tab bar on mobile
- **Gestures**: Swipe support for cards, pull-to-refresh
- **Orientation**: Support both portrait and landscape

---

## Accessibility Standards

### WCAG 2.1 AA Compliance

#### Color Contrast
- **Normal text**: 4.5:1 minimum
- **Large text**: 3:1 minimum
- **UI components**: 3:1 minimum

#### Keyboard Navigation
- All interactive elements accessible via Tab
- Visual focus indicators (2px blue outline)
- Skip navigation links
- Modal trap focus
- ESC to close modals/dropdowns

#### Screen Readers
- Semantic HTML (nav, main, article, etc.)
- ARIA labels for icon buttons
- ARIA live regions for dynamic content
- Alt text for all images
- Form labels explicitly associated

#### Other Requirements
- No flashing content (seizure prevention)
- Text resizable up to 200%
- Visible focus indicators
- Consistent navigation
- Error identification and suggestions

---

## Interaction Patterns

### Feedback Timing

- **Instant** (0ms): Button press, hover states
- **Fast** (150ms): Transitions, page changes
- **Medium** (500ms): Toast notifications appearance
- **Slow** (2s): Toast auto-dismiss
- **Informative**: Progress indicators for >1s operations

### Micro-interactions

1. **Button Click**
   - Scale down on press (0.98)
   - Ripple effect from click point
   - Return to normal on release

2. **Card Hover**
   - Slight elevation increase
   - Subtle scale (1.02)
   - Shadow deepens

3. **Form Validation**
   - Real-time validation after blur
   - Checkmark animation on success
   - Shake animation on error

4. **Upload Progress**
   - Smooth progress bar fill
   - Percentage counter
   - Success animation on complete

### Error Handling

```html
<div class="toast toast-error">
  <svg class="toast-icon">Error icon</svg>
  <div class="toast-content">
    <h4 class="toast-title">Upload Failed</h4>
    <p class="toast-message">File too large. Maximum 10MB.</p>
  </div>
  <button class="toast-close">&times;</button>
</div>
```

**Error States**:
- Toast notification (non-blocking)
- Inline form errors
- Empty states with helpful actions
- 404/500 pages with navigation options

---

## Content Guidelines

### Tone of Voice

- **Friendly**: Conversational, not robotic
- **Clear**: Simple language, avoid jargon
- **Helpful**: Guide users, don't blame
- **Concise**: Respect user's time

### Writing Style

**Buttons**:
- Use verbs: "Upload Document", "Save Changes"
- Be specific: "Delete Article" not "Delete"

**Errors**:
- Explain what happened: "File too large"
- Suggest fix: "Please choose a file under 10MB"
- Avoid: "Error 400: Invalid request"

**Empty States**:
- Explain why it's empty: "You haven't uploaded any documents yet"
- Provide action: "Upload your first document to get started"
- Include illustration or icon

**Loading**:
- Be specific: "Processing image..." not "Loading..."
- Show progress when possible: "45% complete"
- Estimate time if >5s: "This usually takes 30 seconds"

---

## Dark Mode

### Color Adjustments

```css
@media (prefers-color-scheme: dark) {
  --gray-50: #18181B;
  --gray-100: #27272A;
  --gray-900: #F4F4F5;
  /* Adjust all grays */
  
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
  /* Deeper shadows */
}
```

### Implementation
- Use CSS custom properties
- Respect system preference
- Provide manual toggle
- Persist user choice
- Adjust images/illustrations

---

## Performance Standards

### Loading Targets

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

### Optimization Strategies

1. **Code Splitting**: Lazy load routes
2. **Image Optimization**: WebP, responsive images
3. **Caching**: Service worker, aggressive caching
4. **Compression**: Gzip/Brotli
5. **CDN**: Static assets on CDN
6. **Bundle Size**: Keep main bundle < 200KB

---

## Design Tokens (JSON)

```json
{
  "colors": {
    "primary": {
      "50": "#EFF6FF",
      "500": "#2563EB",
      "900": "#1E3A8A"
    },
    "gray": {
      "50": "#F9FAFB",
      "500": "#6B7280",
      "900": "#111827"
    }
  },
  "spacing": {
    "1": "0.25rem",
    "4": "1rem",
    "8": "2rem"
  },
  "fontSize": {
    "sm": "0.875rem",
    "base": "1rem",
    "xl": "1.25rem"
  }
}
```

---

## Component Library

### Recommended Stack

- **Framework**: React 18+ or Vue 3+
- **Styling**: Tailwind CSS 3+
- **Components**: Headless UI or Radix UI
- **Icons**: Heroicons or Lucide
- **Forms**: React Hook Form or Vee-Validate
- **State**: Zustand or Pinia
- **HTTP**: Axios or TanStack Query
- **Routing**: React Router or Vue Router

---

## Testing Requirements

### Visual Regression
- Chromatic or Percy
- Test all breakpoints
- Test light/dark modes

### Accessibility Testing
- axe DevTools
- WAVE
- Keyboard navigation testing

### Cross-browser
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

---

## Documentation for Developers

### Component Documentation

Each component should include:
1. **Description**: What it does
2. **Props/API**: All options with types
3. **Examples**: Common use cases
4. **Accessibility**: ARIA requirements
5. **Styling**: CSS classes available

### Storybook

All components should have Storybook stories showing:
- Default state
- All variants
- Interactive props
- Accessibility checks

---

**Maintained by**: Design Team  
**Next Review**: February 24, 2026  
**Version History**: Initial release (1.0.0)
