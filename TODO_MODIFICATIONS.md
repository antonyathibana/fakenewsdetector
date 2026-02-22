# TODO: Fake News Detection - Remove URL Feature

## Progress Tracker

- [x] Review and analyze all relevant files
- [x] Create plan for modifications
- [x] Get user approval for plan
- [x] Update index.html - Remove URL option
- [x] Update history.html - Fix table layout
- [x] Update app.py - Remove URL logic
- [x] Update style.css - Add table-container class

## Implementation Steps

### 1. index.html ✅
- [x] Remove "From URL" button
- [x] Remove hidden input_type field
- [x] Remove URL input section
- [x] Keep only textarea with name="news_text"
- [x] Update form to method="POST" action="{{ url_for('predict') }}"
- [x] Remove JavaScript for input type switching
- [x] Remove Type column from Recent Predictions table

### 2. history.html ✅
- [x] Wrap table in <div class="table-container">
- [x] Reduce text preview max-width to 300px with ellipsis
- [x] Remove Type column

### 3. app.py ✅
- [x] Remove extract_text_from_url() function
- [x] Remove BeautifulSoup and requests imports (kept requests for fact check API)
- [x] Clean up /predict route - remove URL logic

### 4. style.css ✅
- [x] Add .table-container { overflow-x: auto; } class
- [x] Add table-layout: auto; width: 100%; to table

