import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Analyse des Catégories", page_icon="📦", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre de la page
styled_title("📦 Analyse des Catégories")

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
        n_categories = len(df_filtered['Category'].unique())
        st.metric("Nombre de Catégories", n_categories)
    with col2:
        avg_price = df_filtered['Purchase Amount (USD)'].mean()
        st.metric("Prix Moyen (USD)", f"${avg_price:,.2f}")
    with col3:
        max_price = df_filtered['Purchase Amount (USD)'].max()
        st.metric("Prix Maximum (USD)", f"${max_price:,.2f}")

# Analyse des catégories
styled_subheader("📊 Performance par Catégorie")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Nombre de ventes par catégorie
        category_sales = df_filtered['Category'].value_counts().reset_index()
        category_sales.columns = ['Catégorie', 'Nombre de Ventes']
        fig_category = px.bar(
            category_sales,
            x='Catégorie',
            y='Nombre de Ventes',
            title='Volume de Ventes par Catégorie',
            color='Catégorie',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_category.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Catégorie",
            yaxis_title="Nombre de Ventes"
        )
        st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        # Revenus par catégorie
        category_revenue = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
        category_revenue.columns = ['Catégorie', 'Revenus']
        fig_revenue = px.bar(
            category_revenue,
            x='Catégorie',
            y='Revenus',
            title='Revenus par Catégorie (USD)',
            color='Catégorie',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_revenue.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Catégorie",
            yaxis_title="Revenus (USD)"
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

# Analyse saisonnière
styled_subheader("🌤️ Tendances Saisonnières")
with styled_container():
    # Heatmap des ventes par catégorie et saison
    seasonal_sales = df_filtered.groupby(['Category', 'Season']).size().reset_index(name='count')
    pivot_table = seasonal_sales.pivot(index='Category', columns='Season', values='count')
    
    fig_heatmap = px.imshow(
        pivot_table,
        title='Ventes par Catégorie et Saison',
        labels=dict(x="Saison", y="Catégorie", color="Nombre de Ventes"),
        color_continuous_scale=['#E3F2FD', '#1E88E5']
    )
    fig_heatmap.update_layout(
        margin=dict(t=30, l=0, r=0, b=0),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Prix et Popularité
styled_subheader("💰 Analyse des Prix")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des prix par catégorie
        fig_price_dist = px.box(
            df_filtered,
            x='Category',
            y='Purchase Amount (USD)',
            title='Distribution des Prix par Catégorie',
            color='Category',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_price_dist.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Catégorie",
            yaxis_title="Prix (USD)"
        )
        st.plotly_chart(fig_price_dist, use_container_width=True)

    with col2:
        # Prix moyen par catégorie
        avg_price_cat = df_filtered.groupby('Category')['Purchase Amount (USD)'].mean().reset_index()
        avg_price_cat.columns = ['Catégorie', 'Prix Moyen']
        fig_avg_price = px.bar(
            avg_price_cat,
            x='Catégorie',
            y='Prix Moyen',
            title='Prix Moyen par Catégorie (USD)',
            color='Catégorie',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_avg_price.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Catégorie",
            yaxis_title="Prix Moyen (USD)"
        )
        st.plotly_chart(fig_avg_price, use_container_width=True)