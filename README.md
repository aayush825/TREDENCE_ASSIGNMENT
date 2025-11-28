# Collaborative Code Editor

A real-time collaborative code editor built with FastAPI and React/TypeScript.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm

### Backend Setup

1. Navigate to backend directory:
   ```powershell
   cd .\backend\
   ```

2. Activate virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Start backend server:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
   Backend: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
   ```powershell
   cd .\frontend\
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start frontend:
   ```powershell
   npm start
   ```
   Frontend: `http://localhost:3000`

## API Endpoints

### Room Management
- `POST /api/rooms/create` - Create new room
- `GET /api/rooms/` - Get all rooms
- `GET /api/rooms/{room_id}` - Get room details
- `PUT /api/rooms/{room_id}/code` - Update code
- `POST /api/rooms/{room_id}/members/{user_id}` - Add member
- `DELETE /api/rooms/{room_id}/members/{user_id}` - Remove member
- `DELETE /api/rooms/{room_id}` - Delete room

### Autocomplete
- `POST /api/autocomplete/suggestions` - Get suggestions
- `GET /api/autocomplete/{room_id}/{line_number}` - Get context

### Real-time
- `WebSocket /ws/editor/{room_id}` - Code collaboration

### System
- `GET /health` - Health check
- `GET /docs` - API documentation

## Features

- Real-time collaborative code editing
- Multi-user support
- Code persistence
- Autocomplete suggestions
- REST API with Swagger docs
