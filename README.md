# desdeo-vis

Visualisations and Jupyter Notebook enabled preference selection widgets for
the [DESDEO interactive multiobjective optimization library](https://github.com/industrial-optimization-group/pyDESDEO).

Currently features:
 * Parallel coordinate plots based on [Vega v3](https://vega.github.io/).
 * Preference selection for NIMBUS (first stage only).

## Installation

A typical installation requires the following commands to be run:

```bash
pip install https://github.com/industrial-optimization-group/desdeo_vis.git#egg=desdeo_vis
jupyter nbextension enable --py [--sys-prefix|--user|--system] desdeo_vis
```

XXX: The below is untested/assumed not to work.

Or, if you use jupyterlab:

```bash
pip install https://github.com/industrial-optimization-group/desdeo_vis.git#egg=desdeo_vis
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

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
