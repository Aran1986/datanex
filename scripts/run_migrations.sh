# Location: datanex/scripts/run_migrations.sh

#!/bin/bash

echo "Running database migrations..."
alembic upgrade head
echo "Migrations completed!"