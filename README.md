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

Each notebook has two versions, one in the `desdeo_notebooks` directory and one
in the `desdeo_notebooks/output` directory. The version in the prior directory
should be scrubbed of all output and is the canonical copy. Currently they have
have to be kept in sync manually, e.g. by regenerating the output notebook from
the canonical version. When regenerating, make sure to save widget state with
`Widgets > Save Notebook Widget State`.

### Known issues ###

If you are developing using a virtualenv (recommended) you may have trouble
widget Javascript from outside the virtualenv getting picked up, meaning you
can't test your changes. This is a problem when you have installed desdeo-vis
outside the virtualenv either system-wide or per-user. Currently, there's no
clear way to isolate this Javascript, so the solution is to uninstall the other
versions of desdeo-vis and make sure to only install it inside virtualenvs.

### Release process ###

1. Update the version number in `desdeo_vis/_version.py` and `package.json`,
   and run `npm install` to update it in `package-lock.json` too.

2. Add an entry to HISTORY.md.

2. Make a release commit.

3. Make a git tag of this commit with `git tag v$VERSION`

4. Push -- including the tags with `git push && git push --tags`

5. Upload to PyPI with `rm -rf build/ && python setup.py sdist bdist_wheel` and `twine upload dist/*`
