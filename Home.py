import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

st.set_page_config(
    page_title="Dashboard - Tendances d'Achat",
    page_icon="🛍️",
    layout="wide"
)

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

# Avertissement si aucune donnée n'est sélectionnée
if df_filtered.empty:
    st.warning("⚠️ Aucune donnée disponible pour les filtres sélectionnés. Veuillez modifier vos critères de sélection.")

# KPIs principaux
styled_subheader("🎯 Indicateurs Clés")
with styled_container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_customers = len(df_filtered['Customer ID'].unique())
        st.metric("👥 Clients Total", f"{total_customers:,}")
        
    with col2:
        avg_purchase = df_filtered['Purchase Amount (USD)'].mean()
        st.metric("💰 Panier Moyen", f"${avg_purchase:.2f}")
        
    with col3:
        total_purchases = len(df_filtered)
        st.metric("🛍️ Total Achats", f"{total_purchases:,}")
        
    with col4:
        avg_rating = df_filtered['Review Rating'].mean()
        st.metric("⭐ Note Moyenne", f"{avg_rating:.1f}/5")
        
    with col5:
        subscription_rate = (df_filtered['Subscription Status'] == 'Yes').mean() * 100
        st.metric("🔄 Taux d'Abonnement", f"{subscription_rate:.1f}%")

# Analyse démographique
styled_subheader("👥 Analyse Démographique")
with styled_container():
    col1, col2 = st.columns(2)

    with col1:
        # Répartition par genre
        gender_dist = px.pie(
            df_filtered,
            names='Gender',
            title='Répartition par Genre',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1']
        )
        gender_dist.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(gender_dist, use_container_width=True)

    with col2:
        # Distribution des âges
        age_dist = px.histogram(
            df_filtered,
            x='Age',
            title='Distribution des Âges',
            nbins=30,
            color_discrete_sequence=['#1E88E5']
        )
        age_dist.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Âge",
            yaxis_title="Nombre de Clients"
        )
        st.plotly_chart(age_dist, use_container_width=True)

# Analyse des ventes
styled_subheader("💰 Analyse des Ventes")
with styled_container():
    col1, col2 = st.columns(2)

    with col1:
        # Ventes par catégorie
        sales_by_category = df_filtered.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
        fig_category = px.bar(
            sales_by_category,
            x='Category',
            y='Purchase Amount (USD)',
            title='Ventes par Catégorie',
            color='Category',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_category.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Catégorie",
            yaxis_title="Ventes (USD)"
        )
        st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        # Ventes par saison
        sales_by_season = df_filtered.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
        fig_season = px.bar(
            sales_by_season,
            x='Season',
            y='Purchase Amount (USD)',
            title='Ventes par Saison',
            color='Season',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_season.update_layout(
            showlegend=False,
            margin=dict(t=30, l=0, r=0, b=0),
            xaxis_title="Saison",
            yaxis_title="Ventes (USD)"
        )
        st.plotly_chart(fig_season, use_container_width=True)

# Analyse des comportements d'achat
styled_subheader("🔄 Comportements d'Achat")
with styled_container():
    col1, col2 = st.columns(2)

    with col1:
        # Distribution des moyens de paiement
        payment_dist = df_filtered['Payment Method'].value_counts().reset_index()
        payment_dist.columns = ['Mode de Paiement', 'Nombre']
        fig_payment = px.pie(
            payment_dist,
            values='Nombre',
            names='Mode de Paiement',
            title='Répartition des Modes de Paiement',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_payment.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    with col2:
        # Fréquence d'achat
        freq_dist = df_filtered['Frequency of Purchases'].value_counts().reset_index()
        freq_dist.columns = ['Fréquence', 'Nombre']
        fig_freq = px.pie(
            freq_dist,
            values='Nombre',
            names='Fréquence',
            title='Répartition des Fréquences d\'Achat',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_freq.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_freq, use_container_width=True)

# Tendances saisonnières
styled_subheader("📊 Tendances Saisonnières")
with styled_container():
    # Matrice des ventes par catégorie et saison
    sales_matrix = pd.crosstab(df_filtered['Category'], df_filtered['Season'])
    fig_heatmap = px.imshow(
        sales_matrix,
        title='Distribution des Ventes par Catégorie et Saison',
        labels=dict(x="Saison", y="Catégorie", color="Nombre de Ventes"),
        color_continuous_scale=['#E3F2FD', '#1E88E5']
    )
    fig_heatmap.update_layout(margin=dict(t=30, l=0, r=0, b=0))
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Insights et opportunités
styled_subheader("� Insights et Opportunités")
with styled_container():
    col1, col2 = st.columns(2)

    with col1:
        # Calcul du pourcentage de clients sans promo
        no_promo_rate = (df_filtered['Promo Code Used'] == 'No').mean() * 100
        st.info(f"🚨 {no_promo_rate:.1f}% des clients n'utilisent pas de code promo - Opportunité marketing !")

    with col2:
        # Calcul de la différence de dépense entre abonnés et non-abonnés
        avg_sub = df_filtered[df_filtered['Subscription Status'] == 'Yes']['Purchase Amount (USD)'].mean()
        avg_non_sub = df_filtered[df_filtered['Subscription Status'] == 'No']['Purchase Amount (USD)'].mean()
        diff_percentage = ((avg_sub - avg_non_sub) / avg_non_sub) * 100
        
        st.info(f"💡 Les clients abonnés dépensent {diff_percentage:.1f}% de plus que les non-abonnés")