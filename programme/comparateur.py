import pandas as pd
from math import ceil,pi,floor


index_prix_quantiter_int = []
def conv_col_str_to_int():
    index_prix_quantiter_str =  df_cellule_general.columns
    for index in index_prix_quantiter_str:
        try:
            index_prix_quantiter_int.append(int(index))
        except:
            None
    index_prix_quantiter_int.sort()

def conv_col_int_to_str(list_int):
    liste_str = []
    for element in list_int:
        liste_str.append(str(element))
    return liste_str


df_cellule_general = pd.read_csv("fichier_5.csv")
pd.options.display.max_colwidth = 1000
VOLTAGE_NOMINAL = 3,6

def utilisateur() :
    utilisateur_voltage = int(input("donner un voltage voulue:"))
    utilisateur_capaciter = int(input("donner une capaciter en watt voulue:"))
    utilisateur_courant_de_decharge_max = int(input("Donner une capaciter de décharge maximum:"))
    amperage_batterie = ceil(utilisateur_capaciter/utilisateur_voltage)
    return utilisateur_voltage,amperage_batterie,utilisateur_courant_de_decharge_max



conv_col_str_to_int()

print(index_prix_quantiter_int)
utilisateur_voltage,amperage_batterie,utilisateur_courant_de_decharge_max= utilisateur()
print(utilisateur_voltage,amperage_batterie,utilisateur_courant_de_decharge_max)
print(type(amperage_batterie))
df_cellule_general["nb_parallele"] = df_cellule_general["capaciter_ah"].apply(lambda capaciter_ah: ceil(amperage_batterie/capaciter_ah))
df_cellule_general["nb_serie"] = df_cellule_general["Tension nominale"].apply(lambda tension_nominal: round(utilisateur_voltage/tension_nominal))
df_cellule_general["nb_cellule"] = df_cellule_general["nb_parallele"]*df_cellule_general["nb_serie"]
print(df_cellule_general.loc[df_cellule_general["nb_cellule"].idxmin()])
#calculer le prix selon la quantiter 
#repérer si la quantiter e.t egal l'une des colonne 
#convertir tout les colonne 50 en int dans l'ordre et les reconvertir en str 

            
            

#calculer le prix si remise et quantiter pile-10 >= quantiter_minimums.