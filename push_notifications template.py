# Pushover Notifications, Optional - will return None if not set up

import requests
import functools
import time
from typing import Callable, Any

class PushoverNotifier:
    def __init__(self, api_token: str, user_key: str):
        self.api_token = api_token
        self.user_key = user_key
        self.api_url = "https://api.pushover.net/1/messages.json"

    def send_notification(self, message: str, title: str) -> bool:
        payload = {
            "token": self.api_token,
            "user": self.user_key,
            "message": message,
            "title": title
        }
        
        try:
            response = requests.post(self.api_url, data=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification: {str(e)}")
            return False

def notify_on_completion(api_token: str, user_key: str):
    """
    Decorator that sends a Pushover notification when a function completes or fails
    """
    
    def decorator(func: Callable) -> Callable:
        if not api_token or not user_key:
            return func  
        
        notifier = PushoverNotifier(api_token, user_key)
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            program_name = func.__name__
            
            try:
                result = func(*args, **kwargs)
                execution_time = round(time.time() - start_time, 2)
                success_message = (
                    f"Program '{program_name}' completed successfully!\n"
                    f"Execution time: {execution_time} seconds"
                )
                notifier.send_notification(
                    message=success_message,
                    title="✅ Program Success"
                )
                return result
                
            except Exception as e:
                execution_time = round(time.time() - start_time, 2)
                error_message = (
                    f"Program '{program_name}' failed!\n"
                    f"Error: {str(e)}\n"
                    f"Execution time: {execution_time} seconds"
                )
                notifier.send_notification(
                    message=error_message,
                    title="❌ Program Failed"
                )
                raise  # Re-raise the exception after sending notification
                
        return wrapper
    return decorator

API_TOKEN = "put api token here"
USER_KEY = "put user key here"