from zipfile import ZipFile
import os
import json
from shutil import rmtree
import datetime
from git import Repo
from datetime import datetime
from glob import glob
import requests
import argparse
import time
import jwt
import io
import uuid
from pprint import pprint
import pyperclip


parser = argparse.ArgumentParser(description='Google Dark Theme Build & Upload Script')
parser.add_argument('--upload', '-u', default=False, action='store_true', help='Upload to mozilla addons after')
args = parser.parse_args()

# TLDs
top_level_domains = ['com', 'com.ar', 'com.au', 'com.br', 'com.cu', 'com.gr', 'com.mx', 'com.pa', 'com.pk', 'com.sg',
                     'com.tr', 'com.tw', 'co.uk', 'co.jp', 'co.in', 'co.kr', 'co.th', 'co.za', 'ae', 'at', 'bg', 'ca', 'ch',
                     'cl', 'de', 'dk', 'es', 'fi', 'fr', 'gr', 'hu', 'ie', 'it', 'nl', 'pl', 'pt', 'rs', 'ru', 'sk']

match_bases = [
    '*://www.google.TLD/',
    '*://www.google.TLD/?*',
    '*://www.google.TLD/imghp*',
    '*://www.google.TLD/webhp*',
    '*://www.google.TLD/videohp*',
    '*://www.google.TLD/search*',
    '*://ogs.google.TLD/*',
    "*://images.google.TLD/*",
    "*://books.google.TLD/*",
    "*://scholar.google.TLD/*",
    "*://translate.google.TLD/*",
]

matches = [match_base.replace('TLD', tld) for tld in top_level_domains for match_base in match_bases]

GUID = '{000a8ba3-ef46-40fd-a51c-daf19e7c00e7}'
addon_files = ['manifest.json', 'style.css'] + glob('icons/*.png')
with open('style.css') as f: style = f.read()

# read environmental variables
with open('.env') as f:
    line = f.readline()
    while line:
        k, v = line.split('=', 1)
        os.environ[k] = v.strip()
        line = f.readline()



def is_ahead(repo):
    # if local repo/branch is ahead of origin
    return sum(1 for c in repo.iter_commits('origin/master..master'))


def create_zip(file):
    """ file: filename or file-type object """
    with ZipFile(file, 'w') as zf:
        for file in addon_files:
            zf.write(file)


def upload(version):
    # e.g. version = '1.1.1.1'

    # create auth JWT token
    jwt_secret = os.environ['jwt-secret']
    jwt_issuer = os.environ['jwt-issuer']
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
    url = f'https://addons.mozilla.org/api/v4/addons/{GUID}/versions/{version}/'
    r = requests.put(url, data, headers=headers, files=data)
    print(r.status_code)
    print(r.json())


if __name__ == '__main__':
    rmtree('builds', ignore_errors=True)
    os.makedirs('builds')

    with open('manifest.json') as f:
        manifest = json.load(f)

    manifest['content_scripts'][0]['matches'] = matches
    with open('manifest.json', 'w') as f:
        json.dump(manifest, f, indent=4)

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
        regex_com = '|'.join([tld.split('com.', 1)[1] for tld in top_level_domains if 'com.' in tld])
        regex_co = '|'.join([tld.split('co.', 1)[1] for tld in top_level_domains if 'co.' in tld])
        regex_other = '|'.join([tld for tld in top_level_domains if 'com' not in tld and 'co' not in tld])
        regex = r'@-moz-document regexp("https?://(www|scholar|translate|ogs)\\.google\\.((com(\\.(' + regex_com + r'))?)|(co\\.(' + 'in|jp|kr|uk' + '))|(' + regex_other + r'))/((webhp|videohp|imghp|search|\\?.*).*)?") {'
        print(regex)
        print(r'@-moz-document regexp("https?://(www|scholar|translate|ogs)\\.google\\.((com(\\.(ar|au|br|gr|mx|pk|tr))?)|(co\\.(in|jp|kr|uk))|(at|be|bg|ca|ch|cl|de|dk|es|fr|hu|ie|it|nl|pl|pt|ru))/((webhp|videohp|imghp|search|\\?.*).*)?") {')
        user_style = (
        '/* ==UserStyle==\n' +
        '@name Google Dark Theme\n' +
        f'@version {date}\n' +
        '@description A dark theme for Google (currently only supports searches).\n' +
        '@author Elijah Lopez\n' +
        '@namespace elibroftw\n' +
        '@homepageURL https://github.com/elibroftw/google-dark-theme\n' +
        '@supportURL https://github.com/elibroftw/google-dark-theme/issues/\n' +
        '@preprocessor stylus\n' +
        '==/UserStyle== */\n\n' +
        r'@-moz-document regexp("https?://(www|scholar|translate|ogs)\\.google\\.((com(\\.(ar|au|br|gr|mx|pk|tr))?)|(co\\.(in|jp|kr|uk))|(at|be|bg|ca|ch|cl|de|dk|es|fr|hu|ie|it|nl|pl|pt|ru))/((webhp|videohp|imghp|search|\\?.*).*)?") {' +
        f'\n\n{style}\n' + '}\n')
        with open('style.user.css', 'w') as f:
            f.write(user_style)
        pyperclip.copy(user_style)
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
    print('https://userstyles.org/styles/180957/edit')
    print('https://chrome.google.com/webstore/devconsole/d9cb1dfc-39c3-47c1-83ca-1ec7b4652439/ohhpliipfhicocldcakcgpbbcmkjkian/edit/package')
    if args.upload:
        upload(version)
    else:
        print(f'https://addons.mozilla.org/en-CA/developers/addon/{url_name}/versions/submit/')
