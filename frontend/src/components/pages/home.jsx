import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import useCreateUser from '../hooks/useCreateUser';
import { useNavigate } from 'react-router-dom';
const Home = () => {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const { loading, error, createUser } = useCreateUser();

  const handleLogin = () => {
    if (name && password) {
      createUser(name, password);
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Please enter both username and password to continue'
      });
    }
  };

  useEffect(() => {
    const userId = localStorage.getItem('userId');
    if (userId) {
      navigate('/chat/' + userId);
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-gray-800 p-4">
      <div className="bg-white p-8 rounded-lg shadow-sm w-full max-w-md transform transition-all duration-300 hover:shadow-md">
        <h1 className="text-3xl font-light mb-8 text-center text-gray-700">Welcome</h1>
        <div className="space-y-6">
          <div className="transform transition-all duration-300 hover:translate-y-[-2px]">
            <label htmlFor="name" className="block text-sm font-light mb-2 text-gray-600">
              Username
            </label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-gray-50 text-gray-800 border border-gray-200 
                focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent
                transition-all duration-300"
              placeholder="Enter username"
            />
          </div>
          <div className="transform transition-all duration-300 hover:translate-y-[-2px]">
            <label htmlFor="password" className="block text-sm font-light mb-2 text-gray-600">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-gray-50 text-gray-800 border border-gray-200 
                focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent
                transition-all duration-300"
              placeholder="Enter password"
            />
          </div>
          <button
            onClick={handleLogin}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg
              transform transition-all duration-300 hover:translate-y-[-2px] hover:shadow-md
              font-light focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
          >
            Create Account or Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;