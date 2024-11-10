import React, { useState, useEffect, useRef } from 'react';
import { io } from 'socket.io-client';
import { API_URL } from '../../constants';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { motion, AnimatePresence } from 'framer-motion';

const Chat = () => {
    const { userId } = useParams();
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const [username, setUsername] = useState('');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    const newSocket = io(API_URL, {
      query: { userId }
    });

    newSocket.on('connect', () => {
      console.log('Connected to socket');
    });

    newSocket.on('message_response', (data) => {
      console.log('Received message:', data);
      setIsLoading(false);
      if (data.message.trim()) {
        setMessages(prev => [...prev, {
          type: 'ai',
          user: 'Itinerary Agent',
          message: data.message
        }]);
      }
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, [userId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const sendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && socket) {
      const userMessage = {
        type: 'user',
        user: username || 'Anonymous',
        message: inputMessage
      };
      setMessages(prev => [...prev, userMessage]);
      setIsLoading(true);
      socket.emit('chat_message', {
        userId,
        message: inputMessage,
        username: username || 'Anonymous'
      });
      setInputMessage('');
    }
  };

  const handleInputChange = (e) => {
    setInputMessage(e.target.value);
  };

  return (
    <div className="h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6 flex flex-col">
      {/* Header Section */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto w-full mb-6"
      >
        <div className="flex items-center justify-between gap-4 mb-4">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-semibold text-gray-800">
              Travel Itinerary Assistant
            </h1>
          </div>
        </div>

        <motion.div 
          whileHover={{ scale: 1.01 }}
          className="bg-white rounded-lg p-4 shadow-sm flex justify-between items-center"
        >
           <p className="text-gray-600 text-sm">
             Chat with our AI travel assistant to plan your perfect trip
           </p>
        </motion.div>
      </motion.div>

      {/* Chat Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto w-full flex-1 bg-white rounded-lg shadow-sm flex flex-col overflow-hidden"
      >
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          <AnimatePresence>
            {messages.map((msg, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`
                  ${msg.type === 'system' 
                    ? 'bg-gray-100 text-gray-600 w-full text-center' 
                    : msg.type === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700'
                  } 
                  p-3 rounded-lg max-w-[70%] text-sm`}
                >
                  {msg.type !== 'system' && (
                    <div className="font-medium text-xs mb-1 opacity-90">
                      {msg.user}
                    </div>
                  )}
                  <ReactMarkdown className="prose prose-sm max-w-none">
                    {msg.message}
                  </ReactMarkdown>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <motion.form 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={sendMessage} 
          className="border-t border-gray-100 p-4 bg-white"
        >
          <div className="flex gap-2 relative">
            
            <div className="flex-1 relative">
              <input
                value={inputMessage}
                onChange={handleInputChange}
                placeholder={isLoading ? "Waiting for response..." : "Type your message..."}
                disabled={isLoading}
                className={`w-full px-3 py-2 rounded-md border border-gray-200 text-gray-600 text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  isLoading ? 'opacity-70' : ''
                }`}
              />
            </div>
            
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              type="submit" 
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-md text-sm transition-colors"
            >
              Send
            </motion.button>
          </div>
        </motion.form>
      </motion.div>
    </div>
  );
};

export default Chat; 