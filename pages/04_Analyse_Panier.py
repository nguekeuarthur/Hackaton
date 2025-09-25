import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Analyse Panier", page_icon="🛒", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre de la page
styled_title("🛒 Analyse du Panier")

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
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_basket = df_filtered['Purchase Amount (USD)'].mean()
        st.metric("Panier Moyen", f"${avg_basket:,.2f}")
    
    with col2:
        total_sales = df_filtered['Purchase Amount (USD)'].sum()
        st.metric("Ventes Totales", f"${total_sales:,.2f}")
    
    with col3:
        max_basket = df_filtered['Purchase Amount (USD)'].max()
        st.metric("Panier Maximum", f"${max_basket:,.2f}")

# Analyse du panier par catégorie
styled_subheader("📊 Performance par Catégorie")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des montants d'achat par catégorie
        fig_amount_dist = px.box(
            df_filtered,
            x='Category',
            y='Purchase Amount (USD)',
            title='Distribution des Montants par Catégorie',
            color='Category',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_amount_dist.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_amount_dist, use_container_width=True)

    with col2:
        # Montant moyen par catégorie
        avg_amount = df_filtered.groupby('Category')['Purchase Amount (USD)'].mean().reset_index()
        avg_amount.columns = ['Catégorie', 'Montant Moyen']
        fig_avg_amount = px.bar(
            avg_amount,
            x='Catégorie',
            y='Montant Moyen',
            title='Montant Moyen par Catégorie',
            color='Catégorie',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_avg_amount.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_avg_amount, use_container_width=True)

# Analyse des fréquences d'achat
styled_subheader("🔄 Fréquence d'Achat")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des fréquences d'achat
        freq_dist = df_filtered['Frequency of Purchases'].value_counts().reset_index()
        freq_dist.columns = ['Fréquence', 'Nombre']
        fig_freq = px.pie(
            freq_dist,
            values='Nombre',
            names='Fréquence',
            title='Répartition des Fréquences d\'Achat',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_freq.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_freq, use_container_width=True)

    with col2:
        # Montant moyen par fréquence d'achat
        avg_amount_freq = df_filtered.groupby('Frequency of Purchases')['Purchase Amount (USD)'].mean().reset_index()
        avg_amount_freq.columns = ['Fréquence', 'Montant Moyen']
        fig_avg_freq = px.bar(
            avg_amount_freq,
            x='Fréquence',
            y='Montant Moyen',
            title='Montant Moyen par Fréquence d\'Achat',
            color='Fréquence',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_avg_freq.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_avg_freq, use_container_width=True)

# Analyse des modes de paiement
styled_subheader("💳 Modes de Paiement")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des modes de paiement
        payment_dist = df_filtered['Payment Method'].value_counts().reset_index()
        payment_dist.columns = ['Mode de Paiement', 'Nombre']
        fig_payment = px.pie(
            payment_dist,
            values='Nombre',
            names='Mode de Paiement',
            title='Répartition des Modes de Paiement',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_payment.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    with col2:
        # Montant moyen par mode de paiement
        avg_amount_payment = df_filtered.groupby('Payment Method')['Purchase Amount (USD)'].mean().reset_index()
        avg_amount_payment.columns = ['Mode de Paiement', 'Montant Moyen']
        fig_avg_payment = px.bar(
            avg_amount_payment,
            x='Mode de Paiement',
            y='Montant Moyen',
            title='Montant Moyen par Mode de Paiement',
            color='Mode de Paiement',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_avg_payment.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_avg_payment, use_container_width=True)