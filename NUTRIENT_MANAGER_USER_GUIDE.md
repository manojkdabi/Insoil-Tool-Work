# Nutrient Manager - Comprehensive User Guide

## 📖 Table of Contents

1. [Overview](#overview)
2. [Getting Started](#getting-started)
3. [Dashboard Features](#dashboard-features)
4. [Feature Walkthrough](#feature-walkthrough)
5. [Advanced Features](#advanced-features)
6. [Tips and Best Practices](#tips-and-best-practices)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)
9. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Overview

### What is Nutrient Manager?

The Nutrient Manager is a comprehensive agricultural tool that helps you:
- Calculate optimal nutrient requirements for crops
- Generate fertilization schedules based on soil test data
- Track nutrient application plans across different growth stages
- Export detailed reports in PDF and CSV formats
- Compare different nutrient plans side-by-side

### Key Benefits

✅ **Science-Based Calculations**: Uses standard RDF or soil-test crop response (STCR) methods  
✅ **Customizable Plans**: Adjust for target yield, soil conditions, and application methods  
✅ **Complete Tracking**: Monitor soil fertility status and nutrient recommendations  
✅ **Professional Reports**: Generate print-ready PDF and CSV exports  
✅ **Historical Analysis**: Save and compare multiple plans over time

---

## Getting Started

### First Time Setup

1. **Access the Module**
   - Navigate to the Nutrient Manager section in the InsoilTool dashboard
   - The module loads with a clean dashboard view

2. **Initial Configuration**
   - Select your **Client** from the dropdown
   - Choose a **Rating Scheme** (affects how soil test results are interpreted)
   - These settings persist across your session

3. **Input Soil Test Data**
   - Enter **Device ID**: Unique identifier for your soil testing device
   - Enter **Test ID**: Reference number for this specific soil test
   - Click **"Load Test"** or use the Quick Action button

### Basic Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. Load Soil Test Data  →  Device ID + Test ID        │
├─────────────────────────────────────────────────────────┤
│  2. Select Crop         →  Choose from dropdown        │
├─────────────────────────────────────────────────────────┤
│  3. Set Target Yield    →  Enter expected yield (t/ha) │
├─────────────────────────────────────────────────────────┤
│  4. Choose Method       →  RDF or STCR calculation     │
├─────────────────────────────────────────────────────────┤
│  5. Select Applications →  Soil/Fertigation/Foliar     │
├─────────────────────────────────────────────────────────┤
│  6. Calculate           →  Generate nutrient plan      │
├─────────────────────────────────────────────────────────┤
│  7. Review & Export     →  PDF, CSV, or Print         │
└─────────────────────────────────────────────────────────┘
```

---

## Dashboard Features

### Statistics Cards

The dashboard displays four key metrics at the top of the module:

#### 📋 Total Plans Created
- **What it shows**: Total number of nutrient plans you've calculated
- **Updates**: Automatically increments with each new calculation
- **Use case**: Track your overall planning activity

#### 🧮 Active Calculations
- **What it shows**: Number of plans calculated in the current session
- **Updates**: Resets when you start a new session
- **Use case**: Monitor your current work progress

#### 💰 Total Cost
- **What it shows**: Cumulative cost of fertilizers across all plans
- **Currency**: Displays in your local currency format
- **Use case**: Budget planning and cost tracking

#### 🎯 Average Yield Target
- **What it shows**: Mean target yield across all your plans
- **Units**: Tonnes per hectare (t/ha)
- **Use case**: Compare actual vs. planned yields

### Quick Actions Panel

Six one-click shortcuts for common tasks:

| Icon | Action | Description |
|------|--------|-------------|
| 🔬 | **Load Test** | Quickly load soil test data using Device ID and Test ID |
| ⚡ | **Calculate** | Fast nutrient plan calculation with current inputs |
| 📄 | **Export PDF** | Generate and download a professional PDF report |
| 📊 | **Export CSV** | Download plan data in spreadsheet format |
| 🖨️ | **Print** | Open print-optimized view for hard copies |
| 📅 | **View Schedule** | Jump directly to the application schedule tab |
| 🔍 | **Filters** | Show/hide advanced filtering options |
| ⚖️ | **Compare** | Compare two nutrient plans side-by-side |
| 🔄 | **Clear All** | Reset all inputs and start fresh (with confirmation) |
| ❓ | **Help** | Display context-sensitive help information |

---

## Feature Walkthrough

### 1. Loading Soil Test Data

**Step-by-step:**

1. Locate the **Device ID** input field in the toolbar
2. Enter your soil testing device identifier (e.g., "STD-001")
3. Enter the **Test ID** for the specific test (e.g., "TEST-20240101")
4. Click **"Load Test"** button or use the 🔬 Quick Action

**What happens:**
- System fetches soil test results from the database
- Soil nutrient values populate automatically
- Fertility status displays in the "Soil Test Summary" tab
- Context strip shows field and soil information

**Visual Feedback:**
- Loading spinner appears while fetching data
- Success toast notification confirms data loaded
- Green checkmark icon indicates successful operation

### 2. Selecting Your Crop

**Options:**

The crop dropdown includes major agricultural crops:
- Cereals: Rice, Wheat, Maize, Sorghum
- Pulses: Chickpea, Pigeon Pea, Green Gram
- Oilseeds: Groundnut, Soybean, Sunflower
- Cash Crops: Cotton, Sugarcane, Tobacco
- Vegetables: Tomato, Potato, Onion, Cabbage
- Fruits: Banana, Mango, Grapes, Citrus

**Crop-Specific Features:**
- Each crop has predefined nutrient requirement coefficients
- Growth stages are automatically configured
- Default target yields are suggested based on crop type

**Tooltip Help:**  
Hover over the crop field to see: *"Select the crop for which you want to calculate nutrient requirements"*

### 3. Setting Target Yield

**Understanding Target Yield:**

Target yield is your expected crop production per hectare.

**Input Guidelines:**
- **Units**: Tonnes per hectare (t/ha)
- **Range**: 0 to 200 t/ha (realistic agricultural range)
- **Optional**: Leave blank to use crop default
- **Precision**: Up to 2 decimal places

**Examples:**
- Rice: 5-8 t/ha (typical), 10-12 t/ha (high-yield)
- Wheat: 4-6 t/ha (typical), 8-10 t/ha (high-yield)
- Tomato: 40-60 t/ha (typical), 80-100 t/ha (greenhouse)

**Visual Validation:**
- ✅ **Green border**: Valid input within range
- ❌ **Red border**: Invalid input (negative or > 200 t/ha)
- **Tooltip**: *"Expected crop yield per hectare"*

### 4. Choosing Calculation Method

**Two Methods Available:**

#### RDF (Recommended Dose of Fertilizer)
- **Description**: Standard fertilizer dosage based on general recommendations
- **Use when**: Soil test data is unavailable or for general planning
- **Basis**: Research-based blanket recommendations for soil types
- **Pros**: Simple, widely used, well-established
- **Cons**: Doesn't account for specific soil test values

#### STCR (Soil Test Crop Response)
- **Description**: Soil-specific dosage based on actual test results
- **Use when**: You have recent soil test data
- **Basis**: Soil nutrient levels and crop response equations
- **Pros**: Precise, optimized for your specific soil
- **Cons**: Requires soil test data

**Tooltip Help:**  
*"RDF: Standard dosage | STCR: Soil-based dosage"*

**Recommendation:**  
✅ Use **STCR** for precision farming with soil test data  
✅ Use **RDF** for general planning or missing soil data

### 5. Selecting Application Types

Choose one or more application methods:

#### ☑️ Soil Application
- Direct application to soil
- Base fertilizers and top dressing
- Granular or powder forms
- **Best for**: N, P, K in field crops

#### ☑️ Fertigation
- Fertilizer through irrigation water
- Requires drip or sprinkler system
- Water-soluble fertilizers only
- **Best for**: High-value crops, vegetables, orchards

#### ☑️ Foliar Application
- Spray on leaves
- Micronutrient correction
- Quick response to deficiencies
- **Best for**: Micronutrients, emergency correction

**Note:** You can select multiple methods. The system will distribute nutrients accordingly.

### 6. Calculating Nutrient Plan

**Click "Calculate" or "Recalculate"**

**What the System Does:**

```
┌──────────────────────────────────────────────────────┐
│ 1. Validates all inputs                              │
│ 2. Retrieves soil test nutrient values              │
│ 3. Calculates nutrient requirements                 │
│ 4. Determines fertilizer recommendations            │
│ 5. Generates application schedule                   │
│ 6. Updates dashboard metrics                        │
│ 7. Saves to history automatically                   │
└──────────────────────────────────────────────────────┘
```

**Processing Time:**
- Typical: 1-3 seconds
- With complex calculations: up to 5 seconds
- Progress indicator shows during processing

**Success Indicators:**
- ✅ Green success toast: "Calculation Complete"
- Updated soil fertility summary
- Populated application schedule
- PDF preview generated

### 7. Reviewing Results

#### Soil Test Summary Tab

Displays soil fertility status for all nutrients:

| Nutrient | Available (kg/ha) | Rating | Status |
|----------|-------------------|--------|--------|
| N (Nitrogen) | 245 | Medium | 🟡 |
| P (Phosphorus) | 18.5 | High | 🟢 |
| K (Potassium) | 312 | Adequate | 🟢 |
| S (Sulfur) | 12.3 | Low | 🔴 |

**Status Badge Legend:**
- 🔴 **Low/Deficient**: Requires significant addition
- 🟡 **Medium/Moderate**: Requires moderate addition
- 🟢 **High/Adequate**: Minimal or no addition needed
- 🔵 **Sufficient**: No addition required

#### Nutrient Schedule Tab

Shows recommended nutrient quantities by growth stage:

```
Stage         | N (kg/ha) | P₂O₅ (kg/ha) | K₂O (kg/ha)
──────────────|-----------|--------------|-------------
Basal         | 40        | 30           | 25
Tillering     | 35        | 0            | 15
Panicle Init. | 30        | 0            | 15
Flowering     | 15        | 0            | 10
──────────────|-----------|--------------|-------------
Total         | 120       | 30           | 65
```

**Stage Information:**
- Each crop has 3-5 growth stages
- Timing indicated in days after planting
- Split application optimizes uptake

#### Fertilizer Schedule

Specific fertilizer products and quantities:

```
Fertilizer        | Quantity (kg/ha) | Timing
------------------|------------------|------------------
Urea              | 87               | Basal (Day 0)
DAP               | 65               | Basal (Day 0)
MOP               | 42               | Tillering (Day 30)
Urea              | 76               | Panicle (Day 60)
```

### 8. Exporting Reports

#### PDF Export 📄

**Features:**
- Professional formatted report
- Includes all plan details
- Tables, charts, and summary
- Print-ready layout

**How to Export:**
1. Click **"Export PDF"** Quick Action
2. Progress bar shows generation status
3. PDF downloads automatically
4. Filename: `nutrient_plan_{device}_{test}_{date}.pdf`

**PDF Contents:**
- Plan metadata (Device, Test, Crop, Yield)
- Soil fertility summary table
- Nutrient application schedule
- Fertilizer recommendations
- Cost summary
- Calculation date and method

#### CSV Export 📊

**Features:**
- Spreadsheet-compatible format
- All data in tabular form
- Easy to import into Excel/Sheets
- Machine-readable format

**How to Export:**
1. Click **"Export CSV"** Quick Action
2. CSV file downloads immediately
3. Filename: `nutrient_plan_{device}_{test}_{date}.csv`

**CSV Structure:**
```
Section 1: Plan Metadata (key-value pairs)
Section 2: Soil Fertility Status (table)
Section 3: Nutrient Schedule (table)
Section 4: Fertilizer Schedule (table)
Section 5: Cost Summary
```

**Use Cases:**
- Import into farm management software
- Bulk data analysis
- Historical tracking in spreadsheets
- Integration with other systems

#### Print View 🖨️

**Features:**
- Clean, professional layout
- Removes toolbars and buttons
- Shows all tabs on separate pages
- Optimized for A4/Letter paper

**How to Print:**
1. Click **"Print"** Quick Action
2. Print dialog opens automatically
3. Select printer or "Save as PDF"
4. Choose options (pages, orientation)
5. Print or save

**Print Layout:**
- Header with plan details
- Page breaks between sections
- Black borders on tables
- Readable font sizes (10-14pt)

---

## Advanced Features

### Recent Plans History

**Auto-Save Functionality:**
- Every calculated plan is automatically saved
- Maximum 10 recent plans stored
- Older plans are removed automatically (FIFO)
- Data persists across browser sessions

**Viewing Recent Plans:**

The Recent Plans panel shows:
```
┌─────────────────────────────────────────────────┐
│ Recent Plans                                     │
├─────────────────────────────────────────────────┤
│ 🌾 Wheat (STD-001 / TEST-001)                   │
│    Target: 6.5 t/ha | N:120 P:60 K:80          │
│    📅 2024-01-15 10:30 AM                       │
├─────────────────────────────────────────────────┤
│ 🌾 Rice (STD-002 / TEST-002)                    │
│    Target: 8.0 t/ha | N:150 P:75 K:90          │
│    📅 2024-01-14 03:45 PM                       │
└─────────────────────────────────────────────────┘
```

**Loading a Saved Plan:**
1. Scroll through Recent Plans panel
2. Click on any plan to load it
3. All inputs and results restore instantly
4. Continue working or export again

**Clearing History:**
- Click "Clear All" in Recent Plans panel
- Confirmation dialog prevents accidental deletion
- Action cannot be undone

### Search and Filter

**Filter Panel Options:**

#### Device/Test ID Search
- Text input accepts partial matches
- Searches both Device ID and Test ID
- Case-insensitive search
- Real-time filtering

#### Crop Filter
- Dropdown with all available crops
- Shows only plans for selected crop
- Clear option to reset

#### Date Range Filter
- From Date: Start of date range
- To Date: End of date range
- Format: YYYY-MM-DD
- Includes both boundary dates

**Using Filters:**

1. Click **🔍 Filters** Quick Action
2. Filter panel slides open
3. Enter filter criteria:
   ```
   Search: [wheat________]  (searches device/test IDs)
   
   Crop:   [Wheat       ▼]  (select crop)
   
   From:   [2024-01-01___]
   To:     [2024-01-31___]
   ```
4. Click **"Apply Filters"**
5. Results update in real-time
6. Filter count shows: "Showing 3 of 10 plans"

**Clearing Filters:**
- Click **"Clear Filters"** button
- All criteria reset to defaults
- Full plan list displays again

### Plan Comparison

**Comparing Two Plans:**

1. Click **⚖️ Compare** Quick Action
2. Comparison panel opens with two dropdowns
3. Select **Plan A** from first dropdown
4. Select **Plan B** from second dropdown
5. Click **"Compare"** button

**Comparison View:**

```
┌──────────────────────────────────────────────────────┐
│               Plan A          |        Plan B         │
├──────────────────────────────────────────────────────┤
│ Device ID    STD-001          |       STD-002         │
│ Crop         Wheat             |       Wheat           │
│ Target       6.5 t/ha          |  8.0 t/ha  (+23.1%) ⬆│
│ N Required   120 kg/ha         |  150 kg/ha (+25.0%) ⬆│
│ P Required   60 kg/ha          |  75 kg/ha  (+25.0%) ⬆│
│ K Required   80 kg/ha          |  90 kg/ha  (+12.5%) ⬆│
│ Date         2024-01-15        |       2024-01-20      │
└──────────────────────────────────────────────────────┘
```

**Difference Highlighting:**
- 🟢 **Green**: Positive difference (increase)
- 🔴 **Red**: Negative difference (decrease)
- ⬜ **Gray**: No difference
- **Percentage shown**: For numeric values

**Use Cases:**
- Compare different fields
- Analyze impact of target yield changes
- Track seasonal variations
- Optimize fertilizer usage

### Data Validation

**Real-Time Input Validation:**

The system validates inputs as you type:

#### Crop Name
- **Rule**: Must select from dropdown
- **Visual**: Green border when valid
- **Error**: Red border if invalid/empty

#### Target Yield
- **Rule**: 0-200 t/ha, numeric only
- **Visual**: Green if valid, red if invalid
- **Error Message**: "Yield must be between 0 and 200 t/ha"

#### Date Inputs
- **Rule**: YYYY-MM-DD format, valid date
- **Visual**: Red border for invalid format
- **Error Message**: "Invalid date format. Use YYYY-MM-DD"

#### Device/Test IDs
- **Rule**: Alphanumeric, hyphens, underscores only
- **Visual**: Real-time validation feedback
- **Error Message**: "Only letters, numbers, hyphens, and underscores allowed"

**Validation Triggers:**
- **On blur**: When you leave an input field
- **On submit**: Before calculation starts
- **Real-time**: As you type (for some fields)

**Benefits:**
- Prevents calculation errors
- Saves time by catching issues early
- Provides clear guidance
- Improves data quality

### Enhanced Error Handling

**User-Friendly Error Messages:**

Errors appear as prominent banners with three components:

```
┌──────────────────────────────────────────────────────┐
│ ⚠️  No Plan Available                                 │
│                                                       │
│ Please calculate a nutrient plan before exporting.   │
│                                                       │
│ 💡 Suggestion: Calculate a plan first using the      │
│    Recalculate button.                               │
│                                                   [×] │
└──────────────────────────────────────────────────────┘
```

**Components:**
1. **Title**: Brief error description
2. **Message**: Detailed explanation
3. **Suggestion**: Actionable next step (optional)
4. **Close button**: Manual dismiss option

**Auto-Dismiss:**
- Errors auto-disappear after 8 seconds
- Gives time to read without being intrusive
- Can be dismissed manually anytime

**Common Error Scenarios:**

| Error | Cause | Solution |
|-------|-------|----------|
| No Plan Available | Export attempted before calculation | Calculate plan first |
| Invalid Input | Validation failure | Correct highlighted fields |
| Missing Device ID | Required field empty | Enter Device ID |
| Load Failed | Network or data issue | Check connection, retry |
| Export Failed | File generation error | Try again or contact support |

---

## Tips and Best Practices

### For Accurate Calculations

✅ **Use Recent Soil Test Data**
- Soil test data should be < 1 year old
- Test at the same time each year
- Consistent sampling depth (0-15cm for most crops)

✅ **Set Realistic Target Yields**
- Based on historical yields
- Consider climatic conditions
- Account for irrigation availability
- Factor in crop variety potential

✅ **Choose Appropriate Method**
- **STCR**: When you have soil test data
- **RDF**: For general planning or when soil data is unavailable

✅ **Consider All Application Types**
- Soil: Primary method for most nutrients
- Fertigation: For high-value crops with drip/sprinkler
- Foliar: Supplement for micronutrients

### For Better Organization

📋 **Use Consistent Naming**
- Device IDs: Use systematic codes (e.g., FIELD-01, FIELD-02)
- Test IDs: Include date (e.g., TEST-20240115)
- Helps with searching and filtering later

📊 **Export Regularly**
- Save PDF reports for records
- Export CSV for data analysis
- Print hard copies for field reference

🔄 **Compare Plans Regularly**
- Track changes over seasons
- Optimize fertilizer costs
- Improve yield predictions

### For Cost Optimization

💰 **Split Applications**
- Reduces nutrient losses
- Improves efficiency
- Often lowers total fertilizer needed

💰 **Use Appropriate Fertilizer Types**
- Complex fertilizers for ease of application
- Straight fertilizers for flexibility
- Water-soluble for fertigation

💰 **Time Applications Well**
- Match with crop growth stages
- Consider weather patterns
- Avoid losses from rain/irrigation

### For Data Management

💾 **Regular Exports**
- Export plans to CSV monthly
- Maintain spreadsheet database
- Backup important plans

📈 **Track Performance**
- Compare planned vs. actual yields
- Record fertilizer costs
- Note any adjustments made

🔍 **Use Filters Effectively**
- Filter by crop for crop-specific analysis
- Use date ranges for seasonal tracking
- Search by field for field-specific history

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "No Data Loaded" Message

**Symptoms:**
- Soil fertility table is empty
- Cannot proceed with calculation

**Causes:**
- Device ID or Test ID not entered
- Data doesn't exist in database
- Network connection issue

**Solutions:**
1. ✅ Verify Device ID and Test ID are correct
2. ✅ Click "Load Test" button
3. ✅ Check network connection
4. ✅ Confirm test data exists in system
5. ✅ Try loading a different test

#### Issue: Calculation Not Working

**Symptoms:**
- Click Calculate but nothing happens
- Error message appears

**Causes:**
- Missing required inputs
- Invalid data in fields
- Validation errors

**Solutions:**
1. ✅ Check for red-bordered input fields
2. ✅ Ensure crop is selected
3. ✅ Verify target yield is valid (0-200 t/ha)
4. ✅ Confirm at least one application method is selected
5. ✅ Review error messages for specific guidance

#### Issue: PDF Not Downloading

**Symptoms:**
- Click Export PDF but no download starts
- Browser shows error

**Causes:**
- No plan calculated yet
- Browser popup blocker
- Insufficient permissions

**Solutions:**
1. ✅ Calculate plan first before exporting
2. ✅ Allow popups for this site
3. ✅ Check browser download settings
4. ✅ Try different browser
5. ✅ Use CSV export as alternative

#### Issue: Data Not Saving to History

**Symptoms:**
- Recent Plans panel is empty
- Plans don't persist after refresh

**Causes:**
- Browser localStorage disabled
- Private/incognito mode
- Storage quota exceeded

**Solutions:**
1. ✅ Enable localStorage in browser settings
2. ✅ Exit private browsing mode
3. ✅ Clear browser cache to free space
4. ✅ Try different browser

#### Issue: Print View Not Working

**Symptoms:**
- Print shows toolbars/buttons
- Layout is not optimized

**Causes:**
- Browser print settings
- CSS not loading

**Solutions:**
1. ✅ Use Chrome or Firefox for best results
2. ✅ Select "Print backgrounds" option
3. ✅ Choose A4 or Letter paper size
4. ✅ Try "Save as PDF" option
5. ✅ Use PDF export as alternative

#### Issue: Filter Not Working

**Symptoms:**
- Filter doesn't show results
- No plans displayed after filtering

**Causes:**
- No plans match criteria
- Invalid date format
- Empty history

**Solutions:**
1. ✅ Broaden filter criteria
2. ✅ Check date format (YYYY-MM-DD)
3. ✅ Click "Clear Filters" to reset
4. ✅ Ensure plans exist in history
5. ✅ Try searching with partial text

#### Issue: Comparison Shows No Difference

**Symptoms:**
- Comparison displays but shows all gray
- No differences highlighted

**Causes:**
- Selected the same plan twice
- Plans are identical

**Solutions:**
1. ✅ Select two different plans
2. ✅ Verify plan details in dropdowns
3. ✅ Calculate new plans with different parameters

### Browser Compatibility Issues

**Recommended Browsers:**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+ (Chromium-based)

**Known Issues:**
- ❌ Internet Explorer: Not supported
- ⚠️ Safari < 14: Limited CSS support
- ⚠️ Mobile browsers: Some features may be touch-optimized

### Performance Issues

**Slow Loading:**
1. Clear browser cache
2. Check internet connection speed
3. Close unnecessary browser tabs
4. Disable browser extensions temporarily

**Calculation Taking Long:**
1. Normal: 1-3 seconds
2. If > 10 seconds, refresh page
3. Check browser console for errors
4. Try simplified calculation (fewer application types)

---

## FAQ

### General Questions

**Q: What's the difference between RDF and STCR?**

A: **RDF (Recommended Dose of Fertilizer)** uses standard recommendations based on general soil types and crop requirements. **STCR (Soil Test Crop Response)** uses your specific soil test data to calculate precise nutrient needs. STCR is more accurate but requires soil testing.

**Q: Can I save multiple plans?**

A: Yes! The system automatically saves the last 10 plans. Older plans are removed automatically. You can export important plans as PDF or CSV for permanent storage.

**Q: How often should I update my nutrient plan?**

A: Update your plan:
- Every growing season (minimum)
- When changing crops
- After new soil tests (recommended annually)
- When changing target yields

**Q: Can I use this offline?**

A: Partially. The interface works offline, but loading soil test data and some features require internet connection. Export plans as PDF/CSV for offline reference.

### Calculation Questions

**Q: Why does my calculation show different values than expected?**

A: Calculations are based on:
- Soil test values
- Crop nutrient requirements
- Target yield
- Selected method (RDF vs STCR)
- Application types chosen

Verify all inputs are correct. STCR results vary with soil test data, while RDF uses standard values.

**Q: What if I don't know my target yield?**

A: Leave the target yield field empty. The system will use the crop's default target yield based on typical values for that crop.

**Q: Can I adjust the recommended doses?**

A: The system provides scientifically calculated recommendations. While you can note adjustments in your records, the interface shows standard calculations for consistency and accuracy.

**Q: What nutrients are included in calculations?**

A: The system calculates:
- **Macronutrients**: N (Nitrogen), P₂O₅ (Phosphorus), K₂O (Potassium)
- **Secondary nutrients**: S (Sulfur), Ca (Calcium), Mg (Magnesium)
- **Micronutrients**: Fe, Mn, Zn, Cu, B, Mo (availability depends on soil test data)

### Export Questions

**Q: What format are the PDF reports?**

A: PDF reports are A4-sized, print-ready documents with:
- Professional formatting
- Tables and data summaries
- Plan metadata and calculations
- Date and method information

**Q: Can I edit the CSV file after export?**

A: Yes! CSV files open in Excel, Google Sheets, or any spreadsheet software. You can edit, add columns, or integrate with other data. The original plan in the system remains unchanged.

**Q: How long are plans stored?**

A: In browser: Last 10 plans (localStorage)  
After export: Permanently (PDF/CSV files on your device)

**Q: Can I share plans with others?**

A: Yes, share exported PDF or CSV files via email, cloud storage, or messaging apps. The files contain all plan information.

### Technical Questions

**Q: Is my data secure?**

A: Yes. Plans are stored locally in your browser. Only exported files are saved to your device. Soil test data is retrieved from your organization's database with appropriate authentication.

**Q: What if I clear my browser data?**

A: Clearing browser data will remove your Recent Plans history. Export important plans as PDF/CSV before clearing browser data.

**Q: Can I access my plans from different devices?**

A: Plans are stored per browser/device. To access on multiple devices:
1. Export plans as PDF/CSV
2. Store in cloud service (Google Drive, Dropbox)
3. Access files from any device

**Q: What are the system requirements?**

A: 
- Modern web browser (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- JavaScript enabled
- Internet connection (for loading data)
- ~10MB free storage (for browser cache)

---

## Keyboard Shortcuts

### Navigation

| Shortcut | Action |
|----------|--------|
| `Tab` | Move to next input field |
| `Shift + Tab` | Move to previous input field |
| `Enter` | Activate focused button |
| `Esc` | Close panels/modals |

### Quick Actions

| Shortcut | Action | Description |
|----------|--------|-------------|
| `Ctrl/Cmd + L` | Load Test | Quick load test data |
| `Ctrl/Cmd + K` | Calculate | Fast calculation |
| `Ctrl/Cmd + P` | Print | Open print dialog |
| `Ctrl/Cmd + E` | Export | Export to PDF |
| `Ctrl/Cmd + F` | Filter | Toggle filter panel |
| `Ctrl/Cmd + H` | Help | Show help information |

### Browser Standard

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + S` | Save page (not recommended, use Export) |
| `Ctrl/Cmd + R` | Refresh page |
| `F5` | Refresh page |
| `Ctrl/Cmd + 0` | Reset zoom |
| `Ctrl/Cmd + +` | Zoom in |
| `Ctrl/Cmd + -` | Zoom out |

### Tips for Efficiency

**Use Tab Navigation:**
1. Enter Device ID
2. Press Tab → Enter Test ID
3. Press Tab → Select Crop
4. Press Tab → Enter Target Yield
5. Press Enter → Calculate

**Use Mouse for Quick Actions:**
- Click Quick Action buttons for common tasks
- Hover over tooltips for help
- Use dashboard metrics for overview

---

## Accessibility Features

### Screen Reader Support

✅ ARIA labels on all interactive elements  
✅ Semantic HTML structure  
✅ Descriptive button text  
✅ Form field labels properly associated

### Visual Accessibility

✅ WCAG AA compliant color contrast  
✅ Clear visual hierarchy  
✅ Color not sole means of conveying information  
✅ Status badges include text labels

### Keyboard Accessibility

✅ All features accessible via keyboard  
✅ Visible focus indicators  
✅ Logical tab order  
✅ No keyboard traps

### Responsive Design

✅ Works on all screen sizes  
✅ Touch-optimized for mobile  
✅ Readable on small screens  
✅ Adapts to portrait/landscape

---

## Getting Help

### In-App Help

Click the **❓ Help** button in Quick Actions for:
- Context-sensitive guidance
- Feature explanations
- Quick tips

### Documentation

- **This Guide**: Comprehensive usage information
- **Quick Reference**: Fast lookup guide
- **Feature List**: Complete feature catalog

### Support Channels

For technical support:
1. Check the Troubleshooting section
2. Review the FAQ
3. Contact your system administrator
4. Refer to organization's IT support

### Reporting Issues

When reporting an issue, include:
- Browser type and version
- Steps to reproduce
- Error messages (if any)
- Screenshots (if applicable)
- Device ID and Test ID (if relevant)

---

## Appendix

### Nutrient Abbreviations

| Symbol | Full Name | Notes |
|--------|-----------|-------|
| N | Nitrogen | Usually as NO₃ or NH₄ |
| P₂O₅ | Phosphorus | Measured as phosphate |
| K₂O | Potassium | Measured as potash |
| S | Sulfur | Secondary nutrient |
| Ca | Calcium | Secondary nutrient |
| Mg | Magnesium | Secondary nutrient |
| Fe | Iron | Micronutrient |
| Mn | Manganese | Micronutrient |
| Zn | Zinc | Micronutrient |
| Cu | Copper | Micronutrient |
| B | Boron | Micronutrient |
| Mo | Molybdenum | Micronutrient |

### Fertilizer Types

**Straight Fertilizers:**
- Urea (46% N)
- DAP (18% N, 46% P₂O₅)
- MOP (60% K₂O)
- SSP (16% P₂O₅)

**Complex Fertilizers:**
- NPK 10:26:26
- NPK 20:20:0
- NPK 12:32:16

**Organic:**
- FYM (Farm Yard Manure)
- Compost
- Green manure

### Growth Stages (Example: Wheat)

1. **Basal** (Day 0): Seedbed preparation
2. **Tillering** (Day 25-30): Multiple stem formation
3. **Jointing** (Day 45-50): Stem elongation
4. **Booting** (Day 60-70): Flag leaf emergence
5. **Flowering** (Day 75-85): Anthesis

Different crops have different stages and timing.

### Rating Scales

Common soil test rating scales:

| Rating | Available Nutrient Level |
|--------|--------------------------|
| Low | < 280 kg/ha (N), < 11 kg/ha (P), < 110 kg/ha (K) |
| Medium | 280-560 kg/ha (N), 11-22 kg/ha (P), 110-280 kg/ha (K) |
| High | > 560 kg/ha (N), > 22 kg/ha (P), > 280 kg/ha (K) |

*Actual thresholds vary by rating scheme and region*

### Conversion Factors

**Units:**
- 1 tonne (t) = 1000 kg
- 1 hectare (ha) = 10,000 m² = 2.47 acres
- 1 t/ha ≈ 0.446 ton/acre

**Nutrient Conversions:**
- P₂O₅ → P: multiply by 0.436
- P → P₂O₅: multiply by 2.29
- K₂O → K: multiply by 0.830
- K → K₂O: multiply by 1.205

---

**Document Version:** 1.0  
**Last Updated:** January 2025  
**Module Version:** Enhanced UI/UX v5.70

---

**End of User Guide**

For quick reference, see **NUTRIENT_MANAGER_QUICK_REFERENCE.md**  
For complete feature list, see **NUTRIENT_MANAGER_FEATURE_LIST.md**
