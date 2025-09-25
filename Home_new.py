import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Tableau de Bord - Vue d'Ensemble", page_icon="📊", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre principal
styled_title("📊 Tableau de Bord - Vue d'Ensemble")

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

if df_filtered.empty:
    st.warning("⚠️ Aucune donnée disponible pour les filtres sélectionnés. Veuillez modifier vos critères de sélection.")
    st.stop()

# Section des KPIs
styled_subheader("🎯 Indicateurs Clés")
with styled_container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "👥 Clients Total",
            f"{len(df_filtered['Customer ID'].unique()):,}"
        )
    with col2:
        st.metric(
            "💰 Panier Moyen",
            f"${df_filtered['Purchase Amount (USD)'].mean():.2f}"
        )
    with col3:
        st.metric(
            "📦 Total Achats",
            f"{len(df_filtered):,}"
        )
    with col4:
        st.metric(
            "⭐ Note Moyenne",
            f"{df_filtered['Review Rating'].mean():.2f}/5"
        )
    with col5:
        st.metric(
            "🔄 Taux d'Abonnement",
            f"{(df_filtered['Subscription Status'] == 'Yes').mean() * 100:.1f}%"
        )

# Section des graphiques
col1, col2 = st.columns(2)

with col1:
    with styled_container():
        styled_subheader("👥 Répartition par Genre")
        fig_gender = px.pie(
            df_filtered,
            names='Gender',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1']
        )
        fig_gender.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=0, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_gender, use_container_width=True)

with col2:
    with styled_container():
        styled_subheader("📊 Distribution des Âges")
        fig_age = px.histogram(
            df_filtered,
            x='Age',
            nbins=30,
            color_discrete_sequence=['#1E88E5']
        )
        fig_age.update_layout(
            showlegend=False,
            margin=dict(t=0, l=0, r=0, b=0),
            xaxis_title="Âge",
            yaxis_title="Nombre de Clients"
        )
        st.plotly_chart(fig_age, use_container_width=True)

# Tendances des ventes
styled_subheader("📈 Tendances des Ventes")
with styled_container():
    seasonal_sales = df_filtered.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
    fig_season = px.bar(
        seasonal_sales,
        x='Season',
        y='Purchase Amount (USD)',
        color='Season',
        color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
    )
    fig_season.update_layout(
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(t=0, l=0, r=0, b=0)
    )
    st.plotly_chart(fig_season, use_container_width=True)

# Catégories populaires
styled_subheader("🏷️ Top des Catégories")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        category_sales = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
        category_sales = category_sales.sort_values('Purchase Amount (USD)', ascending=True)
        fig_category = px.bar(
            category_sales,
            x='Purchase Amount (USD)',
            y='Category',
            orientation='h',
            color='Category',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_category.update_layout(
            showlegend=False,
            margin=dict(t=0, l=0, r=0, b=0),
            xaxis_title="Montant des Ventes (USD)",
            yaxis_title="Catégorie"
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        payment_dist = df_filtered['Payment Method'].value_counts().reset_index()
        payment_dist.columns = ['Méthode', 'Nombre']
        fig_payment = px.pie(
            payment_dist,
            values='Nombre',
            names='Méthode',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_payment.update_layout(
            title="Répartition des Méthodes de Paiement",
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_payment, use_container_width=True)