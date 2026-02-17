# InsoilTool Migration Guide: Supabase + Vercel Deployment

## Executive Summary

This guide provides a comprehensive roadmap for migrating InsoilTool from Google Apps Script to a modern cloud infrastructure using **Supabase** (backend/database) and **Vercel** (frontend hosting).

**Current Architecture:** Google Apps Script + Google Sheets  
**Target Architecture:** Supabase PostgreSQL + Vercel Next.js/React  
**Estimated Migration Time:** 8-12 weeks  
**Estimated Cost:** $25-100/month (vs $0 for Google Workspace)

---

## Table of Contents

1. [Architecture Comparison](#1-architecture-comparison)
2. [Benefits of Migration](#2-benefits-of-migration)
3. [Migration Challenges](#3-migration-challenges)
4. [Database Schema Design](#4-database-schema-design)
5. [API Layer Design](#5-api-layer-design)
6. [Authentication Migration](#6-authentication-migration)
7. [Frontend Migration](#7-frontend-migration)
8. [File Storage Strategy](#8-file-storage-strategy)
9. [External API Integration](#9-external-api-integration)
10. [Migration Phases](#10-migration-phases)
11. [Cost Analysis](#11-cost-analysis)
12. [Deployment Guide](#12-deployment-guide)
13. [Testing Strategy](#13-testing-strategy)
14. [Rollback Plan](#14-rollback-plan)

---

## 1. Architecture Comparison

### Current Architecture (Google Apps Script)

```
┌─────────────────────────────────────────────────────────────┐
│                    USERS (Browsers)                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         Google Apps Script Web App (doGet/doPost)           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Frontend: HTML/JS/CSS (32,713 lines)               │   │
│  │  Backend: Google Apps Script (7,477 lines)          │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Google Sheets Storage                      │
│  • RGB_Data, QC_Data, SoilTest_Results                     │
│  • Device_Registry, Service_Config                          │
│  • Master tables (Criteria, STV, QC_Criteria)              │
│  • 15+ sheets total                                         │
└─────────────────────────────────────────────────────────────┘
```

### Target Architecture (Supabase + Vercel)

```
┌─────────────────────────────────────────────────────────────┐
│                    USERS (Browsers)                         │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│            Vercel Edge Network (CDN + SSR)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Next.js/React Frontend                             │   │
│  │  • Server Components                                │   │
│  │  • API Routes (/api/*)                              │   │
│  │  • Static Assets (CSS, images)                      │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   Supabase Platform                         │
│  ┌────────────────────────────────────────────────────┐    │
│  │  PostgreSQL Database (Relational)                  │    │
│  │  • Proper foreign keys, indexes                    │    │
│  │  • Row-level security (RLS)                        │    │
│  │  • Full-text search                                │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Supabase Auth (JWT-based)                        │    │
│  │  • Email/password, OAuth, MFA                      │    │
│  │  • Role-based access control                       │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Supabase Storage (S3-compatible)                  │    │
│  │  • PDF reports, service documents                  │    │
│  │  • User uploads                                    │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │  Edge Functions (Optional)                         │    │
│  │  • Serverless compute for heavy processing         │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               External Services                              │
│  • Mistral AI API (QC diagnostics)                          │
│  • Email service (SendGrid, Postmark)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Benefits of Migration

### Technical Benefits

| Benefit | Description | Impact |
|---------|-------------|--------|
| **True Database** | PostgreSQL with ACID compliance, foreign keys, triggers | HIGH |
| **Better Performance** | Indexed queries, connection pooling, caching | HIGH |
| **Scalability** | Horizontal scaling, read replicas | HIGH |
| **Modern Development** | TypeScript, hot reload, component libraries | HIGH |
| **Version Control** | Git-based deployment, CI/CD | HIGH |
| **Real-time Features** | WebSocket subscriptions (live data updates) | MEDIUM |
| **Better Security** | Row-level security, JWT auth, OAuth providers | HIGH |
| **Global CDN** | Fast page loads worldwide via Vercel Edge | MEDIUM |
| **Monitoring** | Built-in logging, error tracking, analytics | MEDIUM |

### Business Benefits

- **Professional Domain:** Custom domain (app.insoil.com) vs script.google.com URL
- **Better UX:** Faster page loads, instant navigation, progressive web app
- **Independence:** No dependency on Google Workspace account
- **Branding:** Full control over UI/UX, white-label capability
- **Mobile Apps:** Can build native iOS/Android apps with same backend
- **Compliance:** Better data privacy controls, audit trails

### Developer Experience

- **Modern Stack:** React/Next.js with TypeScript
- **Component Libraries:** MUI, Chakra UI, Tailwind CSS
- **Testing:** Jest, Playwright for E2E tests
- **DevOps:** Automated deployments, preview environments
- **Debugging:** Source maps, React DevTools, better error messages

---

## 3. Migration Challenges

### Major Challenges

| Challenge | Current Solution | Migration Requirement | Effort |
|-----------|------------------|----------------------|---------|
| **Google Sheets as DB** | Direct SpreadsheetApp API | Convert to PostgreSQL schema | HIGH |
| **No REST APIs** | google.script.run calls | Build REST/GraphQL API layer | HIGH |
| **Authentication** | Custom username/password | Migrate to Supabase Auth | MEDIUM |
| **File Storage** | Google Drive | Migrate to Supabase Storage | MEDIUM |
| **Monolithic File** | 32,713 line HTML file | Split into components | HIGH |
| **No Build Process** | Direct HTML delivery | Set up Next.js/Vite | MEDIUM |
| **Batch Processing** | ScriptApp triggers | Set up cron jobs/workers | MEDIUM |
| **Cache Service** | CacheService API | Redis or Vercel KV | LOW |
| **Lock Service** | LockService for concurrency | PostgreSQL locks/transactions | LOW |

### Breaking Changes

⚠️ **User Impact:**
- Users will need new login credentials (migration process)
- URL will change (redirect old URLs)
- Browser localStorage will be cleared
- Bookmarks will need updating

⚠️ **Data Migration:**
- Must export all Google Sheets data
- Transform to PostgreSQL-compatible format
- Validate data integrity
- Handle large datasets (350+ devices, thousands of tests)

---

## 4. Database Schema Design

### PostgreSQL Schema Overview

```sql
-- Core Tables
- users (replaces Users sheet)
- devices (replaces Device_Registry sheet)
- rgb_data (replaces RGB_Data sheet)
- qc_data (replaces QC_Data sheet)
- soil_test_results (replaces SoilTest_Results sheet)

-- Master Data Tables
- nutrient_master
- nutrient_stages
- nutrient_sources
- soil_fertility_ratings
- criteria
- stv_master
- qc_criteria
- blanks

-- Configuration Tables
- service_config
- prod_batches
- qc_batches

-- Audit/Log Tables
- stv_update_log (immutable)
- admin_audit_log
- service_tickets

-- Inventory Tables (7 tables)
- inventory_constitution
- inventory_parts
- inventory_built_units
- inventory_liquidation
- inventory_clients
- inventory_approvals
- inventory_refill_batches
```

### Detailed Schema Examples

#### Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  employee_id VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, -- bcrypt hash, not plaintext!
  role VARCHAR(50) NOT NULL DEFAULT 'user',
  access_modules JSONB, -- Store as JSON array
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  last_login TIMESTAMP WITH TIME ZONE,
  is_active BOOLEAN DEFAULT true,
  
  -- Indexes
  INDEX idx_users_email (email),
  INDEX idx_users_employee_id (employee_id),
  INDEX idx_users_role (role)
);

-- Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Admins can view all users"
  ON users FOR SELECT
  USING (auth.jwt()->>'role' = 'admin');
```

#### Devices Table

```sql
CREATE TABLE devices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  device_id VARCHAR(15) UNIQUE NOT NULL, -- 15-digit device ID
  sim_number VARCHAR(22) NOT NULL,
  client_name VARCHAR(100) NOT NULL,
  company_name VARCHAR(100),
  pan VARCHAR(10),
  gstin VARCHAR(15),
  address TEXT,
  aadhaar VARCHAR(12),
  mobile VARCHAR(15),
  mo_name VARCHAR(100),
  installation_date DATE,
  place VARCHAR(100),
  lat_lon POINT, -- PostgreSQL geometric type
  pin_code VARCHAR(6),
  block VARCHAR(50),
  district VARCHAR(50),
  state VARCHAR(50),
  prod_batch_id VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_devices_device_id (device_id),
  INDEX idx_devices_client (client_name),
  INDEX idx_devices_location (lat_lon) USING GIST,
  INDEX idx_devices_district (district),
  
  -- Foreign Keys
  FOREIGN KEY (prod_batch_id) REFERENCES prod_batches(batch_id)
);

-- Full-text search
CREATE INDEX idx_devices_fts ON devices 
  USING GIN (to_tsvector('english', client_name || ' ' || company_name));
```

#### RGB Data Table

```sql
CREATE TABLE rgb_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  test_id VARCHAR(50) UNIQUE NOT NULL,
  device_id VARCHAR(15) NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  
  -- Sensor readings (50+ columns)
  r_red INTEGER,
  r_green INTEGER,
  r_blue INTEGER,
  g_red INTEGER,
  g_green INTEGER,
  g_blue INTEGER,
  b_red INTEGER,
  b_green INTEGER,
  b_blue INTEGER,
  
  -- Computed parameters (store as JSONB for flexibility)
  parameters JSONB,
  
  -- Metadata
  batch_id VARCHAR(50),
  qc_status VARCHAR(20) DEFAULT 'pending',
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_rgb_test_id (test_id),
  INDEX idx_rgb_device_id (device_id),
  INDEX idx_rgb_timestamp (timestamp DESC),
  INDEX idx_rgb_qc_status (qc_status),
  INDEX idx_rgb_parameters (parameters) USING GIN,
  
  -- Foreign Keys
  FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
  
  -- Constraints
  CONSTRAINT chk_qc_status CHECK (qc_status IN ('pending', 'pass', 'fail', 'review'))
);

-- Partitioning by month for performance
CREATE TABLE rgb_data_2026_01 PARTITION OF rgb_data
  FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

#### Soil Test Results Table

```sql
CREATE TABLE soil_test_results (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  test_id VARCHAR(50) UNIQUE NOT NULL,
  device_id VARCHAR(15) NOT NULL,
  farmer_name VARCHAR(100),
  mobile VARCHAR(15),
  place VARCHAR(100),
  district VARCHAR(50),
  state VARCHAR(50),
  crop VARCHAR(50),
  crop_variety VARCHAR(50),
  area_acres DECIMAL(10,2),
  
  -- Soil parameters
  nitrogen DECIMAL(10,2),
  phosphorus DECIMAL(10,2),
  potassium DECIMAL(10,2),
  ph DECIMAL(4,2),
  ec DECIMAL(10,2),
  organic_carbon DECIMAL(10,2),
  
  -- STV methodology
  stv_version VARCHAR(20),
  stv_values JSONB,
  
  -- Recommendations
  recommendations JSONB,
  pdf_url TEXT,
  
  -- Metadata
  test_date DATE NOT NULL,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- Indexes
  INDEX idx_soil_test_id (test_id),
  INDEX idx_soil_device_id (device_id),
  INDEX idx_soil_farmer (farmer_name),
  INDEX idx_soil_test_date (test_date DESC),
  INDEX idx_soil_location (district, state),
  
  -- Foreign Keys
  FOREIGN KEY (device_id) REFERENCES devices(device_id)
);
```

---

## 5. API Layer Design

### API Structure (Next.js API Routes)

```
/api
├── /auth
│   ├── /login                 POST    - User login
│   ├── /logout                POST    - User logout
│   ├── /register              POST    - User registration
│   ├── /reset-password        POST    - Password reset
│   └── /verify-token          GET     - Validate JWT
│
├── /devices
│   ├── /                      GET     - List devices (paginated)
│   ├── /                      POST    - Create device
│   ├── /:id                   GET     - Get device details
│   ├── /:id                   PUT     - Update device
│   ├── /:id                   DELETE  - Delete device
│   └── /search                GET     - Search devices
│
├── /rgb-data
│   ├── /                      GET     - List RGB data (paginated)
│   ├── /                      POST    - Create RGB entry
│   ├── /import-csv            POST    - Import CSV file
│   ├── /:id                   GET     - Get RGB entry
│   ├── /:id                   PUT     - Update RGB entry
│   └── /sync-to-qc            POST    - Move to QC
│
├── /qc-data
│   ├── /                      GET     - List QC data
│   ├── /:id                   GET     - Get QC entry
│   ├── /:id/validate          POST    - Mark as validated
│   └── /diagnose              POST    - AI diagnostics
│
├── /soil-tests
│   ├── /                      GET     - List soil tests
│   ├── /                      POST    - Create soil test
│   ├── /:id                   GET     - Get soil test
│   ├── /:id/recommendations   GET     - Get recommendations
│   └── /:id/pdf               GET     - Generate PDF report
│
├── /analytics
│   ├── /dashboard             GET     - Dashboard metrics
│   ├── /trends                GET     - Trend data
│   └── /export                POST    - Export to Excel/CSV
│
├── /admin
│   ├── /users                 GET     - List users
│   ├── /users                 POST    - Create user
│   ├── /users/:id             PUT     - Update user
│   ├── /users/:id/permissions PUT     - Update permissions
│   └── /audit-log             GET     - View audit log
│
└── /config
    ├── /master-lists          GET     - Get master data
    ├── /stv                   GET     - Get STV config
    └── /criteria              GET     - Get criteria config
```

### Example API Implementation (Next.js)

#### /api/devices/index.ts

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { createClient } from '@supabase/supabase-js';
import { verifyAuth } from '@/lib/auth';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Verify authentication
  const user = await verifyAuth(req);
  if (!user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_KEY!
  );

  switch (req.method) {
    case 'GET':
      return await getDevices(req, res, supabase, user);
    case 'POST':
      return await createDevice(req, res, supabase, user);
    default:
      return res.status(405).json({ error: 'Method not allowed' });
  }
}

async function getDevices(req, res, supabase, user) {
  const { page = 1, limit = 50, search = '' } = req.query;
  
  let query = supabase
    .from('devices')
    .select('*', { count: 'exact' })
    .order('created_at', { ascending: false })
    .range((page - 1) * limit, page * limit - 1);

  // Apply search filter
  if (search) {
    query = query.or(`client_name.ilike.%${search}%,device_id.ilike.%${search}%`);
  }

  const { data, error, count } = await query;

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  return res.status(200).json({
    data,
    pagination: {
      page: parseInt(page),
      limit: parseInt(limit),
      total: count,
      totalPages: Math.ceil(count / limit)
    }
  });
}

async function createDevice(req, res, supabase, user) {
  // Check permissions
  if (!user.access_modules?.includes('device_registry')) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const deviceData = req.body;

  // Validate required fields
  const required = ['device_id', 'client_name'];
  for (const field of required) {
    if (!deviceData[field]) {
      return res.status(400).json({ error: `${field} is required` });
    }
  }

  // Insert device
  const { data, error } = await supabase
    .from('devices')
    .insert([deviceData])
    .select()
    .single();

  if (error) {
    return res.status(500).json({ error: error.message });
  }

  // Log audit trail
  await supabase.from('admin_audit_log').insert([{
    user_id: user.id,
    action: 'CREATE_DEVICE',
    resource_id: data.id,
    details: { device_id: data.device_id }
  }]);

  return res.status(201).json({ data });
}
```

---

## 6. Authentication Migration

### Current: Custom Username/Password

**Issues:**
- Passwords stored in plaintext ⚠️
- No password hashing ⚠️
- Hardcoded admin credentials ⚠️
- No OAuth support
- No MFA
- Manual session management

### Target: Supabase Auth

**Features:**
- ✅ Built-in JWT authentication
- ✅ Password hashing (bcrypt)
- ✅ Email verification
- ✅ OAuth providers (Google, GitHub, etc.)
- ✅ Multi-factor authentication (MFA)
- ✅ Password reset flow
- ✅ Role-based access control (RBAC)

### Migration Steps

#### 1. Enable Supabase Auth

```bash
# In Supabase dashboard
1. Go to Authentication > Settings
2. Enable Email authentication
3. Configure email templates
4. Set JWT expiry (default: 1 hour)
5. Enable refresh tokens
```

#### 2. Migrate User Data

```typescript
// scripts/migrate-users.ts
import { createClient } from '@supabase/supabase-js';
import bcrypt from 'bcryptjs';

async function migrateUsers() {
  const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_KEY
  );

  // Read users from Google Sheets export
  const users = await readUsersFromCSV('users_export.csv');

  for (const user of users) {
    // Generate temporary password
    const tempPassword = generateRandomPassword();
    
    // Create auth user
    const { data: authUser, error: authError } = await supabase.auth.admin.createUser({
      email: user.email,
      password: tempPassword,
      email_confirm: true,
      user_metadata: {
        employee_id: user.employee_id,
        role: user.role
      }
    });

    if (authError) {
      console.error(`Failed to create user ${user.email}:`, authError);
      continue;
    }

    // Create user profile
    const { error: profileError } = await supabase
      .from('users')
      .insert([{
        id: authUser.user.id,
        employee_id: user.employee_id,
        email: user.email,
        role: user.role,
        access_modules: user.access_modules
      }]);

    if (profileError) {
      console.error(`Failed to create profile for ${user.email}:`, profileError);
      continue;
    }

    // Send password reset email
    await supabase.auth.resetPasswordForEmail(user.email, {
      redirectTo: 'https://app.insoil.com/reset-password'
    });

    console.log(`✅ Migrated user: ${user.email}`);
  }
}
```

#### 3. Update Frontend Auth

```typescript
// lib/auth.ts
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

export async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });

  if (error) throw error;
  return data;
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function getCurrentUser() {
  const { data: { user }, error } = await supabase.auth.getUser();
  if (error) throw error;
  return user;
}

export async function checkPermission(module: string) {
  const user = await getCurrentUser();
  if (!user) return false;

  const { data: profile } = await supabase
    .from('users')
    .select('access_modules, role')
    .eq('id', user.id)
    .single();

  if (profile?.role === 'admin') return true;
  return profile?.access_modules?.includes(module) || false;
}
```

---

## 7. Frontend Migration

### Current: Monolithic HTML File

**Structure:**
- Single 32,713-line HTML file
- Embedded CSS (5,350 lines)
- Embedded JavaScript (4,982+ functions)
- No component reusability
- No build process
- No TypeScript

### Target: Next.js + React + TypeScript

**Structure:**
```
insoil-frontend/
├── public/
│   ├── images/
│   └── fonts/
├── src/
│   ├── app/                    # Next.js 13+ App Router
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   └── register/
│   │   ├── dashboard/
│   │   ├── devices/
│   │   ├── rgb-data/
│   │   ├── soil-tests/
│   │   ├── analytics/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── ui/                # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Table.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── ...
│   │   ├── charts/            # Chart components
│   │   │   ├── TrendChart.tsx
│   │   │   └── ...
│   │   └── forms/             # Form components
│   ├── lib/
│   │   ├── supabase.ts        # Supabase client
│   │   ├── auth.ts            # Auth utilities
│   │   └── api.ts             # API client
│   ├── hooks/
│   │   ├── useDevices.ts
│   │   ├── useAuth.ts
│   │   └── ...
│   ├── types/
│   │   ├── database.types.ts  # Generated from Supabase
│   │   └── ...
│   └── styles/
│       └── globals.css
├── package.json
├── tsconfig.json
└── next.config.js
```

### Component Examples

#### Device Table Component

```typescript
// components/devices/DeviceTable.tsx
import { useState, useEffect } from 'react';
import { useDevices } from '@/hooks/useDevices';
import { Table, Pagination, SearchBar } from '@/components/ui';

export default function DeviceTable() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  
  const { devices, loading, error, pagination } = useDevices({
    page,
    limit: 50,
    search
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="space-y-4">
      <SearchBar 
        value={search} 
        onChange={setSearch}
        placeholder="Search devices..."
      />
      
      <Table
        columns={[
          { key: 'device_id', label: 'Device ID' },
          { key: 'client_name', label: 'Client' },
          { key: 'district', label: 'District' },
          { key: 'installation_date', label: 'Installed' }
        ]}
        data={devices}
        onRowClick={(device) => router.push(`/devices/${device.id}`)}
      />
      
      <Pagination
        currentPage={page}
        totalPages={pagination.totalPages}
        onPageChange={setPage}
      />
    </div>
  );
}
```

#### Custom Hook for Devices

```typescript
// hooks/useDevices.ts
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';

export function useDevices({ page = 1, limit = 50, search = '' }) {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({});

  useEffect(() => {
    async function fetchDevices() {
      try {
        setLoading(true);
        
        let query = supabase
          .from('devices')
          .select('*', { count: 'exact' })
          .order('created_at', { ascending: false })
          .range((page - 1) * limit, page * limit - 1);

        if (search) {
          query = query.or(`client_name.ilike.%${search}%,device_id.ilike.%${search}%`);
        }

        const { data, error, count } = await query;

        if (error) throw error;

        setDevices(data);
        setPagination({
          page,
          limit,
          total: count,
          totalPages: Math.ceil(count / limit)
        });
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    fetchDevices();
  }, [page, limit, search]);

  return { devices, loading, error, pagination };
}
```

### Migration Strategy

**Phase 1: Extract Components**
1. Identify reusable patterns in current HTML
2. Create React components for each pattern
3. Extract CSS into Tailwind classes or CSS modules

**Phase 2: Replace google.script.run Calls**
1. Find all `google.script.run` calls
2. Replace with fetch to Next.js API routes
3. Update error handling for HTTP responses

**Phase 3: State Management**
1. Replace global variables with React Context or Zustand
2. Implement proper prop drilling or state management
3. Add React Query for data fetching

---

## 8. File Storage Strategy

### Current: Google Drive

- Service reports stored via DriveApp
- PDF reports generated and uploaded
- Limited to Google ecosystem

### Target: Supabase Storage

**Features:**
- S3-compatible object storage
- Public/private buckets
- CDN integration
- Access control with RLS
- Automatic image transformations

#### Setup Buckets

```bash
# In Supabase dashboard
1. Go to Storage
2. Create buckets:
   - 'soil-test-pdfs' (private)
   - 'service-reports' (private)
   - 'user-uploads' (private)
   - 'public-assets' (public)
```

#### Upload Files

```typescript
// lib/storage.ts
import { supabase } from './supabase';

export async function uploadPDF(
  testId: string,
  pdfBlob: Blob,
  fileName: string
) {
  const filePath = `soil-tests/${testId}/${fileName}`;

  const { data, error } = await supabase.storage
    .from('soil-test-pdfs')
    .upload(filePath, pdfBlob, {
      cacheControl: '3600',
      upsert: false
    });

  if (error) throw error;

  // Get public URL (with signed URL for private buckets)
  const { data: urlData } = await supabase.storage
    .from('soil-test-pdfs')
    .createSignedUrl(filePath, 3600); // 1 hour expiry

  return urlData.signedUrl;
}

export async function downloadPDF(filePath: string) {
  const { data, error } = await supabase.storage
    .from('soil-test-pdfs')
    .download(filePath);

  if (error) throw error;
  return data;
}
```

---

## 9. External API Integration

### Mistral AI (QC Diagnostics)

**Current Implementation:**
```javascript
// Google Apps Script
const response = UrlFetchApp.fetch('https://api.mistral.ai/v1/chat/completions', {
  method: 'post',
  headers: { 'Authorization': `Bearer ${apiKey}` },
  payload: JSON.stringify(payload)
});
```

**New Implementation (Next.js API Route):**
```typescript
// /api/qc/diagnose.ts
export default async function handler(req, res) {
  const { testData } = req.body;

  const response = await fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MISTRAL_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'mistral-large-latest',
      messages: [
        {
          role: 'system',
          content: 'You are a QC diagnostics expert...'
        },
        {
          role: 'user',
          content: JSON.stringify(testData)
        }
      ]
    })
  });

  const data = await response.json();
  return res.json(data);
}
```

---

## 10. Migration Phases

### Phase 1: Foundation (Weeks 1-2)

**Tasks:**
- [ ] Set up Supabase project
- [ ] Design PostgreSQL schema
- [ ] Create all tables with proper indexes
- [ ] Set up Supabase Auth
- [ ] Create Next.js project structure
- [ ] Configure development environment

**Deliverables:**
- Working Supabase database
- Next.js app skeleton
- Authentication flow

---

### Phase 2: Data Migration (Weeks 3-4)

**Tasks:**
- [ ] Export all Google Sheets data
- [ ] Transform data to PostgreSQL format
- [ ] Write migration scripts
- [ ] Import data to Supabase
- [ ] Validate data integrity
- [ ] Migrate user accounts

**Deliverables:**
- All historical data in PostgreSQL
- Data validation reports
- User migration complete

---

### Phase 3: API Development (Weeks 5-6)

**Tasks:**
- [ ] Build all API routes (devices, RGB, QC, soil tests)
- [ ] Implement authentication middleware
- [ ] Add input validation
- [ ] Set up error handling
- [ ] Write API documentation
- [ ] Add rate limiting

**Deliverables:**
- Complete REST API
- API documentation
- Postman collection

---

### Phase 4: Frontend Rebuild (Weeks 7-9)

**Tasks:**
- [ ] Create component library
- [ ] Build dashboard page
- [ ] Build device registry module
- [ ] Build RGB data module
- [ ] Build soil test module
- [ ] Build analytics module
- [ ] Implement real-time updates
- [ ] Add responsive design

**Deliverables:**
- Complete frontend application
- Component library
- Mobile-responsive UI

---

### Phase 5: Testing & QA (Week 10)

**Tasks:**
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Write E2E tests
- [ ] Perform security audit
- [ ] Load testing
- [ ] User acceptance testing

**Deliverables:**
- Test suite (70%+ coverage)
- Security audit report
- Performance benchmarks

---

### Phase 6: Deployment & Migration (Weeks 11-12)

**Tasks:**
- [ ] Deploy to Vercel staging
- [ ] Deploy to Supabase production
- [ ] Set up CI/CD pipeline
- [ ] Configure custom domain
- [ ] Set up monitoring/alerts
- [ ] Train users on new system
- [ ] Parallel run (both systems)
- [ ] Final cutover

**Deliverables:**
- Production deployment
- User training materials
- Rollback plan

---

## 11. Cost Analysis

### Current Costs (Google Apps Script)

| Item | Cost |
|------|------|
| Google Workspace | $6-12/user/month |
| Google Apps Script | Free (within quotas) |
| Google Drive storage | Included |
| **Total** | **$6-12/user/month** |

### New Costs (Supabase + Vercel)

#### Supabase Pricing

| Tier | Price | Includes |
|------|-------|----------|
| Free | $0/month | 500MB database, 1GB storage, 2GB egress |
| Pro | $25/month | 8GB database, 100GB storage, 250GB egress |
| Team | $599/month | 32GB database, 250GB storage, 500GB egress |

**Recommended:** Start with **Pro tier ($25/month)**

#### Vercel Pricing

| Tier | Price | Includes |
|------|-------|----------|
| Hobby | $0/month | Personal projects, 100GB bandwidth |
| Pro | $20/month | Commercial use, 1TB bandwidth, analytics |
| Enterprise | Custom | Custom everything |

**Recommended:** **Pro tier ($20/month)**

#### Additional Services

| Service | Cost | Purpose |
|---------|------|---------|
| SendGrid (Email) | $15/month | 40,000 emails/month |
| Sentry (Error tracking) | $26/month | Error monitoring |
| Vercel KV (Redis) | $10/month | Caching |
| **Total Add-ons** | **$51/month** |

### Total Monthly Costs

| Scenario | Monthly Cost | Annual Cost |
|----------|--------------|-------------|
| Minimal (Free tiers) | $0 | $0 |
| Startup (Pro tiers) | $45-70 | $540-840 |
| Production (with add-ons) | $96-120 | $1,152-1,440 |

**Comparison:**
- Google Apps Script: $72-144/year per user (for 12 users)
- Supabase + Vercel: $540-1,440/year (fixed, unlimited users)

**Break-even:** 5-10 users

---

## 12. Deployment Guide

### Prerequisites

```bash
# Install required tools
node --version  # v18+
npm --version   # v9+
git --version

# Install Supabase CLI
npm install -g supabase

# Install Vercel CLI
npm install -g vercel
```

### Step 1: Set Up Supabase Project

```bash
# Login to Supabase
supabase login

# Initialize project
supabase init

# Link to remote project
supabase link --project-ref <your-project-ref>

# Run migrations
supabase db push

# Generate TypeScript types
supabase gen types typescript --project-id <project-id> > src/types/database.types.ts
```

### Step 2: Configure Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
MISTRAL_API_KEY=your-mistral-key
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### Step 3: Deploy to Vercel

```bash
# Login to Vercel
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Configure custom domain
vercel domains add app.insoil.com
```

### Step 4: Set Up Database Backups

```bash
# Enable Supabase point-in-time recovery (Pro plan)
# Automatic daily backups to 7 days

# Manual backup
supabase db dump -f backup.sql

# Restore from backup
psql $DATABASE_URL < backup.sql
```

---

## 13. Testing Strategy

### Unit Tests (Jest)

```typescript
// __tests__/lib/auth.test.ts
import { signIn, checkPermission } from '@/lib/auth';

describe('Authentication', () => {
  test('signIn with valid credentials', async () => {
    const result = await signIn('user@example.com', 'password123');
    expect(result.user).toBeDefined();
    expect(result.session).toBeDefined();
  });

  test('checkPermission for admin user', async () => {
    const hasAccess = await checkPermission('device_registry');
    expect(hasAccess).toBe(true);
  });
});
```

### Integration Tests (Playwright)

```typescript
// e2e/devices.spec.ts
import { test, expect } from '@playwright/test';

test('create new device', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'admin@insoil.com');
  await page.fill('[name="password"]', 'admin123');
  await page.click('button[type="submit"]');

  await page.goto('/devices');
  await page.click('text=Add Device');
  
  await page.fill('[name="device_id"]', '123456789012345');
  await page.fill('[name="client_name"]', 'Test Client');
  await page.click('button:has-text("Save")');

  await expect(page.locator('text=Device created successfully')).toBeVisible();
});
```

### Load Testing (k6)

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
};

export default function () {
  const res = http.get('https://app.insoil.com/api/devices?page=1&limit=50');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

---

## 14. Rollback Plan

### Scenario 1: Critical Bug in Production

**Steps:**
1. Immediately rollback Vercel deployment
   ```bash
   vercel rollback
   ```
2. Check error logs in Sentry/Vercel dashboard
3. Fix bug in development
4. Deploy fix to staging
5. Test thoroughly
6. Redeploy to production

### Scenario 2: Database Issues

**Steps:**
1. Stop all write operations
2. Enable read-only mode in Supabase
3. Restore from backup
   ```bash
   supabase db reset --db-url $DATABASE_URL
   ```
4. Re-run migrations
5. Validate data integrity
6. Resume normal operations

### Scenario 3: Complete System Failure

**Steps:**
1. Redirect users to Google Apps Script version (keep old URL active)
2. Communicate outage to users
3. Debug and fix issues
4. Test fixes in staging
5. Gradual rollout (10% → 50% → 100% of users)

---

## 15. Monitoring & Observability

### Set Up Monitoring

#### Vercel Analytics

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

#### Error Tracking (Sentry)

```typescript
// sentry.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
});
```

#### Database Monitoring

```sql
-- Create monitoring views
CREATE VIEW active_connections AS
SELECT count(*) FROM pg_stat_activity;

CREATE VIEW slow_queries AS
SELECT query, query_start, now() - query_start AS duration
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '5 seconds';
```

### Key Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| API response time | < 200ms | > 1s |
| Page load time | < 2s | > 5s |
| Error rate | < 0.1% | > 1% |
| Database CPU | < 50% | > 80% |
| Database memory | < 70% | > 85% |
| Uptime | 99.9% | < 99% |

---

## 16. Security Checklist

### Before Going Live

- [ ] Remove all hardcoded credentials
- [ ] Enable HTTPS only (no HTTP)
- [ ] Configure CORS properly
- [ ] Enable Row Level Security (RLS) on all tables
- [ ] Set up rate limiting on API routes
- [ ] Enable Vercel WAF (Web Application Firewall)
- [ ] Add Content Security Policy (CSP) headers
- [ ] Enable Supabase email verification
- [ ] Set up MFA for admin accounts
- [ ] Configure session timeouts
- [ ] Add SQL injection protection
- [ ] Sanitize all user inputs
- [ ] Enable audit logging
- [ ] Set up automated security scanning
- [ ] Perform penetration testing
- [ ] Review all environment variables
- [ ] Enable database encryption at rest
- [ ] Configure backup retention
- [ ] Set up incident response plan
- [ ] Train team on security practices

---

## 17. Post-Migration Tasks

### Week 1 After Launch

- [ ] Monitor error rates daily
- [ ] Review user feedback
- [ ] Fix critical bugs
- [ ] Optimize slow queries
- [ ] Update documentation

### Month 1 After Launch

- [ ] Analyze performance metrics
- [ ] Gather user satisfaction data
- [ ] Plan feature enhancements
- [ ] Review costs vs budget
- [ ] Optimize infrastructure

### Quarter 1 After Launch

- [ ] Security audit
- [ ] Scalability review
- [ ] ROI analysis
- [ ] Plan Phase 2 features
- [ ] Update roadmap

---

## 18. Resources & Documentation

### Official Documentation

- [Supabase Docs](https://supabase.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [Vercel Docs](https://vercel.com/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

### Learning Resources

- [Supabase Crash Course](https://www.youtube.com/watch?v=7uKQBl9uZ00)
- [Next.js 13 Tutorial](https://nextjs.org/learn)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

### Community

- [Supabase Discord](https://discord.supabase.com/)
- [Next.js Discord](https://nextjs.org/discord)
- [r/Supabase](https://reddit.com/r/Supabase)

---

## Conclusion

Migrating InsoilTool to Supabase + Vercel offers significant benefits in terms of scalability, performance, and modern development practices. While the migration requires 8-12 weeks of focused work, the result will be a production-ready, enterprise-grade application.

### Key Takeaways

✅ **Scalability:** Handle 10x more users and data  
✅ **Performance:** 5-10x faster page loads  
✅ **Security:** Modern auth, encryption, RLS  
✅ **DX:** Better development experience with TypeScript, hot reload, testing  
✅ **Independence:** No Google Workspace dependency  
✅ **Professional:** Custom domain, white-label capability  

### Next Steps

1. Review this guide with your team
2. Create a project plan with timeline
3. Set up Supabase and Vercel accounts
4. Start with Phase 1 (Foundation)
5. Build incrementally, test thoroughly
6. Deploy to staging first
7. Gradual rollout to production

**Questions?** Refer to the official documentation or reach out to the community for support.

---

**Document Version:** 1.0  
**Last Updated:** February 17, 2026  
**Author:** GitHub Copilot Code Analysis
