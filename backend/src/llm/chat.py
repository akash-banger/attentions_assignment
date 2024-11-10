import openai  # You'll need to install this
import os
from src.llm.interact import interact_with_gen_llm
from src.memory.memory_manager import MemoryManager
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)
async def get_ai_response(messages: List[Dict], user_id: str, memory_manager: MemoryManager):
    try:
        response = await interact_with_gen_llm(messages, user_id, memory_manager)
        return response
    except Exception as e:
        logger.error(f"Error getting AI response: {str(e)}")
        return "I apologize, but I encountered an error processing your request." 