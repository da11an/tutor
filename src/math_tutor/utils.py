import time

def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start timing
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # End timing
        duration = end_time - start_time  # Calculate duration
        return result, duration  # Return result and duration as a tuple
    return wrapper
