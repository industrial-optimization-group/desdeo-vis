import sys
from os import mkdir
from os.path import isdir, join as pjoin
from shutil import copyfileobj

from pkg_resources import resource_stream, resource_listdir, resource_isdir

if len(sys.argv) >= 2:
    dest_dir = sys.argv[1]
else:
    dest_dir = '.'

if not isdir(dest_dir):
    mkdir(dest_dir)

desdeo_notebooks = 'desdeo_notebooks'

for nbf in resource_listdir(desdeo_notebooks, 'notebooks'):
    if not nbf.endswith('.ipynb'):
        continue
    path = 'notebooks/' + nbf
    if resource_isdir(desdeo_notebooks, path):
        continue
    copyfileobj(
        resource_stream(desdeo_notebooks, path),
        open(pjoin(dest_dir, nbf), 'wb'))
