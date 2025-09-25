import streamlit as st
import pandas as pd
import plotly.express as px
from pages.client_analysis import show_client_analysis
from pages.product_analysis import show_product_analysis
from pages.financial_analysis import show_financial_analysis
from pages.customer_behavior import show_customer_behavior
from pages.payment_shipping import show_payment_shipping
from state_codes import STATE_DICT

# Configuration de la page
st.set_page_config(
    page_title="Analyse Détaillée des Tendances d'Achat",
    page_icon="🛍️",
    layout="wide"
)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre principal
st.title("🛍️ Analyse Détaillée des Tendances d'Achat")

# Navigation dans la sidebar
st.sidebar.title("Navigation")
selected_tab = st.sidebar.radio(
    "",
    ["👥 Analyse Client",
     "📦 Analyse Produit",
     "💰 Analyse Financière",
     "🎯 Comportement Client",
     "💳 Paiement & Livraison"],
    label_visibility="collapsed"
)

# Filtres globaux dans la sidebar
st.sidebar.markdown("---")
st.sidebar.header("Filtres Globaux")
selected_category = st.sidebar.multiselect(
    "Catégorie de Produits",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

selected_season = st.sidebar.multiselect(
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

# Affichage conditionnel des sections en fonction de l'onglet sélectionné
if selected_tab == "👥 Analyse Client":
    st.header("Analyse Client")
    
    # Métriques clés clients
    col1, col2, col3 = st.columns(3)
    with col1:
        total_customers = len(df_filtered['Customer ID'].unique()) if not df_filtered.empty else 0
        st.metric("Nombre Total de Clients", f"{total_customers:,}")
    with col2:
        avg_age = df_filtered['Age'].mean() if not df_filtered.empty else 0
        st.metric("Âge Moyen", f"{avg_age:.1f} ans")
    with col3:
        subscription_rate = (df_filtered['Subscription Status'] == 'Yes').mean() * 100 if not df_filtered.empty else 0
        st.metric("Taux d'Abonnement", f"{subscription_rate:.1f}%")

    col1, col2 = st.columns(2)
    
    with col1:
        # Pyramide des âges par genre
        fig_age_gender = px.histogram(
            df_filtered,
            x='Age',
            color='Gender',
            barmode='group',
            title='Distribution des Âges par Genre',
            labels={'Age': 'Âge', 'count': 'Nombre de Clients'}
        )
        st.plotly_chart(fig_age_gender, use_container_width=True)

    with col2:
        # Répartition géographique des clients
        df_filtered['State_Code'] = df_filtered['Location'].map(STATE_DICT)
        location_counts = df_filtered.groupby('State_Code').size().reset_index()
        location_counts.columns = ['State_Code', 'Count']
        
        fig_geo = px.choropleth(
            location_counts,
            locations='State_Code',
            locationmode="USA-states",
            color='Count',
            scope="usa",
            color_continuous_scale="Viridis",
            title='Répartition Géographique des Clients',
            labels={'Count': 'Nombre de Clients'}
        )
        fig_geo.update_layout(
            geo_scope='usa',
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_geo, use_container_width=True)

    # Segmentation des clients par fréquence d'achat
    freq_dist = px.pie(
        df_filtered,
        names='Frequency of Purchases',
        title='Segmentation par Fréquence d\'Achat'
    )
    st.plotly_chart(freq_dist, use_container_width=True)

elif selected_tab == "📦 Analyse Produit":
    st.header("Analyse Produit")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_products = len(df_filtered['Item Purchased'].unique()) if not df_filtered.empty else 0
        st.metric("Nombre de Produits Uniques", f"{total_products:,}")
    with col2:
        top_category = df_filtered['Category'].mode().iloc[0] if not df_filtered.empty else "Aucune donnée"
        st.metric("Catégorie la Plus Populaire", top_category)
    with col3:
        top_color = df_filtered['Color'].mode().iloc[0] if not df_filtered.empty else "Aucune donnée"
        st.metric("Couleur la Plus Vendue", top_color)

    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition des catégories de produits
        fig_categories = px.pie(
            df_filtered,
            names='Category',
            title='Répartition des Catégories de Produits',
            hole=0.3
        )
        st.plotly_chart(fig_categories, use_container_width=True)

    with col2:
        # Top 10 des produits les plus vendus
        top_items = df_filtered['Item Purchased'].value_counts().head(10)
        fig_top_items = px.bar(
            x=top_items.index,
            y=top_items.values,
            title='Top 10 des Produits les Plus Vendus',
            labels={'x': 'Produit', 'y': 'Nombre de Ventes'}
        )
        st.plotly_chart(fig_top_items, use_container_width=True)

    # Matrice des tailles et couleurs
    size_color_matrix = pd.crosstab(df_filtered['Size'], df_filtered['Color'])
    fig_matrix = px.imshow(
        size_color_matrix,
        title='Matrice Tailles/Couleurs',
        labels=dict(x='Couleur', y='Taille', color='Nombre de Produits')
    )
    st.plotly_chart(fig_matrix, use_container_width=True)

elif selected_tab == "💰 Analyse Financière":
    st.header("Analyse Financière")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_revenue = df_filtered['Purchase Amount (USD)'].sum() if not df_filtered.empty else 0
        st.metric("Chiffre d'Affaires Total", f"${total_revenue:,.2f}")
    with col2:
        avg_purchase = df_filtered['Purchase Amount (USD)'].mean() if not df_filtered.empty else 0
        st.metric("Panier Moyen", f"${avg_purchase:.2f}")
    with col3:
        discount_rate = (df_filtered['Discount Applied'] == 'Yes').mean() * 100 if not df_filtered.empty else 0
        st.metric("Taux d'Utilisation des Remises", f"{discount_rate:.1f}%")

    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution des ventes par saison
        seasonal_sales = df_filtered.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
        fig_seasonal = px.bar(
            seasonal_sales,
            x='Season',
            y='Purchase Amount (USD)',
            title='Ventes par Saison',
            color='Season'
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)

    with col2:
        # Distribution des montants d'achat
        fig_purchase_dist = px.histogram(
            df_filtered,
            x='Purchase Amount (USD)',
            title='Distribution des Montants d\'Achat',
            nbins=30
        )
        st.plotly_chart(fig_purchase_dist, use_container_width=True)

    # Impact des promotions sur les ventes
    promo_impact = df_filtered.groupby('Promo Code Used')['Purchase Amount (USD)'].agg(['mean', 'count']).reset_index()
    fig_promo = px.bar(
        promo_impact,
        x='Promo Code Used',
        y='mean',
        title='Impact des Codes Promo sur le Montant Moyen d\'Achat',
        labels={'mean': 'Montant Moyen d\'Achat ($)'}
    )
    st.plotly_chart(fig_promo, use_container_width=True)

elif selected_tab == "🎯 Comportement Client":
    st.header("Comportement Client")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        avg_rating = df_filtered['Review Rating'].mean() if not df_filtered.empty else 0
        st.metric("Note Moyenne", f"{avg_rating:.2f}/5")
    with col2:
        avg_purchases = df_filtered['Previous Purchases'].mean() if not df_filtered.empty else 0
        st.metric("Nombre Moyen d'Achats Précédents", f"{avg_purchases:.1f}")
    with col3:
        returning_rate = (df_filtered['Previous Purchases'] > 0).mean() * 100 if not df_filtered.empty else 0
        st.metric("Taux de Clients Fidèles", f"{returning_rate:.1f}%")

    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des notes
        fig_ratings = px.histogram(
            df_filtered,
            x='Review Rating',
            title='Distribution des Notes Client',
            nbins=20
        )
        st.plotly_chart(fig_ratings, use_container_width=True)

    with col2:
        # Relation entre notes et montant d'achat
        fig_rating_purchase = px.scatter(
            df_filtered,
            x='Review Rating',
            y='Purchase Amount (USD)',
            title='Relation entre Notes et Montant d\'Achat',
            trendline="ols"
        )
        st.plotly_chart(fig_rating_purchase, use_container_width=True)

    # Analyse des achats précédents
    fig_previous = px.histogram(
        df_filtered,
        x='Previous Purchases',
        title='Distribution du Nombre d\'Achats Précédents',
        nbins=30
    )
    st.plotly_chart(fig_previous, use_container_width=True)

elif selected_tab == "💳 Paiement & Livraison":
    st.header("Analyse des Moyens de Paiement et Livraison")
    
    col1, col2 = st.columns(2)
    with col1:
        most_used_payment = df_filtered['Payment Method'].mode().iloc[0] if not df_filtered.empty else "Aucune donnée"
        st.metric("Moyen de Paiement le Plus Utilisé", most_used_payment)
    with col2:
        most_used_shipping = df_filtered['Shipping Type'].mode().iloc[0] if not df_filtered.empty else "Aucune donnée"
        st.metric("Mode de Livraison le Plus Populaire", most_used_shipping)

    col1, col2 = st.columns(2)
    
    with col1:
        # Répartition des méthodes de paiement
        fig_payment = px.pie(
            df_filtered,
            names='Payment Method',
            title='Répartition des Méthodes de Paiement',
            hole=0.3
        )
        st.plotly_chart(fig_payment, use_container_width=True)

    with col2:
        # Répartition des types de livraison
        fig_shipping = px.pie(
            df_filtered,
            names='Shipping Type',
            title='Répartition des Types de Livraison',
            hole=0.3
        )
        st.plotly_chart(fig_shipping, use_container_width=True)

    # Relation entre type de livraison et montant d'achat
    shipping_amount = df_filtered.groupby('Shipping Type')['Purchase Amount (USD)'].mean().reset_index()
    fig_shipping_amount = px.bar(
        shipping_amount,
        x='Shipping Type',
        y='Purchase Amount (USD)',
        title='Montant Moyen d\'Achat par Type de Livraison',
        color='Shipping Type'
    )
    st.plotly_chart(fig_shipping_amount, use_container_width=True)

    # Préférences de paiement vs méthode utilisée
    payment_comparison = pd.crosstab(
        df_filtered['Payment Method'],
        df_filtered['Preferred Payment Method']
    )
    fig_payment_comparison = px.imshow(
        payment_comparison,
        title='Méthode de Paiement Utilisée vs. Préférée',
        labels=dict(x='Méthode Préférée', y='Méthode Utilisée', color='Nombre de Transactions')
    )
    st.plotly_chart(fig_payment_comparison, use_container_width=True)