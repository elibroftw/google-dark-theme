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


def git_push():
    try:
        repo = Repo('.git')
        repo.git.add(update=True)
        repo.index.commit('Updated style.css')
        origin = repo.remote(name='origin')
        origin.pull()
        origin.push()
    except: print('Some error occured while pushing the code')
    finally: print('Git push from script succeeded')


def create_zip(file):
    """ file: filename or file-type object """
    with ZipFile(file, 'w') as zf:
        zf.write('manifest.json')
        for icon in os.listdir('icons'):
            # add icons to archive
            zf.write(f'icons/{icon}')
        zf.write('style.css')
        # zf.write('background.js')


if __name__ == '__main__':
    rmtree('builds', ignore_errors=True)
    # TODO: use files = glob.glob('/YOUR/PATH/*'); os.remove(f)
    os.makedirs('builds')

    with open('manifest.json') as f:
        data = json.load(f)

    # versioning: year.month.day.builds
    date = datetime.today().strftime('%Y.%#m.%#d')
    build_no = int(data['version'].split('.')[-1]) + 1
    version = f'{date}.{build_no}'
    data['version'] = version

    with open('manifest.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    name = data['short_name']
    filename = f'{name} {version}.zip'
    create_zip(f'builds/{filename}')
    print(f'Build successful. Version: {version}\nTimestamp: {datetime.now().time()}')
    url_name = 'dark-theme-for-google-searches'
    print('https://raw.githubusercontent.com/elibroftw/google-dark-theme/cd732b2bc6e13c2e5c40455807082f0fd9827864/style.user.css')
    print('https://userstyles.org/styles/180957/edit')
    print(f'https://addons.mozilla.org/en-CA/developers/addon/{url_name}/versions/submit/')
    print('https://chrome.google.com/webstore/devconsole/d9cb1dfc-39c3-47c1-83ca-1ec7b4652439/ohhpliipfhicocldcakcgpbbcmkjkian/edit/package')
    git_push()
