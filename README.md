This document outlines the backend development of **AetherWalls**, a minimalist dark-themed wallpaper site, including its API endpoints, database schema, and system design.

---

## **Project Overview**

**AetherWalls** is a curated collection of high-resolution, dark-themed wallpapers. The goal is to offer a sleek, immersive browsing experience for users who appreciate moody aesthetics.

**Key Features:**

- 5 thematic collections
- Dynamically generated pages per collection
- Masonry-style image layout
- Modal-based downloads with multiple resolution options
- Clean, responsive frontend

---

## **Static Frontend Setup**

**Goal:** Build a visually appealing, responsive landing page to showcase wallpaper collections with a focus on minimalism and dark aesthetics.

### Key Features:

- Fullscreen dark UI with smooth transitions
- Static wallpapers served from `/static/images/`
- Download modal supporting multiple resolutions (Original, Mobile, Tablet, 4K)
- "About" modal with credits and contact links

### File Structure (partial):

```
AetherWalls/
├── app.py                 # Main Flask app
├── static/
│   └── images/           # Uploaded wallpaper assets
├── templates/            # Jinja2 HTML templates
├── database.py           # (Optional) DB setup/utility file

```

---

## **Basic Navigation Flow**

### **Index Page (Landing)**

The landing page is mostly static and is styled around a fullscreen slider layout.

### Technologies:

- **Swiper.js** for interactive slides
- **Vanilla JS + CSS** for transitions and modals

### **Header:**

- Left: Site title (AetherWalls)
- Right: "About" button
- Layout achieved using space-between in flexbox

> TO DO: Consider adding search, theme switcher, or user login here in the future.
> 

### **Hero Section (Slider):**

- Wrapped in a `.content` tag, housing the slider container
- `.slider-wrapper` acts as the Swiper’s direct child — this is where all slides live
- Each `.swiper-slide` is an individual collection preview

### Inside Each Slide:

- Title, subtitle, description
- “Explore” button linking to that collection's page

### Slider Controls:

- Custom pagination with collection names
- JS logic to sync active slide with pagination underline

---

### **Collection Template**

Each collection has its own page, rendered dynamically by Flask using a single shared template.

### Layout:

- Simple header (same as index)
- Title & description pulled dynamically from backend
- A masonry-style **wallpaper grid**

### Wallpaper Grid:

- Responsive column layout
- Images dynamically loaded via JavaScript from `/api/wallpapers`
- Each wallpaper includes:
    - Preview image
    - Download button
    - Author info
    - Tags (shown in modal)

### Modals:

- **Download Modal**: Lets users choose resolution
- **About Modal**: Site info and contact links
- Scrollbar bug on modal was fixed with `overflow: hidden` tweak

---

## **Python Backend (Flask)**

The backend powers all dynamic content, image uploads, and API responses.

### Key Routes:

- `/` → Renders index.html
- `/collection/<collection_name>` → Renders the respective collection page
- `/upload` → Handles image uploads (POST only)
- `/api/wallpapers` → Serves JSON data of wallpapers (optionally filtered by collection)

### Upload System:

- Images uploaded via form
- Stored in `static/images/` with timestamped filenames
- Metadata (filename, tags, author, collection) stored in SQLite database

### API Endpoint:

- Returns a list of wallpapers in the requested collection
- Each item includes:
    - Filename
    - Author
    - Tags (parsed into a list)
    - Auto-generated alt text from filename

---

## Adding Authentication

First let’s try to build a authentication model in a seprate project.

## **Next Steps / Ideas**

- Add user authentication and favorite feature
- Integrate search by tags or keywords
- Allow users to submit collections
- Responsive mobile optimizations
- Admin panel for managing uploads

## Dev Notes

- All uploads must be done via POST with key `image`
- Use Postman or a file upload form to test `/upload`
- Ensure `app.py` is run from the project root to keep relative paths consistent
