import inspect
import time
from functools import partial, wraps

# Global dictionary to store execution times
execution_times = {}


def timer(request_id=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if func is a partial function and get original function name
            if isinstance(func, partial):
                func_name = func.func.__name__
            else:
                func_name = func.__name__

            start_time = time.time()
            sig = inspect.signature(func)
            if len(sig.parameters) == 0:
                result = func()
            else:
                result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            if request_id not in execution_times:
                execution_times[request_id] = {}

            execution_times[request_id][func_name] = execution_time

            return result

        return wrapper

    return decorator


def async_timer(request_id=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Check if func is a partial function and get original function name
            if isinstance(func, partial):
                func_name = func.func.__name__
            else:
                func_name = func.__name__

            start_time = time.time()

            # Check if the decorated function expects any arguments
            sig = inspect.signature(func)
            if len(sig.parameters) == 0:
                result = await func()
            else:
                result = await func(*args, **kwargs)

            end_time = time.time()
            execution_time = end_time - start_time

            nonlocal request_id
            if request_id is None:
                request_id = "default"

            if request_id not in execution_times:
                execution_times[request_id] = {}

            execution_times[request_id][func_name] = execution_time

            return result

        return wrapper

    return decorator


def get_inference_time(request_id):
    if request_id in execution_times:
        inference_times = execution_times.pop(request_id, {})
        total_time = sum(inference_times.values())
        inference_times["TotalTime"] = total_time
        return {"InferenceTime": inference_times}
    else:
        return {"InferenceTime": {}}
