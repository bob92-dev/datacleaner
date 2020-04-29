#!/usr/bin/python
# coding:utf-8

import datetime
import os
import csv
import shutil
import mail


def my_date():
    date = datetime.datetime.now()
    date_clean = date.strftime("%d-%m-%Y")
    return date_clean


def checkPrice(price):
    # price sous la forme [1234]
    #  print(price)
    S = price[1:-1]
    # print(S)
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


def comparingTo(liste_marques, cleaned_array):
    liste_marque_ok = []
    for marque in liste_marques:
        # print("Marques : " + marque)
        for annonce in cleaned_array:
            print("ANNONCES :" + annonce)
            if len(annonce) == 9:
                #  print("ANNONCES +len :" + annonce)
                url, id, publish_date, expiration_date, title, text, price, city, postal_code = annonce
                if (marque in title) or (marque in text):
                    liste_marque_ok.append(str(annonce))
    #  print(liste_marque_ok)
    return liste_marque_ok


def cleanerNew(fichier):
    with open(fichier, "r") as f:
        ma_liste_a_retourner = []
        ma_liste_pourrie = []
        reader = csv.reader(f)

        # On saute la première ligne
        next(reader)

        for line in reader:
            # print len(line)
            if len(line) == 9:
                # On récupère les 9 colonnes
                # Source Url,Id,Date Publication Annonce,Date Expiration Annonce,Titre,Texte Central,Prix,Ville,Code Postal
                url, id, publish_date, expiration_date, title, text, price, city, postal_code = line

                # On traite chaque colonne pour s'assurer qu'elles sont correctes

                checked_price = checkPrice(price)
                if checked_price is not None:
                    # print(" ici le checked price de la ligne 89" + str(checked_price))
                    ma_liste_a_retourner.append(str(line))


                else:
                    ma_liste_pourrie.append(str(line))
            else:
                print("erreur sur le nombre de colonnes")
        bad_data = "{}/{}_bad_data.csv".format(output_dir, file_prefix)

        with open(bad_data, "w") as bad:
            for item in ma_liste_pourrie:
                bad.write(item + '\n')
                # message="erreur lors du clean" + bad_data
            # mail.mailMe('boblepongedev92', 'casselboris92@gmail.com', 'boblepongedev92@gmail.com', 'spongebob;',
            #  'coucou', message, 'tapiecejointe.txt')

            bad.close()
        # print(type(ma_liste_a_retourner))
        return ma_liste_a_retourner


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

# on crée le fichier de travail
with open(lbc_price, "w") as f:
    cleaned_array = cleanerNew(input_file)
    # print(cleaned_array)
    maListefinale = comparingTo(createList("marques.csv"), cleaned_array)
    # print(maListefinale)
    for elem in maListefinale:
        # On saute une ligne entre chaque insertion
        f.write(elem + '\n')
    # print ("coucou f" + str(f))
    f.close()
