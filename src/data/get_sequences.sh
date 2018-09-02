#! /bin/bash

#==============================================================#
#  Script for downloading fasta sequences for proteins.        #
#  Downloads data from UNIPROT, given a protein's UNIPROT id.  #
#                                                              #
#  Usage: ./get_sequences.sh RECEPTOR_TYPE                     #
#  RECEPTOR_TYPE is one of: GPCRs, ion-channels, kinases,      #
#  or nuclear-receptors.                                       #
#==============================================================#

if [ $# -eq 0 ]; then
    echo "No arguments provided."
    echo "Usage: $0 RECEPTOR_TYPE"
    exit 1
fi

# Get directory containing current script
pushd `dirname $0` > /dev/null
# Get directory contatining receptor ids
pushd ../../data/02_receptor_ids/ > /dev/null
DATADIR=`pwd`
popd > /dev/null
# Get output directory
pushd ../../data/04_sequences/ > /dev/null
OUTDIR=`pwd`
popd > /dev/null
# Return to initial directory
popd > /dev/null

# Extract list of protein IDs
ids=`tail -n+2 ${DATADIR}/${1}.csv | awk -F "," '{print $2}'`

# Create output directory, if it doesn't exist
if [ ! -d ${OUTDIR}/$1 ]; then
  mkdir -p ${OUTDIR}/$1
fi


echo "Downloading sequences."
BASEPATH="https://www.uniprot.org/uniprot"

pushd ${OUTDIR}/$1 > /dev/null

for id in $ids; do
    wget ${BASEPATH}/${id}.fasta
done

popd > /dev/null
echo "Done."
