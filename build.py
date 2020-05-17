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
    

rmtree('Builds', ignore_errors=True)
# TODO: use files = glob.glob('/YOUR/PATH/*'); os.remove(f)
os.makedirs('Builds')

with open('manifest.json') as f:
    data = json.load(f)

# versioning: year.month.day.builds
version = datetime.today().strftime('%Y.%#m.%#d')
version = f"{version}.{int(data['version'].split('.')[-1]) + 1}"
data['version'] = version

with open('manifest.json', 'w') as fp:
    json.dump(data, fp, indent=4)

name = data['short_name']
filename = name + ' ' + version + '.zip'

with ZipFile('Builds/' + filename, 'w') as zf:
    zf.write('manifest.json')  # add manifiest.json to archive
    for icon in os.listdir('icons'):  # add icons to archive
        zf.write(f'icons/{icon}')
    zf.write('style.css')  # add css file to archive
    # zf.write('background.js')  # add js file to archive

print(f'Build successful. Version: {version}\nTimestamp: {datetime.now().time()}')
# TODO: use web-ext? 

git_push()

URL_NAME = 'dark-theme-for-google-searches'
# TODO: https://addons-server.readthedocs.io/en/latest/topics/api/signing.html
# GUID = '000a8ba3-ef46-40fd-a51c-daf19e7c00e7'
# requests.put(f'https://addons.mozilla.org/api/v4/addons/{GUID}/versions/{version}/')

print('https://userstyles.org/styles/180957/edit')
print(f'https://addons.mozilla.org/en-CA/developers/addon/{URL_NAME}/versions/submit/')
print('https://chrome.google.com/webstore/devconsole/d9cb1dfc-39c3-47c1-83ca-1ec7b4652439/ohhpliipfhicocldcakcgpbbcmkjkian/edit/package')
