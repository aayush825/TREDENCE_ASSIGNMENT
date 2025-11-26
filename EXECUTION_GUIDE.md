# Execution & Deployment Guide

## 📋 Complete Execution Instructions

### Prerequisites Check

- Python 3.8+ installed ✓
- Node.js 16+ installed ✓
- Virtual environment created ✓
- All dependencies installed ✓

---

## 🎯 Method 1: Local Development (Recommended)

### Terminal 1 - Start Backend Server

```powershell
# Navigate to backend
cd "c:\Users\user\Desktop\TREDENCE ASSIGNMENT\backend"

# Activate Python virtual environment
.\venv\Scripts\Activate.ps1

# Start FastAPI development server with auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
```

✅ **Backend Status**: Ready at `http://localhost:8000`

**Available Endpoints:**

- API Docs (Swagger): `http://localhost:8000/docs`
- API ReDoc: `http://localhost:8000/redoc`
- Health Check: `http://localhost:8000/health`
- Root Info: `http://localhost:8000/`

---

### Terminal 2 - Start Frontend Development Server

```powershell
# Navigate to frontend
cd "c:\Users\user\Desktop\TREDENCE ASSIGNMENT\frontend"

# Start React development server
npm start
```

**Expected Output:**

```
Compiled successfully!

You can now view collaborative-code-editor in the browser.

Local:            http://localhost:3000
```

✅ **Frontend Status**: Ready at `http://localhost:3000`

---

### Step-by-Step Usage

1. **Open Browser**: Navigate to `http://localhost:3000`

2. **Create a New Room**:

   - Enter a room name in the left sidebar (e.g., "JavaScript Collaboration")
   - Select a language (default: JavaScript)
   - Click "Create" button
   - You'll be automatically added to the room

3. **Start Coding**:

   - Type code in the editor
   - Changes are automatically synced to other users

4. **Join from Another Tab/User**:

   - Open another browser tab: `http://localhost:3000`
   - Select the room you created from "Available Rooms"
   - Both tabs/users now share the same code in real-time

5. **Monitor Active Users**:
   - Right panel shows active connection count
   - Updates every 3 seconds

---

## 🐳 Method 2: Docker Setup (Optional)

### Create Docker Compose File

Create `docker-compose.yml` in the root directory:

```yaml
version: "3.8"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./test.db
      - DEBUG=True
    volumes:
      - ./backend/app:/code/app
    command: python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend/src:/app/src
    stdin_open: true
    tty: true
```

### Run with Docker Compose

```powershell
# From root directory
docker-compose up

# Or in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🧪 Testing the Application

### Test Backend Endpoints (PowerShell)

```powershell
# Health Check
Invoke-WebRequest -Uri "http://localhost:8000/health" | ConvertTo-Json

# Get All Rooms
Invoke-WebRequest -Uri "http://localhost:8000/api/rooms/" | ConvertTo-Json

# Create a Room
$body = @{
    room_name = "Test Room"
    language = "python"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/api/rooms/create" `
    -Method Post `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body

$roomData = $response.Content | ConvertFrom-Json
$roomId = $roomData.room_id

Write-Host "Created room with ID: $roomId"

# Get Specific Room
Invoke-WebRequest -Uri "http://localhost:8000/api/rooms/$roomId" | ConvertTo-Json
```

### Test Frontend

1. Open browser DevTools (F12)
2. Go to Console tab
3. Check for any JavaScript errors
4. Test WebSocket connection by opening Network tab → WS filter

---

## 📊 Monitoring & Debugging

### Backend Debugging

```powershell
# Run with verbose logging
python -m uvicorn app.main:app --reload --log-level debug

# Check database
# Open test.db with SQLite Browser (GUI) or:
sqlite3 test.db
sqlite> .tables
sqlite> SELECT * FROM rooms;
sqlite> SELECT * FROM users;
```

### Frontend Debugging

```powershell
# Run with source maps for debugging
npm start

# Build for production
npm run build

# Check console for WebSocket connection status
# In browser console, type: ws (then check Network tab for WebSocket connections)
```

### Common Issues and Fixes

| Issue                      | Solution                                                      |
| -------------------------- | ------------------------------------------------------------- |
| Port 8000 in use           | `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| WebSocket connection fails | Ensure backend is running, check firewall                     |
| Frontend won't load        | Clear browser cache (Ctrl+F5), check console for errors       |
| CORS errors                | Verify `ALLOWED_ORIGINS` in `backend/app/config.py`           |
| Database locked            | Delete `test.db` and restart                                  |

---

## 📦 Production Deployment

### Build Frontend for Production

```powershell
cd frontend
npm run build
```

This creates a `build/` folder with optimized static files.

### Backend Production Setup

```powershell
# Use production server (Gunicorn on Linux/Mac or Waitress on Windows)
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Or use Waitress for Windows
pip install waitress
waitress-serve --port=8000 app.main:app
```

### Environment Configuration for Production

Update `backend/.env`:

```
DATABASE_URL=postgresql://user:password@localhost/db_name
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 🔒 Security Considerations

### Before Production:

1. **Change DEBUG to False** in `.env`
2. **Add Authentication** - Implement JWT tokens
3. **Add Input Validation** - Already using Pydantic, enhance if needed
4. **Use HTTPS** - Configure SSL certificates
5. **Database Security** - Use strong passwords for production DB
6. **CORS Configuration** - Restrict to specific domains
7. **Rate Limiting** - Add request throttling
8. **SQL Injection Prevention** - Using SQLAlchemy ORM (safe by default)

---

## 📈 Performance Optimization

### Backend

- Use PostgreSQL instead of SQLite for production
- Add caching with Redis
- Implement connection pooling
- Add database indexes on frequently queried fields

### Frontend

- Code splitting with React.lazy()
- Lazy load components
- Minimize bundle size
- Use CDN for static assets

---

## 🚀 Deployment Options

### Option 1: Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Option 2: AWS EC2

```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Clone repo and setup
git clone <repo-url>
cd project
./setup.sh
```

### Option 3: DigitalOcean

```bash
# Using App Platform for easy deployment
# Push to GitHub and connect DigitalOcean
```

### Option 4: Vercel (Frontend) + Railway (Backend)

- Deploy frontend to Vercel
- Deploy backend to Railway
- Connect via environment variables

---

## ✅ Verification Checklist

Before considering the project complete:

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:3000
- [ ] Can create a new room
- [ ] Can join an existing room
- [ ] Real-time code sync works (test in 2 tabs)
- [ ] Active users counter updates
- [ ] WebSocket connection established
- [ ] Database persists code changes
- [ ] All API endpoints respond correctly
- [ ] No console errors in browser
- [ ] No warnings in terminal

---

## 📚 Useful Commands Reference

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1          # Activate venv
deactivate                            # Deactivate venv
pip install -r requirements.txt      # Install deps
python -m uvicorn app.main:app --reload  # Run dev server

# Frontend
cd frontend
npm install                           # Install deps
npm start                             # Dev server
npm run build                         # Production build
npm test                              # Run tests

# Database
sqlite3 test.db                       # Open SQLite shell
.tables                               # List tables
.schema rooms                         # Show table structure
.exit                                 # Exit shell

# Git
git status                            # Check status
git add .                             # Stage changes
git commit -m "message"               # Commit
git push                              # Push to remote
```

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **WebSockets**: https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **TypeScript**: https://www.typescriptlang.org/docs/

---

## 📞 Support & Help

- Check browser console (F12) for frontend errors
- Check terminal output for backend errors
- Review `README.md` for detailed documentation
- Check `QUICK_START.md` for common issues

---

**Application Ready! 🎉**

Start with Terminal 1 (Backend) then Terminal 2 (Frontend).
