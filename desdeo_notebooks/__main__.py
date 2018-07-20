import sys
from os import mkdir
from os.path import isdir, join as pjoin
from shutil import copyfileobj

from pkg_resources import resource_stream, resource_listdir, resource_isdir


def main():
    output = False
    dest_dir = '.'

    for arg in sys.argv[1:]:
        if arg == '-o' or arg == '--output':
            output = True
        else:
            dest_dir = arg

    if not isdir(dest_dir):
        mkdir(dest_dir)

    desdeo_notebooks = 'desdeo_notebooks'
    if output:
        nb_dir = "output/"
    else:
        nb_dir = ""

    for nbf in resource_listdir(desdeo_notebooks, nb_dir):
        if not nbf.endswith('.ipynb'):
            continue
        path = nb_dir + nbf
        if resource_isdir(desdeo_notebooks, path):
            continue
        copyfileobj(
            resource_stream(desdeo_notebooks, path),
            open(pjoin(dest_dir, nbf), 'wb'))


if __name__ == '__main__':
    main()
