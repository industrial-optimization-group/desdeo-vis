#!/usr/bin/env python
# coding: utf-8

from ipywidgets import DOMWidget
from traitlets import Unicode, Dict, List, Bool, observe, default
from desdeo.utils.exceptions import DESDEOException
from desdeo.method.NIMBUS import NIMBUS
from desdeo.preference import NIMBUSClassification
from desdeo_vis._version import EXTENSION_SPEC_VERSION
from desdeo_vis.conf import get_conf

module_name = "desdeo_vis"


class InvalidNimbusPreferencesException(DESDEOException):
    pass


class VegaWidget(DOMWidget):
    _model_name = Unicode('VegaModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)
    _view_name = Unicode('VegaView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(EXTENSION_SPEC_VERSION).tag(sync=True)

    spec = Dict().tag(sync=True)


class ParplotWidget(VegaWidget):
    """
    A parallel plot widget to display solutions to a multi-objective
    optimization problem.
    """

    _model_name = Unicode('ParplotModel').tag(sync=True)
    _view_name = Unicode('ParplotView').tag(sync=True)

    maximized = List().tag(sync=True)
    orig_max_as_min = Bool().tag(sync=True)
    cur_max_as_min = Bool().tag(sync=True)

    def __init__(self, results, problem, max_as_min=None, **kwargs):
        """
        Parameters
        ----------
        results
            The solutions to plot.

        problem
            The DESDEO problem with which the plot is made with respect to.

        max_as_min
            Whether to reformulate maximized functions as minimized functions.
        """
        self.results = results
        self.problem = problem
        self.maximized = problem.maximized
        if max_as_min is not None:
            self.orig_max_as_min = max_as_min
        else:
            self.orig_max_as_min = get_conf('max_as_min')
        self.update_spec()

        super().__init__(**kwargs)

    @default('cur_max_as_min')
    def _max_as_min_default(self):
        return self.orig_max_as_min

    @observe('cur_max_as_min')
    def update_max_as_min(self, change):
        self.update_spec()

    def update_spec(self):
        from desdeo_vis.plot.parallel import vega3_parplot_spec
        self.spec = vega3_parplot_spec(
            self.results, self.problem,
            max_as_min=self.cur_max_as_min,
            dim_tooltips=True, dim_symbols=True)


class NimbusPrefWidget(ParplotWidget):
    """
    A NIMBUS preference selection widget. This allows for graphical selection
    of preferences in the form NIMBUS requires.
    """

    _model_name = Unicode('NimbusPrefModel').tag(sync=True)
    _view_name = Unicode('NimbusPrefView').tag(sync=True)

    prefs = List(Dict()).tag(sync=True)
    prob = Unicode(allow_none=True).tag(sync=True)

    def __init__(self, results, problem, max_as_min=None, **kwargs):
        super().__init__(results, problem, max_as_min=max_as_min, **kwargs)

    def nimbus_clf(self, meth: NIMBUS) -> NIMBUSClassification:
        """
        Get the NIMBUS preference currently selected with the widget as a
        NIMBUSClassification. Raises a InvalidNimbusPreferencesException if an
        invalid preference is chosen.
        """
        if self.prob is not None:
            raise InvalidNimbusPreferencesException(
                "Preference is invalid: " + self.prob)
        return NIMBUSClassification(
            meth, [
                (
                    pref['kind'],
                    float(pref['val']) if 'val' in pref else 0.0
                )
                for pref in self.prefs
            ]
        )
