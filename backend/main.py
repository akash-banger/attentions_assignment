from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn
import logging
from fastapi import HTTPException
from src.db.helpers import create_user, get_user_by_id, get_user_by_username
from pydantic import BaseModel
from src.llm.chat import get_ai_response
from typing import List, Dict
from src.llm.prompt import system_prompt
from src.memory.memory_manager import MemoryManager


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create a Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*'
)

socket_app = socketio.ASGIApp(sio, app)

class UserCreate(BaseModel):
    username: str
    password: str
    
@app.post("/api/users")
async def create_new_user(user: UserCreate):
    try:
        existing_user = get_user_by_username(user.username)
        if existing_user:
            if existing_user.password == user.password:
                return {"message": "User already exists", "user_id": str(existing_user.id)}
            else: 
                raise HTTPException(status_code=400, detail="Invalid password")
        new_user = create_user(user.username, user.password)
        return {"message": "User created successfully", "user_id": str(new_user.id)}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@sio.event
async def connect(sid, environ):
    query_string = environ['QUERY_STRING']
    params = dict(param.split('=') for param in query_string.split('&'))
    user_id = params.get('userId')
    try:
        user = get_user_by_id(user_id)
        if user:
            if user_id not in chat_histories:
                chat_histories[user_id] = [{
                    "role": "system",
                    "content": system_prompt
                }]
            logger.info(f"User {user.username} (ID: {user_id}) connected with SID: {sid}")
            return True
        else:
            return True
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        return False
    
@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")
    
# Modify the chat histories to be user-specific
chat_histories: Dict[str, Dict[str, List[Dict[str, str]]]] = {}

# Add this after creating the chat_histories dictionary
memory_managers: Dict[str, MemoryManager] = {}

@sio.event
async def chat_message(sid, data):
    user_id = data.get('userId')
    message = data.get('message')
    username = data.get('username', 'Anonymous')
    try:
        user = get_user_by_id(user_id)
        if user:
            # Initialize memory manager for user if not exists
            if user_id not in memory_managers:
                memory_managers[user_id] = MemoryManager()
                
            formatted_message = f"**[{username}]:** {message}"
            
            if user_id not in chat_histories:
                chat_histories[user_id] = []
                
            chat_histories[user_id].append({
                "role": "user",
                "content": formatted_message
            })
            
            # Pass the memory_manager to get_ai_response
            ai_response = await get_ai_response(
                chat_histories[user_id],
                user_id,
                memory_managers[user_id]
            )
            
            if ai_response and ai_response.strip():
                formatted_ai_response = f"**[Itinerary Agent]:** {ai_response}"
                chat_histories[user_id].append({
                    "role": "assistant",
                    "content": formatted_ai_response
                })
                
                await sio.emit('message_response', {
                    'user': 'Itinerary Agent',
                    'message': ai_response,
                    'type': 'ai'
                }, to=sid)
            
        return True
    except Exception as e:
        logger.error(f"Error in chat_message: {str(e)}")
        return False

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")
    # Clean up memory manager if it exists
    if sid in memory_managers:
        memory_managers[sid].close()
        del memory_managers[sid]
    return True


if __name__ == "__main__":
    uvicorn.run("main:socket_app", host="127.0.0.1", port=8000, reload=True, log_level="info")