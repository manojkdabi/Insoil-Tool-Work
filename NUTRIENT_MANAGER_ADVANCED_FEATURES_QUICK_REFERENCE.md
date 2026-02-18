# Nutrient Manager Advanced Features - Quick Reference

## Quick Access Guide

### 🚀 Quick Actions Panel
Located in the dashboard, provides instant access to all advanced features:

| Icon | Feature | Function |
|------|---------|----------|
| 📊 | Export CSV | Export plan data to CSV file |
| 🖨️ | Print | Clean print view of current plan |
| 🔍 | Filters | Toggle search and filter panel |
| ⚖️ | Compare | Compare two nutrient plans |

---

## Feature Usage

### 1. CSV Export 📊
**Use Case:** Export plan data for external analysis or record-keeping

**Steps:**
1. Calculate a nutrient plan
2. Click **Export CSV** button
3. File downloads automatically as `nutrient_plan_{device}_{test}_{date}.csv`

**Exports:**
- Plan metadata (Device, Test, Crop, Yield)
- Soil fertility status table
- Nutrient application schedule
- Fertilizer schedule with costs

---

### 2. Search & Filter 🔍
**Use Case:** Find specific plans in history

**Steps:**
1. Click **Filters** button to show filter panel
2. Enter search criteria:
   - **Search:** Type Device ID or Test ID
   - **Crop:** Select from dropdown
   - **Date Range:** Set From/To dates
3. Click **Apply Filters**
4. Click **Clear Filters** to reset

**Filter Options:**
- Device/Test ID text search
- Crop type dropdown
- Date range selection

---

### 3. Print View 🖨️
**Use Case:** Print or save plan as PDF

**Steps:**
1. Calculate a nutrient plan
2. Click **Print** button
3. Use browser print dialog (Ctrl/Cmd+P)
4. Select printer or "Save as PDF"

**Print Features:**
- Clean layout without UI clutter
- All tables formatted professionally
- Plan header with details
- Page breaks between sections

---

### 4. Plan Comparison ⚖️
**Use Case:** Compare two nutrient plans side-by-side

**Steps:**
1. Ensure you have at least 2 plans in history
2. Click **Compare** button
3. Select **first plan** from dropdown
4. Select **second plan** from dropdown
5. Click **Compare** button
6. View side-by-side comparison

**Comparison Shows:**
- Crop types
- Target yields
- N, P₂O₅, K₂O totals
- Percentage differences (color-coded)

**Difference Colors:**
- 🟢 Green = Positive increase
- 🔴 Red = Decrease
- ⚪ Gray = No change

---

### 5. Plan History 📋
**Use Case:** Access previously calculated plans

**How it Works:**
- Plans auto-save after calculation
- Stored in browser (localStorage)
- Maximum 10 recent plans kept
- Persists across browser sessions

**Recent Plans Panel:**
- Shows automatically when plans exist
- Click any plan to load it
- Click **Clear All** to remove history

**Each Plan Shows:**
- Device ID and Test ID
- Crop name
- Target yield
- N, P, K totals
- Date calculated

**To Load a Plan:**
1. Find plan in Recent Plans panel
2. Click on the plan
3. Plan loads automatically
4. Click "Recalculate Plan" to refresh UI

---

### 6. Error Messages ⚠️
**Use Case:** Understand what went wrong and how to fix it

**Error Banner Shows:**
- **Title:** Brief description
- **Message:** Detailed explanation
- **Suggestion:** What to do next
- **Close button:** Dismiss manually

**Common Errors:**
- "No Plan Available" → Calculate a plan first
- "Invalid Yield Target" → Enter value 0-200 t/ha
- "Selection Required" → Select plans for comparison
- "Validation Failed" → Check highlighted fields

**Auto-Dismiss:** Errors close automatically after 8 seconds

---

### 7. Input Validation ✅
**Use Case:** Ensure data quality before calculation

**Validated Fields:**

#### Device ID & Test ID
- ✅ Alphanumeric, hyphens, underscores only
- ❌ No special characters or spaces
- Visual feedback: Green (valid) / Red (invalid)

#### Crop Selection
- ✅ Must select from dropdown
- ❌ Cannot be empty
- Visual feedback on selection

#### Target Yield
- ✅ Optional field
- ✅ Range: 0-200 t/ha
- ✅ Numeric values only
- Visual feedback: Green (valid) / Red (invalid)

#### Date Inputs
- ✅ Format: YYYY-MM-DD
- ✅ Must be valid date
- Used in filter date range

**Visual Feedback:**
- 🟢 Green border = Valid input
- 🔴 Red border = Invalid input
- Error message appears with suggestion

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Print | Ctrl/Cmd + P (after clicking Print button) |
| Close Error | Click × on error banner |

---

## Tips & Best Practices

### 💡 Tips

1. **Save Important Plans**
   - Plans auto-save, but only 10 are kept
   - Export important plans to CSV for permanent records

2. **Use Filters Effectively**
   - Combine multiple filters for precise results
   - Clear filters to see all plans again

3. **Print to PDF**
   - Use browser's "Save as PDF" option
   - Creates permanent record with all formatting

4. **Compare Similar Plans**
   - Compare plans with same crop for meaningful results
   - Check percentage differences for optimization

5. **Check Validation**
   - Green borders mean data is valid
   - Fix red-bordered fields before calculating

### ⚠️ Important Notes

- **History Limit:** Only 10 most recent plans are saved
- **Browser Storage:** History is per-browser/device
- **Export First:** Export important plans before clearing history
- **Validation Required:** Cannot calculate with invalid inputs
- **LocalStorage:** If disabled, history won't work

---

## Troubleshooting

### CSV Export Issues
**Problem:** Export button does nothing
**Solution:** Ensure a plan is calculated first

**Problem:** Garbled characters in CSV
**Solution:** Open CSV in Excel/Sheets with UTF-8 encoding

### Print Issues
**Problem:** UI elements still visible
**Solution:** Use browser's print preview to verify

**Problem:** Tables cut off
**Solution:** Adjust print margins or use landscape orientation

### History Issues
**Problem:** Plans not saving
**Solution:** Check if localStorage is enabled in browser

**Problem:** History cleared unexpectedly
**Solution:** Browser cleared storage or incognito mode used

### Comparison Issues
**Problem:** Cannot select plans
**Solution:** Need at least 2 plans in history

**Problem:** No percentage shown
**Solution:** First plan value is zero (division by zero)

### Validation Issues
**Problem:** Cannot calculate plan
**Solution:** Check all red-bordered fields and fix errors

**Problem:** Yield validation fails
**Solution:** Enter value between 0-200 t/ha

---

## Feature Status

| Feature | Status | Browser Support |
|---------|--------|-----------------|
| CSV Export | ✅ Production | All browsers |
| Search/Filter | ✅ Production | All browsers |
| Print View | ✅ Production | All browsers |
| Comparison | ✅ Production | All browsers |
| History | ✅ Production | localStorage required |
| Error Handling | ✅ Production | All browsers |
| Validation | ✅ Production | All browsers |

---

## Support

### Getting Help
- Check error messages for specific guidance
- Review this quick reference guide
- See detailed documentation: `NUTRIENT_MANAGER_ADVANCED_FEATURES.md`

### Reporting Issues
If you encounter problems:
1. Note the error message
2. Record steps to reproduce
3. Check browser console for errors (F12)
4. Contact support team

---

## Version Information
**Version:** v5.70
**Last Updated:** 2024-12-19
**Module:** Nutrient Manager
**Status:** Production Ready ✅

---

## Quick Command Reference

```javascript
// Enable debug mode
window.nmSetDebugEnabled(true);

// Check plan history
console.log(window.nmPlanHistory);

// Clear history manually
localStorage.removeItem('nmPlanHistory');

// Check current plan
console.log(window.nmCurrentStages);
```

---

*For detailed technical documentation, see NUTRIENT_MANAGER_ADVANCED_FEATURES.md*
