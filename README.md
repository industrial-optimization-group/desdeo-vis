# desdeo-vis

Visualisations and Jupyter Notebook enabled preference selection widgets for
the [https://github.com/industrial-optimization-group/pyDESDEO](DESDEO
interactive multiobjective optimization library).

Currently features:
 * Parallel coordinate plots based on [https://vega.github.io/](Vega v3).
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
