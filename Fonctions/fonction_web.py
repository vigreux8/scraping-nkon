import streamlit as st
import pandas as pd
from constante.constante_scrapeur import PatchFile

st.title("hi see you lather")

df_cellule = pd.read_csv(PatchFile.cellule_18650) 
st.dataframe(df_cellule)
