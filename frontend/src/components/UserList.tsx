import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface UserListProps {
  roomId: string;
}

const UserList: React.FC<UserListProps> = ({ roomId }) => {
  const [userCount, setUserCount] = useState(0);

  useEffect(() => {
    const fetchUserCount = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/ws/rooms/${roomId}/connections`);
        setUserCount(response.data.active_connections);
      } catch (error) {
        console.error('Failed to fetch user count:', error);
      }
    };

    fetchUserCount();
    const interval = setInterval(fetchUserCount, 3000);

    return () => clearInterval(interval);
  }, [roomId]);

  return (
    <div style={{ padding: '10px', borderRight: '1px solid #ccc' }}>
      <h3>Active Users</h3>
      <p>{userCount} user(s) connected</p>
    </div>
  );
};

export default UserList;
