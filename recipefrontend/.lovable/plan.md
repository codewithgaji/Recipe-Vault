
# RecipeVault Frontend Fixes - Implementation Plan

## Overview
Fix three critical issues: broken filters, URL-based image input, and blank recipe detail modal.

## Changes to Implement

### 1. Fix API Base URL
**File:** `src/services/api.ts`

Replace localhost with a placeholder for your Railway URL:
```typescript
const API_BASE_URL = "YOUR_RAILWAY_URL";
```
You'll replace `YOUR_RAILWAY_URL` with your actual Railway backend URL.

### 2. Fix Filter/Debounce Bug  
**File:** `src/pages/Index.tsx`

- Change import from `useMemo` to `useEffect`
- Replace broken `useState` pattern with proper `useEffect` debouncing
- Ensures category and difficulty filters trigger API calls immediately

### 3. Create Image Upload Component
**New File:** `src/components/ImageUpload.tsx`

Features:
- Click to open file browser (works on mobile too)
- Drag and drop support
- Image preview before and after upload
- Upload progress indicator
- Error handling with user feedback
- Uploads directly to Cloudinary

Placeholders you'll replace:
- `YOUR_CLOUD_NAME` - Your Cloudinary cloud name
- `YOUR_UPLOAD_PRESET` - Your unsigned upload preset name

### 4. Update Recipe Form
**File:** `src/components/RecipeForm.tsx`

- Remove the text input for image URL
- Add the new ImageUpload component
- Handle the returned Cloudinary URL

### 5. Fix Recipe Detail Modal
**File:** `src/components/RecipeDetail.tsx`

- Add null/undefined checks for `ingredients` and `instructions` arrays
- Remove duplicate close button (the Dialog component already has one built-in)
- Prevent crashes when recipe data has missing fields

## File Summary

| File | Action | Purpose |
|------|--------|---------|
| `src/services/api.ts` | Modify | Update API URL placeholder |
| `src/pages/Index.tsx` | Modify | Fix debounce/filter bug |
| `src/components/ImageUpload.tsx` | Create | Cloudinary upload component |
| `src/components/RecipeForm.tsx` | Modify | Use ImageUpload instead of URL input |
| `src/components/RecipeDetail.tsx` | Modify | Add null checks, fix close button |

## After Implementation

Once I implement these changes, you'll need to:

1. **Find and replace** `YOUR_RAILWAY_URL` in `src/services/api.ts` with your Railway URL
2. **Find and replace** `YOUR_CLOUD_NAME` and `YOUR_UPLOAD_PRESET` in `src/components/ImageUpload.tsx` with your Cloudinary credentials

Alternatively, you can paste your credentials in the chat right now, and I'll include them directly in the code.

## Technical Notes

- The Cloudinary upload uses unsigned upload (no backend needed)
- Image uploads work on both desktop and mobile devices
- The filter fix ensures category/difficulty changes are instant (no debounce delay)
- Search still uses 300ms debounce to avoid excessive API calls while typing
