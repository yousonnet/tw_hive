from httpx import AsyncClient

from twitter.scraper import Scraper
import asyncio
from httpx import AsyncClient
# from fastapi import FastAPI
# import requests
from utils import is_str_in_data_value
from curl_cffi import requests
import json
async def test_call_function():
       async with requests.AsyncSession() as client:
            request_data = {
            "account_index": 1,
            "call_class": "scraper",
            "method_name": "users",  # 替换为你要调用的方法名
            "parameters_dict": {"screen_names": ['elonmusk'],"pbar":False,"save":False,"limit":5}  # 替换为实际参数
        }
        
            data = json.dumps(request_data)
            response = await client.post("http://127.0.0.1:7666/call-function", headers={'content-type': 'application/json'},data=data)
            return response.json()
            try:
                print(response.json())
            except Exception as e:
                print(f"Failed to parse JSON: {e}")
# 运行测试
async def iii():
    data = await test_call_function()
    print(type(data))
    print(is_str_in_data_value(data,'elonmusk'))
    return is_str_in_data_value(data,'elonmusk')
asyncio.run(iii())
# print((requests.get("http://127.0.0.1:7666/")).json())


# from a_hive_router import a_hive
# print(a_hive.root_data[5])
# print(a_hive.scrapers[5].users(['yousonnet'],limit=5))