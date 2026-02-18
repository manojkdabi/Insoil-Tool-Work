# Analytics Module Enhancement - Quick Start Guide

## Introduction

This guide provides step-by-step instructions to implement the analytics module improvements for the Insoil Tool. The enhancements are organized into phases for manageable implementation.

---

## Prerequisites

### Skills Required
- JavaScript (ES6+)
- HTML/CSS
- Chart.js library
- Google Apps Script (for backend)

### Tools Needed
- Code editor (VS Code recommended)
- Git for version control
- Browser developer tools for testing

---

## Phase 1: Quick Wins (Week 1-2)

### 1.1 Statistical Summary Panel

**Time Estimate:** 4-6 hours

**Steps:**

1. **Add HTML Structure** (in frontend file, after line 7996):

```html
<!-- Statistical Summary Panel -->
<div id="stats-summary-panel" class="section" style="margin-bottom: 24px;">
    <div class="section-header">
        <h3>📊 Statistical Summary</h3>
        <button onclick="toggleStatsPanel()" class="btn-toggle">
            <span id="stats-toggle-icon">▼</span>
        </button>
    </div>
    <div id="stats-grid" class="stats-grid"></div>
</div>
```

2. **Add CSS Styles** (add to <style> section around line 3286):

```css
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-top: 16px;
}

.stat-card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.stat-card h4 {
    font-size: 12px;
    color: #64748b;
    margin-bottom: 8px;
    text-transform: uppercase;
}

.stat-value-main {
    font-size: 28px;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 4px;
}

.stat-label {
    font-size: 11px;
    color: #94a3b8;
}

.stat-details {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #e2e8f0;
}
```

3. **Add JavaScript Functions** (add near updateAnalyticsCharts function around line 20669):

```javascript
function calculateStatistics(data, paramKey) {
    const values = data
        .map(row => parseFloat(row[paramKey]))
        .filter(v => !isNaN(v) && v !== null);
    
    if (values.length === 0) {
        return null;
    }
    
    values.sort((a, b) => a - b);
    
    const sum = values.reduce((a, b) => a + b, 0);
    const mean = sum / values.length;
    
    const median = values.length % 2 === 0
        ? (values[values.length / 2 - 1] + values[values.length / 2]) / 2
        : values[Math.floor(values.length / 2)];
    
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
    const stdDev = Math.sqrt(variance);
    
    return {
        count: values.length,
        min: values[0],
        max: values[values.length - 1],
        mean: mean,
        median: median,
        stdDev: stdDev,
        q1: values[Math.floor(values.length * 0.25)],
        q3: values[Math.floor(values.length * 0.75)]
    };
}

function renderStatisticsSummary(data) {
    const statsGrid = document.getElementById('stats-grid');
    if (!statsGrid || !data || data.length === 0) return;
    
    const params = getSelectedAnalyticsParams();
    
    statsGrid.innerHTML = '';
    
    params.forEach(param => {
        const stats = calculateStatistics(data, param.k);
        
        if (!stats) return;
        
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
            <h4>${param.label}</h4>
            <div class="stat-value-main">${stats.mean.toFixed(2)}</div>
            <div class="stat-label">Mean Value</div>
            <div class="stat-details">
                <div>
                    <div class="stat-label">Min</div>
                    <div style="font-weight: 600;">${stats.min.toFixed(2)}</div>
                </div>
                <div>
                    <div class="stat-label">Max</div>
                    <div style="font-weight: 600;">${stats.max.toFixed(2)}</div>
                </div>
                <div>
                    <div class="stat-label">Median</div>
                    <div style="font-weight: 600;">${stats.median.toFixed(2)}</div>
                </div>
                <div>
                    <div class="stat-label">Std Dev</div>
                    <div style="font-weight: 600;">${stats.stdDev.toFixed(2)}</div>
                </div>
            </div>
        `;
        
        statsGrid.appendChild(card);
    });
}

function toggleStatsPanel() {
    const grid = document.getElementById('stats-grid');
    const icon = document.getElementById('stats-toggle-icon');
    
    if (grid.style.display === 'none') {
        grid.style.display = 'grid';
        icon.textContent = '▼';
    } else {
        grid.style.display = 'none';
        icon.textContent = '▶';
    }
}
```

4. **Integrate with updateAnalyticsCharts** (modify existing function around line 20669):

```javascript
// Add this line at the end of updateAnalyticsCharts() function
renderStatisticsSummary(rows);
```

---

### 1.2 CSV Export Functionality

**Time Estimate:** 3-4 hours

**Steps:**

1. **Add Export Button** (in toolbar around line 8008):

```html
<button class="btn btn-teal" onclick="exportAnalyticsData('csv')">
    💾 Export CSV
</button>
```

2. **Add Export Function**:

```javascript
function exportAnalyticsData(format) {
    const device = document.getElementById('an-device').value;
    const dateFrom = document.getElementById('an-date-from').value;
    const dateTo = document.getElementById('an-date-to').value;
    const params = getSelectedAnalyticsParams();
    
    if (!device) {
        alert('Please select a device first');
        return;
    }
    
    // Filter data
    const filteredData = rgbData.filter(row => {
        const deviceMatch = row.device_id === device || 
                           row.deviceId === device ||
                           row['Device ID'] === device;
        
        if (!deviceMatch) return false;
        
        const rowDate = new Date(row.timestamp || row.Timestamp);
        const fromDate = dateFrom ? new Date(dateFrom) : new Date(0);
        const toDate = dateTo ? new Date(dateTo) : new Date();
        
        return rowDate >= fromDate && rowDate <= toDate;
    });
    
    if (filteredData.length === 0) {
        alert('No data to export');
        return;
    }
    
    if (format === 'csv') {
        exportToCSV(filteredData, params, device, dateFrom, dateTo);
    } else if (format === 'json') {
        exportToJSON(filteredData, params, device, dateFrom, dateTo);
    }
}

function exportToCSV(data, params, device, dateFrom, dateTo) {
    // Build CSV header
    const headers = ['Timestamp', 'Device ID', ...params.map(p => p.label)];
    let csv = headers.join(',') + '\n';
    
    // Build CSV rows
    data.forEach(row => {
        const values = [
            row.timestamp || row.Timestamp || '',
            row.device_id || row.deviceId || row['Device ID'] || '',
            ...params.map(p => {
                const val = row[p.k] || row[p.label] || '';
                return typeof val === 'number' ? val.toFixed(2) : val;
            })
        ];
        csv += values.join(',') + '\n';
    });
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `insoil_analytics_${device}_${dateFrom}_${dateTo}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
}

function exportToJSON(data, params, device, dateFrom, dateTo) {
    const exportData = {
        metadata: {
            device: device,
            dateRange: { from: dateFrom, to: dateTo },
            exportDate: new Date().toISOString(),
            recordCount: data.length
        },
        data: data
    };
    
    const json = JSON.stringify(exportData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `insoil_analytics_${device}_${dateFrom}_${dateTo}.json`;
    link.click();
    window.URL.revokeObjectURL(url);
}
```

---

### 1.3 Threshold Indicators (Basic)

**Time Estimate:** 4-5 hours

**Steps:**

1. **Define Threshold Configuration**:

```javascript
// Add near top of analytics section (around line 20640)
const PARAMETER_THRESHOLDS = {
    pH: { min: 5.5, max: 7.5, optimal: [6.0, 7.0], unit: '' },
    Moisture: { min: 20, max: 80, optimal: [40, 60], unit: '%' },
    Temperature: { min: 10, max: 35, optimal: [20, 28], unit: '°C' },
    EC: { min: 0.5, max: 4.0, optimal: [1.0, 2.5], unit: 'dS/m' },
    'Ammonium-N': { min: 0, max: 100, optimal: [10, 40], unit: 'mg/kg' },
    'Nitrate-N': { min: 0, max: 100, optimal: [20, 50], unit: 'mg/kg' }
};
```

2. **Add Threshold Visualization to Charts**:

```javascript
function addThresholdAnnotations(chartConfig, paramKey) {
    const threshold = PARAMETER_THRESHOLDS[paramKey];
    if (!threshold) return chartConfig;
    
    // Add Chart.js annotation plugin configuration
    if (!chartConfig.options.plugins) {
        chartConfig.options.plugins = {};
    }
    
    chartConfig.options.plugins.annotation = {
        annotations: {
            minLine: {
                type: 'line',
                yMin: threshold.min,
                yMax: threshold.min,
                borderColor: 'rgba(239, 68, 68, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                label: {
                    content: `Min: ${threshold.min}${threshold.unit}`,
                    enabled: true,
                    position: 'start',
                    backgroundColor: 'rgba(239, 68, 68, 0.8)'
                }
            },
            maxLine: {
                type: 'line',
                yMin: threshold.max,
                yMax: threshold.max,
                borderColor: 'rgba(239, 68, 68, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                label: {
                    content: `Max: ${threshold.max}${threshold.unit}`,
                    enabled: true,
                    position: 'end',
                    backgroundColor: 'rgba(239, 68, 68, 0.8)'
                }
            },
            optimalZone: {
                type: 'box',
                yMin: threshold.optimal[0],
                yMax: threshold.optimal[1],
                backgroundColor: 'rgba(34, 197, 94, 0.1)',
                borderWidth: 0
            }
        }
    };
    
    return chartConfig;
}
```

3. **Modify Chart Rendering** (update existing chart render functions):

```javascript
// In renderTrendChart function, before creating the chart:
chartConfig = addThresholdAnnotations(chartConfig, paramKey);
```

---

## Phase 2: Core Enhancements (Week 3-6)

### 2.1 Multi-Device Comparison

**Steps:**

1. **Change Device Selector to Multi-Select**:

```html
<!-- Replace single select with multi-select -->
<select id="an-device" multiple size="5" 
        onchange="updateAnalyticsCharts()" 
        style="min-width:200px;">
    <!-- Options populated dynamically -->
</select>
```

2. **Update Chart Functions to Handle Multiple Devices**:

```javascript
function getSelectedDevices() {
    const select = document.getElementById('an-device');
    return Array.from(select.selectedOptions).map(opt => opt.value);
}

function renderMultiDeviceTrendChart(paramKey) {
    const devices = getSelectedDevices();
    const dateFrom = document.getElementById('an-date-from').value;
    const dateTo = document.getElementById('an-date-to').value;
    
    const datasets = devices.map((deviceId, idx) => {
        const deviceData = normalizeAnalyticsRows(
            rgbData.filter(r => {
                const match = r.device_id === deviceId || r.deviceId === deviceId;
                const dateMatch = true; // Add date filtering
                return match && dateMatch;
            })
        );
        
        const colors = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899'];
        
        return {
            label: `Device ${deviceId}`,
            data: deviceData.map(r => ({
                x: new Date(r.timestamp),
                y: parseFloat(r[paramKey])
            })),
            borderColor: colors[idx % colors.length],
            backgroundColor: colors[idx % colors.length] + '33',
            tension: 0.4
        };
    });
    
    // Create chart with multiple datasets
    const chartConfig = {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            scales: {
                x: { type: 'time' },
                y: { beginAtZero: false }
            }
        }
    };
    
    // Render chart...
}
```

---

## Phase 3: Advanced Features (Week 7-12)

### 3.1 Heatmap Visualization

**Prerequisites:**
- Install Chart.js Matrix plugin

**Implementation:**

```javascript
function renderHeatmap(paramKey) {
    const devices = getSelectedDevices();
    const dateFrom = document.getElementById('an-date-from').value;
    const dateTo = document.getElementById('an-date-to').value;
    
    // Aggregate data by device and day
    const heatmapData = [];
    
    devices.forEach(deviceId => {
        const deviceData = rgbData.filter(r => 
            (r.device_id === deviceId || r.deviceId === deviceId)
        );
        
        // Group by date
        const dailyAverages = {};
        deviceData.forEach(row => {
            const date = new Date(row.timestamp).toISOString().split('T')[0];
            if (!dailyAverages[date]) {
                dailyAverages[date] = { sum: 0, count: 0 };
            }
            const val = parseFloat(row[paramKey]);
            if (!isNaN(val)) {
                dailyAverages[date].sum += val;
                dailyAverages[date].count++;
            }
        });
        
        // Create heatmap points
        Object.keys(dailyAverages).forEach(date => {
            heatmapData.push({
                x: date,
                y: deviceId,
                v: dailyAverages[date].sum / dailyAverages[date].count
            });
        });
    });
    
    // Create heatmap chart
    const chartConfig = {
        type: 'matrix',
        data: {
            datasets: [{
                label: paramKey,
                data: heatmapData,
                width: ({ chart }) => (chart.chartArea || {}).width / 30 - 1,
                height: ({ chart }) => (chart.chartArea || {}).height / devices.length - 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: () => '',
                        label: (context) => {
                            const v = context.dataset.data[context.dataIndex];
                            return `${v.y} on ${v.x}: ${v.v.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: { type: 'time', display: true },
                y: { display: true }
            }
        }
    };
    
    // Render...
}
```

---

## Testing Checklist

After each implementation phase:

- [ ] Test with different date ranges
- [ ] Test with single vs multiple devices
- [ ] Test with missing/incomplete data
- [ ] Test export functionality
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile devices
- [ ] Verify performance with large datasets (1000+ records)
- [ ] Check for console errors
- [ ] Validate exported data accuracy

---

## Deployment Steps

1. **Backup Current Version**
   ```bash
   git checkout -b backup-analytics-before-enhancement
   git push origin backup-analytics-before-enhancement
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/analytics-enhancement
   ```

3. **Implement Changes**
   - Make incremental commits for each feature
   - Test thoroughly after each commit

4. **Code Review**
   - Use code_review tool
   - Address all feedback

5. **Security Scan**
   - Run codeql_checker
   - Fix any vulnerabilities

6. **Merge to Main**
   ```bash
   git checkout main
   git merge feature/analytics-enhancement
   git push origin main
   ```

7. **Deploy to Production**
   - Update Google Apps Script
   - Monitor for errors
   - Collect user feedback

---

## Troubleshooting

### Issue: Statistics not showing
**Solution:** Check that data has the expected parameter keys. Use console.log to inspect data structure.

### Issue: Export downloads empty file
**Solution:** Verify data filtering logic. Check browser console for errors.

### Issue: Charts not rendering with thresholds
**Solution:** Ensure Chart.js annotation plugin is loaded. Check plugin configuration syntax.

### Issue: Performance slow with large datasets
**Solution:** Implement data aggregation or pagination. Consider using web workers for calculations.

---

## Support & Resources

- **Chart.js Documentation:** https://www.chartjs.org/docs/
- **Chart.js Plugins:** https://github.com/chartjs
- **Google Apps Script:** https://developers.google.com/apps-script

---

## Next Steps

After completing all phases:

1. Gather user feedback
2. Monitor performance metrics
3. Plan additional enhancements based on usage patterns
4. Consider backend optimizations for better performance
5. Implement automated testing suite

---

**Last Updated:** February 2026  
**Maintainer:** Insoil Tool Development Team
