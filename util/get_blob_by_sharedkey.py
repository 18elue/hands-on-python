import os
import base64
import hmac
import hashlib
import requests
from datetime import datetime
import json

# load config data
with open('configure/get_blob_by_sharedkey.json') as f:
    config = json.load(f)

xmsdate = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# string format standard by azure
string2sign = 'GET\n\n\n\n\n\n\n\n\n\n\n\nx-ms-date:{}\nx-ms-version:{}\n/{}{}'.format(
    xmsdate, config['xmsversion'], config['account_name'], config['file_path'])

# sign the string
signature = hmac.new(
    base64.b64decode(config['access_key']),
    msg=string2sign.encode('utf-8'),
    digestmod=hashlib.sha256
).digest()

signature64 = base64.b64encode(signature)

# make https request to get blob data
conn = requests.get(config['end_point']+config['file_path'],
                    headers={'Authorization': 'SharedKey {}:{}'.format(config['account_name'], signature64.decode('utf-8')),
                             'x-ms-date': xmsdate,
                             'x-ms-version': config['xmsversion']})

print(conn.text)