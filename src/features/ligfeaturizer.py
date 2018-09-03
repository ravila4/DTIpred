"""Generate ligand features by applying a mol2vec representation model.
References
----------
Mol2vec: Unsupervised Machine Learning Approach with Chemical Intuition

Usage
-----
python ligfeaturizer.py
"""


import numpy as np
import pandas as pd
from pathlib import Path
import pickle
from rdkit import Chem
from mol2vec.features import mol2alt_sentence
from gensim.models import word2vec
from tqdm import tqdm


def featurize(ligand_data, trained_model, outpath):
    """Generate features from mol2vec model.
    Parameters
    ----------
    ligand_data: (str) A path to a csv file containing ligand structure data.
    trained_model: (str) Path to a pickle file of a trained word2vec model.
    outpath: (str) Path for storing output files.
    """
    data = pd.read_csv(ligand_data)
    # Create new column to store fingerprints
    data['words'] = np.zeros(len(data), dtype='object')

    # Read chemical structures
    ligands = (Chem.MolFromSmiles(x) for x in data['canonical_smiles'])

    # Generate fingerprints
    print("Generating molecular fingerprints.")
    i = 0
    with tqdm(total=len(data)) as pbar:
        for l in ligands:
            fingerprint = mol2alt_sentence(l, 1)
            data['words'][i] = list(fingerprint)
            i += 1
            pbar.update()
    pickle.dump(data, open("fingerprints.pkl", 'wb'))

    print("Finding unique fingerprints.")
    all_words = np.array(
            [word for sentence in data['words'] for word in sentence])
    unique_words = np.unique(all_words)

    # Create a data frame of embeddings
    print("Storing embeddings.")
    model = word2vec.Word2Vec.load('model_300dim.pkl')
    embeddings = {}
    for word in unique_words:
        try:
            embeddings[word] = model.wv.word_vec(word)
        except:
            embeddings[word] = np.zeros(300)
    embeddings = pd.DataFrame(embeddings)
    pickle.dump(embeddings, open("embeddings.pkl", 'wb'))

    # Create a data frame to store ligand vectors
    vectors = {}
    print("Generating vectors.")
    for mol in tqdm(data['molecule_chembl_id']):
        fingerprint = data.loc[data.molecule_chembl_id == mol]['words']
        for sentence in fingerprint:
            components = embeddings[sentence]
            vec = np.sum(components, axis=1)
        vectors[mol] = vec
    vectors = pd.DataFrame(vectors).T

    print("Writing csv file.")
    pickle.dump(vectors, open("vectors.pkl", 'wb'))
    vectors.to_csv("ligand_vectors.csv")


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[2]
    data_file = str(project_dir) + "/data/05_mol2vec/all_unique_ligands.csv"
    output_dir = str(project_dir) + "/data/05_mol2vec"
    trained_model = project_dir + "/src/features/model_300dim.pkl"
    featurize(data_file, output_dir)
