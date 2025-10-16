# FreJun - Virtual Workspace Room Booking System 🎯

A Django REST Framework API for managing workspace room bookings, cancellations, and availability in a shared office environment.

## 📋 Overview

This system manages booking for:
- **8 Private Rooms** (1 person each)
- **4 Conference Rooms** (teams of 3+ members)
- **3 Shared Desks** (up to 4 people each)

### Business Rules
- Booking time slots: 9 AM – 6 PM (hourly slots)
- One booking per user/team at a time
- No overlapping bookings for the same room
- Conference rooms require teams of 3+ members
- Children (age < 10) are included in headcount but don't occupy seats
- Shared desks are filled sequentially up to capacity

## 🚀 Quick Start Options

### 🎯 **For Interviewers** - Run from Docker Hub (Easiest)

**Prerequisites**: Docker only

```bash
# One command to run the complete application
docker run -p 8000:8000 rohaanyh/frejun-assignment:latest
```

**Access immediately:**
- **🔧 Django Admin**: http://localhost:8000/admin/ (`admin` / `admin123`)
- **📊 REST API**: http://localhost:8000/api/v1/

*No cloning, no building, no setup required!*

---

### 💻 **For Developers** - Build from Source

**Prerequisites**: Docker and Docker Compose OR Python 3.11+

#### Option A: Docker (Recommended)
```bash
git clone <your-repo-url> && cd frejun
make demo    # Complete Docker setup + demo data
```

#### Option B: Local Development
```bash
git clone <your-repo-url> && cd frejun
make setup   # Install + migrate + create demo data
make run     # Start development server
```

### 📋 All Available Commands
```bash
make help    # See all available commands
```

**Key Commands:**
- `make demo` - Complete Docker setup + demo data
- `make setup` - Local development setup  
- `make run` - Start development server
- `make test` - Run tests
- `make docker-down` - Stop Docker containers

### Manual Setup (Alternative)

1. **Clone and navigate to the project**:
   ```bash
   git clone <your-repo-url>
   cd frejun
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

3. **Access the System**:
   - **Django Admin Panel**: http://localhost:8000/admin/ (admin/admin123)
   - **REST API Base URL**: http://localhost:8000/api/v1/

The system will automatically:
- Set up SQLite3 database
- Run migrations
- Create initial room data
- Create a superuser account

## 📊 Database Schema

### Core Models

#### Users
- Custom user model extending Django's AbstractUser
- Fields: `username`, `first_name`, `last_name`, `email`, `age`, `gender`
- Property: `is_child` (age < 10)

#### Teams
- Group bookings for conference rooms
- Fields: `name`, `members` (M2M), `created_by`
- Properties: `member_count`, `adult_member_count`, `child_member_count`

#### Rooms
- 15 total rooms with different types
- Fields: `room_number`, `room_type`, `capacity`, `is_active`
- Types: `PRIVATE`, `CONFERENCE`, `SHARED`

#### Bookings
- Central booking management
- Fields: `booking_id`, `room`, `date`, `start_time`, `end_time`, `user`, `team`, `status`
- Constraints: Must have either user OR team (not both)
- Auto-generates unique booking IDs

## 🔗 API Endpoints

### 1. Create Booking
```
POST /api/v1/bookings/
```

**Request Body:**
```json
{
  "room": 1,
  "date": "2024-10-15",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "user": 1  // For individual booking
}
```

**OR for team booking:**
```json
{
  "room": 5,
  "date": "2024-10-15",
  "start_time": "14:00:00",
  "end_time": "16:00:00",
  "team": 1  // For team booking
}
```

**Success Response:**
```json
{
  "message": "Booking created successfully",
  "booking": {
    "booking_id": "BK20241015143022",
    "room": {
      "id": 1,
      "room_number": "P01",
      "room_type": "PRIVATE",
      "capacity": 1
    },
    "date": "2024-10-15",
    "start_time": "10:00:00",
    "end_time": "11:00:00",
    "booker_name": "John Doe",
    "booking_type": "Individual",
    "status": "ACTIVE"
  }
}
```

### 2. Cancel Booking
```
POST /api/v1/cancel/{booking_id}/
```

**Success Response:**
```json
{
  "message": "Booking cancelled successfully",
  "booking": {
    "booking_id": "BK20241015143022",
    "status": "CANCELLED",
    "cancelled_at": "2024-10-15T15:30:22Z"
  }
}
```

### 3. List All Bookings
```
GET /api/v1/bookings/list/
```

**Optional Query Parameters:**
- `date`: Filter by specific date (YYYY-MM-DD)
- `room_type`: Filter by room type (PRIVATE, CONFERENCE, SHARED)

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "booking_id": "BK20241015143022",
      "room_number": "P01",
      "room_type": "Private Room",
      "date": "2024-10-15",
      "start_time": "10:00:00",
      "end_time": "11:00:00",
      "booker_name": "John Doe",
      "booking_type": "Individual",
      "status": "ACTIVE"
    }
  ]
}
```

### 4. Check Room Availability
```
GET /api/v1/rooms/available/
```

**Required Query Parameters:**
- `date`: Date to check (YYYY-MM-DD)
- `start_time`: Start time (HH:MM:SS)
- `end_time`: End time (HH:MM:SS)

**Optional Query Parameters:**
- `room_type`: Filter by room type

**Example:**
```
GET /api/v1/rooms/available/?date=2024-10-15&start_time=10:00:00&end_time=11:00:00
```

**Response:**
```json
{
  "date": "2024-10-15",
  "time_slot": "10:00:00 - 11:00:00",
  "available_rooms": [
    {
      "room": {
        "id": 2,
        "room_number": "P02",
        "room_type": "PRIVATE",
        "capacity": 1
      },
      "available_capacity": 1,
      "current_occupancy": 0
    },
    {
      "room": {
        "id": 13,
        "room_number": "S01",
        "room_type": "SHARED",
        "capacity": 4
      },
      "available_capacity": 2,
      "current_occupancy": 2
    }
  ],
  "total_available": 2
}
```

### 5. Additional Endpoints
- `GET /api/v1/rooms/` - List all rooms
- `GET /api/v1/users/` - List/create users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/teams/` - List/create teams
- `POST /api/v1/teams/` - Create new team

## 🔧 Development Setup (Local)

### Prerequisites
- Python 3.11+
- SQLite3 (included with Python)
- No external dependencies required

### Setup Steps

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database** (SQLite3 - no external dependencies):
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Set up initial room data
   python manage.py setup_rooms
   
   # Create superuser
   python manage.py createsuperuser
   ```

5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## 🧪 Testing the API

### Using curl

1. **Create a user**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "age": 25,
       "gender": "M"
     }'
   ```

2. **Book a private room**:
   ```bash
   curl -X POST http://localhost:8000/api/v1/bookings/ \
     -H "Content-Type: application/json" \
     -d '{
       "room": 1,
       "date": "2024-10-15",
       "start_time": "10:00:00",
       "end_time": "11:00:00",
       "user": 1
     }'
   ```

3. **Check availability**:
   ```bash
   curl "http://localhost:8000/api/v1/rooms/available/?date=2024-10-15&start_time=10:00:00&end_time=11:00:00"
   ```

## 📁 Project Structure

```
frejun/
├── config/                 # Django settings and configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/                  # User and team management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── rooms/                  # Room management
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── management/commands/setup_rooms.py
├── bookings/              # Booking system core
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
├── entrypoint.sh        # Container startup script
└── manage.py           # Django management script
```

## 🏗️ Architecture Decisions

### Database Design
- **Normalization**: Separate tables for Users, Teams, Rooms, and Bookings for clarity and maintainability
- **Constraints**: Database-level constraints ensure data integrity
- **Indexes**: Added indexes on frequently queried fields (booking_id, room+date+time)

### Business Logic
- **Model-level validation**: Core business rules enforced in model `clean()` methods
- **Service-level validation**: Additional checks in API views for availability
- **Atomic operations**: Booking creation is atomic to prevent race conditions

### API Design
- **RESTful conventions**: Standard HTTP methods and status codes
- **Comprehensive responses**: Detailed success/error messages
- **Query parameters**: Flexible filtering for list endpoints

## 🔒 Security Considerations

- **CORS**: Configured for development (restrict in production)
- **Authentication**: Currently allows anonymous access (add authentication as needed)
- **Validation**: Comprehensive input validation at model and serializer levels
- **SQL Injection**: Protected by Django ORM
- **Rate Limiting**: Consider adding for production use

## 🚀 Production Considerations

1. **Environment Variables**: Update `.env` with production values
2. **Database**: Use managed PostgreSQL service
3. **Static Files**: Configure proper static file serving
4. **Monitoring**: Add logging and monitoring
5. **Authentication**: Implement proper user authentication
6. **Rate Limiting**: Add API rate limiting
7. **HTTPS**: Enable SSL/TLS certificates

## 🐛 Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `404`: Not Found
- `409`: Conflict (overlapping bookings)

Example error response:
```json
{
  "error": "No available room for the selected slot and type."
}
```

##  Publishing to Docker Hub

For developers who want to publish their own version:

### Step 1: Build and Push Your Image
```bash
# Login and build
docker login
docker build -t yourusername/frejun-assignment:latest .
docker push yourusername/frejun-assignment:latest
```
```bash
docker login                                    # Login to Docker Hub
docker build -t yourusername/frejun-assignment:latest .
docker push yourusername/frejun-assignment:latest
```

### Step 2: Share with Interviewers
```bash
# They can run your image with:
docker run -p 8000:8000 yourusername/frejun-assignment:latest
```

**Benefits:**
- ✅ **Zero setup** for interviewers
- ✅ **Consistent environment** across all machines  
- ✅ **Professional deployment** knowledge demonstration
- ✅ **Easy to test** - just one Docker command

---

## 🎯 **Perfect for Interview Demo!**

### Django Admin Interface: http://localhost:8000/admin/
**Login**: `admin` / `admin123`

**What makes this impressive:**
- **Visual Data Management**: See all rooms, users, teams, and bookings in clean tables
- **CRUD Operations**: Add, edit, delete records with user-friendly forms
- **Business Logic**: All model constraints and validations work seamlessly
- **Real-time Updates**: Changes reflect immediately in the API
- **Professional UI**: Shows Django expertise and attention to detail

**Demo Flow:**
1. Show the 15 rooms (8 Private, 4 Conference, 3 Shared) 
2. Create users and teams
3. Make bookings and show constraint validations
4. Cancel bookings and show status updates

### API Access:
- **REST API Base**: http://localhost:8000/api/v1/
- **Django REST Framework Browsable API**: Available at each endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is created for the FreJun Backend Developer Take-Home Challenge.

---

**Developed by**: Rohan Honnakatti
**Challenge**: FreJun Backend Developer Take-Home  
**Date**: October 2024
