# ⭐ Favorites Feature - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Django development server running
- User account created and logged in
- Articles exist in the database

---

## 📋 Step-by-Step Testing

### 1. Start the Development Server

```bash
cd main
python manage.py runserver
```

Server will start at: **http://127.0.0.1:8000/**

---

### 2. Login to Your Account

1. Navigate to: **http://127.0.0.1:8000/**
2. Click **"Login"** in the header
3. Enter your credentials
4. You should see your username in the header

> **Note:** Star icons only appear when logged in!

---

### 3. Test Saving from Feed Page

1. Navigate to: **http://127.0.0.1:8000/articles/**
2. Look for **star icons** in the top-right corner of each article card
3. **Click a star icon:**
   - Star should turn **gold** (⭐)
   - No page reload
   - Instant visual feedback
4. **Click again to unsave:**
   - Star should turn **gray** (☆)
   - No page reload

**Expected behavior:**
- ✅ Star toggles between gray and gold
- ✅ No page reload
- ✅ Smooth hover effects
- ✅ Button scales on hover

---

### 4. Test Saving from Home Page

1. Navigate to: **http://127.0.0.1:8000/**
2. Scroll to the **grid of articles** below the featured article
3. Look for **star icons** in the top-right corner of grid cards
4. **Click a star icon:**
   - Star should turn **gold**
   - No page reload
5. **Click again to unsave:**
   - Star should turn **gray**

**Expected behavior:**
- ✅ Same toggle functionality as feed
- ✅ Smaller star buttons (36px)
- ✅ Consistent behavior

---

### 5. Test Saving from Article Detail Page

1. **Click on any article** to open the detail page
2. Look for the **star icon next to the article title**
3. **Click the star:**
   - Star should turn **gold**
   - **Pulse animation** should play
   - No page reload
4. **Click again to unsave:**
   - Star should turn **gray**

**Expected behavior:**
- ✅ Larger star icon (32px)
- ✅ Pulse animation on favoriting
- ✅ Hover effect with background color
- ✅ No page reload

---

### 6. View Your Favorites Page

1. Click your **username** in the header
2. Select **"Favoritos"** from the dropdown
3. Or navigate directly to: **http://127.0.0.1:8000/favorites/**

**You should see:**
- ✅ Header with "Meus Favoritos" and count
- ✅ Grid of favorited articles
- ✅ Each card shows: image, category, title, summary, author, date
- ✅ Star button on each card (filled gold)

---

### 7. Test Removing from Favorites Page

1. On the favorites page, **click a star button**
2. **Watch the animation:**
   - Card fades out
   - Card scales down
   - Card disappears
3. **If you remove all favorites:**
   - Page reloads
   - Empty state appears with message and "Explore News" button

**Expected behavior:**
- ✅ Smooth fade-out animation
- ✅ Card removed from view
- ✅ Empty state when no favorites

---

### 8. Test Empty State

1. Remove all favorites from the favorites page
2. **You should see:**
   - Large star icon
   - "Nenhum favorito ainda" message
   - "Comece a salvar artigos..." description
   - **"Explorar Notícias"** button
3. **Click "Explorar Notícias":**
   - Should navigate to feed page

---

### 9. Test Consistency Across Pages

1. **Save an article from the feed**
2. **Navigate to home page:**
   - Same article should show gold star
3. **Open the article detail:**
   - Star next to title should be gold
4. **Go to favorites page:**
   - Article should appear in the grid
5. **Remove from favorites page:**
   - Go back to feed: star should be gray
   - Go to home: star should be gray
   - Open article: star should be gray

**Expected behavior:**
- ✅ Favorite status consistent across all pages
- ✅ Changes reflect immediately everywhere

---

### 10. Test Responsive Design

#### Desktop (>1024px)
- Open in full browser window
- Favorites grid should show multiple columns
- All hover effects work

#### Tablet (768px - 1024px)
- Resize browser to ~900px width
- Favorites grid adjusts to fewer columns
- Star buttons still visible and clickable

#### Mobile (<768px)
- Resize browser to ~400px width
- Favorites grid shows 1 column
- Star buttons optimized for touch
- All functionality works

---

### 11. Test Dark Mode

1. **Toggle dark mode** (if available in your setup)
2. **Check:**
   - Star buttons have dark background
   - Text is readable
   - Shadows are visible
   - Gold stars still stand out

**Expected behavior:**
- ✅ All elements visible in dark mode
- ✅ Proper contrast maintained
- ✅ Animations work correctly

---

## 🐛 Troubleshooting

### Star icons not appearing?
- ✅ Make sure you're **logged in**
- ✅ Check browser console for errors
- ✅ Verify CSS file loaded: `/static/feed/css/style.css`

### Star not toggling?
- ✅ Check browser console for errors
- ✅ Verify CSRF token is present
- ✅ Check network tab for API request
- ✅ Ensure user is authenticated

### Favorites page empty but you have favorites?
- ✅ Refresh the page
- ✅ Check if you're logged in as the correct user
- ✅ Verify favorites exist in database

### Animations not working?
- ✅ Check if CSS file is loaded
- ✅ Clear browser cache
- ✅ Try hard refresh (Ctrl+F5)

---

## 🎯 Key URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Feed | http://127.0.0.1:8000/articles/ |
| Favorites | http://127.0.0.1:8000/favorites/ |
| Article Detail | http://127.0.0.1:8000/article/[slug]/ |
| API Endpoint | http://127.0.0.1:8000/api/favorite/toggle/[id]/ |

---

## ✅ Testing Checklist

Use this checklist to verify everything works:

- [ ] Star icons visible on feed cards (when logged in)
- [ ] Star icons visible on home grid cards (when logged in)
- [ ] Star icon visible on article detail page (when logged in)
- [ ] Clicking star on feed toggles favorite (no reload)
- [ ] Clicking star on home toggles favorite (no reload)
- [ ] Clicking star on article detail toggles favorite (no reload)
- [ ] Pulse animation plays on article detail when favoriting
- [ ] Favorites page shows all favorited articles
- [ ] Favorites page has proper grid layout
- [ ] Star button on favorites page removes article
- [ ] Card removal animation works smoothly
- [ ] Empty state appears when no favorites
- [ ] "Explorar Notícias" button works
- [ ] Favorite status consistent across all pages
- [ ] Responsive design works on mobile
- [ ] Responsive design works on tablet
- [ ] Dark mode support works correctly
- [ ] No console errors
- [ ] No broken images
- [ ] All hover effects work

---

## 🎉 Success!

If all tests pass, the favorites feature is working perfectly! Users can now:

- ⭐ Save articles from feed, home, or article detail
- 📋 View all saved articles in one place
- 🗑️ Remove articles from favorites
- 📱 Use the feature on any device
- 🌙 Enjoy it in dark mode

**Happy testing! 🚀**

