import base64
import json
import re
import os
from dotenv import load_dotenv
load_dotenv()

cookies_str = os.getenv('accounts_str_included_cookies')

def add_base64_padding(base64_string: str) -> str:
    # Calculate the required padding
    padding = len(base64_string) % 4
    if padding != 0:
        base64_string += '=' * (4 - padding)
    return base64_string

def decode_cookies_from_singlestr(singlestr:str)->dict:
    singlestr = add_base64_padding(singlestr)
    print(len(singlestr))
    decoded_data = base64.b64decode(singlestr).decode('utf-8')

    # Parse the JSON data
    cookies = json.loads(decoded_data)
    return cookies
# def decode_cookies_from_singlestr(singlestr: str) -> dict:
#     try:
#         # Adjust padding
#         padding = len(singlestr) % 4
#         if padding != 0:
#             singlestr += '=' * (4 - padding)
        
#         # Decode the Base64 string
#         decoded_data = base64.b64decode(singlestr).decode('utf-8')
        
#         # Parse the JSON data
#         cookies = json.loads(decoded_data)
#         return cookies
#     except (UnicodeDecodeError, json.JSONDecodeError, base64.binascii.Error) as e:
#         print(f"Error decoding string: {e}")
#         return {}
# def decode_cookies_from_singlestr(singlestr: str) -> dict:
#     try:
#         # Adjust padding
#         padding = len(singlestr) % 4
#         if padding != 0:
#             singlestr += '=' * (4 - padding)
        
#         # Decode the Base64 string
#         decoded_data = base64.b64decode(singlestr)
        
#         # Try decoding with utf-8, fallback to latin1 if necessary
#         try:
#             decoded_data = decoded_data.decode('utf-8')
#         except UnicodeDecodeError:
#             decoded_data = decoded_data.decode('latin1')
        
#         # Parse the JSON data
#         cookies = json.loads(decoded_data)
#         return cookies
#     except Exception as e:
#         print(f"Error decoding string: {e}")
#         return {}
# def decode_cookies_from_singlestr(singlestr: str) -> dict:
#     # Adjust padding
#     padding = len(singlestr) % 4
#     if padding != 0:
#         singlestr += '=' * (4 - padding)
    
#     # Decode the Base64 string
#     decoded_data = base64.b64decode(singlestr).decode('utf-8')

#     # Parse the JSON data
#     cookies = json.loads(decoded_data)
#     return cookies
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
            # print(len(item))
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

