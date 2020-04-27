#coding:utf-8
import datetime
import os


def my_date() :

    date = datetime.datetime.now()
    date_clean = date.strftime("%d-%m-%Y")

    return date_clean

os.mkdir('source_' + my_date())

with open('leboncoin.csv', 'r+') as f:
    data = f.read()
    print(data)


nom_du_fichier = "source_" + my_date() +"/lbc_source_" + my_date() + ".csv"
with open(nom_du_fichier, "w") as f:
    f.write(data)
    f.close()









