"""script to run all aims calculations in the directories created from preprocess.py"""
#!/usr/bin/env python

import time
from glob import glob
import subprocess as sp
import click


@click.command()
@click.argument("workdir")
@click.option("--logfile", default="run.log", show_default=True)
def run(workdir, logfile):
    """run calculations in WORKDIR"""

    workdirs = sorted(glob(f"{workdir}/T_?????"))

    stime = time.time()
    for fol in workdirs:
        print()
        print(f"Compute folder {fol}:")

        # run and pipe to output file
        with open(logfile, "a") as f:
            f.write(f"\n{fol}\n")
            sp.run(f"vibes run singlepoint".split(), cwd=fol, stdout=f)

        print(f".. time elapsed: {time.time() -stime:.2f}s")


if __name__ == "__main__":
    run()
