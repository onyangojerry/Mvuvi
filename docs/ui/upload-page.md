# Document Upload Page - UI/UX Specification

**Version**: 1.0.0  
**Last Updated**: January 24, 2026

## Overview

The Document Upload page is the core feature of Vuva, allowing users to upload images containing text and extract that text using OCR technology. This page must balance simplicity with powerful options, providing instant feedback and clear results.

---

## 1. Page Layout

**Route**: `/upload`  
**Access**: Protected (requires authentication)

### 1.1 Desktop Layout (≥1024px)

```
┌──────────────────────────────────────────────────────────────┐
│ [Top Navigation Bar]                                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────┬───────────────────────────────┐ │
│  │  Upload Area           │  Options Panel                 │ │
│  │  (Left: 60%)           │  (Right: 40%)                  │ │
│  │                        │                                │ │
│  │  [Drag & Drop Zone]    │  OCR Engine: [Dropdown]        │ │
│  │  or                    │  ○ Tesseract (Fast)            │ │
│  │  [Browse Files Button] │  ○ EasyOCR (Accurate)          │ │
│  │                        │  ○ PaddleOCR (Multilang)       │ │
│  │  [Image Preview]       │  ○ Compare All (Slower)        │ │
│  │  (if uploaded)         │                                │ │
│  │                        │  Language: [Dropdown]          │ │
│  │  [Progress Bar]        │  ☑ English                     │ │
│  │  (when processing)     │  ☐ Swahili                     │ │
│  │                        │                                │ │
│  │                        │  [Process Document Button]     │ │
│  │                        │                                │ │
│  └────────────────────────┴───────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │  Results Panel (Shown after processing)                  ││
│  │                                                           ││
│  │  ┌────────────────────┬───────────────────────────────┐ ││
│  │  │  Extracted Text    │  Stats & Actions              │ ││
│  │  │                    │                                │ ││
│  │  │  [Text Output]     │  Processing Time: 2.3s         │ ││
│  │  │                    │  Confidence: 94.2%             │ ││
│  │  │                    │  Characters: 1,234             │ ││
│  │  │                    │  Words: 215                    │ ││
│  │  │                    │                                │ ││
│  │  │                    │  [Copy Text]                   │ ││
│  │  │                    │  [Download .txt]               │ ││
│  │  │                    │  [Share]                       │ ││
│  │  │                    │  [Process Another]             │ ││
│  │  └────────────────────┴───────────────────────────────┘ ││
│  │                                                           ││
│  │  (If "Compare All" selected, show 3 tabs)                ││
│  │  [Tesseract] [EasyOCR] [PaddleOCR]                       ││
│  └──────────────────────────────────────────────────────────┘│
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Mobile Layout (<768px)

```
┌─────────────────────────────┐
│ [Top Nav - Hamburger]       │
├─────────────────────────────┤
│                             │
│ Upload Document             │
│                             │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ │  [Drag & Drop Zone]     │ │
│ │  or                     │ │
│ │  [Browse Files]         │ │
│ │  [Take Photo]           │ │ ← Mobile only
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ [Image Preview]             │
│                             │
│ OCR Engine:                 │
│ [Dropdown - Full width]     │
│                             │
│ Language:                   │
│ [Dropdown - Full width]     │
│                             │
│ [Process Button - Full]     │
│                             │
│ ─── Results ───             │
│                             │
│ [Extracted Text Area]       │
│                             │
│ [Action Buttons]            │
│                             │
└─────────────────────────────┘
```

---

## 2. Components

### 2.1 Upload Zone

**States**:

**Default (Empty) State**:
```html
<div class="upload-zone" data-state="empty">
  <div class="upload-icon">
    [📄 Upload icon - 64px]
  </div>
  <h3>Upload a Document</h3>
  <p>Drag and drop an image here, or click to browse</p>
  <p class="file-types">Supports: JPG, PNG, PDF (max 10MB)</p>
  <button class="btn btn-primary">
    Browse Files
  </button>
</div>
```

**Drag Over State**:
```html
<div class="upload-zone" data-state="drag-over">
  <div class="upload-icon active">
    [📥 Drop icon - animated]
  </div>
  <h3>Drop your file here</h3>
</div>
```

**File Selected State**:
```html
<div class="upload-zone" data-state="file-selected">
  <img src="[preview]" alt="Uploaded document" />
  <div class="file-info">
    <span class="file-name">document.jpg</span>
    <span class="file-size">2.4 MB</span>
  </div>
  <button class="btn-icon btn-remove" aria-label="Remove file">
    [✕ icon]
  </button>
</div>
```

**Uploading State**:
```html
<div class="upload-zone" data-state="uploading">
  <div class="progress-bar">
    <div class="progress-fill" style="width: 45%"></div>
  </div>
  <p>Uploading... 45%</p>
  <button class="btn-secondary btn-sm">Cancel</button>
</div>
```

**Processing State**:
```html
<div class="upload-zone" data-state="processing">
  <div class="spinner"></div>
  <h3>Processing Document...</h3>
  <p>This may take a few seconds</p>
  <div class="progress-bar indeterminate">
    <div class="progress-fill"></div>
  </div>
</div>
```

### 2.2 Options Panel

**OCR Engine Selector**:
```html
<div class="form-group">
  <label for="engine">OCR Engine</label>
  <select id="engine" class="form-select">
    <option value="tesseract" selected>Tesseract (Fast, Good)</option>
    <option value="easyocr">EasyOCR (Slower, More Accurate)</option>
    <option value="paddleocr">PaddleOCR (Multilingual)</option>
    <option value="compare">Compare All (Slowest)</option>
  </select>
  <p class="help-text">
    Tesseract is recommended for most documents
  </p>
</div>
```

**Engine Comparison Table** (shown on hover/click info icon):
| Engine | Speed | Accuracy | Languages | Best For |
|--------|-------|----------|-----------|----------|
| Tesseract | ⚡⚡⚡ | ⭐⭐⭐ | 100+ | English documents |
| EasyOCR | ⚡⚡ | ⭐⭐⭐⭐ | 80+ | High accuracy needed |
| PaddleOCR | ⚡⚡⚡ | ⭐⭐⭐⭐ | 80+ | Multilingual documents |
| Compare All | ⚡ | N/A | All | Quality comparison |

**Language Selector**:
```html
<div class="form-group">
  <label for="language">Language</label>
  <select id="language" class="form-select">
    <option value="en" selected>English</option>
    <option value="sw">Swahili</option>
    <option value="en+sw">English + Swahili</option>
  </select>
  <p class="help-text">
    Select the primary language in your document
  </p>
</div>
```

**Advanced Options** (Collapsible):
```html
<details class="advanced-options">
  <summary>Advanced Options</summary>
  <div class="options-content">
    <label class="checkbox-label">
      <input type="checkbox" id="preprocessing" />
      <span>Enable preprocessing (denoise, contrast)</span>
    </label>
    
    <label class="checkbox-label">
      <input type="checkbox" id="spellcheck" />
      <span>Enable spell checking</span>
    </label>
    
    <div class="form-group">
      <label for="dpi">DPI (Dots Per Inch)</label>
      <input 
        type="range" 
        id="dpi" 
        min="150" 
        max="600" 
        value="300" 
        step="50"
      />
      <output>300</output>
    </div>
  </div>
</details>
```

**Process Button**:
```html
<button 
  type="button" 
  class="btn btn-primary btn-block btn-large"
  disabled
  data-state="disabled"
>
  <span class="btn-text">Process Document</span>
  <span class="btn-icon">[→ icon]</span>
</button>
```

**Button States**:
- **Disabled** (no file): Gray, cursor not-allowed
- **Enabled** (file ready): Primary blue, cursor pointer
- **Processing**: Disabled, with spinner

### 2.3 Results Panel

**Text Output Area**:
```html
<div class="results-panel">
  <div class="results-header">
    <h3>Extracted Text</h3>
    <div class="results-tabs" data-mode="single">
      <!-- Only shown if "Compare All" selected -->
      <button class="tab active" data-engine="tesseract">
        Tesseract
        <span class="confidence">94.2%</span>
      </button>
      <button class="tab" data-engine="easyocr">
        EasyOCR
        <span class="confidence">96.8%</span>
      </button>
      <button class="tab" data-engine="paddleocr">
        PaddleOCR
        <span class="confidence">95.1%</span>
      </button>
    </div>
  </div>
  
  <div class="text-output">
    <textarea 
      class="text-result" 
      readonly
      rows="15"
      aria-label="Extracted text"
    >
      [Extracted text appears here...]
    </textarea>
  </div>
  
  <div class="results-stats">
    <div class="stat">
      <span class="stat-label">Processing Time</span>
      <span class="stat-value">2.34s</span>
    </div>
    <div class="stat">
      <span class="stat-label">Confidence</span>
      <span class="stat-value">94.2%</span>
    </div>
    <div class="stat">
      <span class="stat-label">Characters</span>
      <span class="stat-value">1,234</span>
    </div>
    <div class="stat">
      <span class="stat-label">Words</span>
      <span class="stat-value">215</span>
    </div>
  </div>
  
  <div class="results-actions">
    <button class="btn btn-primary">
      [📋 icon] Copy Text
    </button>
    <button class="btn btn-secondary">
      [💾 icon] Download .txt
    </button>
    <button class="btn btn-secondary">
      [🔄 icon] Process Another
    </button>
  </div>
</div>
```

**Confidence Indicator**:
- **High (>90%)**: Green badge
- **Medium (70-90%)**: Yellow badge
- **Low (<70%)**: Red badge with warning icon

```html
<div class="confidence-badge" data-level="high">
  <span class="badge badge-success">94.2% Confident</span>
</div>

<div class="confidence-badge" data-level="medium">
  <span class="badge badge-warning">⚠️ 82.1% Confident</span>
</div>

<div class="confidence-badge" data-level="low">
  <span class="badge badge-error">❗ 65.3% Confident - Results may be inaccurate</span>
</div>
```

---

## 3. Interactions

### 3.1 File Upload Flow

**Method 1: Drag & Drop**
```
User drags file over upload zone
    ↓
Zone highlights (border changes to blue, bg to blue-50)
    ↓
User drops file
    ↓
Validate file (type, size)
    ↓
If invalid: Show error toast
    ↓
If valid: 
    - Show image preview
    - Enable "Process" button
    - Pre-select recommended engine
```

**Method 2: Click to Browse**
```
User clicks "Browse Files" button
    ↓
File picker opens
    ↓
User selects file
    ↓
Same validation as drag & drop
```

**Method 3: Mobile Camera** (Mobile only)
```
User clicks "Take Photo" button
    ↓
Request camera permission
    ↓
Open device camera
    ↓
User takes photo
    ↓
Photo automatically loaded
    ↓
Preview shown
```

### 3.2 Processing Flow

```
User clicks "Process Document"
    ↓
Disable all controls
    ↓
Show processing state
    ↓
Upload file to server
    ↓
Display upload progress (0-100%)
    ↓
File uploaded
    ↓
Show "Processing..." message
    ↓
Poll status endpoint every 2s
    ↓
GET /api/v1/ingest/status/:job_id
    ↓
Status: "processing"
    ↓
Continue polling
    ↓
Status: "completed"
    ↓
Fetch results
    ↓
Display extracted text
    ↓
Show statistics
    ↓
Enable action buttons
    ↓
Scroll to results (smooth scroll)
```

### 3.3 Copy Text Action

```
User clicks "Copy Text"
    ↓
Copy text to clipboard
    ↓
Show success toast: "Text copied!"
    ↓
Button text changes to "Copied ✓" (2s)
    ↓
Revert to "Copy Text"
```

**Implementation**:
```javascript
async function copyText() {
  try {
    await navigator.clipboard.writeText(extractedText);
    showToast('Text copied to clipboard!', 'success');
    updateButtonText('Copied ✓');
    setTimeout(() => updateButtonText('Copy Text'), 2000);
  } catch (err) {
    showToast('Failed to copy text', 'error');
  }
}
```

### 3.4 Download .txt Action

```
User clicks "Download .txt"
    ↓
Create blob from text
    ↓
Generate filename: "vuva-extract-{timestamp}.txt"
    ↓
Trigger download
    ↓
Show success toast: "File downloaded!"
```

**Implementation**:
```javascript
function downloadText() {
  const blob = new Blob([extractedText], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `vuva-extract-${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('File downloaded!', 'success');
}
```

### 3.5 Process Another Action

```
User clicks "Process Another"
    ↓
Confirm: "Start over? Unsaved results will be lost."
    ↓
If confirmed:
    - Clear file input
    - Clear image preview
    - Clear results
    - Reset form
    - Scroll to top
```

---

## 4. States & Error Handling

### 4.1 File Validation Errors

| Error | Condition | Message | Action |
|-------|-----------|---------|--------|
| Invalid type | Not image/PDF | "Please upload an image (JPG, PNG) or PDF file" | Show error toast |
| File too large | > 10MB | "File is too large. Maximum size is 10MB" | Show error toast |
| Corrupt file | Cannot read | "File appears to be corrupted. Please try another file" | Show error toast |
| Empty file | Size = 0 | "File is empty. Please select a valid file" | Show error toast |

**Error Toast Component**:
```html
<div class="toast toast-error" role="alert">
  <div class="toast-icon">[❌ icon]</div>
  <div class="toast-content">
    <p class="toast-title">Upload Failed</p>
    <p class="toast-message">File is too large. Maximum size is 10MB</p>
  </div>
  <button class="toast-close" aria-label="Close">[✕]</button>
</div>
```

### 4.2 Processing Errors

| Error | Cause | Message | Action |
|-------|-------|---------|--------|
| Network error | Connection lost | "Connection error. Please check your internet and try again." | Retry button |
| Timeout | > 60s | "Processing is taking longer than expected. Please try again." | Retry button |
| OCR failed | Engine error | "Failed to extract text. The image may be too blurry or low quality." | Suggestions |
| No text found | Empty result | "No text detected in this image." | Show tips |
| Server error | 500 | "Server error. Please try again later." | Retry button |
| Rate limit | 429 | "Too many requests. Please wait 60 seconds." | Show countdown |

**Error Display**:
```html
<div class="error-state">
  <div class="error-icon">[⚠️ icon - 64px]</div>
  <h3>Failed to Extract Text</h3>
  <p>The image may be too blurry or low quality.</p>
  
  <div class="error-suggestions">
    <h4>Try these tips:</h4>
    <ul>
      <li>Ensure good lighting and focus</li>
      <li>Avoid glare and shadows</li>
      <li>Keep text horizontal and readable</li>
      <li>Use a higher resolution image</li>
    </ul>
  </div>
  
  <div class="error-actions">
    <button class="btn btn-primary">Try Again</button>
    <button class="btn btn-secondary">Upload Different File</button>
  </div>
</div>
```

### 4.3 No Text Found State

```html
<div class="empty-result-state">
  <div class="empty-icon">[🔍 icon - 64px]</div>
  <h3>No Text Detected</h3>
  <p>We couldn't find any text in this image.</p>
  
  <div class="tips-panel">
    <h4>Make sure your image:</h4>
    <ul>
      <li>Contains clearly visible text</li>
      <li>Has sufficient resolution (at least 300 DPI)</li>
      <li>Is not handwritten (only printed text supported)</li>
      <li>Has good contrast between text and background</li>
    </ul>
  </div>
  
  <button class="btn btn-primary">Upload Another Image</button>
</div>
```

---

## 5. API Integration

### 5.1 Single Engine OCR

**Endpoint**: `POST /api/v1/ocr/extract`

**Request** (multipart/form-data):
```
file: [image file]
engine: "tesseract"
language: "en"
preprocessing: true
```

**Response (200)**:
```json
{
  "job_id": "job_abc123",
  "text": "Extracted text content goes here...",
  "confidence": 94.2,
  "processing_time": 2.34,
  "metadata": {
    "engine": "tesseract",
    "language": "en",
    "image_size": "1920x1080",
    "characters": 1234,
    "words": 215,
    "lines": 45
  }
}
```

### 5.2 Fast Transcribe

**Endpoint**: `POST /api/v1/ocr/transcribe/fast`

**Request** (multipart/form-data):
```
file: [image file]
language: "en"
```

**Response (200)**:
```json
{
  "text": "Extracted text...",
  "confidence": 92.5,
  "processing_time": 1.2
}
```

### 5.3 Compare All Engines

**Endpoint**: `POST /api/v1/ocr/compare`

**Request** (multipart/form-data):
```
file: [image file]
language: "en"
```

**Response (200)**:
```json
{
  "job_id": "job_compare_xyz789",
  "results": {
    "tesseract": {
      "text": "Text from Tesseract...",
      "confidence": 94.2,
      "processing_time": 2.1
    },
    "easyocr": {
      "text": "Text from EasyOCR...",
      "confidence": 96.8,
      "processing_time": 4.5
    },
    "paddleocr": {
      "text": "Text from PaddleOCR...",
      "confidence": 95.1,
      "processing_time": 3.8
    }
  },
  "recommended": "easyocr",
  "total_time": 10.4
}
```

### 5.4 Status Polling

**Endpoint**: `GET /api/v1/ingest/status/:job_id`

**Response** (processing):
```json
{
  "job_id": "job_abc123",
  "status": "processing",
  "progress": 65,
  "message": "Extracting text..."
}
```

**Response** (completed):
```json
{
  "job_id": "job_abc123",
  "status": "completed",
  "result": {
    "text": "Extracted text...",
    "confidence": 94.2
  }
}
```

**Response** (failed):
```json
{
  "job_id": "job_abc123",
  "status": "failed",
  "error": "OCR engine error",
  "message": "Failed to extract text from image"
}
```

---

## 6. Design Specifications

### 6.1 Upload Zone

**Default State**:
- Background: gray-50
- Border: 2px dashed gray-300
- Border radius: 12px
- Padding: 48px 24px
- Text align: center

**Drag Over State**:
- Background: primary-50
- Border: 2px solid primary-500
- Transform: scale(1.02)
- Transition: all 200ms ease

**File Selected State**:
- Image preview: max-width 100%, max-height 400px
- Border: 2px solid gray-300
- Border radius: 12px

### 6.2 Progress Bar

**HTML**:
```html
<div class="progress-bar">
  <div class="progress-fill" style="width: 45%">
    <span class="progress-label">45%</span>
  </div>
</div>
```

**CSS**:
```css
.progress-bar {
  height: 8px;
  background: gray-200;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, primary-500, primary-600);
  transition: width 300ms ease;
  position: relative;
}

.progress-label {
  position: absolute;
  right: 8px;
  top: -24px;
  font-size: 12px;
  font-weight: 600;
  color: primary-600;
}
```

### 6.3 Results Panel

**Text Output**:
- Font: JetBrains Mono, monospace
- Size: 14px
- Line height: 1.6
- Background: gray-50
- Border: 1px solid gray-300
- Border radius: 8px
- Padding: 16px
- Min height: 300px

**Statistics Cards**:
- Display: inline-flex
- Padding: 12px 16px
- Background: white
- Border: 1px solid gray-200
- Border radius: 8px
- Gap: 12px

### 6.4 Mobile Adjustments

**Upload Zone** (Mobile):
- Padding: 32px 16px
- Touch target: 48px minimum
- "Take Photo" button shows camera icon

**Options Panel** (Mobile):
- Full width inputs
- Stack vertically
- Larger tap targets (48px)

**Results** (Mobile):
- Text output: font-size 16px (prevent zoom on iOS)
- Action buttons: full width, stack vertically
- Stats: 2 columns grid

---

## 7. Accessibility

### 7.1 Keyboard Navigation

- Tab through: File input → Engine select → Language select → Process button
- Enter on upload zone: Opens file picker
- Escape: Cancel upload/processing (if applicable)

### 7.2 Screen Reader Support

**Upload Zone**:
```html
<div 
  role="button"
  tabindex="0"
  aria-label="Upload document. Drag and drop or click to browse"
>
  ...
</div>
```

**Progress Bar**:
```html
<div 
  role="progressbar"
  aria-valuenow="45"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
>
  ...
</div>
```

**Results**:
```html
<div aria-live="polite" aria-atomic="true">
  <p>Text extraction complete. Confidence: 94.2%</p>
</div>
```

### 7.3 ARIA Labels

- All buttons have descriptive labels
- Form inputs have associated labels
- Status messages announced to screen readers
- Error messages associated with inputs

---

## 8. Performance Optimization

### 8.1 Image Preview

- Resize large images client-side before preview
- Use canvas to generate thumbnail
- Max preview size: 800x600px
- Compress preview to reduce memory

**Implementation**:
```javascript
function generatePreview(file) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Resize to max 800x600
        const maxWidth = 800;
        const maxHeight = 600;
        let width = img.width;
        let height = img.height;
        
        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }
        
        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(img, 0, 0, width, height);
        
        resolve(canvas.toDataURL('image/jpeg', 0.8));
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });
}
```

### 8.2 Polling Optimization

- Poll every 2s for first 10s
- Then poll every 5s
- Stop polling after 60s (timeout)
- Use exponential backoff on errors

**Implementation**:
```javascript
async function pollStatus(jobId) {
  let attempts = 0;
  const maxAttempts = 20;
  
  while (attempts < maxAttempts) {
    try {
      const response = await fetch(`/api/v1/ingest/status/${jobId}`);
      const data = await response.json();
      
      if (data.status === 'completed') {
        return data.result;
      }
      
      if (data.status === 'failed') {
        throw new Error(data.message);
      }
      
      // Adaptive polling interval
      const interval = attempts < 5 ? 2000 : 5000;
      await sleep(interval);
      attempts++;
      
    } catch (error) {
      console.error('Polling error:', error);
      throw error;
    }
  }
  
  throw new Error('Processing timeout');
}
```

---

## 9. User Education

### 9.1 Tips for Best Results

**Show on first visit** (dismissible banner):
```html
<div class="tips-banner">
  <div class="tips-icon">[💡 icon]</div>
  <div class="tips-content">
    <strong>Tips for best OCR results:</strong>
    <ul>
      <li>Use well-lit, high-resolution images</li>
      <li>Ensure text is horizontal and in focus</li>
      <li>Avoid handwritten text (printed text only)</li>
    </ul>
  </div>
  <button class="tips-close" aria-label="Close tips">[✕]</button>
</div>
```

### 9.2 Comparison Mode Tutorial

**Show when "Compare All" is selected for first time**:
```html
<div class="tutorial-modal">
  <h3>Compare All Engines</h3>
  <p>
    This mode processes your document with all three OCR engines,
    allowing you to compare results and choose the best one.
  </p>
  <p>
    <strong>Note:</strong> This will take 3x longer than single engine mode.
  </p>
  <label>
    <input type="checkbox" id="dont-show-again" />
    Don't show this again
  </label>
  <button class="btn btn-primary">Got it!</button>
</div>
```

---

## 10. Testing Checklist

### Functional Tests
- [ ] File upload (drag & drop) works
- [ ] File upload (click browse) works
- [ ] Mobile camera upload works (mobile only)
- [ ] File validation (type, size) works
- [ ] Image preview displays correctly
- [ ] Engine selection updates correctly
- [ ] Language selection works
- [ ] Process button enables/disables correctly
- [ ] Progress bar updates during upload
- [ ] Processing state displays
- [ ] Results display after completion
- [ ] Copy text to clipboard works
- [ ] Download .txt file works
- [ ] Process another resets form
- [ ] Compare mode shows all 3 results

### Error Handling Tests
- [ ] Invalid file type shows error
- [ ] File too large shows error
- [ ] Network error handled gracefully
- [ ] OCR failure shows helpful message
- [ ] No text found shows tips
- [ ] Timeout handled correctly
- [ ] Rate limit shows countdown

### Accessibility Tests
- [ ] Keyboard navigation works
- [ ] Screen reader announces states
- [ ] Focus visible on all elements
- [ ] ARIA labels present
- [ ] Color contrast passes WCAG AA

### Performance Tests
- [ ] Large images (10MB) upload smoothly
- [ ] Preview generates quickly (<1s)
- [ ] Polling doesn't degrade performance
- [ ] No memory leaks on repeated uploads

### Cross-browser Tests
- [ ] Chrome: All features work
- [ ] Firefox: All features work
- [ ] Safari: All features work
- [ ] Mobile Safari: Camera upload works
- [ ] Chrome Android: Camera upload works

---

**Maintained by**: Product & Design Team  
**Next Review**: February 14, 2026

