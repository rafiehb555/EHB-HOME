# EHB Home Page - Environment Configuration Guide

## 🚀 Quick Start

### Option 1: Using PowerShell Script (Recommended)

```powershell
.\setup-environment.ps1

```

### Option 2: Using Batch File

```cmd
start-backend.bat

```

### Option 3: Manual Setup

Follow the steps below to manually configure your environment.

## 📋 Environment Variables Configuration

### 1. Database Configuration

```bash
DATABASE_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_database
DATABASE_TEST_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_test_db

```

### 2. JWT Authentication

```bash
SECRET_KEY=ehb-super-secret-key-change-this-in-production-2025
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

```

### 3. AI Services

```bash
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key

```

### 4. Blockchain Configuration

```bash
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
POLYGON_RPC_URL=https://polygon-rpc.com
BSC_RPC_URL=https://bsc-dataseed.binance.org
PRIVATE_KEY=your-private-key-for-transactions
CONTRACT_ADDRESS=your-ehbgc-contract-address

```

### 5. Redis & Caching

```bash
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your-redis-password
CACHE_TTL=3600

```

### 6. Email Configuration

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

```

### 7. File Storage

```bash
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
S3_BUCKET_NAME=ehb-storage-bucket

```

### 8. Payment Gateway

```bash
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret

```

### 9. Monitoring & Analytics

```bash
SENTRY_DSN=your-sentry-dsn
GOOGLE_ANALYTICS_ID=your-ga-id
MIXPANEL_TOKEN=your-mixpanel-token

```

### 10. Development Settings

```bash
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

```

### 11. Service Ports

```bash
FRONTEND_PORT=3000
BACKEND_PORT=8000
PSS_PORT=4001
EMO_PORT=4003
EDR_PORT=4002
JPS_PORT=4005
GOSELLR_PORT=4004
WALLET_PORT=5001
FRANCHISE_PORT=4006

```

### 12. Feature Flags

```bash
ENABLE_AI_FEATURES=True
ENABLE_BLOCKCHAIN_FEATURES=True
ENABLE_PAYMENT_FEATURES=True
ENABLE_ANALYTICS=True

```

## 🔧 Manual Setup Instructions

### Step 1: Create Environment File

Create a `.env` file in the project root with the variables above.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 3: Start the Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000

```

## 🐛 Troubleshooting

### PowerShell Syntax Error

If you encounter the `&&` syntax error in PowerShell, use one of these alternatives:

1. **Use the provided scripts:**
   ```powershell

   .\setup-environment.ps1
   ```

2. **Use separate commands:**
   ```powershell

   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

3. **Use Command Prompt:**
   ```cmd

   start-backend.bat
   ```

### Missing Dependencies

If you get import errors, install the required packages:

```bash
pip install fastapi uvicorn python-dotenv

```

### Port Already in Use

If port 8000 is already in use, change the port:

```bash
python -m uvicorn app.main:app --reload --port 8001

```

## 🔐 Security Notes

1. **Never commit real API keys** to version control

2. **Use different keys** for development and production

3. **Rotate secrets regularly** in production

4. **Use environment-specific** configuration files

## 📊 Environment Validation

After setting up, you can validate your configuration by:

1. **Checking the health endpoint:**
   ```

   GET http://localhost:8000/health
   ```

2. **Checking services status:**
   ```

   GET http://localhost:8000/api/services/status
   ```

3. **Checking dashboard data:**
   ```

   GET http://localhost:8000/api/dashboard
   ```

## 🚀 Production Deployment

For production deployment, use the `env.production.example` file as a template and:

1. Set `ENVIRONMENT=production`
2. Set `DEBUG=False`
3. Use strong, unique secrets
4. Configure proper CORS origins
5. Set up monitoring and logging
6. Use HTTPS in production

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure all dependencies are installed
4. Check if required services (PostgreSQL, Redis) are running
