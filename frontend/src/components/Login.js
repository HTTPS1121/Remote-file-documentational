import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/login', 
        { username, password },
        { withCredentials: true }
      );
      if (response.data.success) {
        onLogin();
      }
    } catch (err) {
      setError('שם משתמש או סיסמה שגויים');
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>כניסה למערכת</h2>
        {error && <div className="error-message">{error}</div>}
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="שם משתמש"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="סיסמה"
          required
        />
        <button type="submit">כניסה</button>
      </form>
    </div>
  );
};

export default Login; 