# 🚀 Manual EHB Services Startup Guide

## 📋 **Current Status**
- **EDR Service**: ✅ Running (Port 4002)
- **EMO Service**: ❌ Not Running (Port 4003)
- **PSS Service**: ❌ Not Running (Port 4001)
- **Backend API**: ❌ Not Running (Port 8000)
- **Frontend**: ⏳ Starting (Port 3000)

## 🎯 **Step-by-Step Startup**

### **Step 1: Start Backend API**
```bash
# Open new terminal
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### **Step 2: Start PSS Service**
```bash
# Open new terminal
cd services/pss
python -m uvicorn main:app --host 0.0.0.0 --port 4001 --reload
```

### **Step 3: Start EMO Service**
```bash
# Open new terminal
cd services/emo
python -m uvicorn main:app --host 0.0.0.0 --port 4003 --reload
```

### **Step 4: Start Frontend**
```bash
# Open new terminal
cd frontend
npm run dev
```

## 🔗 **Access URLs After Startup**

| Service | URL | Status |
|---------|-----|--------|
| Frontend | http://localhost:3000 | ⏳ Starting |
| Backend API | http://localhost:8000 | ❌ Not Running |
| PSS Service | http://localhost:4001 | ❌ Not Running |
| EMO Service | http://localhost:4003 | ❌ Not Running |
| EDR Service | http://localhost:4002 | ✅ Running |

## 🧪 **Testing Commands**

### **Test All Services**
```bash
python test_services_simple.py
```

### **Test Individual Services**
```bash
# Test Backend
curl http://localhost:8000/health

# Test PSS
curl http://localhost:4001/health

# Test EMO
curl http://localhost:4003/health

# Test EDR
curl http://localhost:4002/health
```

## 🔧 **Troubleshooting**

### **Port Already in Use**
```bash
# Find process using port
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

### **Service Not Starting**
1. Check if Python is installed: `python --version`
2. Check if uvicorn is installed: `pip install uvicorn`
3. Check if dependencies are installed: `pip install -r requirements.txt`

### **Frontend Issues**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## 📊 **Expected Results**

After starting all services, you should see:

```
🧪 Testing EHB Services...
========================================
✅ Backend API: Running
✅ PSS Service: Running
✅ EMO Service: Running
✅ EDR Service: Running

📊 Summary:
--------------------
Running: 4/4 services
🎉 All services are running!
```

## 🎯 **Next Steps**

1. **Start Backend API** in new terminal
2. **Start PSS Service** in new terminal
3. **Start EMO Service** in new terminal
4. **Verify Frontend** is running
5. **Test Complete System**

---

**Note**: Each service needs to run in a separate terminal window for proper operation.
