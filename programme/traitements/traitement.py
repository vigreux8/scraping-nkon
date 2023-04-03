import sys
sys.path.append("programme")
import pandas as pd 
from math import ceil,pi,floor
import os
df_cellule_general = pd.read_csv(os.path.join("programme","fichier_sortie","fichier_7_21700.csv"))

def index_str_to_int(df):
    index_prix_quantiter_int = []
    index_prix_quantiter_str =  df.index
    for index in index_prix_quantiter_str:
        try:
            index_prix_quantiter_int.append(int(index))
        except:
            None
    index_prix_quantiter_int.sort()
    return index_prix_quantiter_int
    
def detectors_quantiter_reduction(cellule):
    index_ligne = index_str_to_int(cellule)
    print("salut:",len(index_ligne))
    nombre_cellule = cellule["nb_cellule"]
    int_index_quantiter_eligible = 0
    str_index_quantiter_eligible = "prix_regulier"
    if len(index_ligne) == 1:
         if index_ligne < nombre_cellule:
                str_index_quantiter_eligible = str(index_ligne[0])
                return str_index_quantiter_eligible
    else:
        for i in index_ligne:
            if i < nombre_cellule:
                int_index_quantiter_eligible = i
            else:
                str_index_quantiter_eligible = str(int_index_quantiter_eligible)
                if str_index_quantiter_eligible == "0":
                    print(index_ligne)
                    str_index_quantiter_eligible = "prix_regulier"
    return str_index_quantiter_eligible

def prix_calculator():
    tour_de_boucle = 0
    df_cellule_general["prix_total"] = 0
    df_cellule_general["reduction"] = False
    for i in range(len(df_cellule_general)):
        print(tour_de_boucle)
        tour_de_boucle +=1
        cellule =  df_cellule_general.loc[i]
        print(isinstance(cellule, pd.Series))
        cellule.index
        cellule =  df_cellule_general.loc[i][df_cellule_general.loc[i].notna()]
        index_valide = detectors_quantiter_reduction(cellule)
        print("index valide:",index_valide)
        df_cellule_general["prix_total"].loc[i] = df_cellule_general[index_valide].loc[i]*df_cellule_general["nb_cellule"].loc[i]
        if index_valide != "prix_regulier":
            df_cellule_general["reduction"].loc[i] = True

    
VOLTAGE_NOMINAL = 3,6


#utilisateur_parametre pour calculer
utilisateur_voltage = 48
utilisateur_capaciter = 800
amperage_batterie = ceil(utilisateur_capaciter/utilisateur_voltage)

#option de trie : 
utilisateur_courant_de_decharge_max_ampere = 30
surface_diponible_cm_carres =  30000/100
separateur_cellule_surface_mm = 5
option_trie=[["puissance_max_A",utilisateur_courant_de_decharge_max_ampere],["cm²_par_cellule_avec_separateur",surface_diponible_cm_carres]]


df_cellule_general["nb_parallele"] = df_cellule_general["capaciter_ah"].apply(lambda capaciter_ah: ceil(amperage_batterie/capaciter_ah))
df_cellule_general["nb_serie"] = df_cellule_general["Tension nominale"].apply(lambda tension_nominal: round(utilisateur_voltage/tension_nominal))
df_cellule_general["tension_nominale_total"] = df_cellule_general["nb_serie"]*df_cellule_general["Tension nominale"]
df_cellule_general["capaciter_total"] =df_cellule_general["tension_nominale_total"]*amperage_batterie

df_cellule_general["nb_cellule"] = df_cellule_general["nb_parallele"]*df_cellule_general["nb_serie"]
#recuperer la colonne non nul
    
prix_calculator()
#calcule surface que la pile_seul a besoins
df_cellule_general["cm²_par_cellule"] =((df_cellule_general["Diamètre - mm"]/2)**2*pi)/100
df_cellule_general["cm²_total_sans_separateur"] = df_cellule_general["cm²_par_cellule"]*df_cellule_general["nb_cellule"]

#surface que la pile a besoins si séparateur
df_cellule_general["cm²_par_cellule_avec_separateur"] =(((df_cellule_general["Diamètre - mm"]+separateur_cellule_surface_mm*2)/2)**2*pi)/100
df_cellule_general["cm²_total_avec_separateur"] = df_cellule_general["cm²_par_cellule_avec_separateur"]*df_cellule_general["nb_cellule"]

#puissance_maximal de la batterie
df_cellule_general["puissance_max_A"] = df_cellule_general["Courant de décharge - A"]*df_cellule_general["nb_parallele"]
df_cellule_general["puissance_max_W"] = df_cellule_general["puissance_max_A"]*df_cellule_general["tension_nominale_total"]

df_cellule_general["poid_total_kg"] = (df_cellule_general["nb_cellule"]*df_cellule_general["Poids - g"])/1000
df_cellule_general

df_cellule_disponible = df_cellule_general[["nom","reduction","liens","Diamètre - mm","Hauteur - mm","nb_serie","nb_parallele","tension_nominale_total","capaciter_ah","capaciter_total","nb_cellule","prix_total","cm²_total_sans_separateur","cm²_total_avec_separateur","puissance_max_A","puissance_max_W","poid_total_kg"]][df_cellule_general["disponibiliter"]]

df_cellule_disponible.to_csv(os.path.join("programme","fichier_sortie","fichier_7_21700_48_800w.csv"))