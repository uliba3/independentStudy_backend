#!/bin/bash

# Stop all running containers
docker-compose down

# Remove the PostgreSQL volume
docker volume rm independentstudy_postgres_data

# Remove any dangling volumes (optional, but can be helpful)
docker volume prune -f

# Rebuild and start the containers
docker-compose up --build -d

# Wait for the database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Optionally, you can use a more robust way to wait for the database:
# docker-compose exec db pg_isready -U postgres -d db

# Connect to the database and terminate all connections except your own
docker-compose exec db psql -U postgres -d db -c "
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'db' AND pid <> pg_backend_pid();"

echo "Database reset complete. You can now run your startup script."