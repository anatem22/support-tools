import jwt
import requests
import json
import config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KK_URL=config.config.KK_URL
KK_REALM=config.config.KK_REALM

def public_key():
    URL =  f'{KK_URL}realms/{KK_REALM}'
    RESPONCE = requests.get(URL,  verify=False, timeout=20)
    KEY=RESPONCE.json()['public_key']
    PUBLIC_KEY='-----BEGIN PUBLIC KEY-----\n' + KEY + '\n-----END PUBLIC KEY-----'
    return PUBLIC_KEY

