#!/usr/bin/env python
# coding: utf-8

from ipywidgets import DOMWidget
from traitlets import Unicode, Dict, List
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

    prefs = List(Dict()).tag(sync=True)

    def __init__(self, results, problem, **kwargs):
        from desdeo_vis.plot.parallel import vega3_parplot_spec
        spec = vega3_parplot_spec(
            results, problem,
            dim_tooltips=True, dim_symbols=True)
        super().__init__(spec=spec, **kwargs)

    def nimbus_clf(self, meth):
        from desdeo.preference import NIMBUSClassification
        return NIMBUSClassification(
            meth, [
                (
                    pref['kind'],
                    float(pref['val']) if 'val' in pref else 0.0
                )
                for pref in self.prefs
            ]
        )
