@echo off
echo 🚀 Setting up EHB Home Page environment...

REM Set environment variables
set DATABASE_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_database
set DATABASE_TEST_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_test_db
set SECRET_KEY=ehb-super-secret-key-change-this-in-production-2025
set ALGORITHM=HS256
set ACCESS_TOKEN_EXPIRE_MINUTES=30
set REFRESH_TOKEN_EXPIRE_DAYS=7
set OPENAI_API_KEY=your-openai-api-key
set ANTHROPIC_API_KEY=your-anthropic-api-key
set GOOGLE_AI_API_KEY=your-google-ai-api-key
set ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
set POLYGON_RPC_URL=https://polygon-rpc.com
set BSC_RPC_URL=https://bsc-dataseed.binance.org
set PRIVATE_KEY=your-private-key-for-transactions
set CONTRACT_ADDRESS=your-ehbgc-contract-address
set REDIS_URL=redis://localhost:6379
set REDIS_PASSWORD=your-redis-password
set CACHE_TTL=3600
set SMTP_HOST=smtp.gmail.com
set SMTP_PORT=587
set SMTP_USER=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set AWS_ACCESS_KEY_ID=your-aws-access-key
set AWS_SECRET_ACCESS_KEY=your-aws-secret-key
set AWS_REGION=us-east-1
set S3_BUCKET_NAME=ehb-storage-bucket
set STRIPE_SECRET_KEY=your-stripe-secret-key
set STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
set PAYPAL_CLIENT_ID=your-paypal-client-id
set PAYPAL_CLIENT_SECRET=your-paypal-client-secret
set SENTRY_DSN=your-sentry-dsn
set GOOGLE_ANALYTICS_ID=your-ga-id
set MIXPANEL_TOKEN=your-mixpanel-token
set DEBUG=True
set ENVIRONMENT=development
set LOG_LEVEL=DEBUG
set CORS_ORIGINS=http://localhost:3000,http://localhost:8000
set FRONTEND_PORT=3000
set BACKEND_PORT=8000
set PSS_PORT=4001
set EMO_PORT=4003
set EDR_PORT=4002
set JPS_PORT=4005
set GOSELLR_PORT=4004
set WALLET_PORT=5001
set FRANCHISE_PORT=4006
set ENABLE_AI_FEATURES=True
set ENABLE_BLOCKCHAIN_FEATURES=True
set ENABLE_PAYMENT_FEATURES=True
set ENABLE_ANALYTICS=True

echo ✅ Environment variables set successfully!

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo 📁 Found backend directory

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

echo 🐍 Python found

REM Check if uvicorn is available
python -c "import uvicorn" >nul 2>&1
if errorlevel 1 (
    echo ❌ Uvicorn not found. Installing...
    pip install uvicorn
)

echo ⚡ Uvicorn found

REM Navigate to backend directory and start the server
echo 🚀 Starting EHB backend server...
cd backend
python -m uvicorn app.main:app --reload --port 8000
