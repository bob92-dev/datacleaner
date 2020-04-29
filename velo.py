#!/usr/bin/python
# coding:utf-8

import datetime
import os
import csv
import shutil
import mail
# TODO /: enlever les doublons => les doublons peuvent etre identifiés par l'id de l'annonce
# TODO : commenter le code

################################# FONCTIONS######################################################

        ######################### CREATION DATE###########################################@
def my_date():
    date = datetime.datetime.now()
    date_clean = date.strftime("%d-%m-%Y")
    return date_clean



######################### EXTRACTION DU FICHIER MARQUES ###########################################@

def createList(fichier):
    with open(fichier, "r") as f:
        liste_marques = []
        reader = csv.reader(f)

        next(reader)

        for line in reader:
            if len(line) == 2:
                marque, nbr_modele = line
                liste_marques.append(marque)

        print(liste_marques)
        return liste_marques

######################### VERIFICATION COHERENCE PRIX ###########################################@


def comparingTo(liste_marques, fichier_annonces):

     liste_marque_ok = []
     print(fichier_annonces)
     with open(fichier_annonces,"r") as liste_annonce:
        reader = csv.reader(liste_annonce)
        reader = list(reader)
        #print(reader)


        for marque in liste_marques:
                for annonce in reader:
                            if len(annonce) == 9:
                                url, id, publish_date, expiration_date, title, text, price, city, postal_code = annonce
                                if marque in title or marque in text:
                                    if marque in title or marque in text:
                                        liste_marque_ok.append(annonce)


        return liste_marque_ok


            ######################### VERIFICATION COHERENCE DES MARQUES  ###########################################@


def cleanerNew(fichier):
    with open(fichier, "r") as f:
        ma_liste_a_retourner = []
        ma_liste_pourrie = []
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
                    ma_liste_a_retourner.append(line)


                else:
                    ma_liste_pourrie.append(line)
            else:
                print("erreur sur le nombre de colonnes")
        bad_data = "{}/{}_bad_data.csv".format(output_dir, file_prefix)

        with open(bad_data, "w") as bad:
            badwriter =csv.writer(bad)
            for item in ma_liste_pourrie:
                badwriter.writerow(item)
                #message="erreur lors du clean" + bad_data
                #mail.mailMe('boblepongedev92', 'casselboris92@gmail.com', 'boblepongedev92@gmail.com', 'spongebob;',
                 #      'coucou', message, 'tapiecejointe.txt')

            bad.close()

        return ma_liste_a_retourner



                ######################### VERIFICATION COHERENCE DES PRIX ###########################################@

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

input_file = "leboncoin.csv"
output_dir = "source_" + my_date()
file_prefix = "lbc_source_" + my_date()

# Création répertoire de travail
path = "source_" + my_date() + "/lbc_source_" + my_date()
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


maListefinale = comparingTo(createList("marques.csv"),lbc_price)
with open ("fichierfinal.csv","w") as fichierfini:
    finalwriter = csv.writer(fichierfini)
    for item in maListefinale:
        finalwriter.writerow(item)
    fichierfini.close()
