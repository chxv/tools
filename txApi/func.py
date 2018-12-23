import hmac
import base64
from hashlib import sha1
from txApi.configs import configs


def hash_hmac(code, key, sha1):
    """hash"""
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
    return base64.b64encode(hmac_code).decode()


def sign(d: dict, request_method: str, request_url: str) -> str:
    """接收不包含signature参数的参数字典，生成signature字符串"""
    # 1.排序
    sd = sorted(d)  # 获得排序后的字典key
    # 2. 开始拼接字符串
    prefix = request_method.strip().upper() + request_url.strip()  # 前半部分
    suffix = ''  # 后半部分
    for k in sd:
        suffix += f'{k}={str(d[k])}&'
    suffix = suffix[:-1]  # 去掉最后一位多余的 &
    s = prefix + '?' + suffix  # 获得最后拼接完成的字符串
    # 3. 生成签名串
    SecretKey = configs['SecretKey']
    sign_str = hash_hmac(s, SecretKey, sha1)

    return sign_str
