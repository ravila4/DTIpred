# Download data
python src/data/fetch_chembl.py GPCRs 4
python src/data/fetch_chembl.py ion-channels 4
python src/data/fetch_chembl.py kinases 4
python src/data/fetch_chembl.py receptors 4

./src/data/get_sequences.sh GPCRs
./src/data/get_sequences.sh ion-channels
./src/data/get_sequences.sh kinases
./src/data/get_sequences.sh receptors

# Generate features
python ./src/features/get_unique_ligs.py
