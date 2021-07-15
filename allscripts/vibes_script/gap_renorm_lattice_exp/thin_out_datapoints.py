#!/usr/bin/env python

from pathlib import Path
import click
import numpy as np


@click.command()
@click.argument("datafile", type=click.Path(exists=True))
@click.option("--stride", default=5, show_default=True, help="step length")
@click.option("-o", "--output", default="volume-temperature.dat", show_default=True)
def thin_out(datafile, stride, output):
    """Read DATAFILE, pick every STRIDE step and write to OUTPUT"""
    # read temperature-volume data
    data = np.loadtxt(datafile, comments="#", dtype=float)

    # thin out
    thinned_data = data[::stride]

    if Path(output).absolute() == Path(datafile).absolute():
        print(f"Designated output file `{output}` would overwrite input data. Check!")
    else:
        print(f"Save thinned out data to `{output}`.")
        np.savetxt(output, thinned_data)


if __name__ == "__main__":
    thin_out()
