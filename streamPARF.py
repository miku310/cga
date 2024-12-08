import streamlit as st
import networkx as nx
import itertools
import matplotlib.pyplot as plt

# Fonctions utilitaires pour la vérification de la perfection
def est_trou_impair_G(G, cycle):
    sous_graphe = G.subgraph(cycle)
    for u, v in itertools.combinations(cycle, 2):
        if G.has_edge(u, v) and not sous_graphe.has_edge(u, v):
            return False
    return True

def est_trou_impair_Gb(G, cycle):
    Gb = nx.complement(G)
    sous_graphe = Gb.subgraph(cycle)
    for u, v in itertools.combinations(cycle, 2):
        if Gb.has_edge(u, v) and not sous_graphe.has_edge(u, v):
            return False
    return True

def trouver_cycles_impairs_G(G):
    return [cycle for cycle in nx.cycle_basis(G) if len(cycle) >= 5 and len(cycle) % 2 == 1]

def trouver_cycles_impairs_Gbarre(G):
    Gb = nx.complement(G)
    return [cycle for cycle in nx.cycle_basis(Gb) if len(cycle) >= 5 and len(cycle) % 2 == 1]

def est_graphe_parfait(G):
    cycles_impairs_G = trouver_cycles_impairs_G(G)
    for cycle in cycles_impairs_G:
        if est_trou_impair_G(G, cycle):
            return False, "Trou impair trouvé dans G."
    
    cycles_impairs_Gb = trouver_cycles_impairs_Gbarre(G)
    for cycle in cycles_impairs_Gb:
        if est_trou_impair_Gb(G, cycle):
            return False, "Anti-trou impair trouvé dans G bar."
    
    return True, "Le graphe est parfait."

# Fonction pour dessiner le graphe
def dessiner_graphe(G, title="Graphe"):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=1000, font_size=16)
    plt.title(title)
    st.pyplot(plt)

# Interface Streamlit
st.set_page_config(page_title="Analyse de Graphe Parfait", page_icon="🔷", layout="wide")
st.title("🔷 Analyse de Graphe Parfait")
st.write("Entrez les sommets et les arêtes pour vérifier si votre graphe est parfait.")

# Configuration du graphe
with st.sidebar:
    st.header("Configuration du Graphe")
    num_nodes = st.number_input("Nombre de sommets :", min_value=1, step=1, value=5)
    edges = st.session_state.get("edges", [])
    
    # Ajout d'arêtes
    st.subheader("Ajouter des Arêtes")
    col1, col2 = st.columns(2)
    with col1:
        u = st.number_input("Sommet 1", min_value=1, step=1, value=1)
    with col2:
        v = st.number_input("Sommet 2", min_value=1, step=1, value=2)
    
    if st.button("Ajouter l'arête", key="add_edge"):
        if u != v and 1 <= u <= num_nodes and 1 <= v <= num_nodes:
            edges.append((u, v))
            st.session_state["edges"] = edges
            st.success(f"Arête ajoutée : ({u}, {v})")
        else:
            st.error("Arête invalide. Les sommets doivent être différents et compris entre 1 et le nombre de sommets.")
    
    # Affichage des arêtes ajoutées
    st.subheader("Arêtes ajoutées")
    if edges:
        st.write(edges)
    else:
        st.write("Aucune arête ajoutée.")

# Vérification de la perfection
st.header("Vérification de la Perfection")
if st.button("Analyser le Graphe"):
    if edges:
        # Construction du graphe
        G = nx.Graph()
        G.add_edges_from(edges)
        
        # Dessiner le graphe
        dessiner_graphe(G, title="Graphe Entré")
        
        # Analyse de la perfection
        is_perfect, message = est_graphe_parfait(G)
        if is_perfect:
            st.success(message)
        else:
            st.error(message)
    else:
        st.error("Veuillez ajouter des arêtes pour définir un graphe.")
