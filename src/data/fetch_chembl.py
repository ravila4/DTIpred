"""Script that downloads ligand and bioactivity data for the receptors.
Usage
-----
python fetch_chembl.py RECEPTOR_TYPE N_PROCS

Arguments
---------
RECEPTOR_TYPE: one of 'GPCRs', 'ion-channels', 'kinases', or
               'nuclear-receptors'
N_PROCS: number of processes - may speed up processing, but data download may
         be limited by network speed.

Example
-------
python fetch_chembl.py GPCRs 2
"""

from multiprocessing import Pool
import os
import sys

from chembl_webresource_client.new_client import new_client
import pandas as pd
from pathlib import Path
from tqdm import tqdm


def fetch_ligs(gene_id):
    """Fetch a gene's ligands and their bioactivity from the ChEMBL database.
    Writes a csv file for each gene.
    Parameters
    ----------
    gene: (str) A gene id. e.g. 'Q99788'
    """
    target = new_client.target
    activity = new_client.activity
    res = target.filter(target_synonym__icontains=gene_id)
    # Initialize empty data frame
    columns = ['molecule_chembl_id', 'canonical_smiles', 'pchembl_value']
    compounds = pd.DataFrame(columns=columns)
    try:
        t = res[0]['target_chembl_id']
        assays = activity.filter(target_chembl_id=t)
        # Store all activity assays in data frame
        compounds = pd.DataFrame(list(assays))
        compounds = compounds[columns]
        compounds.pchembl_value = compounds.pchembl_value.apply(
                pd.to_numeric, errors='coerce')
        # Remove duplicates and filter out missing values
        compounds = compounds.drop_duplicates(['molecule_chembl_id'])
        compounds = compounds.dropna()
    except:
        pass  # No ligands found
    # Save to csv
    compounds.to_csv(output_path + gene_id + "_ligands.csv")


if __name__ == "__main__":
    rtype = sys.argv[1]
    n_procs = int(sys.argv[2])

    print()

    # Find project directory
    project_dir = Path(__file__).resolve().parents[2]

    input_file = str(project_dir) + "/data/02_receptor_ids/" + rtype + ".csv"
    output_path = str(project_dir) + "/data/03_ligand_smiles/" + rtype + "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
 
    # Fetch compounds
    gene_names = pd.read_csv(input_file).iloc[:, 1]
    pool = Pool(processes=n_procs)
    num_jobs = len(gene_names)
    print("Downloading ligands for", rtype)
    with tqdm(total=num_jobs) as pbar:
        for i, _ in tqdm(enumerate(
                         pool.imap_unordered(fetch_ligs, gene_names))):
            pbar.update()
