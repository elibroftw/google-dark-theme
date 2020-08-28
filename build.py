from zipfile import ZipFile
import os
import json
from shutil import rmtree
from contextlib import suppress
import datetime
from git import Repo
from datetime import datetime
import webbrowser
import requests
import argparse
import time
import jwt
import io
import uuid


parser = argparse.ArgumentParser(description='Google Dark Theme Build & Upload Script')
parser.add_argument('--upload', default=False, action='store_true', help='Upload to mozilla addons after')
args = parser.parse_args()


def is_ahead(repo):
    # if local repo/branch is ahead of origin
    return sum(1 for c in repo.iter_commits('origin/master..master'))


def create_zip(file):
    """ file: filename or file-type object """
    with ZipFile(file, 'w') as zf:
        zf.write('manifest.json')
        for icon in os.listdir('icons'):
            # add icons to archive
            zf.write(f'icons/{icon}')
        zf.write('style.css')
        # zf.write('background.js')


def upload(name, version):
    guid = '{000a8ba3-ef46-40fd-a51c-daf19e7c00e7}'

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
    print(f'uploading version {version}')
    data = {'upload': ('manifest.zip', file.getvalue()), 'channel': 'listed'}
    headers = {'Authorization': f'JWT {jwt_obj}'}
    url = f'https://addons.mozilla.org/api/v4/addons/{guid}/versions/{version}/'
    # url = 'https://postman-echo.com/put/'
    r = requests.put(url, data, headers=headers, files=data)
    if r.status_code == 200:
        print('Sucessfully uploaded')
    else:
        print('Something went wrong')
        print(r.json())


if __name__ == '__main__':
    rmtree('builds', ignore_errors=True)
    os.makedirs('builds')

    with open('manifest.json') as f:
        manifest = json.load(f)

    # versioning: year.month.day.builds
    repo = Repo('.git')
    origin = repo.remote(name='origin')
    commits_behind = sum(1 for c in repo.iter_commits('master..origin/master'))
    if commits_behind:
        # if origin has changes
        commit_message = ', '.join([item.a_path for item in repo.index.diff(None)])
        repo.git.add(update=True)
        repo.index.commit(f'Updated {commit_message}')
        origin.pull()
    if is_ahead(repo) or repo.is_dirty():
        # if need to push or any changes were made
        date = datetime.today().strftime('%Y.%#m.%#d')
        changed_files = {item.a_path for item in repo.index.diff(None)}
        build_no = int(manifest['version'].split('.')[-1])
        if 'style.css' in changed_files or 'manifest.json' in changed_files or 'Icons/icon16.png' in changed_files:
            # only update build if style.css, manifest.json, or icons have changed
            build_no += 1
        version = f'{date}.{build_no}'
        manifest['version'] = version
        with open('manifest.json', 'w') as fp:
            json.dump(manifest, fp, indent=4)
        commit_message = ', '.join([item.a_path for item in repo.index.diff(None)])
        repo.git.add(update=True)
        repo.index.commit(f'Updated {commit_message}')
        origin = repo.remote(name='origin')
        origin.push()
    else:
        version = manifest['version']
    name = manifest['short_name']
    filename = f'{name} {version}.zip'
    create_zip(f'builds/{filename}')

    print(f'Build successful. Version: {version}\nTimestamp: {datetime.now().time()}')
    url_name = 'dark-theme-for-google-searches'
    print('https://raw.githubusercontent.com/elibroftw/google-dark-theme/cd732b2bc6e13c2e5c40455807082f0fd9827864/style.user.css')
    print('https://userstyles.org/styles/180957/edit')
    print('https://chrome.google.com/webstore/devconsole/d9cb1dfc-39c3-47c1-83ca-1ec7b4652439/ohhpliipfhicocldcakcgpbbcmkjkian/edit/package')
    if args.upload:
        upload(name, version)
    else:
        print(f'https://addons.mozilla.org/en-CA/developers/addon/{url_name}/versions/submit/')
