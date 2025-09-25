# Documentation des fonctions

## Module utils.py

### load_css()
```python
def load_css():
    """
    Charge et applique le CSS personnalisé depuis le fichier style.css.
    
    Cette fonction lit le contenu du fichier style.css et l'injecte dans 
    l'application Streamlit via st.markdown.
    
    Returns:
        None
    """
```

### styled_container()
```python
def styled_container():
    """
    Crée un conteneur Streamlit stylisé avec des effets visuels.
    
    Le conteneur inclut :
    - Fond blanc
    - Bordures arrondies
    - Ombre portée
    - Animation au chargement
    
    Returns:
        streamlit.container: Un conteneur Streamlit stylisé
    """
```

### styled_title(text)
```python
def styled_title(text):
    """
    Crée un titre stylisé avec des effets visuels avancés.
    
    Args:
        text (str): Le texte à afficher comme titre
        
    Features:
        - Dégradé de couleur
        - Police personnalisée
        - Espacement optimal
        - Alignement centré
        
    Returns:
        None: Affiche directement le titre via st.markdown
    """
```

### styled_subheader(text)
```python
def styled_subheader(text):
    """
    Crée un sous-titre stylisé avec une mise en forme cohérente.
    
    Args:
        text (str): Le texte à afficher comme sous-titre
        
    Features:
        - Bordure latérale colorée
        - Police distinctive
        - Espacement harmonieux
        
    Returns:
        None: Affiche directement le sous-titre via st.markdown
    """
```

## Fonctions de traitement des données

### load_data()
```python
@st.cache_data
def load_data():
    """
    Charge et met en cache les données du fichier CSV.
    
    Features:
        - Mise en cache via st.cache_data
        - Lecture optimisée du CSV
        - Gestion des types de données
        
    Returns:
        pandas.DataFrame: Le DataFrame contenant les données
    
    Format attendu:
        - Customer ID (int)
        - Age (int)
        - Gender (str)
        - Category (str)
        - Purchase Amount (USD) (float)
        - Review Rating (float)
        - ...
    """
```

## Fonctions de visualisation

### create_sales_chart(data, x, y, title)
```python
def create_sales_chart(data, x, y, title):
    """
    Crée un graphique de ventes stylisé avec Plotly Express.
    
    Args:
        data (pandas.DataFrame): Les données à visualiser
        x (str): Nom de la colonne pour l'axe X
        y (str): Nom de la colonne pour l'axe Y
        title (str): Titre du graphique
        
    Features:
        - Palette de couleurs personnalisée
        - Mise en forme cohérente
        - Interactivité optimale
        
    Returns:
        plotly.graph_objects.Figure: Le graphique créé
    """
```

### create_distribution_chart(data, column, title)
```python
def create_distribution_chart(data, column, title):
    """
    Crée un graphique de distribution avec Plotly Express.
    
    Args:
        data (pandas.DataFrame): Les données à visualiser
        column (str): Nom de la colonne à analyser
        title (str): Titre du graphique
        
    Features:
        - Histogramme personnalisé
        - Statistiques descriptives
        - Annotations automatiques
        
    Returns:
        plotly.graph_objects.Figure: Le graphique créé
    """
```

## Bonnes pratiques de développement

### 1. Gestion des données
- Toujours utiliser `@st.cache_data` pour les fonctions de chargement
- Vérifier les types de données après le chargement
- Gérer les valeurs manquantes de manière appropriée

### 2. Style et mise en page
- Utiliser les fonctions de style du module utils.py
- Maintenir une cohérence visuelle
- Respecter la palette de couleurs définie

### 3. Performance
- Optimiser les requêtes de données
- Minimiser les recalculs inutiles
- Utiliser le cache de manière appropriée

### 4. Interface utilisateur
- Ajouter des messages d'aide contextuels
- Gérer les cas d'erreur gracieusement
- Fournir des retours visuels clairs

### 5. Documentation
- Documenter toutes les nouvelles fonctions
- Inclure des exemples d'utilisation
- Maintenir la documentation à jour

## Guides d'implémentation

### Ajout d'une nouvelle visualisation
1. Créer une fonction dédiée
2. Utiliser la palette de couleurs standard
3. Ajouter la documentation appropriée
4. Tester l'interactivité

### Modification des filtres
1. Mettre à jour la sidebar
2. Gérer la cohérence des données
3. Optimiser la performance
4. Mettre à jour la documentation

### Extension des fonctionnalités
1. Suivre la structure existante
2. Réutiliser les composants disponibles
3. Maintenir la cohérence du style
4. Documenter les changements