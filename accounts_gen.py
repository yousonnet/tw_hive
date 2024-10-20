from proxies_set import proxy_dict_list
from cookies_extract import cookies_list


def match_proxy_account_asc(proxy_dict_list:list,cookies_list:list):
    proxy_numbers = len(proxy_dict_list)
    account_numbers = len(cookies_list)
    avail_accounts_nums = min([proxy_numbers,account_numbers])
    accounts_list =[]
    for index in range(0,avail_accounts_nums):
        proxy ="http://"+proxy_dict_list[index]['user']+":"+proxy_dict_list[index]['password']+"@"+proxy_dict_list[index]['ip']+":"+proxy_dict_list[index]['port']

        accounts_list.append({"proxy":proxy,"ct0":cookies_list[index]['ct0'],'auth_token':cookies_list[index]['auth_token']})
    return accounts_list

accounts_root_data=match_proxy_account_asc(proxy_dict_list,cookies_list)
print(accounts_root_data)