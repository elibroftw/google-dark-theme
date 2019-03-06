from zipfile import ZipFile
import os
import json


with open('manifest.json') as f:
    data = json.load(f)

version = data['version'].split('.')
version[-1] = str(1 + int(version[-1]))
version = '.'.join(version)
data['version'] = version

with open('manifest.json', 'w') as fp:
    json.dump(data, fp)

name = data['short_name']
filename = name + ' ' + version + '.zip'

if not os.path.exists('Builds'):
    os.makedirs('Builds')

try:
    with ZipFile('Builds/' + filename, 'w') as zf:
        zf.write('manifest.json')  # add manifiest.json to archive
        # add icons to archive
        for icon in os.listdir('icons'):
            zf.write(f'icons/{icon}')

        # add css file to archive
        zf.write('style.css')
    done = True
except Exception as e:
    if e != KeyboardInterrupt:
        print(e)
        breakpoint()

print('Build successful')
# TODO: use web-ext
