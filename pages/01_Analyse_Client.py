import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_css, styled_container, styled_title, styled_subheader

# Configuration de la page
st.set_page_config(page_title="Analyse Client", page_icon="👥", layout="wide")

# Chargement du CSS
load_css()

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv('shopping_trends.csv')
    return df

df = load_data()

# Titre de la page
styled_title("👥 Analyse Client")

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
        total_customers = len(df_filtered['Customer ID'].unique()) if not df_filtered.empty else 0
        st.metric("Nombre Total de Clients", f"{total_customers:,}")
    with col2:
        avg_age = df_filtered['Age'].mean() if not df_filtered.empty else 0
        st.metric("Âge Moyen", f"{avg_age:.1f} ans")
    with col3:
        subscription_rate = (df_filtered['Subscription Status'] == 'Yes').mean() * 100 if not df_filtered.empty else 0
        st.metric("Taux d'Abonnement", f"{subscription_rate:.1f}%")

# Distribution démographique
styled_subheader("📊 Analyse Démographique")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Pyramide des âges par genre
        fig_age_gender = px.histogram(
            df_filtered,
            x='Age',
            color='Gender',
            barmode='group',
            title='Distribution des Âges par Genre',
            labels={'Age': 'Âge', 'count': 'Nombre de Clients'},
            color_discrete_sequence=['#1E88E5', '#5E35B1']
        )
        fig_age_gender.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_age_gender, use_container_width=True, key="age_gender_hist")

    with col2:
        # Répartition par genre
        gender_dist = df_filtered['Gender'].value_counts().reset_index()
        gender_dist.columns = ['Genre', 'Nombre']
        fig_gender = px.pie(
            gender_dist,
            values='Nombre',
            names='Genre',
            title='Répartition par Genre',
            hole=0.6,
            color_discrete_sequence=['#1E88E5', '#5E35B1']
        )
        fig_gender.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_gender, use_container_width=True, key="gender_pie")

# Analyse des préférences
styled_subheader("🎯 Préférences Client")
with styled_container():
    col1, col2 = st.columns(2)
    
    with col1:
        # Taille préférée
        size_dist = df_filtered['Size'].value_counts().reset_index()
        size_dist.columns = ['Taille', 'Nombre']
        fig_size = px.pie(
            size_dist,
            values='Nombre',
            names='Taille',
            title='Répartition des Tailles',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_size.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_size, use_container_width=True, key="size_pie")

    with col2:
        # Couleur préférée
        color_dist = df_filtered['Color'].value_counts().reset_index()
        color_dist.columns = ['Couleur', 'Nombre']
        fig_color = px.pie(
            color_dist,
            values='Nombre',
            names='Couleur',
            title='Répartition des Couleurs',
            color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
        )
        fig_color.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=30, l=0, r=0, b=0)
        )
        st.plotly_chart(fig_color, use_container_width=True, key="color_pie")

# Analyse comportementale
styled_subheader("🔄 Comportement d'Achat")
with styled_container():
    # Fréquence d'achat
    purchase_freq = df_filtered['Frequency of Purchases'].value_counts().reset_index()
    purchase_freq.columns = ['Fréquence', 'Nombre']
    fig_freq = px.bar(
        purchase_freq,
        x='Fréquence',
        y='Nombre',
        title='Fréquence des Achats',
        color='Fréquence',
        color_discrete_sequence=['#1E88E5', '#5E35B1', '#43A047', '#FB8C00']
    )
    fig_freq.update_layout(
        showlegend=False,
        margin=dict(t=30, l=0, r=0, b=0),
        xaxis_title="Fréquence d'Achat",
        yaxis_title="Nombre de Clients"
    )
    st.plotly_chart(fig_freq, use_container_width=True, key="freq_bar")