"""Script for generating a merged data frame of all unique ligands across all
receptor types. Necessary prior to featurization.

Usage
-----
python get_unique_ligs.py
"""

import glob

import pandas as pd
from pathlib import Path


def find_unique(folder):
    """Returns a dictionary of unique ligands for all targets in a class.
    Parameters
    ----------
    folder: (str) A path to a folder with csv files containing ligand data.
    """
    data = glob.glob(folder + "/*.csv")
    if len(data) == 0:
        print("No ligand files found.")
        return
    ligs = pd.DataFrame()
    for receptor in data:
        temp_df = pd.read_csv(receptor).iloc[:, 1:3]
        ligs = pd.concat([ligs, temp_df], axis=0)
    ligs = ligs.drop_duplicates(['molecule_chembl_id'])
    return ligs


if __name__ == '__main__':
    project_dir = Path(__file__).resolve().parents[2]
    output_dir = str(project_dir) + "/data/05_mol2vec"

    # Initialize data frame to store unique ligands
    types = ["GPCRs", "kinases", "ion-channels", "nuclear-hormone-receptors"]
    all_ligs = pd.DataFrame()
    
    for item in types:
        print("Joining ligands for", item)
        data_dir = str(project_dir) + "/data/03_ligand_smiles/" + item
        results = find_unique(data_dir)
        if results is not None:
            all_ligs = pd.concat([all_ligs, results], axis=0)
            all_ligs = all_ligs.drop_duplicates(['molecule_chembl_id'])
        print("Number of unique ligands:", len(all_ligs))

    print("Done. Saving data to csv.")
    all_ligs.to_csv(output_dir + "/all_unique_ligands.csv", index=False)
