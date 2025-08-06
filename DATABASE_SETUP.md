# 🗄️ Database Setup Guide

## 📋 **Required Steps**


### 1. **PostgreSQL Installation**


```bash

# Download from: https://www.postgresql.org/download/windows/

# Or use Docker:

docker run --name postgres-ehb -e POSTGRES_PASSWORD=ehb_password -e POSTGRES_DB=ehb_database -p 5432:5432 -d postgres:15

```

### 2. **Database Configuration**


```bash

# Create database user

CREATE USER ehb_user WITH PASSWORD 'ehb_password';
CREATE DATABASE ehb_database OWNER ehb_user;
GRANT ALL PRIVILEGES ON DATABASE ehb_database TO ehb_user;

```

### 3. **Environment Variables**


Update `.env` file:

```env
DATABASE_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_database

```

### 4. **Database Models**


Create these files:

- `backend/models/database/user.py`

- `backend/models/database/service.py`

- `backend/models/database/transaction.py`

- `backend/models/database/wallet.py`

### 5. **Migrations**


```bash
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

```

## 🎯 **Priority: HIGH**


- Database connection required for full functionality

- User authentication depends on database

- All services need database integration
