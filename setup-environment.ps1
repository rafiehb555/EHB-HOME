# ========================================
# EHB Home Page Environment Setup Script
# ========================================

Write-Host "Setting up EHB Home Page environment..." -ForegroundColor Green

# Set environment variables
$env:DATABASE_URL = "postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"
$env:DATABASE_TEST_URL = "postgresql://ehb_user:ehb_password@localhost:5432/ehb_test_db"
$env:SECRET_KEY = "ehb-super-secret-key-change-this-in-production-2025"
$env:ALGORITHM = "HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES = "30"
$env:REFRESH_TOKEN_EXPIRE_DAYS = "7"
$env:OPENAI_API_KEY = "your-openai-api-key"
$env:ANTHROPIC_API_KEY = "your-anthropic-api-key"
$env:GOOGLE_AI_API_KEY = "your-google-ai-api-key"
$env:ETHEREUM_RPC_URL = "https://mainnet.infura.io/v3/your-project-id"
$env:POLYGON_RPC_URL = "https://polygon-rpc.com"
$env:BSC_RPC_URL = "https://bsc-dataseed.binance.org"
$env:PRIVATE_KEY = "your-private-key-for-transactions"
$env:CONTRACT_ADDRESS = "your-ehbgc-contract-address"
$env:REDIS_URL = "redis://localhost:6379"
$env:REDIS_PASSWORD = "your-redis-password"
$env:CACHE_TTL = "3600"
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "your-email@gmail.com"
$env:SMTP_PASSWORD = "your-app-password"
$env:AWS_ACCESS_KEY_ID = "your-aws-access-key"
$env:AWS_SECRET_ACCESS_KEY = "your-aws-secret-key"
$env:AWS_REGION = "us-east-1"
$env:S3_BUCKET_NAME = "ehb-storage-bucket"
$env:STRIPE_SECRET_KEY = "your-stripe-secret-key"
$env:STRIPE_PUBLISHABLE_KEY = "your-stripe-publishable-key"
$env:PAYPAL_CLIENT_ID = "your-paypal-client-id"
$env:PAYPAL_CLIENT_SECRET = "your-paypal-client-secret"
$env:SENTRY_DSN = "your-sentry-dsn"
$env:GOOGLE_ANALYTICS_ID = "your-ga-id"
$env:MIXPANEL_TOKEN = "your-mixpanel-token"
$env:DEBUG = "True"
$env:ENVIRONMENT = "development"
$env:LOG_LEVEL = "DEBUG"
$env:CORS_ORIGINS = "http://localhost:3000,http://localhost:8000"
$env:FRONTEND_PORT = "3000"
$env:BACKEND_PORT = "8000"
$env:PSS_PORT = "4001"
$env:EMO_PORT = "4003"
$env:EDR_PORT = "4002"
$env:JPS_PORT = "4005"
$env:GOSELLR_PORT = "4004"
$env:WALLET_PORT = "5001"
$env:FRANCHISE_PORT = "4006"
$env:ENABLE_AI_FEATURES = "True"
$env:ENABLE_BLOCKCHAIN_FEATURES = "True"
$env:ENABLE_PAYMENT_FEATURES = "True"
$env:ENABLE_ANALYTICS = "True"

Write-Host "Environment variables set successfully!" -ForegroundColor Green

# Check if we're in the correct directory
if (Test-Path "backend") {
    Write-Host "Found backend directory" -ForegroundColor Blue
} else {
    Write-Host "Backend directory not found. Please run this script from the project root." -ForegroundColor Red
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# Check if uvicorn is available
try {
    $uvicornVersion = python -c "import uvicorn; print(uvicorn.__version__)"
    Write-Host "Uvicorn found: $uvicornVersion" -ForegroundColor Blue
} catch {
    Write-Host "Uvicorn not found. Installing..." -ForegroundColor Yellow
    pip install uvicorn
}

# Navigate to backend directory and start the server
Write-Host "Starting EHB backend server..." -ForegroundColor Green
Set-Location backend
python -m uvicorn app.main:app --reload --port 8000
