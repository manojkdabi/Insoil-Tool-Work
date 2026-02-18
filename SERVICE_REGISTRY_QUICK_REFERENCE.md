# Service Registry Module - Quick Reference

## 🚨 Critical Security Fixes

### XSS Prevention
Always escape user input before rendering:
```javascript
// ✅ CORRECT
element.innerHTML = `<div>${escapeHtml(userInput)}</div>`;

// ❌ WRONG
element.innerHTML = `<div>${userInput}</div>`;
```

### Input Validation
```javascript
// Ticket ID format
if (!/^[A-Za-z0-9_-]+$/.test(ticketId)) {
    showToast('Invalid ticket ID format.', 'error');
    return;
}

// File size limit
if (file.size > 10 * 1024 * 1024) {
    showToast('File size must be less than 10MB.', 'error');
    return;
}
```

---

## 📊 Dashboard Functions

### Refresh Statistics
```javascript
refreshServiceDashboard()
```
Updates all 4 metric cards with latest data.

### Toggle Filters
```javascript
toggleServiceFilters()
```
Shows/hides the advanced filter panel.

### Apply Filters
```javascript
applyServiceFilters()
```
Filters tickets by status and date range.

### Export CSV
```javascript
exportServiceRegistryCSV()
```
Downloads all service tickets as CSV file.

---

## 🎨 UI Components

### Loading Indicator
```javascript
showServiceLoading(true);  // Show spinner
showServiceLoading(false); // Hide spinner
```

### Lock/Unlock Form
```javascript
lockServiceForm(true);  // Lock with visual overlay
lockServiceForm(false); // Unlock form
```

### Toast Notifications
```javascript
showToast('Success message', 'success');
showToast('Error message', 'error');
showToast('Info message', 'info');
```

---

## ♿ Accessibility

### ARIA Labels
All buttons have descriptive labels:
```html
<button aria-label="Clear search results" onclick="clearServiceSearch()">
    Clear
</button>
```

### Keyboard Navigation
- **Tab:** Move between controls
- **Enter:** Activate buttons
- **Escape:** Close modals/dropdowns

### Focus Styles
All interactive elements show blue outline when focused (3px solid #2563eb).

---

## 📱 Responsive Design

### Breakpoints
- **Desktop:** > 768px (4-column grid)
- **Tablet:** ≤ 768px (2-column grid)
- **Mobile:** ≤ 480px (1-column grid)

### Mobile Optimizations
- Stacked layout for all sections
- Full-width buttons
- Touch-friendly 44px minimum tap targets

---

## 🔧 State Management

### Clear Search
```javascript
clearServiceSearch()
```
Resets:
- Search input value
- Autocomplete list
- Form data
- Global state variables

### Clear Form
```javascript
clearServiceForm()
```
Resets all form fields to initial state.

---

## 📝 Error Handling Best Practices

### Always Validate
```javascript
if (!element) {
    console.warn('Element not found');
    return;
}
```

### Use Try-Catch
```javascript
try {
    // Risky operation
} catch (err) {
    console.error('Operation failed:', err);
    showToast('Operation failed. Please try again.', 'error');
}
```

### Provide User Feedback
```javascript
// ✅ GOOD
showToast('File uploaded successfully', 'success');

// ❌ BAD
// Silent success
```

---

## 🎯 Common Tasks

### Add New Statistic Card
1. Add HTML in dashboard section
2. Update `calculateServiceStats()`
3. Update `refreshServiceDashboard()`

### Add New Filter
1. Add control in `service-filters-panel`
2. Update `applyServiceFilters()` logic
3. Add validation if needed

### Customize Colors
Edit inline styles in stat cards:
```html
background: linear-gradient(135deg, #START 0%, #END 100%);
```

---

## 🐛 Troubleshooting

### Dashboard Not Showing
- Check if `refreshServiceDashboard()` is called
- Verify element IDs: `svc-stat-total`, `svc-stat-open`, etc.

### Filters Not Working
- Check if filter panel is visible
- Verify filter IDs: `svc-filter-status`, `svc-filter-date-from`, etc.
- Check console for validation errors

### Form Locked Accidentally
- Check `svc-status` value (RESOLVED locks form)
- Use `lockServiceForm(false)` to unlock

### CSV Export Empty
- Verify data source is populated
- Check console for export errors
- Ensure CSV headers match data structure

---

## 📚 Function Reference

### Security Functions
| Function | Purpose |
|----------|---------|
| `escapeHtml(value)` | Escape HTML entities |
| `submitServiceForm()` | Validate and submit form |

### Dashboard Functions
| Function | Purpose |
|----------|---------|
| `refreshServiceDashboard()` | Update statistics |
| `calculateServiceStats()` | Get statistics data |
| `toggleServiceFilters()` | Show/hide filters |
| `applyServiceFilters()` | Apply filter criteria |
| `exportServiceRegistryCSV()` | Export to CSV |

### UI Functions
| Function | Purpose |
|----------|---------|
| `showServiceLoading(bool)` | Show/hide loading |
| `lockServiceForm(bool)` | Lock/unlock form |
| `showToast(msg, type)` | Show notification |
| `clearServiceSearch()` | Clear search state |
| `renderServiceHistoryTable(data)` | Display history |

### Helper Functions
| Function | Purpose |
|----------|---------|
| `updateServiceSummary(device, ticket)` | Update summary cards |
| `processServiceConfig(data)` | Process config data |
| `renderStatusDisplay(status)` | Update status badge |

---

## 🔑 Key Improvements

### Security
- ✅ XSS protection with escapeHtml()
- ✅ Input validation on all forms
- ✅ File size limits enforced
- ✅ Format validation for ticket IDs

### UX
- ✅ Modern dashboard with statistics
- ✅ Advanced filtering system
- ✅ CSV export functionality
- ✅ Loading states and feedback
- ✅ Toast notifications instead of alerts

### Accessibility
- ✅ ARIA labels on all controls
- ✅ Keyboard navigation support
- ✅ WCAG AA color contrast
- ✅ Screen reader compatible

### Responsive
- ✅ Mobile-first design
- ✅ Breakpoints at 768px and 480px
- ✅ Touch-friendly controls
- ✅ Adaptive layouts

---

## 💡 Tips

1. **Always validate before submitting**
2. **Use showToast() instead of alert()**
3. **Escape all user input with escapeHtml()**
4. **Test on mobile devices regularly**
5. **Check console for warnings/errors**
6. **Use loading states for async operations**
7. **Provide clear error messages**
8. **Keep functions small and focused**

---

**Document Version:** 1.0  
**Last Updated:** February 18, 2026  
**Quick Access:** Keep this handy for daily development!
