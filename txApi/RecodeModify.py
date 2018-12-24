import time
import random
# from configs import configs
import urllib.parse
from .func import *


param = {
    # 公共请求参数↓
    'Action': 'RecordModify',
    'Timestamp': int(time.time()),  # unix时间戳 - 秒
    'Nonce': random.randrange(1, 100000),  # 随机整数
    'SecretId': configs['SecretId'],
    # 'Signature': '',必需，但是暂时不填充

    # 接口请求参数↓
    'domain': configs['domain'],
    'recordId': 397834481,  # pi.example.com  解析记录的id，可通过RecodeList查看
    'subDomain': 'pi',  # 子域名
    'recordType': 'A',  # 属性
    'recordLine': '默认',  # 使用默认解析线路
    # 'value': '',  # 记录值，比如A记录的ip，CNAME记录的域名
    # 'ttl': 300,  # 设置ttl为5分钟, 但是当前域名解析套餐支持的最小ttl是600
}


def get_url(domain_value: str, record_id=397834481) -> str:
    param['recordId'] = record_id  # 一般使用默认值即可
    param['value'] = domain_value  # 设置域名的解析值
    url = configs['api_url']
    request_url = url[8:]
    my_sign = sign(param, 'get', request_url)  # 计算Signature
    param['Signature'] = my_sign
    full_url = url + '?'
    for k in sorted(param.keys()):
        full_url += str(k) + '=' + urllib.parse.quote(str(param[k]), safe='') + '&'
    full_url = full_url[:-1]

    return full_url





