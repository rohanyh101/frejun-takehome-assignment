# FreJun - Take Home Assignment Booking API 🎯

A Django REST Framework API for managing workspace room bookings with 15 rooms, team constraints, and time slot validation.

## 🚀 Quick Start

### Docker Image Link: https://hub.docker.com/r/rohaanyh/frejun-assignment

### Docker (Recommended)
```bash
docker run -p 8000:8000 rohaanyh/frejun-assignment:0.1
```

### Local Development
```bash
git clone https://github.com/rohanyh101/frejun-takehome-assignment && cd frejun
make setup && make run
```

**Access:**
- Admin Panel: http://localhost:8000/admin/ (`admin` / `admin123`)
- REST API: http://localhost:8000/api/v1/

## 📋 Features

**15 Rooms:**
- 8 Private Rooms (1 person each)
- 4 Conference Rooms (teams of 3+ members)  
- 3 Shared Desks (up to 4 people each)

**Business Rules:**
- Time slots: 9 AM – 6 PM
- No overlapping bookings
- Children (age < 10) included in headcount but don't occupy seats
- Teams need 3+ members for conference rooms

## 🔗 API Endpoints

### Create Booking
```bash
POST /api/v1/bookings/
{
  "room": 1,
  "date": "2025-10-17",
  "start_time": "10:00:00",
  "end_time": "11:00:00",
  "user": 1
}
```

### Cancel Booking
```bash
POST /api/v1/bookings/cancel/{booking_id}/
```

### Check Availability
```bash
GET /api/v1/rooms/available/?date=2025-10-17&start_time=10:00:00&end_time=11:00:00
```

### List Bookings
```bash
GET /api/v1/bookings/list/
```

### Other Endpoints
- `GET /api/v1/rooms/` - List all rooms
- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/teams/` - List teams

## 🧪 Test the API

```bash
# Create a user
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "first_name": "John", "last_name": "Doe", "email": "john@example.com", "age": 25, "gender": "M"}'

# Book a room
curl -X POST http://localhost:8000/api/v1/bookings/ \
  -H "Content-Type: application/json" \
  -d '{"room": 1, "date": "2025-10-17", "start_time": "10:00:00", "end_time": "11:00:00", "user": 1}'

# Check availability
curl "http://localhost:8000/api/v1/rooms/available/?date=2025-10-17&start_time=10:00:00&end_time=11:00:00"
```

## �️ Local Setup

**Prerequisites:** Python 3.11+

```bash
# Clone and setup
git clone <repo-url> && cd frejun
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Setup database and run
python manage.py migrate
python manage.py setup_rooms
python manage.py createsuperuser
python manage.py runserver
```

## 📦 Docker Build & Push

```bash
# Build and run locally
docker build -t frejun-assignment .
docker run -p 8000:8000 frejun-assignment

# Push to Docker Hub
docker login
docker tag frejun-assignment yourusername/frejun-assignment:0.1
docker push yourusername/frejun-assignment:0.1
```

## 🎯 For Interviewers

**Zero Setup Required:**
```bash
docker run -p 8000:8000 rohaanyh/frejun-assignment:0.1
```

**Demo Features:**
1. **Admin Panel** (http://localhost:8000/admin/) - View all data with user-friendly interface
2. **REST API** (http://localhost:8000/api/v1/) - Test all endpoints with Django REST Framework browser
3. **Business Logic** - Try booking conflicts, team constraints, time validations

---

**Built by:** Rohan Honnakatti | **Challenge:** FreJun Backend Take-Home
