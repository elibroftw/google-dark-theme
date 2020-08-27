import requests
import json
from zipfile import ZipFile
import io
import os
from build import create_zip
import jwt
import time
import uuid

guid = '000a8ba3-ef46-40fd-a51c-daf19e7c00e7'
with open('manifest.json') as f:
    manifest = json.load(f)
    version = manifest['version']
    name = manifest['short_name']

with open('.env') as f:
    line = f.readline()
    while line:
        k, v = line.split('=', 1)
        os.environ[k] = v.strip()
        line = f.readline()

jwt_secret = os.getenv('jwt-secret')
jwt_issuer = os.getenv('jwt-issuer')
assert jwt_issuer and jwt_secret
jwt_obj = {
    'iss': jwt_issuer,
    'jti': str(uuid.uuid4()),
    'iat': time.time(),
    'exp': time.time() + 60
}
jwt_obj = jwt.encode(jwt_obj, jwt_secret, algorithm='HS256').decode()
file = io.BytesIO()
create_zip(file)
data = {'upload': file.getvalue()}
headers = {'Authorization': f'JWT {jwt_obj}'}
r = requests.put(f'https://addons.mozilla.org/api/v4/addons/{guid}/versions/{version}/', data, headers=headers)
print(r.text)
