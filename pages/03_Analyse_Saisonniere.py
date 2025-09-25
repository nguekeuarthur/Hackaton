import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Analyse Saisonnière", page_icon="🌤️", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre de la page
styled_title("🌤️ Analyse Saisonnière")

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

# Métriques clés par saison
with styled_container():
    seasons = df_filtered['Season'].unique()
    cols = st.columns(len(seasons))
    
    for idx, season in enumerate(seasons):
        with cols[idx]:
            season_data = df_filtered[df_filtered['Season'] == season]
            avg_amount = season_data['Purchase Amount (USD)'].mean()
            st.metric(f"Moyenne {season}", f"${avg_amount:,.2f}")

# Tendances saisonnières
styled_subheader("📊 Tendances par Saison")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Volume de ventes par saison
        season_sales = df_filtered['Season'].value_counts().reset_index()
        season_sales.columns = ['Saison', 'Nombre de Ventes']
        fig_season = px.bar(
            season_sales,
            x='Saison',
            y='Nombre de Ventes',
            title='Volume de Ventes par Saison',
            color='Saison',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_season.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_season, use_container_width=True)

    with col2:
        # Revenus par saison
        season_revenue = df_filtered.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
        season_revenue.columns = ['Saison', 'Revenus']
        fig_revenue = px.bar(
            season_revenue,
            x='Saison',
            y='Revenus',
            title='Revenus par Saison (USD)',
            color='Saison',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_revenue.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

# Analyse des catégories par saison
styled_subheader("🎯 Performance des Catégories par Saison")
with styled_container():
    # Heatmap des ventes par catégorie et saison
    category_season = pd.crosstab(df_filtered['Category'], df_filtered['Season'])
    fig_heatmap = px.imshow(
        category_season,
        title='Distribution des Ventes par Catégorie et Saison',
        labels=dict(x="Saison", y="Catégorie", color="Nombre de Ventes"),
        color_continuous_scale=['#E3F2FD', '#1E88E5']
    )
    fig_heatmap.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Analyse des prix par saison
styled_subheader("💰 Analyse des Prix Saisonniers")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des prix par saison
        fig_price_dist = px.box(
            df_filtered,
            x='Season',
            y='Purchase Amount (USD)',
            title='Distribution des Prix par Saison',
            color='Season',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_price_dist.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_price_dist, use_container_width=True)

    with col2:
        # Prix moyen par saison et catégorie
        avg_price = df_filtered.groupby(['Season', 'Category'])['Purchase Amount (USD)'].mean().reset_index()
        fig_avg_price = px.bar(
            avg_price,
            x='Season',
            y='Purchase Amount (USD)',
            color='Category',
            title='Prix Moyen par Saison et Catégorie',
            barmode='group',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_avg_price.update_layout(
            legend=dict(orientation="h", y=-0.2),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_avg_price, use_container_width=True)