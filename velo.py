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
    S = price[1:-1]
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


def cleanerNew(fichier):
    with open(fichier, "r") as f:
        ma_liste_a_retourner = []
        ma_liste_pourrie = []
        reader = csv.reader(f)

        # On saute la première ligne
        next(reader)

        for line in reader:
            # TODO : Chaque ligne doit contenir 9 colonnes. Sinon on ne peut pas. Traiter l'erreur
            # print len(line)
            if len(line) == 9:
                print("it's ok")
                # On récupère les 9 colonnes
                # Source Url,Id,Date Publication Annonce,Date Expiration Annonce,Titre,Texte Central,Prix,Ville,Code Postal
                url, id, publish_date, expiration_date, title, text, price, city, postal_code = line
                # On traite chaque colonne pour s'assurer qu'elles sont correctes
                checked_price = checkPrice(price)
                if checked_price is not None:
                    print(checked_price)
                    ma_liste_a_retourner.append(str(line))


            else:
                ma_liste_pourrie.append(str(line))

            bad_data = "{}/{}_bad_data.csv".format(output_dir, file_prefix)
            with open(bad_data, "w") as bad:
                bad.write(str(ma_liste_pourrie))
                message="erreur lors du clean" + bad_data
                mail.mailMe('boblepongedev92', 'svenlehamster@gmail.com', 'boblepongedev92@gmail.com', 'spongebob;',
                       'coucou', message, 'tapiecejointe.txt')

                bad.close()

            return ma_liste_a_retourner

            # TODO : Si erreur, ça pourrait etre bien de créer une liste pour cela. On pourrait la mettre ensuite dans un fichier


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

# Traitement de la colonne prix
lbc_price = "{}/{}_lbc_price_ok.csv".format(output_dir, file_prefix)

with open(lbc_price, "w") as f:
    cleaned_array = cleanerNew(input_file)
    for elem in cleaned_array:
        # On saute une ligne entre chaque insertion
        f.write(elem + '\n')
    f.close()
