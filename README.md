# desdeo-vis

Visualisations and Jupyter Notebook enabled preference selection widgets for
the [DESDEO interactive multiobjective optimization library](https://github.com/industrial-optimization-group/DESDEO).

Currently features:
 * Parallel coordinate plots based on [Vega v3](https://vega.github.io/).
 * Preference selection for NIMBUS (first stage only).

## Installation / Usage

Typically you should install this at [the same time as DESDEO, by following the
instructions there](https://github.com/industrial-optimization-group/DESDEO).

## Development ##

### Compilation ###

Run:

```bash
npm run watch
```

You will need to refresh your browser, and possibly reload the Jupyter kernel to see some changes.

### Adding/modifying a notebook ###

Each notebook has two versions, one in the `notebooks` directory and one in the
`output-notebooks` directory. The version in the prior directory should be
scrubbed of all output and is the canonical copy. Currently they have have to
be kept in sync manually, e.g. by regenerating the output notebook from the
canonical version.

### Release process ###

1. Make a release commit in which the version is incremented in `_version.py` and `package.json` and an entry is added to HISTORY.md

2. Make a git tag of this commit with `git tag v$VERSION`

3. Push -- including the tags with `git push && git push --tags`

4. Upload to PyPI with `rm -rf build/ && python setup.py sdist bdist_wheel` and `twine upload dist/*`
