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


def comparingTo(liste_marques, fichier_annonces):

     liste_marque_ok = []
     with open(fichier_annonces,"r") as liste_annonce:
        reader = csv.reader(liste_annonce)
        reader = list(reader)
        #print(reader)
        for marque in liste_marques:
                for annonce in reader:
                        #print("annonce :" + annonce)
                        for col in annonce:
                            #print ("COL :" + col)
                            #print(type(col))
                            if marque in col:
                               #print("MARQUE IN COL LIGNE 59" + str(annonce) + "MARQUE TROUVEE : " + str(marque))
                               #print(col["id"])
                               liste_marque_ok.append(str(annonce))


#     print("LISTE ANNONCE \n" + str(liste_annonce))
#     print("LIST MARQUES \n " + str(liste_marques))
     #   print("LISTES MARQUES OK + APRES BOUCLE \n" + str(liste_marque_ok))
        return liste_marque_ok

def cleanerNew(fichier):
    with open(fichier, "r") as f:
        ma_liste_a_retourner = []
        ma_liste_pourrie = []
        reader = csv.reader(f)

        # On saute la première ligne
        #next(reader)

        for line in reader:
            # TODO : Chaque ligne doit contenir 9 colonnes. Sinon on ne peut pas. Traiter l'erreur
            # print len(line)
            if len(line) == 9:
       #         print("it's ok on est dans cleanernew ligne 79")
                # On récupère les 9 colonnes
                # Source Url,Id,Date Publication Annonce,Date Expiration Annonce,Titre,Texte Central,Prix,Ville,Code Postal
                url, id, publish_date, expiration_date, title, text, price, city, postal_code = line
                #print ("c'est lurl ligne 84" + url)
                #print("c'est l'id 84" + id)
                #print ("c'ets la ligne" + str(line))

                # On traite chaque colonne pour s'assurer qu'elles sont correctes
                checked_price = checkPrice(price)
                #print ("ici le checked price ligne 86" + checked_price)
                if checked_price is not None:
                   # print(" ici le checked price de la ligne 89" + str(checked_price))
                    ma_liste_a_retourner.append(str(line))


                else:
                    ma_liste_pourrie.append(str(line))

        bad_data = "{}/{}_bad_data.csv".format(output_dir, file_prefix)

        with open(bad_data, "w") as bad:
                bad.write(str(ma_liste_pourrie))
                message="erreur lors du clean" + bad_data
                mail.mailMe('boblepongedev92', 'casselboris92@gmail.com', 'boblepongedev92@gmail.com', 'spongebob;',
                       'coucou', message, 'tapiecejointe.txt')

                bad.close()
        #f.close()
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


print ("voici le lien du LBC price ligne 129" + lbc_price)

with open(lbc_price, "w") as f:
    cleaned_array = cleanerNew(input_file)
    print(type(cleaned_array))
    print ("coucou cleaned array" + str(cleaned_array))
    for elem in cleaned_array:
       # On saute une ligne entre chaque insertion
       f.write(elem + '\n')
   # print ("coucou f" + str(f))
    f.close()

maListefinale = comparingTo(createList("marques.csv"),lbc_price)
print(str(maListefinale))
with open ("fichierfinal.csv","w") as fichierfini:
    for item in maListefinale:
                fichierfini.write(item + '\n')
    fichierfini.close()
