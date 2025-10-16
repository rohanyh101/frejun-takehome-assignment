# FreJun Workspace Room Booking System - Makefile
# Professional command shortcuts for development and deployment

.PHONY: help install setup migrate test run clean docker-build docker-up docker-down docker-logs admin-user rooms api-test

# Default target - show help
help:
	@echo "🎯 FreJun Workspace Room Booking System - Available Commands:"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install Python dependencies"
	@echo "  make setup       - Complete local setup (install + migrate + rooms + admin)"
	@echo ""
	@echo "🗄️  Database Management:"
	@echo "  make migrate     - Run database migrations"
	@echo "  make rooms       - Create initial room data (15 rooms)"
	@echo "  make admin-user  - Create admin superuser (admin/admin123)"
	@echo "  make reset-db    - Reset database (delete + migrate + setup)"
	@echo ""
	@echo "🚀 Local Development:"
	@echo "  make run         - Start Django development server"
	@echo "  make test        - Run tests"
	@echo "  make clean       - Clean up temporary files"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start with Docker Compose"
	@echo "  make docker-down  - Stop Docker containers"
	@echo ""
	@echo "📋 Quick Start:"
	@echo "  Local:  make setup && make run"
	@echo "  Docker: make demo"

# Python virtual environment setup
install:
	@echo "📦 Installing dependencies..."
	python3 -m venv venv || python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Dependencies installed!"

# Database migrations
migrate:
	@echo "🗄️  Running database migrations..."
	. venv/bin/activate && python manage.py migrate
	@echo "✅ Migrations completed!"

# Create initial room data
rooms:
	@echo "🏢 Creating initial room data..."
	. venv/bin/activate && python manage.py setup_rooms
	@echo "✅ Rooms created: 8 Private, 4 Conference, 3 Shared"

# Create admin superuser
admin-user:
	@echo "👤 Creating admin superuser..."
	. venv/bin/activate && python manage.py shell -c "\
	from users.models import User; \
	User.objects.filter(username='admin').exists() or \
	User.objects.create_superuser('admin', 'admin@example.com', 'admin123', age=30, gender='M') and \
	print('✅ Admin user created: admin/admin123')"

# Complete local setup
setup: install migrate rooms admin-user
	@echo ""
	@echo "🎉 Setup complete! Ready to run:"
	@echo "   make run     - Start development server"
	@echo "   📊 Admin: http://localhost:8000/admin/ (admin/admin123)"
	@echo "   🔌 API: http://localhost:8000/api/v1/"

# Reset database
reset-db:
	@echo "🗄️  Resetting database..."
	rm -f db.sqlite3
	$(MAKE) migrate
	$(MAKE) rooms
	$(MAKE) admin-user
	@echo "✅ Database reset complete!"

# Start development server
run:
	@echo "🚀 Starting Django development server..."
	@echo "📊 Admin Panel: http://localhost:8000/admin/ (admin/admin123)"
	@echo "🔌 API Base URL: http://localhost:8000/api/v1/"
	@echo "Press Ctrl+C to stop"
	. venv/bin/activate && python manage.py runserver

# Run tests
test:
	@echo "🧪 Running tests..."
	. venv/bin/activate && python manage.py test
	@echo "✅ Tests completed!"

# Clean temporary files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	@echo "✅ Cleanup complete!"

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker-compose build
	@echo "✅ Docker image built!"

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d
	@echo "⏳ Waiting for services..."
	sleep 5
	@echo "✅ Docker containers running!"
	@echo "📊 Admin Panel: http://localhost:8000/admin/ (admin/admin123)"
	@echo "🔌 API Base URL: http://localhost:8000/api/v1/"

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Docker containers stopped!"

# Complete demo setup
demo: docker-build docker-up
	@echo ""
	@echo "🎉 FreJun Demo is ready!"
	@echo ""
	@echo "🔧 Django Admin Panel: http://localhost:8000/admin/"
	@echo "   👤 Username: admin"
	@echo "   🔒 Password: admin123"
	@echo ""
	@echo "📊 REST API: http://localhost:8000/api/v1/"
	@echo "   📋 Endpoints: /rooms/, /bookings/, /users/, /teams/"
	@echo ""
	@echo "💾 Database: SQLite3 (no external dependencies)"
	@echo ""
	@echo "🛑 To stop: make docker-down"

# Development shortcuts
dev-server: run
local-setup: setup
start: run
stop: docker-down
build: docker-build
up: docker-up
down: docker-down
logs: docker-logs
