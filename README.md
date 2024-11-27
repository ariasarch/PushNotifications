https://pushover.net/

How to use: 

@notify_on_completion(API_TOKEN, USER_KEY)
your_function_you_want_a_notification_from_here ( )

then later 

try:
    your_function_you_want_a_notification_from_here ( )
except Exception as e:
    print(f"An error occurred: {str(e)}")
