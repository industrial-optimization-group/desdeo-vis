#!/usr/bin/python
from matplotlib.ticker import MaxNLocator
from copy import deepcopy


def ticks(vmin, vmax):
    nbins = 9
    steps = [1, 2, 2.5, 5, 10]
    locator = MaxNLocator(
        nbins=nbins,
        steps=steps,
        prune='both')
    return locator.tick_values(vmin, vmax)


def vega3_parplot_df_spec(
        heading_df,
        values_df,
        custom_axis_values=True,
        dim_labels=True,
        dim_tooltips=False,
        dim_symbols=False):
    # Based on https://vega.github.io/vega/examples/parallel-coordinates/
    from altair.vega.data import to_values

    def min_max(row):
        if row['ideal'] < row['nadir']:
            return row['ideal'], row['nadir']
        else:
            return row['nadir'], row['ideal']

    def scale_of_row(row):
        mn, mx = min_max(row)
        return {
            "name": row['name'],
            "type": "linear",
            "range": "height",
            "zero": False,
            "domain": [mn, mx],
        }

    def axis_of_row(row):
        json = {
            "orient": "left",
            "zindex": 1,
            "scale": row['name'],
            "title": row['name'],
            "offset": {
                "scale": "ord",
                "value": row['name'],
                "mult": -1
            }
        }
        if custom_axis_values:
            mn, mx = min_max(row)
            tick_vals = list(ticks(mn, mx))
            json['values'] = (
                [row['ideal']]
                + tick_vals
                + [mx])
            json['format'] = ".5"
        return json

    def text():
        return {
            "signal": "format(parent[datum.data], \".5\")"
        }

    def full_text():
        return {
            "signal": "parent[datum.data]"
        }

    def mark(type):
        json = {
            "type": type,
            "from": {"data": "fields"},
            "encode": {
                "enter": {
                    "x": {"scale": "ord", "field": "data"},
                    "y": {
                        "scale": {"datum": "data"},
                        "field": {"parent": {
                            "datum": "data"
                         }}
                    },
                }
            }
        }
        if type == 'text':
            json['encode']['enter']['text'] = text()
            json['encode']['enter']['x']['offset'] = 4
        if type == 'line':
            json['encode']['enter'].update({
                "stroke": {"value": "red"},
                "strokeWidth": {"value": 1.01},
                "strokeOpacity": {"value": 1}
            })
        if type == 'symbol':
            json['encode']['enter']["stroke"] = {
                "value": "black"
            }
        return json

    def extra_marks():
        extra_marks = []
        if dim_labels:
            extra_marks.append(mark('text'))
        if dim_symbols:
            extra_marks.append(mark('symbol'))
        if dim_tooltips:
            if len(extra_marks) == 0:
                extra_marks.append(mark('path'))
            extra_marks[-1]['encode']['enter']["tooltip"] = full_text()
        return extra_marks

    json = {
        "$schema": "https://vega.github.io/schema/vega/v3.json",
        "width": 400,
        "height": 200,
        "padding": 5,
        "config": {
            "axisY": {
                "titleX": -5,
                "titleY": 205,
                "titleAngle": -30,
                "titleAlign": "right",
                "titleBaseline": "top"
            }
        },
        "data": [
            {
                "name": "main",
                "values": to_values(values_df)['values']
            },
            {
                "name": "fields",
                "values": list(heading_df.name)
            }
        ],
        "scales": [
            {
                "name": "ord",
                "type": "point",
                "range": "width",
                "domain": {
                    "data": "fields",
                    "field": "data"
                }
            }
        ] + [
            scale_of_row(row)
            for idx, row in heading_df.iterrows()
        ],
        "axes": [
            axis_of_row(row)
            for idx, row in heading_df.iterrows()
        ],
        "marks": [
            {
                "type": "group",
                "clip": {"path": "M -40 -20 H 500 V 220 H -40 Z"},
                "from": {"data": "main"},
                "marks": [mark("line")] + extra_marks()
            },
        ]
    }
    return json


def vega3_parplot_spec(results, problem, *args, **kwargs):
    if 'max_as_min' in kwargs:
        max_as_min = kwargs['max_as_min']
        del kwargs['max_as_min']
    else:
        max_as_min = True
    heading_df, values_df = prepare_dfs(results, problem, max_as_min=max_as_min)
    return vega3_parplot_df_spec(heading_df, values_df, *args, **kwargs)


def vega3_parplot(results, problem):
    """
    Plot a parallel cordinate plot of solutions using Altair and Vega 3.

    Parameters
    ----------
    results
        The solutions to plot.

    problem
        The DESDEO problem with which the plot is made with respect to.
    """

    import altair.vega.v3 as vg
    return vg.vega(vega3_parplot_spec(results, problem), validate=True)


def prepare_dfs(results, problem, max_as_min=True):
    import pandas as pd
    results = deepcopy(results)
    ideal = problem.ideal.copy()
    nadir = problem.nadir.copy()

    def adjust(arr):
        for max, (i, v) in zip(problem.maximized, enumerate(arr)):
            if not max:
                continue
            arr[i] = -v

    if not max_as_min:
        for rec in results:
            adjust(rec)
        adjust(ideal)
        adjust(nadir)

    return (
        pd.DataFrame({
            'name': problem.objectives,
            'ideal': ideal,
            'nadir': nadir
        }),
        pd.DataFrame.from_records(
            results,
            columns=problem.objectives,
        ),
    )
