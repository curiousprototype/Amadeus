#!/usr/bin/env python

from glob import glob
from pathlib import Path
import click
import numpy as np
from preprocess import _datafile, _geometry, _type


@click.command()
@click.argument("workdir", type=_type)
@click.option("--datafile", default=_datafile, show_default=True, type=_type)
@click.option("--geometry", default=_geometry, show_default=True, type=_type)
@click.option("--output", default="bandgaps.dat", show_default=True)
def postprocess(workdir, datafile, geometry, output):
    """read bandgaps from computations in WORKDIR and write to OUTPUT."""

    # read temperature-volume data
    file = Path(workdir) / datafile
    data = np.loadtxt(file, comments="#", dtype=float)

    # use glob to find all output files
    output_files = sorted(glob(f"{workdir}/T_?????/aims/calculations/aims.out"))

    # read the bandgaps and save the temperatures
    bandgaps = []
    temperatures = []
    for file in output_files:
        print(f"Parse {file}")
        try:
            bandgaps.append(get_bandgap(file))
            temperatures.append(float(file.split("_")[1].split("/")[0]))
        except FileNotFoundError:
            print(f"{file} not found, not computed?")
            exit()

    # sort temperatures and bandgaps (just to be sure)
    temperatures, bandgaps = zip(*sorted(zip(temperatures, bandgaps)))

    # write the bandgaps
    print(f"Write bandgaps to {output}")
    with open(output, "w") as f:
        f.write("# Temp [K] bandgap [eV] Volume [AA^3]\n")
        for ((temp, vol), gap) in zip(data, bandgaps):
            if gap:
                f.write(f"{temp:8.1f} {gap:15.10f} {vol:10.5f}\n")


# Helper file to extract band gap from FHI-aims output:
def get_bandgap(file="aims.out"):
    """read aims output file and grep for the bandgap"""
    gap = None
    with open(file) as f:
        # run until '"Band gap" of total set of bands:' appears in output:
        for line in f:
            if '"Band gap" of total set of bands:' in line:
                break

        # grep the energy difference there
        for line in f:
            if "| Energy difference      :" in line:
                gap = float(line.split()[4])

    return gap


if __name__ == "__main__":
    postprocess()
