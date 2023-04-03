import sys
# sys.path.append("programme")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import parametre.parametre_scrapeur as nkp
from os import path
from parametre import *
log = False

class ScrapeurNkon():
    def __init__(self) -> None:
        
        pass

def log_tchek(texte):
    if log:
        print(texte)

nkon_18650 = "https://www.nkon.nl/fr/rechargeable/li-ion/18650-size/show/150.html"
nkon_21700 ="https://www.nkon.nl/fr/rechargeable/li-ion/21700-20700-size.html"

def get_html(liens):
    lien_convertie = BeautifulSoup(liens.content, "html.parser")
    return lien_convertie

def convert_devise_to_float(contenue):
    contenue = float(contenue.replace("€","").replace("\xa0","").replace("\n","").replace(",",".").strip())
    return contenue

def get_nkon_page_info(url):
    #variable_déclaration
    tableaux_cellule = pd.DataFrame()
    loc_index = 0
    list_information_produit = []
    
    cellule_uniter = []
    index_loc = 0
    url = requests.get(url)
    #programme
    if url.status_code == 200:
        nkon = get_html(url)
        div = nkon.find("div",{"class":"category-products"})
        ul = div.find_all("li")
        nb_cellule = 0
        for h2 in ul:
            cellule_uniter = []
            cellule_get_info = h2.find("h2",{"class":"product-name"})
            cellule_get_link = h2.find("a")
            tableaux_cellule.at[index_loc,"nom"] = cellule_get_link['title']
            cellule_uniter.append(cellule_get_link['title'])
            
            tableaux_cellule.at[index_loc,"liens"] = cellule_get_link['href']
            cellule_uniter.append(cellule_get_link['href'])
            url_produit = requests.get(cellule_get_link['href'])
            
            #page produit
            
            if url_produit.status_code == 200:
                page_information_produit = get_html(url_produit)
                page_descriptif_produit = page_information_produit
                
                #page_information_produit = get_html(requests.get("https://www.nkon.nl/fr/rechargeable/li-ion/18650-size/sanyo-ncr18650ga-3350mah-10a-groen.html"))
                page_information_produit = page_information_produit.find("div",{"class":"shop-content-right"})
                #recuperais la disponibiliter
                if tableaux_cellule.at[index_loc,"nom"] == "/":
                    try: 
                        tableaux_cellule.at[index_loc,"nom"] =page_descriptif_produit.find("div",{"class":"product-name"}).find("h1").text
                    except:
                         tableaux_cellule.at[index_loc,"nom"] = None
                    
                try : 
                    disponibiliter = page_information_produit.find("p",{"class":"availability out-of-stock"}).find("span").text.strip()
                    disponibiliter = False
                except AttributeError:
                    try :
                        disponibiliter = page_information_produit.find("p",{"class":"availability in-stock"}).find("span").text.strip()
                        disponibiliter = True
                        cellule_uniter.append(disponibiliter)
                    except:
                        log_tchek("balise_disponibilliter introuvable")
                        disponibiliter = None
                        cellule_uniter.append(None)
                tableaux_cellule.at[index_loc,"disponibiliter"] = disponibiliter
                cellule_uniter.append(None)
                    
                #récuperais prix commun :
                try : 
                    prix_regulier =  page_information_produit.find("span",{"class":"regular-price"})
                    tableaux_cellule.at[index_loc,"prix_regulier"] = convert_devise_to_float(prix_regulier.text)
                    cellule_uniter.append(prix_regulier.text)
                    
                except AttributeError:
                    print("prix inconnue")
                    prix_regulier = None
                    tableaux_cellule.at[index_loc,"prix_regulier"] = prix_regulier
                    cellule_uniter.append(prix_regulier)
                
                # récuperais le prix selon les quantiter
                try:
                    page_prix_quantiter = page_information_produit.find("ul",{"class":"tier-prices product-pricing"}).find_all("li")
                    prix_and_quantiter =[]
                    tableaux_cellule.at[index_loc,"remis_aditionnelle"] =True
                    
                    # index quantiter index = 1 , prix 3 
                    for prix in page_prix_quantiter:
                        quantiter_index = 1
                        prix_index = 3
                        liste_element = prix.text.strip().split(" ")
                        tableaux_cellule.at[index_loc,liste_element[quantiter_index]] = convert_devise_to_float(liste_element[prix_index])
                        prix_and_quantiter = [[liste_element[quantiter_index],liste_element[prix_index]]]
                        cellule_uniter.append(prix_and_quantiter)
                except:
                    log_tchek("pas de remise aditionnelle")
                    cellule_uniter.append(None)
                    tableaux_cellule.at[index_loc,"remis_aditionnelle"] =False
                
                #recuperais info général produit 
                try: 
                    #on récupere tout les tr 
                    #crée une boucle pour lire tout les tr 
                    #on récupere le "label" et "data last"
                    tr_all = page_descriptif_produit.find("table",{"class":"data-table"}).find_all("tr")
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
                        cellule_uniter.append([labels,data_labels])
                        tableaux_cellule.at[index_loc,labels] = data_labels
                except:
                  print("balise detaille introuvable") 
                list_information_produit.append(cellule_uniter)
                log_tchek(cellule_uniter)
            else:
                print("La requête a échoué avec le code d'erreur", url.status_code)
            index_loc +=1
            #Testeur
            #if index_loc == 3:
    else:
        print("La requête a échoué avec le code d'erreur", url.status_code)
    
    return list_information_produit,tableaux_cellule

list,df =  get_nkon_page_info(nkon_21700)
#print(info)

#rajouter la même date a chaque fichier 
#crée un system pour comparer 2 tableaux "en excluant les date" si table1== table2 == False : crée une fonction pour savoir ou se trouve la différence
print(df.columns)
df.to_csv(path.join("programme","fichier_sortie","fichier_7_21700.csv") , index=False)


