from zipfile import ZipFile
import os
import json
from shutil import rmtree
from contextlib import suppress


rmtree('Builds', ignore_errors=True)
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

print('Build successful')
# TODO: use web-ext
