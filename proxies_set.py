from dotenv import load_dotenv
import os

load_dotenv()

proxies_str= os.getenv('proxie_str')

def extract_proxydict_list(whole_string:str):
    proxie_list = [proxie.split(':') for proxie in whole_string.split(',')]
    return_proxies_list =[]
    for item in proxie_list:
        return_proxies_list.append({'ip':item[0],'port':item[1],'user':item[2],'password':item[3]})
    return return_proxies_list


proxy_dict_list = extract_proxydict_list(proxies_str)

