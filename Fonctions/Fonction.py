from constante import constante_scrapeur
from os import path,listdir
from bs4 import BeautifulSoup
import requests
import pandas as pd
class FonctionsScrapeur():
    def __init__(self) -> None:
        self.CONSTANTE_PAGE_PRODUIT = constante_scrapeur.ConstClassPage_produit
        self.CONSTANTE_PAGE_PRINCIPAL = constante_scrapeur.ConstClassPage_principal
        self.CONSTANTE_URL = constante_scrapeur.ConstUrl
        
    
    
class gestion_de_fichier:
    def __init__(self) -> None:
        self.patch = path.join("fichier_sortie")
        self.nom_present_dossier_exporter = self.init_recuperation_list_fichier()
        
    def init_recuperation_list_fichier(self):
       return listdir("exporter")
        

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
        self.index_prix_quantiter_int = []
        self.dataframe = pd.read_csv(PatchFile.cellule_18650)
        self.utilisateur_voltage = 48
        self.capaciter_w = 1200
        self.utilisateur_courant_de_decharge_max = 30
        self.amperage_batterie = None
        self.calcule_amperage_batterie()
        self.conv_col_str_to_int()
        VOLTAGE_NOMINAL = 3,6
    
    def calcule_amperage_batterie(self):
         self.amperage_batterie = ceil(self.utilisateur_capaciter/self.utilisateur_voltage)
        
    def conv_col_str_to_int(self):
        index_prix_quantiter_str =  self.dataframe.columns
        for index in index_prix_quantiter_str:
            try:
                self.index_prix_quantiter_int.append(int(index))
            except:
                None
        self.index_prix_quantiter_int.sort()

    def conv_col_int_to_str(list_int):
        liste_str = []
        for element in list_int:
            liste_str.append(str(element))
        return liste_str

    def run_enrichissement_dataframe(self):