from zipfile import ZipFile
import os
import json
from shutil import rmtree
from contextlib import suppress
import datetime
from git import Repo


def git_push():
    try:
        repo = Repo('.git')
        repo.git.add(update=True)
        repo.index.commit('updated styles')
        origin = repo.remote(name='origin')
        origin.push()
    except: print('Some error occured while pushing the code')
    finally: print('Code push from script succeeded')   
    

rmtree('Builds', ignore_errors=True)
# TODO: use files = glob.glob('/YOUR/PATH/*'); os.remove(f)
os.makedirs('Builds')

with open('manifest.json') as f:
    data = json.load(f)

# versioning: releases.builds
version = data['version'].split('.')
version[-1] = str(1 + int(version[-1]))
version = '.'.join(version)
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

print(f'Build successful. Version: {version}\nTimestamp: {datetime.datetime.now().time()}')
# TODO: use web-ext? 

git_push()