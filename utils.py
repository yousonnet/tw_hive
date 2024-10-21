
import functools
import traceback
import time
import asyncio
import re

def is_key_exists(data, target_key):
    if isinstance(data, dict):
        if target_key in data:
            return True
        return any(is_key_exists(value, target_key) for value in data.values())
    elif isinstance(data, list):
        return any(is_key_exists(item, target_key) for item in data)
    return False

def is_str_in_data_value(data, match_string: str):
    # Compile the regular expression pattern
    pattern = re.compile(match_string)
    
    if isinstance(data, dict):
        # Check if the pattern matches any of the values in the dictionary
        if any(pattern.search(str(value)) for value in data.values()):
            return True
        # Recursively check in the nested dictionaries
        return any(is_str_in_data_value(value, match_string) for value in data.values())
    elif isinstance(data, list):
        # Check if the pattern matches any of the items in the list
        if any(pattern.search(str(item)) for item in data):
            return True
        # Recursively check in the nested lists
        return any(is_str_in_data_value(item, match_string) for item in data)
    
    return False

def key_value_return(data, target_key, default_value):
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]  # Return the first found value
        for value in data.values():
            result = all_key_value_return(value, target_key, default_value)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = all_key_value_return(item, target_key, default_value)
            if result is not None:
                return result
    return default_value  # Return the default value if not found

def all_key_value_return(data, target_key):
    results = []
    
    if isinstance(data, dict):
        if target_key in data:
            results.append(data[target_key])
        for value in data.values():
            results.extend(all_key_value_return(value, target_key))
            
    elif isinstance(data, list):
        for item in data:
            results.extend(all_key_value_return(item, target_key))
    
    return results


def a_retry_decorator(max_retries=100, default_return=None):
    """装饰器：捕获异常并重试指定次数直到函数执行成功，max_retries=0 时立即返回 default_return"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:  # 改为 <= 以包含 max_retries = 0 的情况
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if max_retries == 0 or retries == max_retries:
                        print(f"函数 {func.__name__} 执行失败。错误类型: {type(e).__name__}，错误信息: {e}")
                        print("错误的堆栈跟踪:")
                        traceback.print_exc()  # 打印详细的堆栈跟踪
                        return default_return
                    
                    retries += 1
                    print(
                        f"函数 {func.__name__} 执行失败，将重试 {retries}/{max_retries} 次。错误类型: {type(e).__name__}，错误信息: {e}")
                    print("错误的堆栈跟踪:")
                    traceback.print_exc()  # 打印详细的堆栈跟踪
                    await asyncio.sleep(0.1)
            
            # 这行代码实际上不会被执行到，因为所有情况都在循环中处理了
            # 但为了代码的完整性和清晰度，我们保留它
            return default_return
        return wrapper
    return decorator



def retry_decorator(max_retries=100, default_return=None):
    """装饰器：捕获异常并重试指定次数直到函数执行成功，max_retries=0 时立即返回 default_return"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:  # 改为 <= 以包含 max_retries = 0 的情况
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if max_retries == 0 or retries == max_retries:
                        print(f"函数 {func.__name__} 执行失败。错误类型: {type(e).__name__}，错误信息: {e}")
                        print("错误的堆栈跟踪:")
                        traceback.print_exc()  # 打印详细的堆栈跟踪
                        return default_return
                    
                    retries += 1
                    print(
                        f"函数 {func.__name__} 执行失败，将重试 {retries}/{max_retries} 次。错误类型: {type(e).__name__}，错误信息: {e}")
                    print("错误的堆栈跟踪:")
                    traceback.print_exc()  # 打印详细的堆栈跟踪
                    time.sleep(0.1)  # 使用 time.sleep 代替 asyncio.sleep
            
            # 这行代码实际上不会被执行到，因为所有情况都在循环中处理了
            # 但为了代码的完整性和清晰度，我们保留它
            return default_return
        return wrapper
    return decorator