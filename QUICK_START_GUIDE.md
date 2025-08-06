# 🚀 EHB Quick Start Guide

## 📋 **Prerequisites**


- Python 3.10+


- Node.js 18+


- PostgreSQL (optional, SQLite used by default)

## 🚀 **Quick Start Commands**


### **Option 1: Automatic Startup (Recommended)**


```bash

# Start all services automatically

start_services.bat

# Start frontend in separate terminal

start_frontend.bat

```

### **Option 2: Manual Startup**


#### **Step 1: Start Backend Services**


```bash

# Terminal 1: Backend API

cd backend
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2: PSS Service

cd services/pss
python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload

# Terminal 3: EMO Service

cd services/emo
python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload

# Terminal 4: EDR Service

cd services/edr
python -m uvicorn main:app --host 0.0.0.0 --port 4002 --reload

```

#### **Step 2: Start Frontend**


```bash

# Terminal 5: Frontend

cd frontend
npm install
npm run dev

```

## 🔗 **Access URLs**


| Component | URL | Description |
|-----------|-----|-------------|
| Frontend | http://localhost:3000 | EHB Home Page & Dashboard |
| Backend API | http://localhost:8000 | Main API Documentation |
| PSS Service | http://localhost:4001 | Personal Security System |
| EMO Service | http://localhost:4003 | Easy Management Office |
| EDR Service | http://localhost:4002 | Exam Decision Registration |

## 🧪 **Testing Commands**


### **Backend Testing**


```bash
cd backend
python simple_test.py          # Quick system test

python service_status.py       # Service health check

python -m pytest              # Run all tests

```

### **Frontend Testing**


```bash
cd frontend
npm test                      # Run frontend tests

npm run build                 # Build for production

```

## 📊 **System Status Check**


### **Check Running Services**


```bash

# Check if ports are in use

netstat -an | findstr "8000\|4001\|4002\|4003"

# Test backend health

curl http://localhost:8000/health

# Test service health

curl http://localhost:4001/health
curl http://localhost:4002/health
curl http://localhost:4003/health

```

## 🔧 **Troubleshooting**


### **Common Issues**


1. **Port Already in Use**
   ```bash

   # Find process using port

   netstat -ano | findstr :8000
   # Kill process

   taskkill /PID <PID> /F
   ```

2. **Database Connection Error**
   ```bash

   # Check database setup

   cd backend
   python -c "from utils.database.connection import test_connection; test_connection()"
   ```

3. **Frontend Build Error**
   ```bash

   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

### **Service Status**


| Service | Status | Port | Health Check |
|---------|--------|------|--------------|
| Backend API | ❌ Not Running | 8000 | http://localhost:8000/health |
| PSS | ❌ Not Running | 4001 | http://localhost:4001/health |
| EMO | ❌ Not Running | 4003 | http://localhost:4003/health |
| EDR | ❌ Not Running | 4002 | http://localhost:4002/health |

## 📁 **Project Structure**


```

EHB HOME PAGE/
├── frontend/                 # Next.js application

│   ├── pages/               # React pages

│   ├── components/          # React components

│   └── package.json         # Frontend dependencies

├── backend/                  # FastAPI application

│   ├── app/                 # Main application

│   ├── api/                 # API routes

│   ├── models/              # Database models

│   ├── services/            # Business logic

│   └── tests/               # Backend tests

├── services/                 # Microservices

│   ├── pss/                 # Personal Security System

│   ├── emo/                 # Easy Management Office

│   ├── edr/                 # Exam Decision Registration

│   └── ...                  # Other services

├── start_services.bat       # Service startup script

├── start_frontend.bat       # Frontend startup script

└── README.md                # Project documentation

```

## 🎯 **Development Workflow**


1. **Start Services**: Run `start_services.bat`
2. **Start Frontend**: Run `start_frontend.bat`
3. **Test System**: Run `python simple_test.py`
4. **Develop**: Make changes and see live updates
5. **Test**: Run tests before committing

## 📞 **Support**


- **Documentation**: Check `README.md` and `SYSTEM_STATUS.md`

- **Issues**: Check service logs in terminal windows

- **Testing**: Use `simple_test.py` for quick health checks

---


**Note**: All services need to be running for the complete system to work. Use the batch scripts for easiest startup.
