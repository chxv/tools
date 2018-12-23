from .RecodeModify import get_url as record_modify_url
from .RecordList import get_url as record_list_url

import requests
import json

__all__ = ['modify_record', 'list_record']


def modify_record(domain_value: str, record_id=397834481) -> dict:
    url = record_modify_url(domain_value, record_id)
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return {'status': 'Failed'}


def list_record() -> dict:
    url = record_list_url()
    r = requests.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    return {'status': 'Failed'}







