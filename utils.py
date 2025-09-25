import streamlit as st

# Application du CSS personnalisé dans toutes les pages
def load_css():
    with open('style.css') as f:
        return st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction pour créer un conteneur stylisé
def styled_container():
    return st.container()

# Fonction pour créer un titre stylisé
def styled_title(text):
    return st.markdown(f'<h1 class="stTitle">{text}</h1>', unsafe_allow_html=True)

# Fonction pour créer un sous-titre stylisé
def styled_subheader(text):
    return st.markdown(f'<h3 class="stSubheader">{text}</h3>', unsafe_allow_html=True)