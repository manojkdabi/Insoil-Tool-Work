# Insoil Tool - UI Theme Standardization Mockups

This directory contains HTML mockups demonstrating the proposed unified theme for the Insoil Tool application.

## Overview

These mockups showcase a professional, cohesive design system that standardizes colors, components, spacing, and visual hierarchy across all modules.

## Mockup Files

### 1. `design-system.html`
**Complete Design System Reference**

Comprehensive guide showing:
- Unified color palette (primary, secondary, status colors)
- Button styles and variations
- Card components
- Badge designs
- Table styling
- 8px spacing system

**Key Features:**
- Professional blue (#2563eb) as primary color
- Modern teal (#14b8a6) as secondary/accent
- Consistent status colors (success, warning, danger, info)
- Neutral gray scale for text and backgrounds
- Interactive hover states and shadows

### 2. `dashboard-mockup.html`
**Dashboard Module - Improved**

Demonstrates:
- Standardized stat cards with left border accents
- Consistent icon treatments with subtle backgrounds
- Unified info cards with proper hierarchy
- Professional sidebar navigation
- Clean, modern aesthetics

**Improvements from Current:**
- Unified card design with consistent shadows and borders
- Color-coded left borders instead of random colored boxes
- Better typography hierarchy
- Consistent spacing using 8px grid
- Hover animations for better interactivity

### 3. `data-table-mockup.html`
**RGB/Abs & Device Modules - Improved**

Demonstrates:
- Clean, modern table design
- Consistent action button styling
- Professional toolbar with unified buttons
- Tab navigation with active states
- Pagination controls

**Improvements from Current:**
- Unified button colors (no more orange/gray/purple mix)
- Consistent table styling with hover states
- Better visual hierarchy in toolbars
- Cleaner, more professional appearance
- Standardized spacing and borders

### 4. `soil-test-results-mockup.html`
**Soil Test Results - Improved**

Demonstrates:
- FAIL row highlighting with subtle background color
- Consistent status badges
- Professional download buttons
- Clean table design
- Toggle switch component

**Improvements from Current:**
- Subtle row highlighting for FAIL items instead of harsh red backgrounds
- Consistent button styling
- Better visual distinction between pass/fail
- Professional color treatment
- Improved readability

## Design System Key Elements

### Color Palette

#### Primary
- **Primary**: `#2563eb` (Professional Blue)
- **Primary Hover**: `#1d4ed8`
- **Primary Light**: `#3b82f6`
- Used for: Main actions, active states, primary CTAs

#### Secondary
- **Secondary**: `#14b8a6` (Modern Teal)
- **Secondary Hover**: `#0d9488`
- Used for: Secondary actions, info states, accents

#### Status Colors
- **Success**: `#10b981` (Green) - Positive actions, pass states
- **Warning**: `#f59e0b` (Amber) - Attention items, warnings
- **Danger**: `#ef4444` (Red) - Destructive actions, fail states
- **Info**: `#3b82f6` (Blue) - Informational elements

#### Neutrals
- **Gray Scale**: `#f9fafb` → `#111827`
- Used for: Text, borders, backgrounds, shadows

### Spacing System (8px Grid)
- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px

### Border Radius
- `sm`: 4px - Small elements
- Default: 8px - Most components
- `lg`: 12px - Cards, large containers
- `xl`: 16px - Modal dialogs
- `full`: 9999px - Pills, badges

### Shadows
- **sm**: Subtle - For minor elevation
- **default**: Standard - For cards, buttons
- **md**: Medium - For elevated components
- **lg**: Large - For modals, dropdowns

### Typography
- **Font Family**: Inter, system fonts fallback
- **Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Sizes**: Responsive scale from 0.75rem to 2.5rem

## Component Standards

### Buttons
- **Primary**: Blue background, white text
- **Secondary**: Teal background, white text
- **Success**: Green background, white text
- **Warning**: Amber background, white text
- **Danger**: Red background, white text
- **Outline**: Transparent with blue border

All buttons have:
- 10px vertical, 20px horizontal padding
- 8px border radius
- Hover: translateY(-1px) + shadow
- Consistent font weight (500)

### Cards
- White background
- 12px border radius
- Subtle shadow
- 24px padding
- 4px colored left border for categorization
- Hover: translateY(-2px) + stronger shadow

### Badges
- Rounded pill shape (border-radius: 9999px)
- Light background with darker text (same color family)
- Uppercase text with letter spacing
- Small, compact size (0.75rem)

### Tables
- White background in card container
- Gray header background
- 1px light borders between rows
- Hover: Light gray background
- Consistent padding (16px)
- Uppercase header text

## How to View Mockups

1. Open any HTML file in a modern web browser
2. Files are standalone - no build process needed
3. Use browser dev tools to inspect styles
4. Resize window to test responsive behavior

## Implementation Notes

### CSS Variables
All mockups use CSS custom properties (variables) for easy theming:
```css
:root {
  --primary: #2563eb;
  --secondary: #14b8a6;
  --success: #10b981;
  /* etc... */
}
```

### Consistency Guidelines
1. **Always use CSS variables** instead of hardcoded colors
2. **Follow the 8px spacing grid** for all margins and padding
3. **Use standard border radius** values (4px, 8px, 12px)
4. **Apply hover states** to interactive elements
5. **Maintain consistent shadows** across similar components

### Accessibility
- Sufficient color contrast ratios (WCAG AA compliant)
- Hover states for all interactive elements
- Focus states for keyboard navigation
- Semantic HTML structure
- Proper heading hierarchy

## Benefits of Standardization

1. **Professional Appearance**: Consistent, polished look across all modules
2. **Better UX**: Predictable interaction patterns and visual hierarchy
3. **Maintainability**: Single source of truth for colors and spacing
4. **Scalability**: Easy to extend with new components
5. **Brand Identity**: Cohesive visual language
6. **Accessibility**: Better contrast and readability
7. **Development Speed**: Reusable components and patterns

## Next Steps

1. Review mockups with stakeholders
2. Gather feedback on color choices and component designs
3. Create implementation plan for applying to actual codebase
4. Build component library based on these patterns
5. Document usage guidelines for development team

## Questions or Feedback?

Please review these mockups and provide feedback on:
- Color palette preferences
- Component styling
- Any specific module requirements
- Accessibility concerns
- Additional components needed

---

**Created**: February 2026  
**Purpose**: UI Theme Standardization Initiative  
**Status**: Mockup/Proposal Phase
