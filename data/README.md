# Data used in this project

## 01_pharos_raw_data
Receptor data dump from Pharos. Contains:
 - target ids
 - uniprot keywords
 - publication PubMed IDs
 - pathways
 - Go germs
 - expression

## 02_receptor_ids
Contains Uniprot ids and gene names for receptors from the four major classes of druggable proteins: GPCRs, kinases, ion channels, and nuclear hormone receptors. The data was downloaded from [Pharos](https://pharos.nih.gov), and the receptors were filtered to include only those within the **Tclin** and **Tchem** categories, meaning that they have a sufficient number of known interacting compounds.

## 03_ligand_smiles
Contains the ligand id, SMILES string, and binding affinity for each ligand associated with every protein, retreived from ChEBML database.

## 04_sequences
Contains target sequences, downloaded from [UniProt](http://www.uniprot.org/).

## 05_mol2vec
Containes processed vector embeddings for ligands.

## 06_prot2vec
Contains processeed vector embeddings for proteins.
