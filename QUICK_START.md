# Quick Start Guide - Collaborative Code Editor

## 🚀 Quick Setup (5 minutes)

### Step 1: Setup Backend

Open **PowerShell** and navigate to the backend:

```powershell
# Go to backend directory
cd "c:\Users\user\Desktop\TREDENCE ASSIGNMENT\backend"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies (already done, but just in case)
pip install -r requirements.txt

# Run the backend server
python -m uvicorn app.main:app --reload
```

✅ **Backend is running at**: `http://localhost:8000`

**Available endpoints**:

- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

---

### Step 2: Setup Frontend

Open a **new PowerShell terminal** and navigate to the frontend:

```powershell
# Go to frontend directory
cd "c:\Users\user\Desktop\TREDENCE ASSIGNMENT\frontend"

# Install dependencies
npm install

# Start the development server
npm start
```

✅ **Frontend is running at**: `http://localhost:3000`

---

## 📝 Using the Application

### Create Your First Room

1. Open `http://localhost:3000` in your browser
2. In the left sidebar, enter a room name (e.g., "My First Room")
3. Click the **"Create"** button
4. You're now in the room! Start typing code

### Test Real-time Collaboration

1. Open a **second browser tab** with `http://localhost:3000`
2. Join the same room you created
3. Type in one tab and see the changes appear in the other tab in real-time!

### API Testing

You can test the API endpoints directly:

```powershell
# Test health check
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Create a room (PowerShell)
$body = @{
    room_name = "Test Room"
    language = "javascript"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/rooms/create" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

---

## 📁 Project Structure Overview

```
TREDENCE ASSIGNMENT/
├── backend/
│   ├── app/
│   │   ├── main.py          ← Main FastAPI application
│   │   ├── config.py        ← Settings
│   │   ├── db.py            ← Database setup
│   │   ├── models/          ← Database models
│   │   ├── routers/         ← API routes
│   │   └── services/        ← Business logic
│   ├── venv/                ← Virtual environment
│   ├── requirements.txt     ← Python dependencies
│   └── .env                 ← Environment config
├── frontend/
│   ├── src/
│   │   ├── components/      ← React components
│   │   ├── App.tsx          ← Main app
│   │   └── index.tsx        ← Entry point
│   ├── package.json         ← NPM dependencies
│   └── tsconfig.json        ← TypeScript config
├── README.md                ← Full documentation
└── .gitignore               ← Git ignore
```

---

## 🔧 Backend API Quick Reference

### Create Room

```http
POST /api/rooms/create
Content-Type: application/json

{
  "room_name": "My Room",
  "language": "javascript"
}
```

### Get All Rooms

```http
GET /api/rooms/
```

### Get Room Details

```http
GET /api/rooms/{room_id}
```

### Update Code

```http
PUT /api/rooms/{room_id}/code
Content-Type: application/json

{
  "code": "console.log('Hello World')"
}
```

### WebSocket Connection

```
WS ws://localhost:8000/ws/editor/{room_id}
```

---

## 💡 Key Features Implemented

✅ **Real-time Collaboration** - WebSocket support for live editing
✅ **Multiple Users** - See active users in each room
✅ **Code Persistence** - Changes saved to SQLite database
✅ **Autocomplete** - Language-aware code suggestions
✅ **Room Management** - Create, join, and manage rooms
✅ **Modern Stack** - FastAPI + React + TypeScript

---

## 🐛 Troubleshooting

### Port Already in Use

```powershell
# Check what's using port 8000
netstat -ano | findstr :8000

# Check what's using port 3000
netstat -ano | findstr :3000

# Kill process (replace PID with the actual number)
taskkill /PID <PID> /F
```

### Virtual Environment Not Working

```powershell
# Delete and recreate venv
cd backend
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### npm install fails

```powershell
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json

# Reinstall
npm install
```

---

## 📚 Next Steps

1. **Customize Styling** - Edit `frontend/src/App.css`
2. **Add More Languages** - Update `backend/app/services/autocomplete_service.py`
3. **Use PostgreSQL** - Change `DATABASE_URL` in `backend/.env`
4. **Add Authentication** - Install and integrate JWT
5. **Deploy** - Use Docker or cloud platform

---

## 📞 Support

- **Backend Docs**: Navigate to `http://localhost:8000/docs` while backend is running
- **Frontend Console**: Open browser DevTools (F12) for debugging
- **Logs**: Check terminal output for errors

---

**Happy Coding! 🎉**

For full documentation, see `README.md`
