#!/usr/bin/python
# coding:utf-8

import datetime
import os
import csv
import shutil
import mail
# TODO : commenter le code
# TODO : ajouter dans les fichiers de sortie, la premiere ligne du fichier initial qui contient le nom des col

################################# FONCTIONS######################################################


        ######################### CREATION DATE###########################################@
"""
function that returns the current date with a particular format
"""
def my_date():
    date = datetime.datetime.now()
    date_clean = date.strftime("%d-%m-%Y")
    return date_clean



######################### EXTRACTION DU FICHIER MARQUES ###########################################@
"""
function that take a file as a parameter, retrieves its content and return it in the form of a list
"""
def createList(file):
    with open(file, "r") as f:
        brands_list = []
        reader = csv.reader(f)

        next(reader)

        for line in reader:
            if len(line) == 2:
                brand, nbr_modele = line
                brands_list.append(brand)

        print(brands_list)
        return brands_list

######################### VERIFICATION COHERENCE PRIX ###########################################@
"""
function that takes two parameters, one list and one file,
 search in the file for existing entries from the list,
 and add theses to a new list,
 check for the duplicates,
 returns this new list
"""

def comparingTo(brands_list, ad_file):


     brands_list_temporary = []
     print(ad_file)
     with open(ad_file, "r") as ad_list:
        reader = csv.reader(ad_list)
        reader = list(reader)
        #print(reader)


        for brand in brands_list:
                for ad in reader:
                            if len(ad) == 9:
                                url, id, publish_date, expiration_date, title, text, price, city, postal_code = ad
                                if brand in title or brand in text:
                                    if brand in title or brand in text:
                                            brands_list_temporary.append(ad)

                brands_list_ok = []
                for i in brands_list_temporary:
                    if i not in brands_list_ok:
                        brands_list_ok.append(i)

        brands_list_ok.insert(0,list(first_line))
        return brands_list_ok


            ######################### VERIFICATION COHERENCE DES MARQUES  ###########################################@

"""
function that take a file as a parameter, retrieves its content , 
verify that certain characteristics are respected,
if they are, adds them to a list,
returns this list
"""
def cleanerNew(file):
    with open(file, "r") as f:
        good_list = []
        bad_list = []
        reader = csv.reader(f)

        # On saute la première ligne
        next(reader)

        for line in reader:
            if len(line) == 9:


                # On récupère les 9 colonnes
                # Source Url,Id,Date Publication Annonce,Date Expiration Annonce,Titre,Texte Central,Prix,Ville,Code Postal
                url, id, publish_date, expiration_date, title, text, price, city, postal_code = line


                # On traite chaque colonne pour s'assurer qu'elles sont correctes
                checked_price = checkPrice(price)
                #print ("ici le checked price ligne 86" + checked_price)

                if checked_price is not None:
                    good_list.append(line)



                else:
                    bad_list.append(line)
            else:
                print("erreur sur le nombre de colonnes")
        bad_data = "{}/{}_bad_data.csv".format(output_dir, file_prefix)

        with open(bad_data, "w") as bad:
            badwriter =csv.writer(bad)
            for item in bad_list:
                badwriter.writerow(item)
                #message="erreur lors du clean" + bad_data
                #mail.mailMe('boblepongedev92', 'casselboris92@gmail.com', 'boblepongedev92@gmail.com', 'spongebob;',
                 #      'coucou', message, 'tapiecejointe.txt')

            bad.close()


        return good_list



                ######################### VERIFICATION COHERENCE DES PRIX ###########################################@
"""
function that takes a string as parameter,
slice it and cast it into an integer,
and verifies the consistency of the data
return the integer
"""
def checkPrice(price):
    # price sous la forme [1234]
    print(price)
    S = price[1:-1]
    print(S)
    try:
        priceInt = int(S)
    except:
        print("price format error : '{}'".format(price))
        return None

    if priceInt > 99 and priceInt < 8000:
        return priceInt
    else:
        print("price format outbound")
        return None



######################### LANCEMENT DU SCRIPT  ###########################################@


    ######################### CREATION DU REPERTOIRE DESTINATION DES FICHIERS ###########################################@

my_path = os.getcwd()
input_file = my_path +"/leboncoin.csv"
output_dir = "source_" + my_date()
file_prefix = "lbc_source_" + my_date()

# Création répertoire de travail
path = my_path + "source_" + my_date() + "/lbc_source_" + my_date()
try:
    os.mkdir(output_dir)
    print("Create directory source_{}".format(output_dir))
except:
    print("Use existing directory source_{}".format(my_date()))

# Backup du fichier d'entrée dans le répertoire de travail (avant de commencer à jouer avec)
shutil.copy2(input_file, "{}/{}_backup.csv".format(output_dir, file_prefix))

# Traitement de la colonne prix => fichier recevant
lbc_price = "{}/{}_lbc_price_ok.csv".format(output_dir, file_prefix)

######################### STOCKAGE DES DONNES NETTOYEES  ###########################################@


with open(lbc_price, "w") as f:
    cleaned_array = cleanerNew(input_file)
    my_writer = csv.writer(f)
    for elem in cleaned_array:
        my_writer.writerow(elem)
      # ancienne formule =>  f.write(elem + '\n')
    f.close()


final_list = comparingTo(createList("marques.csv"), lbc_price)
with open ("fichierfinal.csv","w") as final_file:
    finalwriter = csv.writer(final_file)
    for item in final_list:
        finalwriter.writerow(item)
    final_file.close()
