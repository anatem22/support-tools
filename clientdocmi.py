#!/usr/bin/env python3
import json, yaml, os, time
from keycloak.keycloak_openid import KeycloakOpenID
import requests
import hvac
import config
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VAULTOKEN='/var/run/secrets/kubernetes.io/serviceaccount/token'
VAULTSERVER=config.config.VAULTSERVER
VAULTROLE='ef_r'
VAULTPATH_SERVICE=config.config.VAULTPATH_SERVICE
AUTHTOKEN=None
KK_URL=config.config.KK_URL
KK_CLIENT=config.config.KK_CLIENT
KK_REALM=config.config.KK_REALM
USERNAME=None
PASSWORD=None
FFS=config.config.FFS
SECRET = None

def secretGetVault():
    try:
        vault_token = open(VAULTOKEN).read()
        client = hvac.Client(url=VAULTSERVER)
        client.auth.kubernetes.login(VAULTROLE, vault_token)
        VAULTSECRET=client.read(VAULTPATH_SERVICE)
    except:
        VAULTSECRET = None
    return VAULTSECRET

def getting_secrets():
    global SECRET
    global USERNAME
    global PASSWORD
    SECRET = secretGetVault()
    USERNAME=SECRET['data']['KeycloakUser']
    PASSWORD=SECRET['data']['KeycloakPassword']

def tokenGet():
    global SECRET
    if not SECRET:
        getting_secrets()
    try:
        keycloak_openid = KeycloakOpenID(server_url=KK_URL, client_id=KK_CLIENT, realm_name=KK_REALM, verify=False)
        AUTHTOKEN=keycloak_openid.token(USERNAME, PASSWORD)
    except:
        AUTHTOKEN={"access_token": "null"}
    return json.dumps( AUTHTOKEN["access_token"]).replace('"', r'')

def getFile(DOCID):
    METHOD='/v1/file/CLIENTDOC_SERVICE/'
    URL=FFS+METHOD+DOCID
    HEADERS={'Authorization': 'Bearer ' + tokenGet()}
    RESPONCE = requests.get(URL, headers=HEADERS, verify=False, timeout=20)
    return RESPONCE.content

def deleteFile(DOCID):
    METHOD='/v1/file/CLIENTDOC_SERVICE/'
    URL=FFS+METHOD+DOCID
    HEADERS={'Authorization': 'Bearer ' + tokenGet()}
    RESPONCE = requests.delete(URL, headers=HEADERS, verify=False, timeout=20)
    return RESPONCE.status_code

def searceFiles(MASTERID):
    #MASTERID='8dcb386e-d522-4758-bb4d-413f0016a569'
    SEARCH='/v1/file-info/search'
    URL=FFS+SEARCH
    HEADERS={'Content-type': 'application/json', 'Authorization': 'Bearer ' + tokenGet()}

    DATA={}
    JSONDATA={"buckets":["CLIENTDOC_SERVICE"],"meta":{"doc_type":"clientdoc_service","master_id":MASTERID}}
    RESPONCE = requests.post(URL, data=DATA, json=JSONDATA, headers=HEADERS, verify=False, timeout=20)
    JJ=RESPONCE.json()
    out_data = []
    for i in JJ:
        DOC={}
        DOC['masterid']=MASTERID
        DOC['initiator']=" "
        DOC['reason']=" "
        DOC['id']=i["id"]
        DOC['name']=i["name"]
        DOC['createDate']=i["createDate"]
        out_data.append(DOC)
    return out_data
