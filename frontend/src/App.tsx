import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CodeEditor from './components/CodeEditor';
import UserList from './components/UserList';
import './App.css';

interface Room {
  id: number;
  room_id: string;
  room_name: string;
  language: string;
  code_content: string;
}

const App: React.FC = () => {
  const [currentRoom, setCurrentRoom] = useState<Room | null>(null);
  const [code, setCode] = useState('');
  const [roomName, setRoomName] = useState('');
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(false);
  const [ws, setWs] = useState<WebSocket | null>(null);

  // Fetch all rooms on component mount
  useEffect(() => {
    fetchRooms();
  }, []);

  const fetchRooms = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/rooms/');
      setRooms(response.data);
    } catch (error) {
      console.error('Failed to fetch rooms:', error);
    }
  };

  const createRoom = async () => {
    if (!roomName) {
      alert('Please enter a room name');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/rooms/create', {
        room_name: roomName,
        language: 'javascript',
      });
      const newRoom = response.data;
      setCurrentRoom(newRoom);
      setCode(newRoom.code_content);
      setRoomName('');
      await fetchRooms();
      connectWebSocket(newRoom.room_id);
    } catch (error) {
      console.error('Failed to create room:', error);
      alert('Failed to create room');
    } finally {
      setLoading(false);
    }
  };

  const joinRoom = async (room: Room) => {
    setCurrentRoom(room);
    setCode(room.code_content);
    connectWebSocket(room.room_id);
  };

  const connectWebSocket = (roomId: string) => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//localhost:8000/ws/editor/${roomId}`;

    const websocket = new WebSocket(wsUrl);

    websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'code_change') {
        setCode(message.data.code || code);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    websocket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    setWs(websocket);
  };

  const handleCodeChange = async (newCode: string) => {
    setCode(newCode);

    // Send change via WebSocket
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({
        type: 'code_change',
        data: { code: newCode },
        timestamp: new Date().toISOString(),
      }));
    }

    // Also update via HTTP for persistence
    if (currentRoom) {
      try {
        await axios.put(`http://localhost:8000/api/rooms/${currentRoom.room_id}/code`, {
          code: newCode,
        });
      } catch (error) {
        console.error('Failed to update code:', error);
      }
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Collaborative Code Editor</h1>
      </header>

      <div className="app-content">
        <aside className="app-sidebar">
          <section className="create-room-section">
            <h2>Create Room</h2>
            <input
              type="text"
              placeholder="Room name"
              value={roomName}
              onChange={(e) => setRoomName(e.target.value)}
            />
            <button onClick={createRoom} disabled={loading}>
              {loading ? 'Creating...' : 'Create'}
            </button>
          </section>

          <section className="rooms-list-section">
            <h2>Available Rooms</h2>
            {rooms.length === 0 ? (
              <p>No rooms available</p>
            ) : (
              <ul>
                {rooms.map((room) => (
                  <li key={room.room_id}>
                    <button onClick={() => joinRoom(room)}>
                      {room.room_name}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </aside>

        <main className="editor-area">
          {currentRoom ? (
            <div className="editor-container">
              <div className="editor-header">
                <h2>{currentRoom.room_name}</h2>
                <span className="room-id">Room ID: {currentRoom.room_id}</span>
              </div>

              <div className="editor-body">
                <UserList roomId={currentRoom.room_id} />
                <CodeEditor
                  roomId={currentRoom.room_id}
                  code={code}
                  onChange={handleCodeChange}
                />
              </div>
            </div>
          ) : (
            <div className="welcome-message">
              <h2>Welcome to Collaborative Code Editor</h2>
              <p>Create a new room or join an existing one to start collaborating!</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default App;
