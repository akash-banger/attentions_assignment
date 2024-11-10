-- migrate:up

-- Create the users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automatically update `date_modified` timestamp on row update
CREATE OR REPLACE FUNCTION update_date_modified_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.date_modified = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_date_modified
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_date_modified_column();

-- Create index for better query performance
CREATE INDEX idx_users_username ON users(username);

-- migrate:down

-- Drop the index
DROP INDEX IF EXISTS idx_users_username;

-- Drop the trigger
DROP TRIGGER IF EXISTS update_users_date_modified ON users;

-- Drop the function
DROP FUNCTION IF EXISTS update_date_modified_column;

-- Drop the users table
DROP TABLE IF EXISTS users;