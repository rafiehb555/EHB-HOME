<<<<<<< HEAD
# 🏠 EHB Home Page & Dashboard

Complete ecosystem for EHB Technologies - Home Page, Dashboard, and all integrated services.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL
- Docker (optional)

### Installation

1. **Clone Repository**
```bash
git clone <repository-url>
cd EHB-HOME-PAGE
```

2. **Install Frontend Dependencies**
```bash
npm install
```

3. **Install Backend Dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start Development**
```bash
# Frontend (Next.js)
npm run dev

# Backend (FastAPI)
uvicorn app.main:app --reload --port 8000
```

## 🏗️ Project Structure

```
EHB-HOME-PAGE/
├── frontend/                 # Next.js React App
│   ├── components/          # Reusable UI components
│   ├── pages/              # Next.js pages
│   ├── hooks/              # Custom React hooks
│   ├── utils/              # Utility functions
│   └── styles/             # CSS/Tailwind styles
├── backend/                 # FastAPI Backend
│   ├── app/                # Main application
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── api/                # API routes
│   └── utils/              # Backend utilities
├── blockchain/              # Smart contracts
│   ├── contracts/          # Solidity contracts
│   ├── migrations/         # Contract migrations
│   └── scripts/            # Deployment scripts
└── docs/                   # Documentation
```

## 🔧 Services Integration

### Phase 1 - Core Services
- **EHB Dashboard** - Main user interface
- **EHB SQL** - User quality level system
- **PSS** - Personal Security System (KYC)
- **EMO** - Easy Management Office (Business verification)
- **EDR** - Exam Decision Registration (Skill testing)
- **JPS** - Job Profile System

### Phase 2 - Commercial Services
- **GoSellr** - E-commerce marketplace
- **Wallet** - Payment & transaction system
- **Franchise** - Business management system

### Phase 3 - Blockchain Services
- **EHBGC Coin** - Native cryptocurrency
- **Trusty Wallet** - Advanced wallet features
- **Validator Dashboard** - Blockchain validation

### Phase 4 - AI & Advanced Services
- **AI Marketplace** - AI services platform
- **AI Agent** - Intelligent automation
- **AI Robot** - Advanced AI assistant

## 🛠️ Development Commands

```bash
# Frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
npm run test         # Run tests

# Backend
uvicorn app.main:app --reload  # Start FastAPI server
pytest               # Run tests
black .              # Format code
mypy .               # Type checking

# Docker
docker-compose up    # Start all services
docker-compose down  # Stop all services
```

## 🔐 Environment Variables

Create `.env` file with:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ehb_db

# JWT
SECRET_KEY=your-secret-key
ALGORITHM=HS256

# OpenAI
OPENAI_API_KEY=your-openai-key

# Blockchain
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
PRIVATE_KEY=your-private-key

# Redis
REDIS_URL=redis://localhost:6379
```

## 📊 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For support, email support@ehbtechnologies.com or create an issue.

---

**EHB Technologies** - Building the future of decentralized commerce and AI services.
=======
# EHB-HOME
>>>>>>> d91a8add5596fdb6616881732edd159a91fc43be
