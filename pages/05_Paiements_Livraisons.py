import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Paiement et Livraison", page_icon="💳", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre de la page
styled_title("💳 Analyse des Paiements et Livraisons")

# Filtres globaux dans la sidebar
with st.sidebar:
    st.markdown("""
        <div class='sidebar-header'>
            <h3>Filtres Globaux</h3>
        </div>
    """, unsafe_allow_html=True)
    
    selected_category = st.multiselect(
        "Catégorie de Produits",
        options=df['Category'].unique(),
        default=df['Category'].unique()
    )

    selected_season = st.multiselect(
        "Saison",
        options=df['Season'].unique(),
        default=df['Season'].unique()
    )

# Filtrage des données
df_filtered = df[
    (df['Category'].isin(selected_category)) &
    (df['Season'].isin(selected_season))
]

# Métriques clés
with styled_container():
    col1, col2 = st.columns(2)
    with col1:
        payment_method = df_filtered['Payment Method'].mode().iloc[0] if not df_filtered.empty else "N/A"
        st.metric("Moyen de Paiement Préféré", payment_method)
    with col2:
        shipping_type = df_filtered['Shipping Type'].mode().iloc[0] if not df_filtered.empty else "N/A"
        st.metric("Type de Livraison Préféré", shipping_type)

# Analyse des modes de paiement
styled_subheader("💳 Analyse des Paiements")
with styled_container():
    col1, col2 = st.columns(2)

    with col1:
        payment_dist = df_filtered['Payment Method'].value_counts().reset_index()
        payment_dist.columns = ['Payment Method', 'Count']
        fig_payment = px.pie(
            payment_dist,
            values='Count',
            names='Payment Method',
            title='Répartition des Moyens de Paiement',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_payment.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_payment, use_container_width=True, key="payment_pie")

    with col2:
        shipping_dist = df_filtered['Shipping Type'].value_counts().reset_index()
        shipping_dist.columns = ['Shipping Type', 'Count']
        fig_shipping = px.pie(
            shipping_dist,
            values='Count',
            names='Shipping Type',
            title='Répartition des Types de Livraison',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_shipping.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_shipping, use_container_width=True, key="shipping_pie")

# Analyse des montants d'achat
styled_subheader("💵 Analyse des Montants d'Achat")
with styled_container():
    # Relation entre montant d'achat et mode de livraison
    shipping_purchase = df_filtered.groupby('Shipping Type')['Purchase Amount (USD)'].mean().reset_index()
    fig_shipping_purchase = px.bar(
        shipping_purchase,
        x='Shipping Type',
        y='Purchase Amount (USD)',
        title='Montant Moyen d\'Achat par Type de Livraison',
        color='Shipping Type',
        color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
    )
    fig_shipping_purchase.update_layout(
        showlegend=False,
        margin=dict(t=30, l=0, r=0, b=0),
        xaxis_title="Type de Livraison",
        yaxis_title="Montant Moyen d'Achat (USD)"
    )
    st.plotly_chart(fig_shipping_purchase, use_container_width=True, key="shipping_purchase_bar")

    # Relation entre montant d'achat et moyen de paiement
    payment_purchase = df_filtered.groupby('Payment Method')['Purchase Amount (USD)'].mean().reset_index()
    fig_payment_purchase = px.bar(
        payment_purchase,
        x='Payment Method',
        y='Purchase Amount (USD)',
        title='Montant Moyen d\'Achat par Moyen de Paiement',
        color='Payment Method',
        color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
    )
    fig_payment_purchase.update_layout(
        showlegend=False,
        margin=dict(t=30, l=0, r=0, b=0),
        xaxis_title="Moyen de Paiement",
        yaxis_title="Montant Moyen d'Achat (USD)"
    )
    st.plotly_chart(fig_payment_purchase, use_container_width=True, key="payment_purchase_bar")