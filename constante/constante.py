from os import path

class get_Parametre_par_defaut:
     D_EXPORTATION = "exporter"
     F_NOM_DEFAUT = "default.csv"
     elec_VOLTAGE = 48
     elec_PUISSANCE = 800
    
class get_SpecBatterie:
    VOLTAGE_NOMINAL = 3.6
    #VOLTAGE CONVENTIONNEL  = 36,48,52v

class get_ConstUrl():
    NKON_18650 = "https://www.nkon.nl/fr/rechargeable/li-ion/18650-size/show/150.html"
    NKON_21700 = "https://www.nkon.nl/fr/rechargeable/li-ion/21700-20700-size.html"

class get_ConstClassPage_principal():
    LIST_PRODUIT  = ("div",{"class":"category-products"})
    PRODUIT_UNITER_INFO = ("h2",{"class":"product-name"})
    
    
#les get sont dans l'ordre du scraping
class get_ConstClassPage_produit():
        NOM_PRODUIT = ("div",{"class":"product-name"})
        TABLEAUX_RIGHT = ("div",{"class":"shop-content-right"})
        DISPONIBILITER_EN_STOCK = ("p",{"class":"availability out-of-stock"})
        DISPONIBILITER_HORS_STOCK = ("p",{"class":"availability in-stock"})
        PRIX_COMMUN = ("span",{"class":"regular-price"})
        PRIX_REMISE = ("ul",{"class":"tier-prices product-pricing"})
        ALL_DESCRIPTION_remise = ("li")
        TABLEAUX_DESCRIPTION_PRODUIT = ("table",{"class":"data-table"})
        ALL_DESCRIPTION_produit = ("tr")
        LABELS_FLOAT = ("Diamètre - mm","Poids - g","Taille de la batterie","Courant de décharge - A")

class get_PatchFile:
    cellule_18650 = path.join(get_Parametre_par_defaut.D_EXPORTATION,get_Parametre_par_defaut.F_NOM_DEFAUT)