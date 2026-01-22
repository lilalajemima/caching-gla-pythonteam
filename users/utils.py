import time
import functools

def cache_performance(cache_name):
    """
    A decorator to measure how long a function takes to run.
    It prints the time to the console.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"⏱️  {cache_name} took: {duration:.4f} seconds")
            return result
        return wrapper
    return decorator