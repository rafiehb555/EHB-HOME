# PostgreSQL Setup Guide for EHB System

## Overview

This guide will help you set up PostgreSQL for the EHB (EHB Home Page & Dashboard) system. The setup includes database creation, user management, table creation, and initial data population.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker and Docker Compose (optional, for containerized setup)
- PostgreSQL (if not using Docker)

## Quick Setup (Recommended)

### Option 1: Using Docker Compose (Easiest)

1. **Start PostgreSQL with Docker:**
   ```bash
   docker-compose up -d postgres
   ```

2. **Run the setup script:**
   ```bash
   cd backend
   python scripts/setup_postgresql.py
   ```

3. **Verify the setup:**
   ```bash
   python -c "from utils.database import check_database_connection; print('Database ready!' if check_database_connection() else 'Database not ready')"
   ```

### Option 2: Manual PostgreSQL Installation

1. **Install PostgreSQL:**
   - **Windows:** Download from https://www.postgresql.org/download/windows/
   - **macOS:** `brew install postgresql`
   - **Linux:** `sudo apt-get install postgresql postgresql-contrib`

2. **Start PostgreSQL service:**
   ```bash
   # Windows: PostgreSQL service should start automatically
   # macOS: brew services start postgresql
   # Linux: sudo systemctl start postgresql
   ```

3. **Create database and user:**
   ```bash
   psql -U postgres
   CREATE USER ehb_user WITH PASSWORD 'ehb_password';
   CREATE DATABASE ehb_database OWNER ehb_user;
   GRANT ALL PRIVILEGES ON DATABASE ehb_database TO ehb_user;
   \q
   ```

4. **Run the setup script:**
   ```bash
   cd backend
   python scripts/setup_postgresql.py
   ```

## Database Configuration

### Environment Variables

Create a `.env` file in the project root with the following database configuration:

```env
# Database Configuration
DATABASE_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_database
DATABASE_TEST_URL=postgresql://ehb_user:ehb_password@localhost:5432/ehb_test_db
```

### Database Connection Details

- **Host:** localhost
- **Port:** 5432
- **Database:** ehb_database
- **Username:** ehb_user
- **Password:** ehb_password
- **Connection URL:** `postgresql://ehb_user:ehb_password@localhost:5432/ehb_database`

## Database Schema

The EHB system includes the following main tables:

### 1. Users Table
- User accounts and profiles
- SQL level management
- Verification status tracking

### 2. Services Table
- EHB service definitions
- Pricing and usage limits
- Service status management

### 3. Transactions Table
- Financial transactions
- Blockchain transaction tracking
- Payment processing

### 4. Wallets Table
- Multi-chain wallet management
- Balance tracking
- Security features

### 5. Franchises Table
- Franchise applications
- Business information
- Approval workflow

### 6. Verifications Table
- User verification processes
- Document management
- Status tracking

## Database Views

The system creates several views for analytics:

### User Statistics View
```sql
CREATE VIEW user_statistics AS
SELECT
    COUNT(*) as total_users,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_users,
    COUNT(CASE WHEN email_verified = true THEN 1 END) as verified_users,
    COUNT(CASE WHEN sql_level = 'vip' THEN 1 END) as vip_users,
    COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as new_users_30_days
FROM users;
```

### Transaction Statistics View
```sql
CREATE VIEW transaction_statistics AS
SELECT
    COUNT(*) as total_transactions,
    COALESCE(SUM(amount), 0) as total_volume,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_transactions,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_transactions,
    COALESCE(AVG(amount), 0) as average_transaction_amount
FROM transactions;
```

## Migration Management

### Using Alembic

1. **Create a new migration:**
   ```bash
   cd backend
   alembic revision --autogenerate -m "Description of changes"
   ```

2. **Apply migrations:**
   ```bash
   alembic upgrade head
   ```

3. **Rollback migrations:**
   ```bash
   alembic downgrade -1
   ```

4. **View migration history:**
   ```bash
   alembic history
   ```

### Manual Database Setup

If you prefer to set up the database manually:

1. **Create tables:**
   ```bash
   cd backend
   python database/setup.py
   ```

2. **Insert initial data:**
   The setup script automatically inserts default services and creates necessary views.

## Troubleshooting

### Common Issues

1. **Connection Refused:**
   - Ensure PostgreSQL is running
   - Check if the port 5432 is available
   - Verify firewall settings

2. **Authentication Failed:**
   - Check username and password
   - Verify pg_hba.conf configuration
   - Ensure user has proper permissions

3. **Database Not Found:**
   - Create the database manually
   - Check database name in connection string
   - Verify user has access to the database

### Useful Commands

1. **Connect to database:**
   ```bash
   psql -h localhost -U ehb_user -d ehb_database
   ```

2. **List all tables:**
   ```sql
   \dt
   ```

3. **Describe a table:**
   ```sql
   \d table_name
   ```

4. **View database statistics:**
   ```sql
   SELECT * FROM user_statistics;
   SELECT * FROM transaction_statistics;
   ```

## Development Workflow

### Adding New Models

1. **Create the model file:**
   ```python
   # models/new_model.py
   from sqlalchemy import Column, Integer, String
   from .base import Base

   class NewModel(Base):
       __tablename__ = "new_models"
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100), nullable=False)
   ```

2. **Import in models/__init__.py:**
   ```python
   from .new_model import NewModel
   ```

3. **Create and apply migration:**
   ```bash
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

### Database Backup and Restore

1. **Create backup:**
   ```bash
   pg_dump -h localhost -U ehb_user -d ehb_database > backup.sql
   ```

2. **Restore from backup:**
   ```bash
   psql -h localhost -U ehb_user -d ehb_database < backup.sql
   ```

## Performance Optimization

### Indexes

The system automatically creates indexes on:
- User email and username
- Transaction user_id and status
- Wallet user_id
- Verification user_id
- Franchise user_id

### Connection Pooling

The application uses SQLAlchemy connection pooling with:
- Pool size: 10
- Max overflow: 20
- Pool timeout: 30 seconds
- Pool recycle: 300 seconds

## Security Considerations

1. **Change default passwords** in production
2. **Use SSL connections** for remote databases
3. **Implement proper user permissions**
4. **Regular security updates**
5. **Backup strategy implementation**

## Production Deployment

For production deployment:

1. **Use environment-specific configuration**
2. **Implement connection pooling**
3. **Set up monitoring and logging**
4. **Configure automated backups**
5. **Use managed database services** (AWS RDS, Google Cloud SQL, etc.)

## Support

If you encounter issues:

1. Check the logs for error messages
2. Verify database connectivity
3. Ensure all dependencies are installed
4. Review the troubleshooting section above
5. Check the project documentation

For additional help, refer to:
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
