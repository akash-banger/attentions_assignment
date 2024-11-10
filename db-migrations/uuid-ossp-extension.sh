# Run the following command if needed to enable uuid-ossp extension in the database
psql -h 127.0.0.1 -U user_name -d evva_health -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'