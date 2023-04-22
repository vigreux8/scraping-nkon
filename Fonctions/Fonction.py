from constante.constante import (
    get_PatchFile,
    get_ConstClassPage_principal,
    get_ConstClassPage_produit,
    get_ConstUrl,
    get_Parametre_par_defaut,
    get_SpecBatterie)
from os import path,listdir
from bs4 import BeautifulSoup
import requests
import pandas as pd
from math import ceil
import streamlit as st


class FonctionsScrapeur():
    def __init__(self) -> None:
        self.CONSTANTE_PAGE_PRODUIT = get_ConstClassPage_produit
        self.CONSTANTE_PAGE_PRINCIPAL = get_ConstClassPage_principal
        self.CONSTANTE_URL = get_ConstUrl
         
class gestion_de_fichier:
    def __init__(self) -> None:
        self.nom_present_dossier_exporter = self.init_recuperation_list_fichier()
        self.fichier_present_exporter = self.init_recuperation_list_fichier()
             
    def init_recuperation_list_fichier(self):
        listdir(get_Parametre_par_defaut.D_EXPORTATION)
        
    def Patch_constructeur(self):
        path.join(get_Parametre_par_defaut.D_EXPORTATION,self.fichier_present_exporter)
        
class RunScrapingNkon():
    def __init__(self) -> None:
        self.fonction = FonctionsScrapeur()
        self.page_princiaple = self.fonction.CONSTANTE_PAGE_PRINCIPAL
        self.page_produit = self.fonction.CONSTANTE_PAGE_PRODUIT
        self.tableaux_cellule = pd.DataFrame()
        self.loc_index = 0
        self.list_information_produit = []
        self.cellule_uniter = []
        self.index_loc = 0
        self.url = requests.get(self.fonction.CONSTANTE_URL.NKON_18650)
        self.url_produit = None
        self.log = False
    
    def log_tchek(self,texte):
        if self.log:
            print(texte)
    
    def get_html(self,liens):
        lien_convertie = BeautifulSoup(liens.content, "html.parser")
        return lien_convertie
    
    def convert_devise_to_float(self,contenue):
        contenue = float(contenue.replace("€","").replace("\xa0","").replace("\n","").replace(",",".").strip())
        return contenue
    
    def get_page_principale_produit(self):
        if self.url.status_code == 200:
            nkon = self.get_html(self.url)
            div = nkon.find(*self.page_princiaple.LIST_PRODUIT)
            ul = div.find_all("li")
            nb_cellule = 0
            for h2 in ul:
                cellule_uniter = []
                cellule_get_info = h2.find(*self.page_princiaple.PRODUIT_UNITER_INFO)
                cellule_get_link = h2.find("a")
                self.tableaux_cellule.at[self.index_loc,"nom"] = cellule_get_link['title']
                cellule_uniter.append(cellule_get_link['title'])
                self.tableaux_cellule.at[self.index_loc,"liens"] = cellule_get_link['href']
                cellule_uniter.append(cellule_get_link['href'])
                self.url_produit = requests.get(cellule_get_link['href'])
                self.get_page_produit()
        else:
            print("La requête a échoué avec le code d'erreur", self.url.status_code)
            
            #page produit
    
    def get_page_produit(self):
            if self.url_produit.status_code == 200:
                page_information_produit = self.get_html(self.url_produit)
                page_descriptif_produit = page_information_produit
                
                #page_information_produit = get_html(requests.get("https://www.nkon.nl/fr/rechargeable/li-ion/18650-size/sanyo-ncr18650ga-3350mah-10a-groen.html"))
                page_information_produit = page_information_produit.find(*self.page_produit.TABLEAUX_RIGHT)
                
                #recuperais la disponibiliter (certain non pas le nom qui s'affiche correctement a partir de la page produit)
                if self.tableaux_cellule.at[self.index_loc,"nom"] == "/":
                    try: 
                        self.tableaux_cellule.at[self.index_loc,"nom"] =page_descriptif_produit.find(*self.page_produit.NOM_PRODUIT).find("h1").text
                    except:
                         self.tableaux_cellule.at[self.index_loc,"nom"] = None
                    
                try : 
                    disponibiliter = page_information_produit.find(*self.page_produit.DISPONIBILITER_HORS_STOCK).find("span").text.strip()
                    disponibiliter = False
                except AttributeError:
                    try :
                        disponibiliter = page_information_produit.find(*self.page_produit.DISPONIBILITER_EN_STOCK).find("span").text.strip()
                        disponibiliter = True
                        self.cellule_uniter.append(disponibiliter)
                    except:
                        self.log_tchek("balise_disponibilliter introuvable")
                        disponibiliter = None
                        self.cellule_uniter.append(None)
                self.tableaux_cellule.at[self.index_loc,"disponibiliter"] = disponibiliter
                self.cellule_uniter.append(None)
                    
                #récuperais prix commun :
                try : 
                    prix_regulier =  page_information_produit.find(*self.page_produit.PRIX_COMMUN)
                    self.tableaux_cellule.at[self.index_loc,"prix_regulier"] = self.convert_devise_to_float(prix_regulier.text)
                    self.cellule_uniter.append(prix_regulier.text)
                    
                except AttributeError:
                    print("prix inconnue")
                    prix_regulier = None
                    self.tableaux_cellule.at[self.index_loc,"prix_regulier"] = prix_regulier
                    self.cellule_uniter.append(prix_regulier)
                
                # récuperais le prix selon les quantiter
                try:
                    page_prix_quantiter = page_information_produit.find(*self.page_produit.PRIX_REMISE).find_all("li")
                    prix_and_quantiter =[]
                    self.tableaux_cellule.at[self.index_loc,"remis_aditionnelle"] =True
                    
                    # index quantiter index = 1 , prix 3 
                    for prix in page_prix_quantiter:
                        quantiter_index = 1
                        prix_index = 3
                        liste_element = prix.text.strip().split(" ")
                        self.tableaux_cellule.at[self.index_loc,liste_element[quantiter_index]] = self.convert_devise_to_float(liste_element[prix_index])
                        prix_and_quantiter = [[liste_element[quantiter_index],liste_element[prix_index]]]
                        self.cellule_uniter.append(prix_and_quantiter)
                except:
                    self.log_tchek("pas de remise aditionnelle")
                    self.cellule_uniter.append(None)
                    self.tableaux_cellule.at[self.index_loc,"remis_aditionnelle"] =False
                
                #recuperais info général produit 
                try: 
                    #on récupere tout les tr 
                    #crée une boucle pour lire tout les tr 
                    #on récupere le "label" et "data last"
                    tr_all = page_descriptif_produit.find(*self.page_produit.TABLEAUX_DESCRIPTION_PRODUIT).find_all("tr")
                    for tr in tr_all:
                        
                        labels = tr.find("th").text
                        data_labels = tr.find("td").text.replace("\xa0","")
                        if labels == "Min. capacité - mAh":
                            labels = "capaciter_ah"
                            data_labels = round(float(data_labels.replace(",",".").replace(" ","").replace("\xa0",""))/1000,ndigits=2)
                        elif labels =="Diamètre - mm" or labels =="Poids - g" or labels =="Taille de la batterie" or labels =="Courant de décharge - A":
                            data_labels = float(data_labels.replace(",","."))
                        elif labels =="Tension nominale":
                            print(float(data_labels.replace(",",".").replace("V","")))
                            data_labels = float(data_labels.replace(",",".").replace("V",""))
                        self.cellule_uniter.append([labels,data_labels])
                        self.tableaux_cellule.at[self.index_loc,labels] = data_labels
                except:
                  print("balise detaille introuvable") 
                self.list_information_produit.append(self.cellule_uniter)
                self.log_tchek(self.cellule_uniter)
            else:
                print("La requête a échoué avec le code d'erreur", self.url.status_code)
            self.up_index_loc()
    
    def up_index_loc(self):
        self.index_loc +=1
    
    def export_csv(self):
        self.tableaux_cellule.to_csv(path.join("exporter","fichier_18650_Nkon.csv") , index=False)     
    
    def run_scrapts(self):
        self.get_page_principale_produit()
        self.tableaux_cellule.to_csv()
        self.export_csv()

class NkonEnrichissementData:
    def __init__(self) -> None:
        self.choix_amperage_batterie = None
        self.index_ligne = []
        self.index_reduction_on =[]
        self.index_prix_quantiter_int = []
        self.df_enrichie = None
        self.choix_voltage = None
        self.choix_capaciter_w = None
        self.choix_limite_surface_cm_carres = None
        self.choix_limite_ah_max_min = None
        self.choix_limite_nb_pile = None
        self.init_streamlit_composant()
        self.df_origine = pd.read_csv(get_PatchFile.cellule_18650)
        self.init_calcule_amperage_batterie()
        self.choix_courant_Decharge_max = 30
        self.add_enrichissement_dataframe()
        self.filtre()
    
    def filtre(self):
        self.df_enrichie = self.df_origine[["reduction","prix_total","nb_cellule","Ah_max","poids_kg","tension_nominale_total","nb_parallele","nb_serie","nom","liens"]].copy()
        self.df_enrichie = self.df_enrichie.dropna(subset="prix_total")
        self.filtre_avancer(self.df_enrichie,"nb_cellule",self.choix_limite_nb_pile,"le nombre de cellule minimum et de")
        self.filtre_avancer(self.df_enrichie,"Ah_max",self.choix_limite_ah_max_min,"la capaciter minimum en ah possible est de",limite_superieur=False)
        
        
        
        
    def filtre_avancer(self,df_save,nom_colonne,limite,phrase,limite_superieur=True):
        df_save = df_save.copy()
        if self.filtre_actif(limite):
            if limite_superieur:
                self.df_enrichie = self.df_enrichie.drop(self.df_enrichie[self.df_enrichie[nom_colonne] > limite].index)
            else : 
                self.df_enrichie = self.df_enrichie.drop(self.df_enrichie[self.df_enrichie[nom_colonne] < limite].index)
                
            if self.df_enrichie.shape[0] == 0:
                id_min = df_save[nom_colonne].idxmin()
                st.write(id_min)
                valeur_minimum = df_save.loc[id_min,nom_colonne]
                st.write(f"{phrase} {valeur_minimum}")
            
    
    def init_calcule_amperage_batterie(self):
         self.choix_amperage_batterie = ceil(self.choix_capaciter_w/self.choix_voltage)
   

    @staticmethod
    def filtre_actif(filtre):
        if filtre == 0 :
            return False
        else : 
            return True
   
    def init_streamlit_composant(self):
        self.choix_voltage =  st.slider(
            "voltage",
            get_SpecBatterie.VOLTAGE_NOMINAL,
            200.0,
            on_change=self.add_enrichissement_dataframe,
            value=get_Parametre_par_defaut.elec_VOLTAGE,
            step=1.0)

        self.choix_capaciter_w=  st.slider(
            "watt",
            0,
            5000,
            value=get_Parametre_par_defaut.elec_PUISSANCE,
            on_change=self.add_enrichissement_dataframe)
        
        self.choix_limite_surface_cm_carres = st.number_input("limite en cm²",step=1)
        self.choix_limite_ah_max_min = st.number_input("Puissance AH minimum",step=1)
        self.choix_limite_nb_pile = st.number_input("Pile maximum",step=1)
        
        
                     
    def index_str_to_int(self,df):
        index_prix_quantiter_int = []
        index_prix_quantiter_str =  df.index
        for index in index_prix_quantiter_str:
            try:
                index_prix_quantiter_int.append(int(index))
            except:
                None
        index_prix_quantiter_int.sort()
        return index_prix_quantiter_int

    def conv_col_int_to_str(list_int):
        liste_str = []
        for element in list_int:
            liste_str.append(str(element))
        return liste_str
    
    def add_enrichissement_dataframe(self):
        # print(self.index_prix_quantiter_int)
        # print(self.choix_voltage,self.choix_amperage_batterie,self.choix_courant_Decharge_max)
        # print(type(self.choix_amperage_batterie))
        self.df_origine["nb_parallele"] = self.df_origine["capaciter_ah"].apply(lambda capaciter_ah: ceil(self.choix_amperage_batterie/capaciter_ah))
        self.df_origine["nb_serie"] = self.df_origine["Tension_nominale"].apply(lambda tension_nominal: round(self.choix_voltage /tension_nominal))
        self.df_origine["tension_nominale_total"] = self.df_origine["nb_serie"]*self.df_origine["Tension_nominale"]
        self.df_origine["capaciter_total"] =self.df_origine["tension_nominale_total"]*self.choix_amperage_batterie
        self.df_origine["nb_cellule"] = self.df_origine["nb_parallele"]*self.df_origine["nb_serie"]
        self.df_origine["poids_kg"] = (self.df_origine["nb_cellule"]*self.df_origine["Poids - g"])/1000
        self.df_origine["Ah_max"] = self.df_origine["Courant de décharge - A"]*self.df_origine["nb_parallele"]
        
        self.prix_calculator()
    
    def detectors_quantiter_reduction(self,cellule):
        index_ligne = self.index_str_to_int(cellule)
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
    
    def prix_calculator(self):
        tour_de_boucle = 0
        self.df_origine["prix_total"] = 0
        self.df_origine["reduction"] = False
        for i in range(len(self.df_origine)):
            print(tour_de_boucle)
            tour_de_boucle +=1
            cellule =  self.df_origine.loc[i]
            print(isinstance(cellule, pd.Series))
            cellule.index
            cellule =  self.df_origine.loc[i][self.df_origine.loc[i].notna()]
            index_valide = self.detectors_quantiter_reduction(cellule)
            print("index valide:",index_valide)
            self.df_origine["prix_total"].loc[i] = self.df_origine[index_valide].loc[i]*self.df_origine["nb_cellule"].loc[i]
            if index_valide != "prix_regulier":
                self.df_origine["reduction"].loc[i] = True
    
    def new_dataframe(self):
        
        pass


class interface_utilisateur(NkonEnrichissementData):
    
    def run_streamlit(self):
        st.title("Tableaux cellule lithium")
        st.dataframe(self.df_enrichie)
        st.write(self.df_origine.columns)