#!/usr/bin/python
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator


def matplotlib_parplot(data_sets, min_max=None, style=None):
    # Based on https://stackoverflow.com/questions/8230638/parallel-coordinates-plot-in-matplotlib
    dims = len(data_sets[0])
    x = range(dims)
    fig, axes = plt.subplots(1, dims - 1, sharey=False)

    if style is None:
        style = ["r-"] * len(data_sets)

    # Calculate the limits on the data
    min_max_range = []
    if min_max is None:
        for m in zip(*data_sets):
            mn = min(m)
            mx = max(m)
            if mn == mx:
                mn -= 0.5
                mx = mn + 1.
            r = float(mx - mn)
            min_max_range.append((mn, mx, r))
    else:
        for mn, mx in min_max:
            r = float(mx - mn)
            min_max_range.append((mn, mx, r))

    # Normalize the data sets
    norm_data_sets = list()
    for ds in data_sets:
        nds = [
            (value - min_max_range[dimension][0]) / min_max_range[dimension][2]
            for dimension, value in enumerate(ds)
        ]
        norm_data_sets.append(nds)
    data_sets = norm_data_sets

    # Plot the datasets on all the subplots
    for i, ax in enumerate(axes):
        for dsi, d in enumerate(data_sets):
            ax.plot(x, d, style[dsi])
        ax.set_xlim([x[i], x[i + 1]])

    # Set the x axis ticks
    for dimension, (axx, xx) in enumerate(zip(axes, x[:-1])):
        axx.xaxis.set_major_locator(ticker.FixedLocator([xx]))
        ticks = len(axx.get_yticklabels())
        labels = list()
        step = min_max_range[dimension][2] / (ticks - 1)
        mn = min_max_range[dimension][0]
        for i in range(ticks):
            v = mn + i * step
            labels.append("%4.2f" % v)
        axx.set_yticklabels(labels)

    # Move the final axis' ticks to the right-hand side
    axx = plt.twinx(axes[-1])
    dimension += 1
    axx.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
    ticks = len(axx.get_yticklabels())
    step = min_max_range[dimension][2] / (ticks - 1)
    mn = min_max_range[dimension][0]
    labels = ["%4.2f" % (mn + i * step) for i in range(ticks)]
    axx.set_yticklabels(labels)

    # Stack the subplots
    plt.subplots_adjust(wspace=0)

    return fig


def parplot_results_matplotlib(results, problem):
    return matplotlib_parplot(results, zip(problem.ideal, problem.nadir))


def matplotlib_parplot2():
    # XXX: Unfinished
    # This one is the most promising for use with mpld3
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    # vectors to plot: 4D for this example
    y1 = [1, 2.3, 8.0, 2.5]
    y2 = [1.5, 1.7, 2.2, 2.9]

    x = [1, 2, 3, 8]  # spines

    fig, (ax, ax2, ax3) = plt.subplots(1, 3, sharey=False)

    # plot the same on all the subplots
    ax.plot(x, y1, "r-", x, y2, "b-")
    ax2.plot(x, y1, "r-", x, y2, "b-")
    ax3.plot(x, y1, "r-", x, y2, "b-")

    # now zoom in each of the subplots
    ax.set_xlim([x[0], x[1]])
    ax2.set_xlim([x[1], x[2]])
    ax3.set_xlim([x[2], x[3]])

    # set the x axis ticks
    for axx, xx in zip([ax, ax2, ax3], x[:-1]):
        axx.xaxis.set_major_locator(ticker.FixedLocator([xx]))
    ax3.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))  # the last one

    # EDIT: add the labels to the rightmost spine
    for tick in ax3.yaxis.get_major_ticks():
        tick.label2On = True

    # stack the subplots together
    plt.subplots_adjust(wspace=0)

    plt.show()


def altair_parplot(results, problem):
    # XXX: Unfinished
    # https://altair-viz.github.io/user_guide/compound_charts.html#advanced-compound-charts-and-data-specification
    # https://vega.github.io/vega/examples/parallel-coordinates/
    from functools import reduce
    import altair as alt
    #min_max = zip(problem.ideal, problem.nadir)
    data_sets = prepare_df(results, problem)
    charts = []
    for idx, row in data_sets.iterrows():
        df = row.to_frame().T
        chart = alt.Chart(df).mark_circle().encode(
            x='name:Q',
            y='value:Q',
        )
        charts.append(chart)

    return reduce(lambda a, b: a + b, charts)


def ticks(vmin, vmax):
    nbins = 9
    steps = [1, 2, 2.5, 5, 10]
    locator = MaxNLocator(
        nbins=nbins,
        steps=steps,
        prune='both')
    return locator.tick_values(vmin, vmax)


def vega3_parplot(
        heading_df,
        values_df,
        custom_axis_values=True,
        dim_labels=True,
        dim_tooltips=False,
        dim_symbols=False):
    # Based on https://vega.github.io/vega/examples/parallel-coordinates/
    from altair.vega.data import to_values

    def scale_of_row(row):
        return {
            "name": row['name'],
            "type": "linear",
            "range": "height",
            "zero": False,
            "domain": [row['ideal'], row['nadir']],
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
            tick_vals = list(ticks(row['ideal'], row['nadir']))
            json['values'] = (
                [row['ideal']]
                + tick_vals
                + [row['nadir']])
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


def parplot_results_vega3(results, problem, *args, **kwargs):
    return vega3_parplot(*(prepare_dfs(results, problem) + args), **kwargs)


def prepare_dfs(results, problem):
    import pandas as pd
    return (
        pd.DataFrame({
            'name': problem.objectives,
            'ideal': problem.ideal,
            'nadir': problem.nadir
        }),
        pd.DataFrame.from_records(
            results,
            columns=problem.objectives,
        ),
    )
