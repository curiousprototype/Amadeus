"""simple script with command line tools functionality to extract bandgaps"""
#!/usr/bin/env python

from pathlib import Path
import click
import pandas as pd


@click.command()
@click.argument("folders", nargs=-1, type=click.Path(exists=True), required=True)
@click.option("-o", "--output", default="bandgap_data.csv", show_default=True)
@click.option("--direct_bandgap", is_flag=True, show_default=True)
def parse(folders, output, direct_bandgap):
    """parse bandgaps from FOLDERS"""

    click.echo(f"Read bandgaps from these folder:")
    click.echo(f"  {folders}")
    # extract data and save as dictionary
    data = {}

    # run over all folders
    for folder in folders:
        # find all calculations in the folder
        files = sorted(Path().glob(f"{folder}/calculations/*/aims.out"))

        # extract bandgaps
        bandgaps = []
        for file in files:
            bandgap = get_bandgaps(file, direct=direct_bandgap)
            bandgaps.append(bandgap)

        # temperature
        temp = temperature_from_folder(folder)

        # add to dictionary
        data[temp] = bandgaps

    # convert to pandas dataframe, compute mean and standard deviation
    raw_data = pd.DataFrame(data)

    df = pd.DataFrame({"bandgap": raw_data.mean(), "err": raw_data.std()})
    # df.index.name = "Temperatures"

    # save to csv file
    df.to_csv(output, index_label="Temperature")
    click.echo(f"Data written to {output}")


def temperature_from_folder(folder):
    """convert folder name to temperature"""
    return float(Path(folder).name.rstrip("K"))


# Extract band gap from FHI-aims output:
def get_bandgaps(file="aims.out", direct=False):
    """extract homo-lumo gaps (direct & indirect) from aims output file"""
    with open(file) as f:
        direct_gap = None
        for line in f:
            # run until 'ESTIMATED overall HOMO-LUMO gap:' appears
            if "ESTIMATED overall HOMO-LUMO gap:" in line:
                # get the homo-lumo
                homo_lumo = float(line.split()[4])
            # get smalles direct gap
            if "Smallest direct gap" in line:
                direct_gap = float(line.split()[5])

    if direct:
        return direct_gap or homo_lumo
    return homo_lumo


if __name__ == "__main__":
    parse()


plot_style = {
    "linewidth": 2.5,
    "markersize": 10,
    "markeredgewidth": 3,
    "marker": "o",
    "markerfacecolor": "w",
    "capsize": 10,
}
