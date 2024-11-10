import json
import logging
from typing import List, Dict
import ollama
from src.services.weather_service import get_weather_forecast
from src.memory.memory_manager import MemoryManager
from datetime import datetime

async def interact_with_gen_llm(messages: List[Dict], user_id: str, memory_manager: MemoryManager):
    # First ensure user node exists
    memory_manager.create_user_if_not_exists(user_id)
    
    # Extract user message for analysis
    user_message = messages[-1]["content"] if messages[-1]["role"] == "user" else ""
    
    # Get user preferences from memory
    preferences = memory_manager.get_preferences(user_id)
    context = f"User preferences: {preferences}\n"
    
    # Prepare messages with context
    formatted_messages = [
        {"role": "system", "content": context + messages[0]["content"]},
        *[{"role": msg["role"], "content": msg["content"]} for msg in messages[1:]]
    ]
    
    print(formatted_messages)
    
    response = ollama.chat(
        model="llama3.2",
        messages=formatted_messages,
        stream=False,
        # tools=[{
        #     "name": "get_weather",
        #     "description": "Get weather information for a specific city",
        #     "parameters": {
        #         "type": "object",
        #         "properties": {
        #             "city": {
        #                 "type": "string",
        #                 "description": "The name of the city"
        #             }
        #         },
        #         "required": ["city"]
        #     }
        # }]
    )
    
    llm_content = response["message"]["content"]
    
    print(response)
    
    # Handle function calling if present and valid
    if "tool_calls" in response["message"]:
        for tool_call in response["message"]["tool_calls"]:
            if tool_call["function"]["name"] == "get_weather":
                try:
                    args = json.loads(tool_call["function"]["arguments"])
                    if "city" in args and args["city"].strip():  # Verify city is provided and not empty
                        weather_info = get_weather_forecast(args["city"])
                        
                        # Add the initial assistant response and weather function result to messages
                        messages.extend([
                            {"role": "assistant", "content": llm_content},
                            {"role": "function", "name": "get_weather", "content": json.dumps(weather_info)}
                        ])
                        
                        # Generate final response incorporating weather information
                        weather_response = ollama.chat(
                            model="llama3.2",
                            messages=[*formatted_messages, *messages[-2:]],  # Include the two new messages
                            stream=False
                        )
                        llm_content = weather_response["message"]["content"]
                except json.JSONDecodeError:
                    logging.warning("Invalid JSON in weather tool arguments")
                except Exception as e:
                    logging.error(f"Error processing weather tool call: {str(e)}")
    
    # Extract and store preferences if found in the message
    if "prefer" in user_message.lower() or "like" in user_message.lower():
        memory_manager.store_preference(
            user_id,
            {
                "type": "preference",
                "value": user_message,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    return llm_content

