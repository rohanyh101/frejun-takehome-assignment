#!/bin/bash

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Setup initial room data
echo "Setting up initial room data..."
python manage.py setup_rooms

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123', age=30, gender='M')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Start server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
