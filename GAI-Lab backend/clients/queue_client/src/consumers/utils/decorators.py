import asyncio
import time
from functools import wraps


def timer(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        return execution_time, result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        return execution_time, result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def task_data(output_type, data_type, is_raw_output_file, file_suffix=None):
    def decorator(func):
        func.data = {
            "output_type": output_type,
            "data_type": data_type,
            "is_raw_output_file": is_raw_output_file,
            "file_suffix": file_suffix,
        }
        return func

    return decorator
