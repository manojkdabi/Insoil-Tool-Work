# InsoilTool Live Server Migration Guide
## Migrating from Existing Data Collection Server

**Scenario:** You have devices actively sending data to an existing server. You need to migrate to the new InsoilTool system without losing data or interrupting device operations.

**Goal:** Zero-downtime migration with complete data preservation  
**Risk Level:** HIGH - Active data collection system  
**Timeline:** 2-4 weeks (depends on device count)  

---

## Table of Contents

1. [Pre-Migration Assessment](#1-pre-migration-assessment)
2. [Migration Strategy Options](#2-migration-strategy-options)
3. [Recommended Approach: Parallel Operation](#3-recommended-approach-parallel-operation)
4. [Phase 1: Assessment & Planning](#phase-1-assessment--planning)
5. [Phase 2: New System Setup](#phase-2-new-system-setup)
6. [Phase 3: Historical Data Migration](#phase-3-historical-data-migration)
7. [Phase 4: Device Reconfiguration](#phase-4-device-reconfiguration)
8. [Phase 5: Parallel Operation](#phase-5-parallel-operation)
9. [Phase 6: Validation & Cutover](#phase-6-validation--cutover)
10. [Phase 7: Decommission Old Server](#phase-7-decommission-old-server)
11. [Rollback Procedures](#rollback-procedures)
12. [Troubleshooting Guide](#troubleshooting-guide)

---

## 1. Pre-Migration Assessment

### Understanding Your Current Setup

Before starting migration, document your current system:

#### Questions to Answer

**Current Server:**
- [ ] What server technology? (Linux, Windows, cloud?)
- [ ] Where is data stored? (MySQL, PostgreSQL, MongoDB, files?)
- [ ] How do devices send data? (HTTP POST, MQTT, FTP?)
- [ ] What format? (JSON, CSV, XML, binary?)
- [ ] How often do devices send data? (real-time, hourly, daily?)
- [ ] How many devices are active?
- [ ] What's the data retention policy?
- [ ] Any data processing/validation on server?

**Data Volume:**
- [ ] Total historical data size?
- [ ] Daily data ingestion rate?
- [ ] Peak vs average load?
- [ ] Any data gaps or inconsistencies?

**Device Information:**
- [ ] Total devices deployed?
- [ ] Devices accessible remotely?
- [ ] Device firmware version?
- [ ] Can devices be reconfigured remotely?
- [ ] Physical access required?

**Business Constraints:**
- [ ] Acceptable downtime? (none preferred)
- [ ] Critical data collection periods?
- [ ] Regulatory/compliance requirements?
- [ ] Backup and recovery procedures?

---

## 2. Migration Strategy Options

### Option A: Big Bang Migration ❌ NOT RECOMMENDED

**Approach:** Shut down old server, migrate all data, start new system

**Pros:**
- Simpler coordination
- Faster completion

**Cons:**
- ⚠️ Downtime during migration (hours to days)
- ⚠️ High risk of data loss
- ⚠️ No fallback if issues occur
- ⚠️ Devices lose connectivity
- ⚠️ Pressure to complete quickly

**Verdict:** Too risky for production system with active devices

---

### Option B: Parallel Operation ✅ RECOMMENDED

**Approach:** Run both systems simultaneously, gradually migrate devices

**Pros:**
- ✅ Zero downtime
- ✅ Continuous data collection
- ✅ Time to validate new system
- ✅ Easy rollback if issues
- ✅ Can migrate devices in batches
- ✅ Low risk

**Cons:**
- Requires more planning
- Temporary duplicate infrastructure
- Longer migration period

**Verdict:** Best approach for production systems

---

### Option C: Hybrid (Data Bridge)

**Approach:** Keep old server, add middleware to forward data to new system

**Pros:**
- Minimal changes to devices
- Can test new system with real data
- Gradual transition

**Cons:**
- Requires middleware development
- Double data storage temporarily
- More complex architecture

**Verdict:** Good for complex device protocols or remote devices

---

## 3. Recommended Approach: Parallel Operation

### Overview

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: CURRENT STATE (Week 0)                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Devices → Old Server → Database                            │
│           (collecting)   (all data)                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: PARALLEL OPERATION (Week 1-3)                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Batch 1 Devices → New System → Supabase                    │
│  Batch 2 Devices → Old Server → Database                    │
│  Batch 3 Devices → Old Server → Database                    │
│                                                              │
│  Both systems active, devices gradually migrated             │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: CUTOVER (Week 4)                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  All Devices → New System → Supabase                        │
│                                                              │
│  Old Server: Read-only for historical reference             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Timeline

| Week | Phase | Activities |
|------|-------|------------|
| **Week 0** | Assessment | Document current system, plan migration |
| **Week 1** | Setup | Deploy new system, migrate historical data |
| **Week 2-3** | Migration | Reconfigure devices in batches, validate |
| **Week 4** | Cutover | Final validation, decommission old server |

---

## Phase 1: Assessment & Planning

### Step 1.1: Document Current System

**Create inventory file:**

```bash
# current-system-inventory.txt

Server Details:
- Hostname: insoil-data-server-01
- IP Address: 192.168.1.100
- OS: Ubuntu 20.04
- Database: PostgreSQL 13
- Data endpoint: http://192.168.1.100:8080/api/data

Device Details:
- Total devices: 350
- Active devices: 320
- Inactive devices: 30
- Device IDs: [list in CSV]

Data Protocol:
- Method: HTTP POST
- Format: JSON
- Endpoint: /api/data
- Headers: {"Content-Type": "application/json", "Authorization": "Bearer xyz"}
- Frequency: Every 1 hour

Data Format Example:
{
  "device_id": "123456789012345",
  "timestamp": "2026-02-17T10:30:00Z",
  "readings": {
    "r_red": 120,
    "r_green": 150,
    "r_blue": 180,
    ...
  }
}

Historical Data:
- Database size: 50 GB
- Oldest record: 2023-01-01
- Total records: 2.5 million
- Format: PostgreSQL tables
```

### Step 1.2: Analyze Data Structure

**Export sample data:**

```bash
# Export 1000 sample records from current server
pg_dump -h localhost -U postgres -t sensor_data --data-only --limit 1000 > sample_data.sql

# Or if REST API available:
curl -X GET http://192.168.1.100:8080/api/data?limit=1000 > sample_data.json
```

**Map to InsoilTool schema:**

```
Current Server          →    InsoilTool (Supabase)
─────────────────────────────────────────────────────
sensor_data table       →    rgb_data table
- device_id             →    device_id
- timestamp             →    timestamp
- sensor_readings       →    readings (JSONB)
- temperature           →    readings.temperature
- humidity              →    readings.humidity

devices table           →    devices table
- device_id             →    device_id
- client_name           →    client_name
- location              →    location (POINT)
```

### Step 1.3: Create Migration Plan

**Document:**

```markdown
# Migration Plan

## Timeline
- Start date: 2026-02-24
- End date: 2026-03-23
- Total duration: 4 weeks

## Device Batches
Batch 1 (Week 2): 10 devices (test batch)
- Device IDs: [list]
- Location: Test site
- Owner: Internal team

Batch 2 (Week 2-3): 100 devices
- Device IDs: [list]
- Location: District A
- Owner: Client A

Batch 3 (Week 3): 100 devices
- Device IDs: [list]
- Location: District B
- Owner: Client B

Batch 4 (Week 3): 110 devices
- Device IDs: [list]
- Location: District C
- Owner: Client C

## Risks & Mitigations
Risk: Data loss during migration
Mitigation: Keep old server running, validate data integrity

Risk: Device connectivity issues
Mitigation: Migrate in small batches, test thoroughly

Risk: Performance issues on new system
Mitigation: Load test before migration
```

---

## Phase 2: New System Setup

### Step 2.1: Deploy InsoilTool

Follow one of these guides:
- FREE_TIER_DEPLOYMENT_GUIDE.md (for free tier)
- SUPABASE_VERCEL_MIGRATION_GUIDE.md (for production)

**Checklist:**
- [ ] Supabase project created
- [ ] Database schema created
- [ ] Frontend deployed to Vercel
- [ ] Authentication configured
- [ ] API endpoints tested
- [ ] Sample data inserted

### Step 2.2: Create Data Ingestion API

**New endpoint for device data:**

```typescript
// /api/device-data/ingest.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { device_id, timestamp, readings } = req.body;

    // Validate device exists
    const { data: device } = await supabase
      .from('devices')
      .select('device_id')
      .eq('device_id', device_id)
      .single();

    if (!device) {
      return res.status(404).json({ error: 'Device not found' });
    }

    // Insert data
    const { data, error } = await supabase
      .from('rgb_data')
      .insert([{
        device_id,
        timestamp,
        readings,
        test_id: `${device_id}_${Date.now()}`,
        qc_status: 'pending'
      }]);

    if (error) throw error;

    return res.status(200).json({ 
      success: true, 
      message: 'Data ingested successfully',
      data 
    });

  } catch (error) {
    console.error('Data ingestion error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      details: error.message 
    });
  }
}
```

**Test the endpoint:**

```bash
# Test data ingestion
curl -X POST https://your-app.vercel.app/api/device-data/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "123456789012345",
    "timestamp": "2026-02-17T10:30:00Z",
    "readings": {
      "r_red": 120,
      "r_green": 150,
      "r_blue": 180
    }
  }'
```

### Step 2.3: Load Testing

**Test with simulated device data:**

```typescript
// scripts/load-test.ts
import { faker } from '@faker-js/faker';

async function simulateDeviceData() {
  const devices = 100; // Simulate 100 devices
  const dataPoints = 24; // 24 hours of data

  for (let d = 0; d < devices; d++) {
    for (let h = 0; h < dataPoints; h++) {
      const data = {
        device_id: `1234567890${String(d).padStart(5, '0')}`,
        timestamp: new Date(Date.now() - (h * 3600000)).toISOString(),
        readings: {
          r_red: faker.number.int({ min: 100, max: 255 }),
          r_green: faker.number.int({ min: 100, max: 255 }),
          r_blue: faker.number.int({ min: 100, max: 255 }),
          // Add more sensor readings
        }
      };

      await fetch('https://your-app.vercel.app/api/device-data/ingest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      // Rate limit: 100ms between requests
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
}

simulateDeviceData();
```

**Run load test:**

```bash
npx ts-node scripts/load-test.ts
```

**Monitor performance:**
- Check Supabase dashboard for database performance
- Check Vercel analytics for API response times
- Verify data is being stored correctly

---

## Phase 3: Historical Data Migration

### Step 3.1: Export Data from Current Server

**Option A: Database Dump**

```bash
# PostgreSQL
pg_dump -h current-server -U postgres \
  --table=sensor_data \
  --table=devices \
  --format=custom \
  --file=historical_data.dump

# MySQL
mysqldump -h current-server -u root -p \
  database_name sensor_data devices > historical_data.sql
```

**Option B: API Export**

```bash
# If current server has export API
curl -X GET http://current-server/api/export \
  --output historical_data.json
```

**Option C: Custom Script**

```python
# export_historical_data.py
import psycopg2
import json
from datetime import datetime

# Connect to current server
conn = psycopg2.connect(
    host="current-server",
    database="insoil_db",
    user="postgres",
    password="password"
)

cursor = conn.cursor()

# Export in batches
batch_size = 10000
offset = 0

with open('historical_data.jsonl', 'w') as f:
    while True:
        cursor.execute(f"""
            SELECT device_id, timestamp, sensor_readings
            FROM sensor_data
            ORDER BY timestamp
            LIMIT {batch_size} OFFSET {offset}
        """)
        
        rows = cursor.fetchall()
        if not rows:
            break
        
        for row in rows:
            data = {
                'device_id': row[0],
                'timestamp': row[1].isoformat(),
                'readings': json.loads(row[2])
            }
            f.write(json.dumps(data) + '\n')
        
        offset += batch_size
        print(f"Exported {offset} records...")

conn.close()
print("Export complete!")
```

### Step 3.2: Transform Data

**Map old format to new format:**

```typescript
// scripts/transform-data.ts
import fs from 'fs';
import readline from 'readline';

interface OldFormat {
  device_id: string;
  timestamp: string;
  sensor_readings: any;
}

interface NewFormat {
  device_id: string;
  test_id: string;
  timestamp: string;
  readings: any;
  qc_status: string;
}

async function transformData(inputFile: string, outputFile: string) {
  const fileStream = fs.createReadStream(inputFile);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  const writeStream = fs.createWriteStream(outputFile);
  let count = 0;

  for await (const line of rl) {
    const oldData: OldFormat = JSON.parse(line);
    
    const newData: NewFormat = {
      device_id: oldData.device_id,
      test_id: `${oldData.device_id}_${new Date(oldData.timestamp).getTime()}`,
      timestamp: oldData.timestamp,
      readings: oldData.sensor_readings, // May need mapping
      qc_status: 'pending'
    };

    writeStream.write(JSON.stringify(newData) + '\n');
    count++;

    if (count % 10000 === 0) {
      console.log(`Transformed ${count} records...`);
    }
  }

  writeStream.end();
  console.log(`Total transformed: ${count} records`);
}

transformData('historical_data.jsonl', 'transformed_data.jsonl');
```

### Step 3.3: Import to Supabase

**Option A: Bulk Insert via API**

```typescript
// scripts/import-to-supabase.ts
import { createClient } from '@supabase/supabase-js';
import fs from 'fs';
import readline from 'readline';

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
);

async function importData(filename: string) {
  const fileStream = fs.createReadStream(filename);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  let batch: any[] = [];
  const batchSize = 1000;
  let totalImported = 0;

  for await (const line of rl) {
    batch.push(JSON.parse(line));

    if (batch.length >= batchSize) {
      const { error } = await supabase
        .from('rgb_data')
        .insert(batch);

      if (error) {
        console.error('Batch import error:', error);
        // Log failed batch for retry
        fs.appendFileSync('failed_imports.jsonl', 
          batch.map(b => JSON.stringify(b)).join('\n') + '\n'
        );
      } else {
        totalImported += batch.length;
        console.log(`Imported ${totalImported} records...`);
      }

      batch = [];
      
      // Rate limiting
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  // Import remaining
  if (batch.length > 0) {
    const { error } = await supabase
      .from('rgb_data')
      .insert(batch);

    if (!error) {
      totalImported += batch.length;
    }
  }

  console.log(`Total imported: ${totalImported} records`);
}

importData('transformed_data.jsonl');
```

**Option B: Direct SQL Import (Faster)**

```bash
# 1. Upload transformed data to Supabase Storage
supabase storage create historical-imports
supabase storage upload historical-imports/data.csv transformed_data.csv

# 2. Use SQL to import (in Supabase SQL Editor)
COPY rgb_data(device_id, test_id, timestamp, readings, qc_status)
FROM '/storage/historical-imports/data.csv'
DELIMITER ','
CSV HEADER;
```

### Step 3.4: Validate Historical Data

```sql
-- Compare record counts
SELECT COUNT(*) FROM rgb_data;

-- Check date ranges
SELECT MIN(timestamp), MAX(timestamp) FROM rgb_data;

-- Check device coverage
SELECT device_id, COUNT(*) as record_count
FROM rgb_data
GROUP BY device_id
ORDER BY record_count DESC;

-- Verify data integrity
SELECT 
  COUNT(*) as total_records,
  COUNT(DISTINCT device_id) as unique_devices,
  COUNT(CASE WHEN readings IS NULL THEN 1 END) as null_readings
FROM rgb_data;
```

**Create validation report:**

```typescript
// scripts/validate-migration.ts
import { createClient } from '@supabase/supabase-js';

async function validateMigration() {
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );

  // Get statistics
  const { data: stats } = await supabase.rpc('get_migration_stats');

  console.log('Migration Validation Report');
  console.log('===========================');
  console.log(`Total records: ${stats.total_records}`);
  console.log(`Unique devices: ${stats.unique_devices}`);
  console.log(`Date range: ${stats.min_date} to ${stats.max_date}`);
  console.log(`Data quality: ${stats.quality_score}%`);
  
  // Compare with original
  console.log('\nComparison with original server:');
  console.log(`Original records: ${stats.original_count}`);
  console.log(`Migrated records: ${stats.migrated_count}`);
  console.log(`Difference: ${stats.original_count - stats.migrated_count}`);
  
  if (stats.migrated_count === stats.original_count) {
    console.log('✅ All data migrated successfully!');
  } else {
    console.log('⚠️  Some data missing. Check logs.');
  }
}
```

---

## Phase 4: Device Reconfiguration

### Step 4.1: Prepare Device Configuration

**New endpoint URL:**

```
Old: http://192.168.1.100:8080/api/data
New: https://your-app.vercel.app/api/device-data/ingest
```

**Configuration changes needed:**
- API endpoint URL
- Authentication token (if changed)
- Data format (if changed)
- Headers (if changed)

### Step 4.2: Create Reconfiguration Procedures

**Option A: Remote Reconfiguration (Preferred)**

If devices support remote configuration:

```bash
# Script to reconfigure devices remotely
# reconfigure-device.sh

DEVICE_ID=$1
NEW_ENDPOINT="https://your-app.vercel.app/api/device-data/ingest"

# Send configuration command to device
curl -X POST http://${DEVICE_IP}/config \
  -H "Content-Type: application/json" \
  -d "{
    \"endpoint\": \"${NEW_ENDPOINT}\",
    \"auth_token\": \"${NEW_AUTH_TOKEN}\"
  }"

echo "Device ${DEVICE_ID} reconfigured"
```

**Option B: Manual Reconfiguration**

If physical access required:

```markdown
# Device Reconfiguration Checklist

Per Device:
1. [ ] Connect to device (USB/Bluetooth/WiFi)
2. [ ] Access configuration interface
3. [ ] Update API endpoint URL
4. [ ] Update authentication credentials
5. [ ] Test connectivity
6. [ ] Verify data transmission
7. [ ] Document completion
8. [ ] Label device as "Migrated"
```

### Step 4.3: Batch Migration Process

**Week 2: Batch 1 (Test) - 10 devices**

```bash
# Day 1: Monday
# Reconfigure 10 test devices
for device_id in device_list_batch1.txt; do
  ./reconfigure-device.sh $device_id
  sleep 10  # Wait between devices
done

# Day 2-3: Tuesday-Wednesday
# Monitor test devices
# Check data is arriving in new system
# Compare with old system data
# Fix any issues

# Day 4: Thursday
# If successful, proceed to Batch 2
# If issues, rollback and investigate
```

**Week 2-3: Batch 2-4 (Production) - 310 devices**

```bash
# Spread over 2 weeks
# ~25 devices per day
# Always maintain rollback capability
```

### Step 4.4: Device Tracking

**Migration tracking spreadsheet:**

```csv
Device_ID,Batch,Status,Reconfigured_Date,Validated,Notes
123456789012345,1,Complete,2026-02-24,Yes,Working perfectly
123456789012346,1,Complete,2026-02-24,Yes,
123456789012347,2,In Progress,,,Scheduled for 2026-02-26
123456789012348,2,Pending,,,
```

**Update tracking after each device:**

```typescript
// scripts/update-tracking.ts
import { createClient } from '@supabase/supabase-js';

async function updateDeviceStatus(
  deviceId: string,
  status: string,
  notes: string = ''
) {
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );

  await supabase
    .from('device_migration_tracking')
    .update({
      status,
      reconfigured_date: new Date().toISOString(),
      notes
    })
    .eq('device_id', deviceId);

  console.log(`Device ${deviceId} status updated to ${status}`);
}
```

---

## Phase 5: Parallel Operation

### Step 5.1: Monitor Both Systems

**Daily checks:**

```bash
# Check old server
curl http://old-server/api/stats
# Expected: Devices = 310 (decreasing as migrated)

# Check new system
curl https://new-app.vercel.app/api/stats
# Expected: Devices = 10 (increasing as migrated)
```

**Automated monitoring:**

```typescript
// scripts/monitor-migration.ts
import { createClient } from '@supabase/supabase-js';

async function monitorMigration() {
  // Check old server
  const oldServerResponse = await fetch('http://old-server/api/stats');
  const oldStats = await oldServerResponse.json();

  // Check new system
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );

  const { count: newDeviceCount } = await supabase
    .from('devices')
    .select('*', { count: 'exact', head: true });

  console.log('Migration Progress:');
  console.log(`Old system: ${oldStats.active_devices} devices`);
  console.log(`New system: ${newDeviceCount} devices`);
  console.log(`Remaining: ${oldStats.active_devices} devices`);
  console.log(`Progress: ${(newDeviceCount / 320 * 100).toFixed(1)}%`);

  // Check for issues
  if (oldStats.active_devices + newDeviceCount !== 320) {
    console.warn('⚠️  Device count mismatch! Some devices may be offline.');
  }
}

// Run every hour
setInterval(monitorMigration, 3600000);
```

### Step 5.2: Data Consistency Validation

**Compare data between systems:**

```typescript
// scripts/compare-data.ts
async function compareDeviceData(deviceId: string, date: string) {
  // Get from old server
  const oldData = await fetch(
    `http://old-server/api/data?device=${deviceId}&date=${date}`
  ).then(r => r.json());

  // Get from new system
  const supabase = createClient(
    process.env.SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );

  const { data: newData } = await supabase
    .from('rgb_data')
    .select('*')
    .eq('device_id', deviceId)
    .gte('timestamp', `${date}T00:00:00Z`)
    .lt('timestamp', `${date}T23:59:59Z`);

  // Compare
  console.log(`Device ${deviceId} on ${date}:`);
  console.log(`Old system: ${oldData.length} records`);
  console.log(`New system: ${newData?.length || 0} records`);

  if (oldData.length === newData?.length) {
    console.log('✅ Data matches!');
  } else {
    console.log('⚠️  Data mismatch!');
    // Log details for investigation
  }
}
```

---

## Phase 6: Validation & Cutover

### Step 6.1: Pre-Cutover Checklist

**Complete this checklist before final cutover:**

- [ ] All 320 devices reconfigured
- [ ] All devices sending data to new system
- [ ] Historical data fully migrated
- [ ] Data validation passed
- [ ] User acceptance testing complete
- [ ] Backup of old server created
- [ ] Rollback procedure tested
- [ ] Team trained on new system
- [ ] Documentation updated
- [ ] Monitoring alerts configured

### Step 6.2: Final Validation

**Run comprehensive validation:**

```bash
# 1. Device connectivity
npm run validate-devices

# 2. Data integrity
npm run validate-data

# 3. Performance
npm run load-test

# 4. User acceptance
npm run e2e-tests
```

**Validation report:**

```
InsoilTool Migration Validation Report
Date: 2026-03-20

✅ Devices
   - Total migrated: 320/320 (100%)
   - Active devices: 318/320 (99.4%)
   - Data transmission: Working

✅ Historical Data
   - Records migrated: 2,500,000/2,500,000 (100%)
   - Date coverage: 2023-01-01 to 2026-03-20
   - Data integrity: PASSED

✅ Performance
   - API response time: 150ms avg (target: < 200ms)
   - Database queries: 50ms avg (target: < 100ms)
   - Page load: 1.2s (target: < 2s)

✅ Functionality
   - User authentication: PASSED
   - Device registry: PASSED
   - Data visualization: PASSED
   - Analytics: PASSED
   - PDF generation: PASSED

⚠️  Minor Issues
   - 2 devices offline (farmer reported, not migration-related)
   - 1 device with intermittent connectivity (investigating)

RECOMMENDATION: PROCEED WITH CUTOVER
```

### Step 6.3: Cutover Execution

**Cutover Day Schedule:**

```
08:00 AM - Final backup of old server
08:30 AM - Verify all devices on new system
09:00 AM - Send notification to users
09:30 AM - Set old server to read-only mode
10:00 AM - Update DNS/documentation to point to new system
10:30 AM - Monitor for 30 minutes
11:00 AM - Declare cutover complete (if no issues)

Throughout day: Monitor actively
```

**Cutover script:**

```bash
#!/bin/bash
# cutover.sh

echo "Starting cutover process..."

# 1. Final backup
echo "Creating final backup of old server..."
pg_dump -h old-server -U postgres insoil_db > final_backup.sql

# 2. Set old server read-only
echo "Setting old server to read-only..."
ssh old-server "sudo systemctl stop data-ingestion-service"

# 3. Verify new system
echo "Verifying new system..."
curl https://new-app.vercel.app/api/health

# 4. Send notifications
echo "Sending notifications to users..."
node scripts/send-cutover-notification.ts

# 5. Update DNS (if applicable)
echo "Updating DNS records..."
# Manual step or API call to DNS provider

echo "Cutover complete! Monitor closely for next 24 hours."
```

---

## Phase 7: Decommission Old Server

### Step 7.1: Keep Old Server for Grace Period

**Week 1 post-cutover:**
- Keep old server running (read-only)
- Monitor new system closely
- Be ready to rollback if critical issues

**Week 2-4 post-cutover:**
- Old server available for reference
- No new data being written
- Validate everything working on new system

### Step 7.2: Archive Old Server Data

```bash
# Create complete archive
tar -czf old-server-complete-archive-$(date +%Y%m%d).tar.gz \
  /var/lib/postgresql/data \
  /opt/insoil-server/config \
  /opt/insoil-server/logs

# Upload to secure storage
aws s3 cp old-server-complete-archive-*.tar.gz \
  s3://insoil-archives/old-server/

# Verify archive
aws s3 ls s3://insoil-archives/old-server/
```

### Step 7.3: Decommission

**After 30 days of successful operation:**

```bash
# 1. Final verification
echo "Are you sure you want to decommission the old server? (yes/no)"
read answer

if [ "$answer" = "yes" ]; then
  # 2. Stop all services
  ssh old-server "sudo systemctl stop all-insoil-services"
  
  # 3. Remove from monitoring
  # (Manual step in monitoring dashboard)
  
  # 4. Document decommission
  echo "$(date): Old server decommissioned" >> decommission-log.txt
  
  # 5. If cloud: terminate instance
  # aws ec2 terminate-instances --instance-ids i-xxxxxxxx
  
  echo "Old server decommissioned successfully"
else
  echo "Decommission cancelled"
fi
```

---

## Rollback Procedures

### Scenario 1: Issues During Batch Migration

**If problems detected with migrated devices:**

```bash
# 1. Stop further migrations
echo "STOP" > migration-control.flag

# 2. Revert affected devices to old server
for device_id in affected_devices.txt; do
  ./reconfigure-device.sh $device_id http://old-server/api/data
done

# 3. Investigate issues
# 4. Fix problems
# 5. Resume when ready
```

### Scenario 2: Critical Issues Post-Cutover

**If major issues within first 24 hours:**

```bash
#!/bin/bash
# emergency-rollback.sh

echo "EMERGENCY ROLLBACK INITIATED"

# 1. Send alert to team
curl -X POST slack-webhook-url -d '{"text":"EMERGENCY ROLLBACK"}'

# 2. Reconfigure ALL devices back to old server
for device_id in $(cat all-devices.txt); do
  ./reconfigure-device.sh $device_id http://old-server/api/data
done

# 3. Restart old server services
ssh old-server "sudo systemctl start data-ingestion-service"

# 4. Update DNS
# (Manual or scripted based on your DNS provider)

# 5. Document incident
echo "$(date): Emergency rollback executed" >> incident-log.txt

echo "Rollback complete. Old server is primary again."
```

### Scenario 3: Data Corruption Detected

**If data integrity issues found:**

```bash
# 1. Stop writes to affected table
# (In Supabase SQL editor)
ALTER TABLE rgb_data SET (fillfactor = 100);
-- Or use RLS to block writes temporarily

# 2. Restore from backup
# Use point-in-time recovery if on Pro plan
# Or restore specific data from old server

# 3. Validate restored data
npm run validate-data

# 4. Resume normal operations
```

---

## Troubleshooting Guide

### Issue: Devices Not Connecting to New System

**Symptoms:**
- Device data not appearing in new system
- Old server still receiving data

**Diagnosis:**
```bash
# Check device configuration
curl http://<device-ip>/config

# Check network connectivity
ping your-app.vercel.app

# Check API endpoint
curl https://your-app.vercel.app/api/device-data/ingest
```

**Solution:**
1. Verify device has correct new endpoint URL
2. Check authentication credentials
3. Verify network/firewall settings
4. Check API logs for errors

---

### Issue: Historical Data Import Failing

**Symptoms:**
- Import script errors
- Missing records in Supabase
- Timeout errors

**Diagnosis:**
```bash
# Check import logs
tail -f import-log.txt

# Check Supabase database size
# In Supabase dashboard

# Check for constraint violations
# In Supabase SQL editor
SELECT * FROM pg_stat_activity WHERE state = 'error';
```

**Solution:**
1. Import in smaller batches
2. Add retry logic for failed batches
3. Check for data format issues
4. Increase timeout values

---

### Issue: Performance Degradation

**Symptoms:**
- Slow API responses
- Page load times > 5 seconds
- Database queries timing out

**Diagnosis:**
```sql
-- Check slow queries
SELECT query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Check table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**Solution:**
1. Add missing indexes
2. Optimize slow queries
3. Enable caching
4. Upgrade to Supabase Pro if needed

---

### Issue: Data Mismatch Between Systems

**Symptoms:**
- Record counts don't match
- Missing data in new system
- Duplicate data

**Diagnosis:**
```bash
# Compare record counts
./scripts/compare-counts.sh

# Check for duplicates
npm run check-duplicates

# Review import logs
grep ERROR import-log.txt
```

**Solution:**
1. Identify missing/duplicate records
2. Re-import affected data
3. Add unique constraints to prevent duplicates
4. Validate data transformation logic

---

## Migration Checklist

### Pre-Migration
- [ ] Document current system
- [ ] Export sample data
- [ ] Map data structures
- [ ] Create migration plan
- [ ] Test new system
- [ ] Create data ingestion API
- [ ] Perform load testing

### Data Migration
- [ ] Export historical data
- [ ] Transform data format
- [ ] Import to Supabase
- [ ] Validate data integrity
- [ ] Create comparison reports

### Device Migration
- [ ] Prepare reconfiguration procedures
- [ ] Create device tracking system
- [ ] Test with pilot devices (Batch 1)
- [ ] Migrate production devices (Batches 2-4)
- [ ] Validate each batch

### Parallel Operation
- [ ] Monitor both systems
- [ ] Compare data daily
- [ ] Fix issues promptly
- [ ] Update documentation

### Cutover
- [ ] Complete pre-cutover checklist
- [ ] Run final validation
- [ ] Execute cutover
- [ ] Monitor intensively
- [ ] Document completion

### Post-Migration
- [ ] Keep old server for 30 days
- [ ] Archive old server data
- [ ] Decommission old server
- [ ] Update all documentation
- [ ] Conduct lessons learned session

---

## Success Metrics

**Migration is successful when:**

- ✅ All devices migrated (100%)
- ✅ All historical data migrated (100%)
- ✅ Data integrity validated
- ✅ No data loss
- ✅ Performance meets targets
- ✅ Users satisfied with new system
- ✅ Old server decommissioned
- ✅ Documentation complete

---

## Support & Resources

**During Migration:**
- Daily standup meetings
- Dedicated Slack channel: #insoil-migration
- On-call support: [phone number]
- Issue tracker: [link]

**Documentation:**
- SUPABASE_VERCEL_MIGRATION_GUIDE.md
- FREE_TIER_DEPLOYMENT_GUIDE.md
- API documentation: [link]

**Contacts:**
- Migration lead: [name]
- Technical support: [name]
- Business owner: [name]

---

## Timeline Summary

| Week | Focus | Key Activities |
|------|-------|----------------|
| **Week 0** | Planning | Assessment, documentation, planning |
| **Week 1** | Setup | Deploy new system, migrate historical data |
| **Week 2** | Pilot | Migrate test batch, validate approach |
| **Week 3** | Production | Migrate remaining devices in batches |
| **Week 4** | Cutover | Final validation, cutover, monitor |
| **Week 5-8** | Stabilization | Grace period, decommission old server |

**Total:** 8 weeks from start to complete decommission

---

## Conclusion

This migration requires careful planning and execution, but with the parallel operation approach, you can achieve zero-downtime migration with complete data preservation.

**Key Success Factors:**
1. Thorough testing before production migration
2. Small batch approach for device reconfiguration
3. Continuous monitoring and validation
4. Quick rollback capability
5. Clear communication with stakeholders

**Remember:** It's better to go slow and ensure success than to rush and lose data!

---

**Document Version:** 1.0  
**Last Updated:** February 17, 2026  
**Next Review:** During migration execution
