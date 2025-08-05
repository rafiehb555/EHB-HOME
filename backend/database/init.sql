-- EHB Database Initialization Script
-- This script sets up the initial database structure for EHB system

-- Create database if it doesn't exist
-- Note: This needs to be run as a superuser or with appropriate privileges

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types for enums
DO $$ BEGIN
    CREATE TYPE user_level AS ENUM ('free', 'basic', 'normal', 'high', 'vip');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended', 'pending');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE service_type AS ENUM ('pss', 'emo', 'edr', 'jps', 'gosellr', 'wallet', 'franchise', 'ai_marketplace', 'ai_agent', 'ai_robot');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE service_status AS ENUM ('active', 'inactive', 'maintenance', 'deprecated');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE transaction_type AS ENUM ('deposit', 'withdrawal', 'transfer', 'payment', 'refund', 'fee', 'reward');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE transaction_status AS ENUM ('pending', 'completed', 'failed', 'cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE wallet_type AS ENUM ('hot', 'cold', 'multisig');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE wallet_status AS ENUM ('active', 'inactive', 'locked', 'pending');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE franchise_status AS ENUM ('pending', 'approved', 'rejected', 'active', 'suspended', 'closed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE franchise_type AS ENUM ('retail', 'service', 'food', 'technology', 'education', 'healthcare');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE verification_type AS ENUM ('pss', 'emo', 'edr', 'kyc', 'email', 'phone', 'document');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE verification_status AS ENUM ('pending', 'in_progress', 'approved', 'rejected', 'expired');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_sql_level ON users(sql_level);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_wallets_user_id ON wallets(user_id);
CREATE INDEX IF NOT EXISTS idx_verifications_user_id ON verifications(user_id);
CREATE INDEX IF NOT EXISTS idx_franchises_user_id ON franchises(user_id);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
-- Note: These will be created by SQLAlchemy models, but we can add them here for reference
-- CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- CREATE TRIGGER update_wallets_updated_at BEFORE UPDATE ON wallets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- CREATE TRIGGER update_franchises_updated_at BEFORE UPDATE ON franchises FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
-- CREATE TRIGGER update_verifications_updated_at BEFORE UPDATE ON verifications FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default services
INSERT INTO services (name, service_type, status, description, version, price_per_month, usage_limit) VALUES
('Personal Security System', 'pss', 'active', 'Advanced personal security and verification system', '1.0.0', 29.99, 1000),
('Easy Management Office', 'emo', 'active', 'Comprehensive office management solution', '1.0.0', 49.99, 2000),
('Exam Decision Registration', 'edr', 'active', 'Educational examination and decision system', '1.0.0', 39.99, 1500),
('Job Profile System', 'jps', 'active', 'Professional job profile and career management', '1.0.0', 19.99, 1000),
('GoSellr E-commerce', 'gosellr', 'active', 'Complete e-commerce platform for businesses', '1.0.0', 79.99, 5000),
('EHB Wallet', 'wallet', 'active', 'Multi-chain cryptocurrency wallet', '1.0.0', 0.00, 10000),
('Franchise Management', 'franchise', 'active', 'Franchise application and management system', '1.0.0', 99.99, 500),
('AI Marketplace', 'ai_marketplace', 'active', 'AI services marketplace', '1.0.0', 59.99, 3000),
('AI Agent', 'ai_agent', 'active', 'Intelligent AI agent services', '1.0.0', 39.99, 2000),
('AI Robot', 'ai_robot', 'active', 'Advanced AI robot automation', '1.0.0', 89.99, 1000)
ON CONFLICT (id) DO NOTHING;

-- Create a view for user statistics
CREATE OR REPLACE VIEW user_statistics AS
SELECT
    COUNT(*) as total_users,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_users,
    COUNT(CASE WHEN email_verified = true THEN 1 END) as verified_users,
    COUNT(CASE WHEN sql_level = 'vip' THEN 1 END) as vip_users,
    COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as new_users_30_days
FROM users;

-- Create a view for transaction statistics
CREATE OR REPLACE VIEW transaction_statistics AS
SELECT
    COUNT(*) as total_transactions,
    SUM(amount) as total_volume,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_transactions,
    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_transactions,
    AVG(amount) as average_transaction_amount
FROM transactions;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ehb_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ehb_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO ehb_user;
