from httpx import Client
from twitter.account import Account
from twitter.scraper import Scraper
from twitter.search import Search
from utils import a_retry_decorator
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

class Hive():
    def __init__(self,accounts_gen_data:list[dict]):
        self.root_data = accounts_gen_data
        self.scrapers = list(map(lambda x : Scraper(cookies={'ct0':x['ct0'],'auth_token':x['auth_token']},session=Client(proxies=x['proxy'])),accounts_gen_data))
        self.accounts = list(map(lambda x : Account(cookies={'ct0':x['ct0'],'auth_token':x['auth_token']},session=Client(proxies=x['proxy'])),accounts_gen_data))
        self.searches = list(map(lambda x : Search(cookies={'ct0':x['ct0'],'auth_token':x['auth_token']},session=Client(proxies=x['proxy'])),accounts_gen_data))
        self.accounts_length = len(accounts_gen_data)
    # @a_retry_decorator(3,'error')
    # async def call_func(self,account_index:int,call_class:str,method_name:str,parameters_dict:dict):
    #     if call_class == 'account':
    #         account = self.accounts[account_index]
    #         method = getattr(account, method_name)  # 使用 getattr 动态获取方法
    #         return method(**parameters_dict)  # 调用方法并传递参数
    #     elif call_class =='scraper':
    #         scrapers = self.scrapers[account_index]
    #         method = getattr(scrapers, method_name)  # 使用 getattr 动态获取方法
    #         return method(**parameters_dict)  # 调用方法并传递参数
    #     elif call_class =='search':
    #         searches = self.searches[account_index]
    #         method = getattr(searches, method_name)  # 使用 getattr 动态获取方法
    #         return method(**parameters_dict)  # 调用方法并传递参数
    #     else:
    #         return 'can not find matchable call_class'
    @a_retry_decorator(3, 'error')
    async def call_func(self, account_index: int, call_class: str, method_name: str, parameters_dict: dict):
        print(self.root_data[account_index]['proxy'])
        if call_class == 'account':
            account = self.accounts[account_index]
            method = getattr(account, method_name)
            return await method(**parameters_dict)
        elif call_class == 'scraper':
            scraper = self.scrapers[account_index]
            method = getattr(scraper, method_name)
            if asyncio.iscoroutinefunction(method):
                return await method(**parameters_dict)
            else:
                loop = asyncio.get_running_loop()
                with ThreadPoolExecutor() as executor:
                    func_with_args = partial(method, **parameters_dict)
                    return await loop.run_in_executor(executor, func_with_args)
        elif call_class == 'search':
            search = self.searches[account_index]
            method = getattr(search, method_name)
            return await method(**parameters_dict)
        else:
            return 'cannot find matchable call_class'