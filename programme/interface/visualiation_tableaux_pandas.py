import sys
sys.path.append("programme")
import tkinter as tk
import pandas as pd
import numpy as np
import os



class creation_widjet_tableaux : 
    def __init__(self,df_pandas,fenetre) -> None:
        self.fenetre = fenetre
        self.df_pandas = df_pandas
        self.matrix_numpy = df_pandas.to_numpy()
        pass
    def afficher_tableaux(self):
        canvas = tk.Canvas(self.fenetre, width=200, height=100)
        canvas.pack()
        for i, row in enumerate(self.matrix_numpy):
            for j, value in enumerate(row):
                canvas.create_text(j*50+25, i*25+12.5, text=str(value))
# Créer un DataFrame pandas

# Créer une fenêtre tkinter

# Convertir le DataFrame en une matrice NumPy


# Créer un widget Canvas pour afficher la matrice


# Lancer la boucle principale tkinter


fenetre = tk.Tk()

chemins_fichier =  pd.read_csv(os.path.join("programme","fichier_sortie","fichier_7_21700.csv"))
tableaux =  creation_widjet_tableaux(chemins_fichier,fenetre)
tableaux.afficher_tableaux()

fenetre.mainloop()