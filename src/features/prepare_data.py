# This script concatenates an array of drug features to an array of
# receptor features

import glob
import numpy as np
import pickle
import pandas as pd
from tqdm import tqdm


# Load drug vectors
def drug_vecs():
    drug_vecs = pickle.load(open("vectors.pkl", 'rb'))
    print("Storing drug vectors")
    drugs = interactions['ligand']
    X_drugs = drug_vecs.loc[drugs]
    print("Drug features shape:", X_drugs.shape)
    return X_drugs


# Load receptor vectors
def receptor_vecs():
    receptor_vecs = pd.read_csv("all_receptor_vecs.csv", index_col=0)
    print("Storing receptor vectors")
    receptors = interactions['receptor']
    X_receptors = receptor_vecs.loc[receptors]
    print("Receptor features shape:", X_receptors.shape)
    return X_receptors


if __name__ == "__main__":
    # Read data of receptor ids
    receptor_data = glob.glob("receptor_ids/*.csv")
    cols = ["Uniprot ID", "GeneSymbol"]
    receptor_ids = pd.DataFrame(columns=cols)

    for f in receptor_data:
        data = pd.read_csv(f)
        receptor_ids = pd.concat([receptor_ids, data], axis=0)

    all_files = glob.glob("ligands/*/*.csv")
    cols = ["receptor", "ligand", "affinity"]
    interactions = pd.DataFrame(columns=cols)

    # Open each ligand file and store the receptor, ligands and activity
    print("Storing interactions")
    for f in tqdm(all_files[:300]):
        temp_df = pd.DataFrame(columns=cols)
        receptor = f.replace("_ligands.csv", "").split("/")[-1]
        r_id = receptor_ids.loc[receptor_ids.GeneSymbol == receptor]['Uniprot ID']
        ligfile = pd.read_csv(f)
        num_ligands = ligfile.shape[0]
        ligs = ligfile['molecule_chembl_id']
        affinities = ligfile['pchembl_value']
        temp_df['receptor'] = np.full(num_ligands, r_id)
        temp_df['ligand'] = ligs
        temp_df['affinity'] = affinities
        interactions = pd.concat([interactions, temp_df], axis=0)
    # Drop NAs
    interactions = interactions.dropna()
    interactions.to_csv("interactions.csv")
    print("Interactions:", interactions.shape)

    X_drugs = drug_vecs()
    X_receptors = receptor_vecs()

    # Combine features
    X = np.concatenate([X_receptors, X_drugs], axis=1)
    print("All features shape:", X.shape)

    # Extract values
    Y = np.array(interactions['affinity'])
    print("Y values shape:", Y.shape)

    # Save 
    print("Pickling")
    pickle.dump(X, open("X_features.pkl", 'wb'))
    pickle.dump(Y, open("Y_values.pkl", 'wb'))
    print("Saving to file")
    np.savetxt("X_features.csv", X, delimiter=",")
    np.savetxt("Y_values.csv", Y, delimiter=",")
