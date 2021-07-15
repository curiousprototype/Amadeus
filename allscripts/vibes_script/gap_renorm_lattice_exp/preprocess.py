#!/usr/bin/env python

import shutil
from pathlib import Path
from ase.io import read
import click
import numpy as np

_type = click.Path(exists=True)
_datafile = "volume-temperature.dat"
_geometry = "geometry.in"
_workdir = "working"


@click.command()
@click.argument("datafile", type=_type)
@click.option("--geometry", default=_geometry, show_default=True, type=_type)
@click.option("--workdir", default=_workdir, show_default=True)
@click.option("--aimsin", default="aims.in", show_default=True, type=_type)
@click.option("--format", default="aims", show_default=True)
def preprocess(datafile, geometry, workdir, aimsin, format):
    """Create structures with volumes accoding to temperature-vol. data in DATAFILE

    conversion from volume to lattice parameter:

        i) convert to volume of conventional cell (*4)

        ii) go to lattice paramter (cubic root)
    """

    # read input
    structure = read(geometry, format=format)

    # read temperature-volume data
    data = np.loadtxt(datafile, comments="#", dtype=float)

    # set up the folders for each temperature
    workdir = Path(workdir)
    for temp, volume in data:
        folder = workdir / f"T_{temp:05.1f}"
        # write control.in
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            print(f"{folder} created")
        else:
            print(f"{folder} already exists, skip.")
            continue
        shutil.copy(aimsin, folder / aimsin)

        # copy and scale the volume of the structure to match with the volume
        # at the particular temperature
        scaled_structure = structure.copy()
        scale = (volume / scaled_structure.get_volume()) ** (1 / 3)
        scaled_structure.set_cell(scaled_structure.cell * scale, scale_atoms=True)

        scaled_structure.write(folder / geometry, format=format, scaled=True)

    # save the temp-vol data
    print(f"Copy datafile `{datafile}` to working directory `{workdir}`")
    shutil.copy(datafile, Path(workdir) / _datafile)


if __name__ == "__main__":
    preprocess()
