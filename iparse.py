"""iparse

ip 地址替换
"""
import sys
import re

# ip正则匹配
# 250-255 | 200-249 | 0-199
# 25[0-5]|2[0-4]\d|1?\d{1,2} 匹配0-255
# (){3} 将目标匹配三次
raw_ip_pattern = re.compile(
    r'((25[0-5]|2[0-4]\d|1?\d{1,2})\.){3}(25[0-5]|2[0-4]\d|1?\d{1,2})$')

# 匹配16进制的ip格式
hex_ip_pattern = re.compile(r'0x[0-9a-fA-F]{0,8}$')


def hex2bin(ip: str) -> str:
    """十六进制ip转普通格式ip"""
    d = int(ip, 16)             # 十六进制str转十进制int
    d2 = bin(d)[2:]             # 十进制int转二进制str
    d2 = (32-len(d2))*'0' + d2  # 得到32位二进制数
    result = ''
    for i in range(0, 32, 8):
        result += str(int(d2[i:i+8], 2))
        if i < 24:
            result += '.'
    return result


def bin2hex(ip: str) -> str:
    """普通格式ip转对应的十六进制"""
    result = ''
    d = ip.split('.')
    for i in d:
        b = bin(int(i))[2:]
        b = (8-len(b))*'0' + b
        result += b
    result = int(result, 2)
    result = hex(result)
    return result


def main() -> None:
    if len(sys.argv) == 2:
        target_ip = sys.argv[1]
    else:
        target_ip = input('Input target ip: ')

    r = raw_ip_pattern.match(target_ip)
    if r:
        # 输入参数为普通ip格式
        result = bin2hex(target_ip)
        print(result)
    else:
        r = hex_ip_pattern.match(target_ip)
        if r:
            # 输入参数为16进制ip
            result = hex2bin(target_ip)
            print(result)
        else:
            print('[-] error: invalid target ip')


if __name__ == "__main__":
    main()
