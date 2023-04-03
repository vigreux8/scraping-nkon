class ConstUrl():
    NKON_18650 = "https://www.nkon.nl/fr/rechargeable/li-ion/18650-size/show/150.html"
    NKON_21700 = "https://www.nkon.nl/fr/rechargeable/li-ion/21700-20700-size.html"

class ConstClassPage_principal():
    GET_CONTENANT_LIST_PRODUIT  = ("div",{"class":"category-products"})
    GET_CONTENANT_PRODUIT_UNITER_INFO = ("h2",{"class":"product-name"})
    
    
#les get sont dans l'ordre du scraping
class ConstClassPage_produit():
    GET_NOM_PRODUIT = ("div",{"class":"product-name"})
    GET_TABLEAUX_RIGHT = ("div",{"class":"shop-content-right"})
    GET_DISPONIBILITER_EN_STOCK = ("p",{"class":"availability out-of-stock"})
    GET_DISPONIBILITER_HORS_STOCK = ("p",{"class":"availability in-stock"})
    GET_PRIX_COMMUN = ("span",{"class":"regular-price"})
    GET_PRIX_REMISE = ("ul",{"class":"tier-prices product-pricing"})
    GET_ALL_DESCRIPTION = ("li")
    GET_TABLEAUX_DESCRIPTION_PRODUIT = ("table",{"class":"data-table"})
    GET_ALL_DESCRIPTION = ("tr")
    GET_LABELS_FLOAT = ("Diamètre - mm","Poids - g","Taille de la batterie","Courant de décharge - A")
    
    
