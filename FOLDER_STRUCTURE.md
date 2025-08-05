# 📁 EHB Home Page & Dashboard - Complete Folder Structure

## 🏗️ Project Overview
```
EHB-HOME-PAGE/
├── 📁 frontend/                 # Next.js React Application
├── 📁 backend/                  # FastAPI Python Backend
├── 📁 services/                 # Individual EHB Services
├── 📁 blockchain/               # Smart Contracts & Web3
├── 📁 docs/                     # Documentation
├── 📁 database/                 # Database Files
└── 📁 deployment/               # Deployment Configurations
```

## 🎨 Frontend Structure (Next.js)

### 📁 `/frontend/`
```
frontend/
├── 📁 pages/                    # Next.js Pages
│   ├── 📄 _app.tsx             # Main App Component
│   ├── 📄 index.tsx            # Home Page
│   ├── 📁 admin/               # Admin Pages
│   │   ├── 📄 index.tsx        # Admin Dashboard
│   │   ├── 📄 users.tsx        # User Management
│   │   ├── 📄 services.tsx     # Service Management
│   │   ├── 📄 analytics.tsx    # Analytics Dashboard
│   │   └── 📄 settings.tsx     # Admin Settings
│   ├── 📁 dashboard/           # User Dashboard Pages
│   │   ├── 📄 index.tsx        # Main Dashboard
│   │   ├── 📄 profile.tsx      # User Profile
│   │   ├── 📄 wallet.tsx       # Wallet Management
│   │   └── 📄 settings.tsx     # User Settings
│   ├── 📁 services/            # Service Pages
│   │   ├── 📄 gosellr.tsx      # GoSellr Marketplace
│   │   ├── 📄 pss.tsx          # PSS Verification
│   │   ├── 📄 emo.tsx          # EMO Business
│   │   ├── 📄 edr.tsx          # EDR Testing
│   │   └── 📄 jps.tsx          # JPS Profiles
│   └── 📁 auth/                # Authentication Pages
│       ├── 📄 login.tsx        # Login Page
│       ├── 📄 register.tsx     # Registration
│       └── 📄 forgot.tsx       # Password Reset
├── 📁 components/              # Reusable Components
│   ├── 📁 admin/              # Admin Components
│   │   ├── 📄 Sidebar.tsx     # Admin Sidebar
│   │   ├── 📄 UserTable.tsx   # User Management Table
│   │   ├── 📄 ServiceCard.tsx # Service Management
│   │   ├── 📄 Analytics.tsx   # Analytics Charts
│   │   └── 📄 Settings.tsx    # Admin Settings
│   ├── 📁 dashboard/          # Dashboard Components
│   │   ├── 📄 Sidebar.tsx     # User Sidebar
│   │   ├── 📄 Stats.tsx       # Statistics Cards
│   │   ├── 📄 Wallet.tsx      # Wallet Component
│   │   └── 📄 Profile.tsx     # Profile Component
│   ├── 📁 services/           # Service Components
│   │   ├── 📄 ServiceCard.tsx # Service Cards
│   │   ├── 📄 ProductCard.tsx # Product Cards
│   │   └── 📄 OrderCard.tsx   # Order Cards
│   └── 📁 shared/             # Shared Components
│       ├── 📄 Header.tsx      # Header Component
│       ├── 📄 Footer.tsx      # Footer Component
│       ├── 📄 Button.tsx      # Button Component
│       ├── 📄 Modal.tsx       # Modal Component
│       └── 📄 Loading.tsx     # Loading Component
├── 📁 hooks/                  # Custom React Hooks
│   ├── 📄 useAuth.ts          # Authentication Hook
│   ├── 📄 useWallet.ts        # Wallet Hook
│   ├── 📄 useServices.ts      # Services Hook
│   └── 📄 useAdmin.ts         # Admin Hook
├── 📁 utils/                  # Utility Functions
│   ├── 📄 api.ts              # API Functions
│   ├── 📄 auth.ts             # Auth Utilities
│   ├── 📄 blockchain.ts       # Blockchain Utils
│   ├── 📄 validation.ts       # Form Validation
│   └── 📄 helpers.ts          # Helper Functions
├── 📁 styles/                 # CSS & Styling
│   ├── 📄 globals.css         # Global Styles
│   ├── 📄 components.css      # Component Styles
│   └── 📄 admin.css           # Admin Styles
├── 📁 public/                 # Static Assets
│   ├── 📁 images/             # Images
│   ├── 📁 icons/              # Icons
│   └── 📄 favicon.ico         # Favicon
├── 📄 package.json            # Dependencies
├── 📄 next.config.js          # Next.js Config
├── 📄 tailwind.config.js      # Tailwind Config
├── 📄 postcss.config.js       # PostCSS Config
└── 📄 tsconfig.json           # TypeScript Config
```

## 🐍 Backend Structure (FastAPI)

### 📁 `/backend/`
```
backend/
├── 📁 app/                    # Main Application
│   ├── 📄 main.py             # FastAPI App Entry
│   ├── 📄 config.py           # Configuration
│   └── 📄 dependencies.py     # Dependencies
├── 📁 models/                 # Database Models
│   ├── 📁 database/           # Database Models
│   │   ├── 📄 user.py         # User Model
│   │   ├── 📄 service.py      # Service Model
│   │   ├── 📄 transaction.py  # Transaction Model
│   │   └── 📄 wallet.py       # Wallet Model
│   ├── 📄 base.py             # Base Model
│   └── 📄 schemas.py          # Pydantic Schemas
├── 📁 services/               # Business Logic
│   ├── 📁 auth/               # Authentication
│   │   ├── 📄 auth.py         # Auth Service
│   │   ├── 📄 jwt.py          # JWT Utils
│   │   └── 📄 permissions.py  # Permissions
│   ├── 📁 sql/                # SQL System
│   │   ├── 📄 sql_service.py  # SQL Logic
│   │   └── 📄 levels.py       # Level Management
│   ├── 📁 blockchain/         # Blockchain
│   │   ├── 📄 web3_service.py # Web3 Integration
│   │   └── 📄 contracts.py    # Smart Contracts
│   └── 📁 admin/              # Admin Services
│       ├── 📄 user_management.py
│       ├── 📄 service_management.py
│       └── 📄 analytics.py
├── 📁 api/                    # API Routes
│   ├── 📁 v1/                 # API Version 1
│   │   ├── 📄 auth.py         # Auth Routes
│   │   ├── 📄 users.py        # User Routes
│   │   ├── 📄 services.py     # Service Routes
│   │   └── 📄 dashboard.py    # Dashboard Routes
│   ├── 📁 admin/              # Admin API
│   │   ├── 📄 users.py        # User Management
│   │   ├── 📄 services.py     # Service Management
│   │   ├── 📄 analytics.py    # Analytics API
│   │   └── 📄 settings.py     # Settings API
│   └── 📄 deps.py             # Dependencies
├── 📁 utils/                  # Utilities
│   ├── 📁 database/           # Database Utils
│   │   ├── 📄 connection.py   # DB Connection
│   │   └── 📄 migrations.py   # Migrations
│   ├── 📁 auth/               # Auth Utils
│   │   ├── 📄 security.py     # Security Utils
│   │   └── 📄 validation.py   # Validation
│   ├── 📁 blockchain/         # Blockchain Utils
│   │   ├── 📄 web3.py         # Web3 Utils
│   │   └── 📄 contracts.py    # Contract Utils
│   └── 📄 helpers.py          # General Helpers
├── 📄 requirements.txt         # Python Dependencies
└── 📄 alembic.ini             # Database Migrations
```

## 🔧 Services Structure

### 📁 `/services/`
```
services/
├── 📁 pss/                    # Personal Security System
│   ├── 📄 main.py             # PSS Service
│   ├── 📄 models.py           # PSS Models
│   ├── 📄 api.py              # PSS API
│   └── 📄 verification.py     # Verification Logic
├── 📁 emo/                    # Easy Management Office
│   ├── 📄 main.py             # EMO Service
│   ├── 📄 models.py           # EMO Models
│   ├── 📄 api.py              # EMO API
│   └── 📄 business.py         # Business Logic
├── 📁 edr/                    # Exam Decision Registration
│   ├── 📄 main.py             # EDR Service
│   ├── 📄 models.py           # EDR Models
│   ├── 📄 api.py              # EDR API
│   └── 📄 testing.py          # Testing Logic
├── 📁 jps/                    # Job Profile System
│   ├── 📄 main.py             # JPS Service
│   ├── 📄 models.py           # JPS Models
│   ├── 📄 api.py              # JPS API
│   └── 📄 profiles.py         # Profile Logic
├── 📁 gosellr/                # E-commerce Platform
│   ├── 📄 main.py             # GoSellr Service
│   ├── 📄 models.py           # GoSellr Models
│   ├── 📄 api.py              # GoSellr API
│   └── 📄 marketplace.py      # Marketplace Logic
├── 📁 wallet/                 # Wallet System
│   ├── 📄 main.py             # Wallet Service
│   ├── 📄 models.py           # Wallet Models
│   ├── 📄 api.py              # Wallet API
│   └── 📄 transactions.py     # Transaction Logic
├── 📁 franchise/              # Franchise System
│   ├── 📄 main.py             # Franchise Service
│   ├── 📄 models.py           # Franchise Models
│   ├── 📄 api.py              # Franchise API
│   └── 📄 management.py       # Management Logic
├── 📁 ai-agent/               # AI Agent
│   ├── 📄 main.py             # AI Agent Service
│   ├── 📄 models.py           # AI Models
│   ├── 📄 api.py              # AI API
│   └── 📄 intelligence.py     # AI Logic
└── 📁 ai-robot/               # AI Robot
    ├── 📄 main.py             # AI Robot Service
    ├── 📄 models.py           # Robot Models
    ├── 📄 api.py              # Robot API
    └── 📄 automation.py       # Automation Logic
```

## ⛓️ Blockchain Structure

### 📁 `/blockchain/`
```
blockchain/
├── 📁 contracts/              # Smart Contracts
│   ├── 📄 EHBGC.sol          # EHBGC Token
│   ├── 📄 TrustyWallet.sol   # Trusty Wallet
│   ├── 📄 Validator.sol       # Validator Contract
│   └── 📄 Marketplace.sol     # Marketplace Contract
├── 📁 scripts/                # Deployment Scripts
│   ├── 📄 deploy.py           # Deployment Script
│   ├── 📄 verify.py           # Contract Verification
│   └── 📄 upgrade.py          # Contract Upgrade
├── 📁 migrations/             # Contract Migrations
│   ├── 📄 1_deploy_token.js   # Token Deployment
│   ├── 📄 2_deploy_wallet.js  # Wallet Deployment
│   └── 📄 3_deploy_validator.js
├── 📁 test/                   # Contract Tests
│   ├── 📄 EHBGC.test.js       # Token Tests
│   ├── 📄 TrustyWallet.test.js
│   └── 📄 Validator.test.js   # Validator Tests
├── 📄 hardhat.config.js       # Hardhat Config
├── 📄 package.json            # Blockchain Dependencies
└── 📄 truffle-config.js       # Truffle Config
```

## 📚 Documentation Structure

### 📁 `/docs/`
```
docs/
├── 📁 api/                    # API Documentation
│   ├── 📄 auth.md             # Authentication API
│   ├── 📄 users.md            # Users API
│   ├── 📄 services.md         # Services API
│   └── 📄 admin.md            # Admin API
├── 📁 deployment/             # Deployment Guides
│   ├── 📄 docker.md           # Docker Deployment
│   ├── 📄 kubernetes.md       # Kubernetes Setup
│   ├── 📄 aws.md              # AWS Deployment
│   └── 📄 production.md       # Production Setup
├── 📁 user-guide/             # User Documentation
│   ├── 📄 getting-started.md  # Getting Started
│   ├── 📄 features.md         # Features Guide
│   ├── 📄 troubleshooting.md  # Troubleshooting
│   └── 📄 faq.md              # FAQ
├── 📁 admin-guide/            # Admin Documentation
│   ├── 📄 admin-setup.md      # Admin Setup
│   ├── 📄 user-management.md  # User Management
│   ├── 📄 service-management.md
│   └── 📄 analytics.md        # Analytics Guide
└── 📄 README.md               # Main Documentation
```

## 🔄 Data Flow Architecture

### 📊 User Journey Flow:
```
1. User Registration (JPS)
   ↓
2. Identity Verification (PSS)
   ↓
3. Business Verification (EMO)
   ↓
4. Skill Testing (EDR)
   ↓
5. SQL Level Assignment
   ↓
6. Service Access (GoSellr, Wallet, etc.)
   ↓
7. Blockchain Integration (EHBGC)
   ↓
8. AI Services (AI Agent/Robot)
```

### 🔗 Service Communication:
```
Frontend (Next.js)
    ↓ HTTP/WebSocket
Backend (FastAPI)
    ↓ API Calls
Individual Services (PSS, EMO, EDR, etc.)
    ↓ Database
PostgreSQL + Redis
    ↓ Blockchain
Ethereum/Polygon Network
```

## 🚀 Development Workflow

### 📋 Development Phases:
1. **Phase 1**: Core Services (PSS, EMO, EDR, JPS)
2. **Phase 2**: Commercial Services (GoSellr, Wallet, Franchise)
3. **Phase 3**: Blockchain Integration (EHBGC, Trusty Wallet)
4. **Phase 4**: AI Services (AI Agent, AI Robot)

### 🛠️ Technology Stack:
- **Frontend**: Next.js, React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, SQLAlchemy, PostgreSQL
- **Blockchain**: Solidity, Web3.js, Hardhat
- **AI**: OpenAI, LangChain, Anthropic
- **Deployment**: Docker, Kubernetes, AWS

---

**EHB Technologies** - Complete Ecosystem Architecture
