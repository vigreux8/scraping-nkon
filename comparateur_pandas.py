import pandas as pd
from math import ceil

fichier_1 = pd.read_csv("fichier_3.csv")
fichier_2 = pd.read_csv("fichier_4.csv")

pd.set_option("display.max_colwidth",None)

#print(fichier_1 == fichier_2)
différence_1 =  fichier_1.compare(fichier_2)
différence_2 =  fichier_2.compare(fichier_1)
#print(différence.index)
print(fichier_1.loc[1,["disponibiliter"]])
print(fichier_2.loc[1,["disponibiliter"]])

#------- Log et donner de modification sur le site-----# 
#on enregistre les changements dans un log avec la date, | l'index | le nom, et l'élément changer (avant et apres)
#on modifie la base de donner actuels avec la date du dernier changements

#---on utilise la fonction comparer pour repérer les changements 
#---on doit repérer les compte a rebours qui se mette a jour pour ne pas les inclures dans les changements 

#--------utisation des donner et fonctionnaliter---
#---utilisateur : cm² ou mm² , voltage, capaciter, épaisseur, circonférence support cellul / option --> batterie le plus : petit | moins chers | cellule de marque | plus légers | toujours trier par prix et indiquer les économie d'acheter en gros
#--- programme : /
# calculer une surface pie*racine² = 
#incorporer les cellule dans le volume si possible 
#sinon indiquer le volume manquant  ou le maximum de cellule dans se volume

voltage_utilisateur = 48
capaciter_utilisateur = 22*1000

voltage_nominal = 3.6
capaciter = 3200
poids_g = 48
prix_normale =  3.62
prix_reduit_100 = 2.70
frais_de_transport = 14

nb_serie = voltage_utilisateur/voltage_nominal
nb_parralele = capaciter_utilisateur/capaciter

nb_cellule = ceil((nb_serie*nb_parralele))

cout_total = nb_cellule*prix_normale


poids_batterie = poids_g*nb_cellule/1000

si_prix_reduit = 100*prix_reduit_100 


print("vous avez de besoins de :",nb_cellule)
print("la batterie ferat :",poids_batterie,"kg")
print("cout total")

#regarde toute les remise en quantiter et comparer les prix entre tous
if si_prix_reduit <= cout_total:
    print(f"Si vous commander {100-nb_cellule} en plus le prix est de: {si_prix_reduit} au lieux de {cout_total} la différence et de : {round(si_prix_reduit-cout_total)} euro")
