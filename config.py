import os

class config(object):
    HOST = os.getenv('HOST') 
    PORT = os.getenv('PORT')
    VAULTSERVER=os.getenv('VAULTSERVER')
    VAULTPATH_SERVICE=os.getenv('VAULTPATH_SERVICE')
    VAULTPATH=os.getenv('VAULTPATH')
    KK_URL=os.getenv('KK_URL')
    KK_CLIENT=os.getenv('KK_CLIENT')
    KK_REALM=os.getenv('KK_REALM')
    FFS=os.getenv('FFS')
