import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Fonction pour vérifier si un cycle a une diagonale
def a_diagonale(graphe, cycle):
    n = len(cycle)
    for i in range(n):
        for j in range(i + 2, n):
            if j != (i + n - 1) % n and graphe.has_edge(cycle[i], cycle[j]):
                return True
    return False

# Fonction pour vérifier si un graphe est triangulé
def est_triangule(graphe):
    messages = []
    for cycle in nx.cycle_basis(graphe):
        if len(cycle) >= 4 and not a_diagonale(graphe, cycle):
            messages.append(f"Le graphe n'est pas triangulé car le cycle {cycle} (longueur >= 4) n'a pas de corde.")
    if messages:
        return False, messages
    return True, ["Le graphe est triangulé."]

# Fonction pour vérifier si un graphe est planaire
def est_planaire(graphe):
    return nx.check_planarity(graphe)

# Fonction pour dessiner un graphe
def dessiner_graphe(graphe, title="Graphe", layout="spring"):
    if layout == "planar" and nx.check_planarity(graphe)[0]:
        pos = nx.planar_layout(graphe)
    else:
        pos = nx.spring_layout(graphe)
    
    plt.figure(figsize=(8, 8))
    nx.draw(graphe, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1000, font_size=16)
    plt.title(title)
    st.pyplot(plt)

# Interface Streamlit
st.set_page_config(page_title="Analyse Triangulé & Planaire", page_icon="🔺", layout="wide")
st.title("🔺 Analyse de Graphe : Triangulé et Planaire")
st.write("Ajoutez les sommets et les arêtes de votre graphe pour effectuer une analyse.")

# Saisie des sommets et des arêtes
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

# Sélection de l'analyse
st.header("Analyse du Graphe")
analyse_type = st.radio("Choisissez l'analyse à effectuer :", ["Vérification Triangulé", "Vérification Planaire"])

if st.button("Effectuer l'Analyse"):
    if edges:
        # Construction du graphe
        G = nx.Graph()
        G.add_edges_from(edges)

        if analyse_type == "Vérification Triangulé":
            # Vérification si le graphe est triangulé
            est_triangule_flag, messages = est_triangule(G)
            dessiner_graphe(G, title="Graphe Entré")
            if est_triangule_flag:
                st.success(messages[0])
            else:
                st.error("Le graphe n'est pas triangulé.")
                for msg in messages:
                    st.warning(msg)

        elif analyse_type == "Vérification Planaire":
            # Vérification si le graphe est planaire
            is_planar, _ = est_planaire(G)
            if is_planar:
                st.success("Le graphe est planaire.")
                dessiner_graphe(G, title="Graphe Planaire", layout="planar")
            else:
                st.error("Le graphe n'est pas planaire.")
                dessiner_graphe(G, title="Graphe (non planaire)")
    else:
        st.error("Veuillez ajouter des arêtes pour définir un graphe.")
