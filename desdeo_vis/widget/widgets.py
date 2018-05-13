#!/usr/bin/env python
# coding: utf-8

from ipywidgets import DOMWidget
from traitlets import Unicode, Dict
from desdeo_vis._version import EXTENSION_SPEC_VERSION

module_name = "desdeo_vis"


class VegaWidget(DOMWidget):
    _model_name = Unicode('VegaModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _view_name = Unicode('VegaView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)

    spec = Dict().tag(sync=True)


class NimbusPrefWidget(VegaWidget):
    _model_name = Unicode('NimbusPrefModel').tag(sync=True)
    _view_name = Unicode('NimbusPrefView').tag(sync=True)

    def __init__(self, results, problem, **kwargs):
        from desdeo_vis.plot.parallel import prepare_df, vega3_parplot
        df = prepare_df(results, problem)
        spec = vega3_parplot(df, dim_tooltips=True, dim_symbols=True)
        super().__init__(spec=spec, **kwargs)
