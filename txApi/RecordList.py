import time
import random
# from configs import configs
import requests
import urllib.parse
import json
from .func import *  # 隐含了from configs import configs

param = {
    # 公共请求参数↓
    'Action': 'RecordList',

    'Timestamp': int(time.time()),  # unix时间戳 - 秒
    'Nonce': random.randrange(1, 100000),  # 随机整数
    'SecretId': configs['SecretId'],
    # 'Signature': '',必需，但是暂时不填充

    # 接口请求参数↓
    # 'offset': 0,
    # 'length': 20,
    'domain': configs['domain'],
    # 'subDomain': 'pi',  # 过滤器，比如只显示子域名为pi的记录
}


def get_url() -> str:
    url = 'https://cns.api.qcloud.com/v2/index.php'
    request_url = url[8:]
    my_sign = sign(param, 'get', request_url)
    param['Signature'] = my_sign
    full_url = url + '?'
    for k in sorted(param.keys()):
        full_url += str(k) + '=' + urllib.parse.quote(str(param[k]), safe='') + '&'
    full_url = full_url[:-1]

    return full_url





