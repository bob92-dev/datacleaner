#!/bin/bash

ref_file=$1
input_dir=$2

# Tri du fichier orignal par ordre alphabetique (sort)
# On ne prend pas en compte la première ligne qui contient les noms des colonnes
cat $ref_file |tail -n+1 |sort > ${ref_file}_sorted.csv

# Récupération de la première ligne
first_line=$(cat $ref_file | head -1)

# Tri des fichiers bad_data + lbc_price_ok
sort ${input_dir}/bad_data.csv > ${ref_file}_bad_data_sorted.csv
sort ${input_dir}/lbc_price_ok.csv > ${ref_file}_lbc_price_ok_sorted.csv

# Concaténation et tri de : la première ligne et des fichiers bad_data + lbc_price_ok
echo $first_line > ${ref_file}_shoudBeEqual.csv
cat ${input_dir}/bad_data.csv ${input_dir}/lbc_price_ok.csv |sort >> ${ref_file}_shoudBeEqual.csv

# Les fichiers doivent etre identiques apres reconstitution
diff ${ref_file}_sorted.csv ${ref_file}_shoudBeEqual.csv
if [ $? -ne 0 ]; then
    echo "Des lignes ont été perdues"
    exit 1
fi

echo "OK"
exit 0