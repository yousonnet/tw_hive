import base64
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

cookies_str = os.getenv('accounts_str_included_cookies')


# def decode_cookies_from_singlestr(singlestr:str)->dict:
#     decoded_data = base64.b64decode(singlestr).decode('utf-8')

#     # Parse the JSON data
#     cookies = json.loads(decoded_data)
#     return cookies

def decode_cookies_from_singlestr(singlestr: str) -> dict:
    # Adjust padding
    padding = len(singlestr) % 4
    if padding != 0:
        singlestr += '=' * (4 - padding)
    
    # Decode the Base64 string
    decoded_data = base64.b64decode(singlestr).decode('utf-8')

    # Parse the JSON data
    cookies = json.loads(decoded_data)
    return cookies
# def decode_cookies_from_singlestr(singlestr):
#     # Adjust padding
#     padding = len(singlestr) % 4
#     if padding != 0:
#         singlestr += '=' * (4 - padding)
    
#     # Decode the Base64 string
#     decoded_data = base64.b64decode(singlestr).decode('utf-8')
#     return decoded_data
def extract_base64_data(text,base64_length:int=256)->list[str]:
    # Regular expression pattern to match base64 strings
    base64_pattern = r'[A-Za-z0-9+/=]{40,}'

    # Find all matches in the text
    matches = re.findall(base64_pattern, text)
    return_length_enough =[]
    for item in matches:
        if len(item)>=base64_length:
            return_length_enough.append(item)
    # Return the list of matches
    return return_length_enough

def reg_ct0andauth(single_cookies_list:list):
    cookie_dict={}
    for item in single_cookies_list:
        if item['name'] == 'ct0':
            cookie_dict['ct0'] = item['value']
        elif item['name'] == 'auth_token':
            cookie_dict['auth_token'] = item['value']
    return cookie_dict

cookies_list = list(map(lambda x: reg_ct0andauth( decode_cookies_from_singlestr(x)),extract_base64_data(cookies_str)))


#check account avail
for item in cookies_list:
    if item['auth_token'] and item['ct0']:
        pass
    else:
        print(cookies_list)
        raise Exception('个别账号不可用')

