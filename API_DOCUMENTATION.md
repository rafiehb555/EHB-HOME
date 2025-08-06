# EHB API Documentation

## Overview
The EHB (Ecosystem Hub Bridge) API provides a comprehensive interface for managing user authentication, service verification, and system monitoring.

## Base URL
```
http://localhost:8000
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### POST /api/v1/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### POST /api/v1/auth/login
Authenticate user and get access token.

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com",
  "is_admin": false
}
```

#### GET /api/v1/auth/me
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Health Checks

#### GET /health
Check overall system health.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "backend": "healthy",
    "pss": "healthy",
    "emo": "healthy",
    "edr": "healthy"
  }
}
```

#### GET /api/v1/services/health
Check health of all microservices.

**Response:**
```json
{
  "backend": {
    "status": "healthy",
    "uptime": "2h 15m",
    "version": "1.0.0"
  },
  "pss": {
    "status": "healthy",
    "uptime": "1h 45m",
    "port": 4001
  },
  "emo": {
    "status": "healthy",
    "uptime": "1h 30m",
    "port": 4003
  },
  "edr": {
    "status": "healthy",
    "uptime": "1h 20m",
    "port": 4002
  }
}
```

### Service Management

#### GET /api/v1/services
Get list of available services.

**Response:**
```json
{
  "services": [
    {
      "name": "Personal Security System (PSS)",
      "description": "Identity verification and KYC services",
      "port": 4001,
      "status": "healthy",
      "endpoints": [
        "/verify",
        "/kyc",
        "/identity"
      ]
    },
    {
      "name": "Easy Management Office (EMO)",
      "description": "Business verification and management",
      "port": 4003,
      "status": "healthy",
      "endpoints": [
        "/business",
        "/management",
        "/verification"
      ]
    },
    {
      "name": "Exam Decision Registration (EDR)",
      "description": "Skill testing and certification",
      "port": 4002,
      "status": "healthy",
      "endpoints": [
        "/exam",
        "/certification",
        "/skills"
      ]
    }
  ]
}
```

#### GET /api/v1/services/{service_name}/profile
Get detailed service profile.

**Response:**
```json
{
  "name": "Personal Security System (PSS)",
  "description": "Advanced identity verification and KYC services",
  "version": "1.0.0",
  "port": 4001,
  "status": "healthy",
  "uptime": "1h 45m",
  "features": [
    "Identity verification",
    "KYC processing",
    "Document validation",
    "Biometric authentication"
  ],
  "endpoints": [
    {
      "path": "/verify",
      "method": "POST",
      "description": "Verify user identity"
    },
    {
      "path": "/kyc",
      "method": "POST",
      "description": "Process KYC documents"
    }
  ]
}
```

### Verification

#### POST /api/v1/services/verify
Submit verification request to a specific service.

**Request Body:**
```json
{
  "service": "pss",
  "user_id": 1,
  "verification_data": {
    "document_type": "passport",
    "document_number": "AB123456",
    "full_name": "John Doe",
    "date_of_birth": "1990-01-01"
  }
}
```

**Response:**
```json
{
  "verification_id": "vrf_123456789",
  "service": "pss",
  "status": "pending",
  "submitted_at": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T11:30:00Z"
}
```

#### GET /api/v1/services/verification-status
Get verification status for current user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "user_id": 1,
  "verifications": {
    "pss": {
      "status": "verified",
      "verified_at": "2024-01-15T11:30:00Z",
      "verification_id": "vrf_123456789"
    },
    "emo": {
      "status": "pending",
      "submitted_at": "2024-01-15T10:30:00Z",
      "verification_id": "vrf_987654321"
    },
    "edr": {
      "status": "not_started"
    }
  }
}
```

### Admin Endpoints

#### GET /api/v1/admin/stats
Get system statistics (admin only).

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "total_users": 1250,
  "active_users": 890,
  "total_verifications": 2340,
  "pending_verifications": 45,
  "system_health": "excellent",
  "uptime": "99.9%",
  "revenue": {
    "daily": 12500,
    "monthly": 375000,
    "total": 2500000
  }
}
```

#### GET /api/v1/admin/users
Get all users (admin only).

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response:**
```json
{
  "users": [
    {
      "user_id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "is_admin": false,
      "created_at": "2024-01-15T10:30:00Z",
      "last_login": "2024-01-15T12:30:00Z",
      "verification_status": {
        "pss": "verified",
        "emo": "pending",
        "edr": "not_started"
      }
    }
  ],
  "total": 1250,
  "page": 1,
  "per_page": 50
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Service not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_id": "err_123456789"
}
```

## Rate Limiting
- Authentication endpoints: 5 requests per minute
- API endpoints: 100 requests per minute
- Admin endpoints: 50 requests per minute

## WebSocket Support
For real-time updates, connect to:
```
ws://localhost:8000/ws
```

## SDK Libraries
- Python: `pip install ehb-sdk`
- JavaScript: `npm install @ehb/sdk`
- Java: Available in Maven Central

## Support
For API support and questions:
- Email: api-support@ehb.com
- Documentation: https://docs.ehb.com
- Status Page: https://status.ehb.com
