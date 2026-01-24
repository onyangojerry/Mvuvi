# News Feed Page - UI/UX Specification

**Version**: 1.0.0  
**Last Updated**: January 24, 2026

## Overview

The News Feed page displays AI-curated news articles tailored to user preferences. It emphasizes browsability, readability, and quick access to relevant content. Users can filter, search, and discover articles effortlessly.

---

## 1. Page Layout

**Route**: `/feed`  
**Access**: Protected (requires authentication)

### 1.1 Desktop Layout (≥1024px)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [Top Navigation Bar]                               [Search] [Profile] [Menu] │
├────────────────┬─────────────────────────────────────────────────────────────┤
│                │                                                              │
│  Filters       │  Feed Header                                                │
│  (Sidebar)     │  ┌────────────────────────────────────────────────────────┐ │
│                │  │ [All News ▼] [English ▼]             [Grid] [List]      │ │
│  Categories    │  └────────────────────────────────────────────────────────┘ │
│  ☑ All         │                                                              │
│  ☐ Technology  │  ┌──────────────┬──────────────┬──────────────┐            │
│  ☐ Business    │  │ [Article 1]  │ [Article 2]  │ [Article 3]  │            │
│  ☐ Politics    │  │  [Image]     │  [Image]     │  [Image]     │            │
│  ☐ Sports      │  │  Title       │  Title       │  Title       │            │
│  ☐ Health      │  │  Summary     │  Summary     │  Summary     │            │
│  ☐ Science     │  │  Source·Date │  Source·Date │  Source·Date │            │
│  ☐ Entertainment│ └──────────────┴──────────────┴──────────────┘            │
│  ☐ World       │                                                              │
│                │  ┌──────────────┬──────────────┬──────────────┐            │
│  Language      │  │ [Article 4]  │ [Article 5]  │ [Article 6]  │            │
│  ○ All         │  │  [Image]     │  [Image]     │  [Image]     │            │
│  ○ English     │  │  Title       │  Title       │  Title       │            │
│  ○ Swahili     │  │  Summary     │  Summary     │  Summary     │            │
│                │  │  Source·Date │  Source·Date │  Source·Date │            │
│  Sort By       │  └──────────────┴──────────────┴──────────────┘            │
│  ○ Latest      │                                                              │
│  ○ Trending    │  [Load More]                                                │
│  ○ Popular     │                                                              │
│                │                                                              │
│  [Clear All]   │                                                              │
│                │                                                              │
└────────────────┴─────────────────────────────────────────────────────────────┘
```

### 1.2 Mobile Layout (<768px)

```
┌─────────────────────────────────┐
│ [☰] Vuva Feed       [🔍] [👤]  │
├─────────────────────────────────┤
│                                 │
│ [Filters Button ▼]              │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ [Article Card]              │ │
│ │ ┌─────────────────────────┐ │ │
│ │ │      [Image]            │ │ │
│ │ └─────────────────────────┘ │ │
│ │ [Tech]                      │ │
│ │ Article Title Here...       │ │
│ │ Summary text preview...     │ │
│ │ CNN · 2h ago · 5 min read   │ │
│ └─────────────────────────────┘ │
│                                 │
│ ┌─────────────────────────────┐ │
│ │ [Article Card]              │ │
│ │ ...                         │ │
│ └─────────────────────────────┘ │
│                                 │
│ [Load More]                     │
│                                 │
└─────────────────────────────────┘
```

---

## 2. Components

### 2.1 Article Card

**Grid View** (Desktop):
```html
<article class="article-card" data-layout="grid">
  <a href="/feed/:id" class="card-link">
    <div class="card-image">
      <img 
        src="article-thumbnail.jpg" 
        alt="Article thumbnail"
        loading="lazy"
      />
      <span class="category-badge badge-tech">Technology</span>
    </div>
    <div class="card-content">
      <h3 class="card-title">
        AI Breakthrough Enables Real-Time Translation
      </h3>
      <p class="card-summary">
        Researchers have developed a new AI system that can
        translate speech in real-time with 98% accuracy...
      </p>
      <div class="card-meta">
        <span class="source">TechCrunch</span>
        <span class="separator">·</span>
        <time datetime="2026-01-24T10:30:00Z">2h ago</time>
        <span class="separator">·</span>
        <span class="read-time">5 min read</span>
      </div>
    </div>
  </a>
  
  <div class="card-actions">
    <button class="btn-icon" aria-label="Bookmark">
      [🔖 icon]
    </button>
    <button class="btn-icon" aria-label="Share">
      [🔗 icon]
    </button>
  </div>
</article>
```

**List View** (Desktop):
```html
<article class="article-card" data-layout="list">
  <a href="/feed/:id" class="card-link">
    <div class="card-image">
      <img 
        src="article-thumbnail.jpg" 
        alt="Article thumbnail"
        loading="lazy"
      />
    </div>
    <div class="card-content">
      <span class="category-badge badge-tech">Technology</span>
      <h3 class="card-title">
        AI Breakthrough Enables Real-Time Translation
      </h3>
      <p class="card-summary">
        Researchers have developed a new AI system that can
        translate speech in real-time with 98% accuracy,
        marking a significant advancement in language processing...
      </p>
      <div class="card-meta">
        <span class="source">TechCrunch</span>
        <span class="separator">·</span>
        <time datetime="2026-01-24T10:30:00Z">2h ago</time>
        <span class="separator">·</span>
        <span class="read-time">5 min read</span>
      </div>
    </div>
    <div class="card-actions">
      <button class="btn-icon" aria-label="Bookmark">
        [🔖 icon]
      </button>
      <button class="btn-icon" aria-label="Share">
        [🔗 icon]
      </button>
    </div>
  </a>
</article>
```

**Mobile View**:
```html
<article class="article-card" data-layout="mobile">
  <a href="/feed/:id" class="card-link">
    <div class="card-image">
      <img 
        src="article-thumbnail.jpg" 
        alt="Article thumbnail"
        loading="lazy"
      />
    </div>
    <div class="card-content">
      <div class="card-header">
        <span class="category-badge badge-tech">Tech</span>
        <time datetime="2026-01-24T10:30:00Z">2h ago</time>
      </div>
      <h3 class="card-title">
        AI Breakthrough Enables Real-Time Translation
      </h3>
      <p class="card-summary">
        Researchers have developed a new AI system...
      </p>
      <div class="card-footer">
        <span class="source">TechCrunch</span>
        <span class="read-time">5 min</span>
      </div>
    </div>
  </a>
</article>
```

### 2.2 Category Badges

**Badge Colors** (by category):
```css
.badge-technology { background: #3B82F6; color: white; }
.badge-business { background: #10B981; color: white; }
.badge-politics { background: #8B5CF6; color: white; }
.badge-sports { background: #EF4444; color: white; }
.badge-health { background: #F59E0B; color: white; }
.badge-science { background: #14B8A6; color: white; }
.badge-entertainment { background: #EC4899; color: white; }
.badge-world { background: #6366F1; color: white; }
```

**HTML**:
```html
<span class="category-badge badge-technology">Technology</span>
```

### 2.3 Filter Sidebar

**Desktop Sidebar**:
```html
<aside class="filter-sidebar">
  <div class="filter-section">
    <h3>Categories</h3>
    <div class="filter-options">
      <label class="filter-checkbox">
        <input type="checkbox" value="all" checked />
        <span>All</span>
        <span class="count">(247)</span>
      </label>
      <label class="filter-checkbox">
        <input type="checkbox" value="technology" />
        <span>Technology</span>
        <span class="count">(45)</span>
      </label>
      <label class="filter-checkbox">
        <input type="checkbox" value="business" />
        <span>Business</span>
        <span class="count">(38)</span>
      </label>
      <!-- More categories -->
    </div>
  </div>
  
  <div class="filter-section">
    <h3>Language</h3>
    <div class="filter-options">
      <label class="filter-radio">
        <input type="radio" name="language" value="all" checked />
        <span>All Languages</span>
      </label>
      <label class="filter-radio">
        <input type="radio" name="language" value="en" />
        <span>English</span>
      </label>
      <label class="filter-radio">
        <input type="radio" name="language" value="sw" />
        <span>Swahili</span>
      </label>
    </div>
  </div>
  
  <div class="filter-section">
    <h3>Sort By</h3>
    <div class="filter-options">
      <label class="filter-radio">
        <input type="radio" name="sort" value="latest" checked />
        <span>Latest</span>
      </label>
      <label class="filter-radio">
        <input type="radio" name="sort" value="trending" />
        <span>Trending</span>
      </label>
      <label class="filter-radio">
        <input type="radio" name="sort" value="popular" />
        <span>Popular</span>
      </label>
    </div>
  </div>
  
  <button class="btn btn-secondary btn-block">
    Clear All Filters
  </button>
</aside>
```

**Mobile Filter Dropdown**:
```html
<div class="filter-dropdown">
  <button class="filter-toggle btn btn-secondary">
    <span>Filters</span>
    <span class="badge">3 active</span>
    <span class="icon">[▼ icon]</span>
  </button>
  
  <div class="filter-panel" hidden>
    <!-- Same content as desktop sidebar -->
  </div>
</div>
```

### 2.4 Search Bar

**Desktop Search**:
```html
<div class="search-bar">
  <div class="search-input-wrapper">
    <span class="search-icon">[🔍 icon]</span>
    <input 
      type="search" 
      placeholder="Search articles..." 
      aria-label="Search articles"
      autocomplete="off"
    />
    <button 
      class="clear-search" 
      aria-label="Clear search"
      hidden
    >
      [✕ icon]
    </button>
  </div>
  
  <!-- Search suggestions dropdown -->
  <div class="search-suggestions" hidden>
    <div class="suggestion-group">
      <h4>Recent Searches</h4>
      <button class="suggestion-item">
        <span class="icon">[🕐 icon]</span>
        <span>artificial intelligence</span>
      </button>
      <button class="suggestion-item">
        <span class="icon">[🕐 icon]</span>
        <span>climate change</span>
      </button>
    </div>
    <div class="suggestion-group">
      <h4>Trending</h4>
      <button class="suggestion-item">
        <span class="icon">[🔥 icon]</span>
        <span>tech layoffs 2026</span>
      </button>
    </div>
  </div>
</div>
```

### 2.5 View Toggle

```html
<div class="view-toggle" role="radiogroup" aria-label="View mode">
  <button 
    class="view-option active" 
    data-view="grid"
    role="radio"
    aria-checked="true"
  >
    <span class="icon">[Grid icon]</span>
    <span class="sr-only">Grid view</span>
  </button>
  <button 
    class="view-option" 
    data-view="list"
    role="radio"
    aria-checked="false"
  >
    <span class="icon">[List icon]</span>
    <span class="sr-only">List view</span>
  </button>
</div>
```

### 2.6 Loading States

**Skeleton Card** (while loading):
```html
<div class="article-card skeleton">
  <div class="skeleton-image"></div>
  <div class="skeleton-content">
    <div class="skeleton-text skeleton-title"></div>
    <div class="skeleton-text skeleton-summary"></div>
    <div class="skeleton-text skeleton-summary"></div>
    <div class="skeleton-meta"></div>
  </div>
</div>
```

**Infinite Scroll Spinner**:
```html
<div class="loading-more">
  <div class="spinner"></div>
  <p>Loading more articles...</p>
</div>
```

### 2.7 Empty States

**No Results** (after search/filter):
```html
<div class="empty-state">
  <div class="empty-icon">[🔍 icon - 64px]</div>
  <h3>No Articles Found</h3>
  <p>
    We couldn't find any articles matching your search or filters.
  </p>
  <div class="empty-actions">
    <button class="btn btn-primary">Clear Filters</button>
    <button class="btn btn-secondary">Browse All Articles</button>
  </div>
</div>
```

**No Feed Content** (no articles at all):
```html
<div class="empty-state">
  <div class="empty-icon">[📰 icon - 64px]</div>
  <h3>No Articles Yet</h3>
  <p>
    We're curating fresh content for you. Check back soon!
  </p>
  <button class="btn btn-primary">Refresh</button>
</div>
```

---

## 3. Interactions

### 3.1 Filter Interaction

```
User clicks category checkbox
    ↓
Update URL params: ?category=technology
    ↓
Show loading skeletons
    ↓
Fetch filtered articles
    ↓
Replace feed content
    ↓
Update article count in filter sidebar
    ↓
Scroll to top (smooth)
```

**Multiple Filters**:
- URL: `?category=technology,business&language=en&sort=latest`
- Filters combine with AND logic
- Active filters shown in "Filters" button badge (mobile)

### 3.2 Search Interaction

```
User types in search bar
    ↓
Debounce input (300ms)
    ↓
Show search suggestions dropdown
    ↓
User selects suggestion or presses Enter
    ↓
Update URL: ?q=artificial+intelligence
    ↓
Show loading state
    ↓
Fetch search results
    ↓
Display results
    ↓
Highlight search terms in titles
```

**Search Features**:
- Auto-suggestions based on trending topics
- Recent searches saved (localStorage)
- Clear search button appears when input has value
- Escape key clears search and closes suggestions

### 3.3 Infinite Scroll

```
User scrolls to bottom
    ↓
Detect when 200px from bottom
    ↓
Show "Loading more..." spinner
    ↓
Fetch next page: ?offset=20&limit=20
    ↓
Append new articles to feed
    ↓
Update offset
    ↓
Continue monitoring scroll
```

**OR Manual Load More**:
```html
<button class="btn btn-secondary btn-block load-more">
  Load More Articles
</button>
```

### 3.4 Article Card Interaction

**Click/Tap**:
- Entire card is clickable
- Navigate to article detail page `/feed/:id`
- Open in new tab: Cmd+Click (Mac) / Ctrl+Click (Win)

**Hover** (Desktop):
- Card lifts slightly: `transform: translateY(-4px)`
- Shadow increases
- Image slightly zooms: `transform: scale(1.05)`
- Transition: 200ms ease

**Bookmark**:
```
User clicks bookmark icon
    ↓
POST /api/v1/feed/:id/bookmark
    ↓
Icon changes to filled bookmark
    ↓
Show toast: "Article bookmarked"
    ↓
Add to user's bookmarks list
```

**Share**:
```
User clicks share icon
    ↓
Show share modal with options:
    - Copy link
    - Share on Twitter
    - Share on Facebook
    - Share via email
```

### 3.5 View Toggle Interaction

```
User clicks List view icon
    ↓
Save preference: localStorage.setItem('feedView', 'list')
    ↓
Animate transition (fade out, change layout, fade in)
    ↓
Re-render cards in list layout
    ↓
Update active state on toggle button
```

---

## 4. API Integration

### 4.1 Fetch Feed

**Endpoint**: `GET /api/v1/feed`

**Query Parameters**:
- `category`: string (technology, business, etc.) or comma-separated
- `language`: string (en, sw, or omit for all)
- `sort`: string (latest, trending, popular)
- `q`: string (search query)
- `offset`: number (pagination)
- `limit`: number (default: 20, max: 50)

**Request Example**:
```
GET /api/v1/feed?category=technology&language=en&sort=latest&offset=0&limit=20
```

**Response (200)**:
```json
{
  "articles": [
    {
      "id": "article_abc123",
      "title": "AI Breakthrough Enables Real-Time Translation",
      "summary": "Researchers have developed a new AI system...",
      "content": "Full article content...",
      "url": "https://example.com/article",
      "image_url": "https://example.com/image.jpg",
      "category": "technology",
      "language": "en",
      "source": {
        "name": "TechCrunch",
        "url": "https://techcrunch.com",
        "favicon": "https://techcrunch.com/favicon.ico"
      },
      "published_at": "2026-01-24T10:30:00Z",
      "read_time_minutes": 5,
      "author": "Jane Doe",
      "tags": ["AI", "translation", "machine learning"],
      "bookmarked": false
    }
    // ... more articles
  ],
  "total": 247,
  "offset": 0,
  "limit": 20,
  "has_more": true
}
```

### 4.2 Search Articles

**Endpoint**: `GET /api/v1/feed/search`

**Query Parameters**:
- `q`: string (required, min 2 characters)
- `category`: string (optional filter)
- `language`: string (optional filter)
- `offset`: number
- `limit`: number

**Request Example**:
```
GET /api/v1/feed/search?q=artificial+intelligence&limit=20
```

**Response (200)**:
```json
{
  "results": [
    {
      "id": "article_def456",
      "title": "The Future of <mark>Artificial Intelligence</mark>",
      "summary": "...<mark>Artificial intelligence</mark> is reshaping...",
      "relevance_score": 0.95,
      // ... same fields as feed article
    }
  ],
  "query": "artificial intelligence",
  "total": 42,
  "search_time_ms": 123
}
```

**Note**: Server returns `<mark>` tags around search terms for highlighting.

### 4.3 Bookmark Article

**Endpoint**: `POST /api/v1/feed/:id/bookmark`

**Response (200)**:
```json
{
  "bookmarked": true,
  "message": "Article bookmarked successfully"
}
```

**Unbookmark**: `DELETE /api/v1/feed/:id/bookmark`

### 4.4 Get Trending Topics

**Endpoint**: `GET /api/v1/feed/trending`

**Response (200)**:
```json
{
  "topics": [
    {
      "keyword": "AI regulations",
      "count": 45,
      "trend": "up"
    },
    {
      "keyword": "climate summit",
      "count": 38,
      "trend": "up"
    }
  ]
}
```

---

## 5. Design Specifications

### 5.1 Article Card (Grid View)

**Dimensions**:
- Width: 100% (container width)
- Image aspect ratio: 16:9
- Image height: 180px
- Content padding: 16px
- Card border: 1px solid gray-200
- Border radius: 12px

**Typography**:
- Title: 18px, font-weight 600, line-height 1.4, 2 lines max (ellipsis)
- Summary: 14px, font-weight 400, line-height 1.6, 3 lines max (ellipsis)
- Meta: 12px, font-weight 400, color gray-600

**Spacing**:
- Image to content: 0 (no gap)
- Title to summary: 8px
- Summary to meta: 12px

**Colors**:
- Background: white
- Border: gray-200
- Hover border: gray-300
- Shadow: 0 1px 3px rgba(0,0,0,0.1)
- Hover shadow: 0 4px 12px rgba(0,0,0,0.15)

### 5.2 Article Card (List View)

**Layout**:
- Flex direction: row
- Image width: 240px (fixed)
- Image height: 160px
- Content: flex-grow
- Padding: 16px

**Responsive** (<1024px):
- Stack vertically
- Image full width
- Image height: 200px

### 5.3 Filter Sidebar

**Dimensions**:
- Width: 240px (fixed on desktop)
- Position: sticky, top: 80px
- Background: white
- Border-right: 1px solid gray-200
- Padding: 24px 16px

**Typography**:
- Section heading: 16px, font-weight 600
- Filter label: 14px, font-weight 400
- Count: 12px, font-weight 500, color gray-500

**Spacing**:
- Between sections: 24px
- Between filters: 8px

### 5.4 Animations

**Card Hover**:
```css
.article-card {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.article-card:hover .card-image img {
  transform: scale(1.05);
  transition: transform 300ms ease;
}
```

**Skeleton Loading**:
```css
@keyframes shimmer {
  0% {
    background-position: -468px 0;
  }
  100% {
    background-position: 468px 0;
  }
}

.skeleton {
  background: linear-gradient(
    to right,
    #f0f0f0 0%,
    #e0e0e0 20%,
    #f0f0f0 40%,
    #f0f0f0 100%
  );
  background-size: 800px 104px;
  animation: shimmer 1.5s infinite linear;
}
```

**Filter Transition**:
```css
.feed-content {
  transition: opacity 300ms ease;
}

.feed-content.loading {
  opacity: 0.5;
}
```

### 5.5 Responsive Grid

**Desktop (≥1280px)**:
- 3 columns
- Gap: 24px

**Tablet (768px - 1279px)**:
- 2 columns
- Gap: 16px

**Mobile (<768px)**:
- 1 column
- Gap: 16px

**CSS Grid**:
```css
.feed-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

@media (max-width: 1279px) {
  .feed-grid {
    gap: 16px;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .feed-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## 6. Accessibility

### 6.1 Keyboard Navigation

**Tab Order**:
1. Search input
2. Filter controls
3. View toggle buttons
4. Article cards (in reading order)
5. Load more button

**Keyboard Shortcuts**:
- `/` : Focus search input
- `Escape` : Clear search, close dropdowns
- `Arrow keys` : Navigate between filter options
- `Space` : Toggle checkbox/radio
- `Enter` : Activate button, follow link

### 6.2 Screen Reader Support

**Article Card**:
```html
<article aria-label="Article: AI Breakthrough Enables Real-Time Translation">
  <a href="/feed/123">
    <img src="..." alt="AI translation visualization" />
    <h3>AI Breakthrough Enables Real-Time Translation</h3>
    <p>Researchers have developed...</p>
    <div aria-label="Published by TechCrunch, 2 hours ago, 5 minute read">
      ...
    </div>
  </a>
</article>
```

**Filter Sidebar**:
```html
<aside aria-label="Article filters">
  <h3>Categories</h3>
  <div role="group" aria-label="Filter by category">
    ...
  </div>
</aside>
```

**Loading State**:
```html
<div 
  role="status" 
  aria-live="polite" 
  aria-label="Loading articles"
>
  <span class="spinner"></span>
  <span class="sr-only">Loading more articles...</span>
</div>
```

### 6.3 ARIA Labels

- All images have alt text
- Interactive elements have aria-labels
- Loading states use aria-live
- Form controls have associated labels
- Card actions use aria-label for icon buttons

### 6.4 Focus Management

- Focus visible on all interactive elements
- Focus trap in modals
- Skip to content link
- Focus returns to trigger after modal close

---

## 7. Performance Optimization

### 7.1 Image Optimization

- Use `loading="lazy"` on all article images
- Serve WebP format with JPG fallback
- Responsive images: `srcset` for different screen sizes
- Thumbnail size: max 600x400px
- Compress images to <100KB

**Example**:
```html
<picture>
  <source 
    srcset="article-thumb.webp" 
    type="image/webp"
  />
  <img 
    src="article-thumb.jpg" 
    alt="Article thumbnail"
    loading="lazy"
    width="600"
    height="400"
  />
</picture>
```

### 7.2 Pagination Strategy

**Infinite Scroll**:
- Load 20 articles initially
- Fetch next 20 when user reaches bottom - 200px
- Cache fetched pages in memory
- Max 100 articles in DOM (virtualization after)

**Virtualization** (for 100+ articles):
- Use React Virtualized or Vue Virtual Scroller
- Only render visible articles + buffer
- Dramatically reduces DOM nodes

### 7.3 Debouncing

**Search Input**:
```javascript
const debouncedSearch = debounce((query) => {
  fetchSearchResults(query);
}, 300);

searchInput.addEventListener('input', (e) => {
  debouncedSearch(e.target.value);
});
```

**Filter Changes**:
```javascript
const debouncedFilter = debounce((filters) => {
  fetchFilteredArticles(filters);
}, 200);
```

### 7.4 Caching

**Browser Cache**:
- Cache article images (1 week)
- Cache API responses (5 minutes)
- Use service worker for offline support

**State Management**:
- Cache feed data in memory
- Invalidate on filter change
- Persist view preference (grid/list)

---

## 8. Edge Cases

### 8.1 No Internet Connection

**Detection**:
```javascript
window.addEventListener('offline', () => {
  showOfflineBanner();
});

window.addEventListener('online', () => {
  hideOfflineBanner();
  refreshFeed();
});
```

**UI**:
```html
<div class="offline-banner">
  <span class="icon">[⚠️ icon]</span>
  <span>You're offline. Showing cached articles.</span>
  <button class="btn-link">Retry</button>
</div>
```

### 8.2 Slow Network

- Show skeleton loaders immediately
- Display cached content while fetching
- Timeout after 30s with retry option

### 8.3 Very Long Titles/Summaries

- Title: max 2 lines, then ellipsis
- Summary: max 3 lines, then ellipsis
- CSS: `text-overflow: ellipsis; overflow: hidden;`

### 8.4 Missing Images

- Show placeholder image
- Fallback: colored background with first letter of title
- Log error for monitoring

**Placeholder**:
```html
<div class="image-placeholder">
  <span class="placeholder-text">A</span>
</div>
```

### 8.5 Special Characters in Search

- Sanitize input before sending to API
- Escape HTML in search results
- Handle Unicode characters correctly

---

## 9. Testing Checklist

### Functional Tests
- [ ] Feed loads with articles
- [ ] Category filters work
- [ ] Language filters work
- [ ] Sort options work
- [ ] Search returns results
- [ ] Search highlights terms
- [ ] Infinite scroll loads more
- [ ] Load more button works
- [ ] Bookmark toggles correctly
- [ ] Share modal opens
- [ ] View toggle switches layout
- [ ] Empty state shows when no results
- [ ] Error handling works

### Accessibility Tests
- [ ] Keyboard navigation works
- [ ] Screen reader announces content
- [ ] Focus visible on all elements
- [ ] ARIA labels present
- [ ] Color contrast passes WCAG AA

### Performance Tests
- [ ] Initial load <2.5s
- [ ] Infinite scroll smooth
- [ ] Images lazy load correctly
- [ ] No layout shift (CLS <0.1)
- [ ] Handles 1000+ articles

### Responsive Tests
- [ ] Desktop layout correct
- [ ] Tablet layout correct
- [ ] Mobile layout correct
- [ ] Touch targets ≥48px
- [ ] Filters work on mobile

### Edge Case Tests
- [ ] Offline mode shows banner
- [ ] Slow network shows loaders
- [ ] Long titles truncate
- [ ] Missing images have placeholder
- [ ] Special chars in search handled

---

**Maintained by**: Product & Design Team  
**Next Review**: February 14, 2026

