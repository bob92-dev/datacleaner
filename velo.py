# coding:utf-8
import datetime
import os
import csv


def my_date():
    date = datetime.datetime.now()
    date_clean = date.strftime("%d-%m-%Y")

    return date_clean


def checkPrice(price):
    priceInt = int(price)
    if priceInt > 99 and priceInt < 8000:
        return priceInt
    else:
        print("error data")


def cleaner(fichier):
    with open(fichier, "r") as f:
        ma_liste_a_retourner=[]
        for line in f.readlines():
            linebis = line.split(',')
            for i in linebis:
                if str.__contains__(i, "[") == True:
                    S = i[1:-1]
                    if S.isdigit():
                        schecked = checkPrice(S)
                        if schecked != "error data" and schecked!="None":
                            ma_liste_a_retourner.append(line)

    print(ma_liste_a_retourner)
    return ma_liste_a_retourner

                        
path = "source_" + my_date() + "/lbc_source_" + my_date()

os.mkdir('source_' + my_date())

with open('leboncoin.csv', 'r+') as f:
    data = f.read()
    # print(data)

nom_du_fichier = path + ".csv"
with open(nom_du_fichier, "w") as f:
    f.write(data)
    f.close()

lbc_price = path + "lbc_price_ok.csv"
with open(lbc_price, "w") as csv:
    csv.write(str(cleaner(nom_du_fichier)))
    csv.close()