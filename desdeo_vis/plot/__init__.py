"""
This module contains the machinery for doing non-interactive plotting of
multidimensional data. Currently it can generate VEGA specifications for
parallel coordinates plots.
"""
__all__ = ['parplot']

from .parallel import vega3_parplot as parplot
