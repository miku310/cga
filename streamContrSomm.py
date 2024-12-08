import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


def is_friend_pair(graph, u, v, cutoff=3):
    """Vérifie si deux sommets u et v forment une paire d'amis."""
    paths = list(nx.all_simple_paths(graph, source=u, target=v, cutoff=cutoff))
    if not paths:
        return False
    for path in paths:
        induced_subgraph = graph.subgraph(path)
        found_even_length_path = False
        for subpath in nx.all_simple_paths(induced_subgraph, source=path[0], target=path[-1]):
            if (len(subpath) - 1) % 2 == 0:
                found_even_length_path = True
                break
        if not found_even_length_path:
            return False
    return True


def find_friend_pairs(graph, cutoff=3):
    """Trouve toutes les paires d'amis dans le graphe."""
    pairs = []
    for u in graph.nodes:
        for v in graph.nodes:
            if u != v and is_friend_pair(graph, u, v, cutoff):
                pairs.append((u, v))
    return pairs


def contract_nodes(graph, u, v):
    """Contraction de deux sommets u et v en un nouveau sommet uv."""
    new_node = f"{u}_{v}"
    neighbors = set(graph.neighbors(u)).union(set(graph.neighbors(v)))
    neighbors.discard(u)
    neighbors.discard(v)
    graph.add_node(new_node)
    for neighbor in neighbors:
        graph.add_edge(new_node, neighbor)
    graph.remove_node(u)
    graph.remove_node(v)
    return graph


def color_graph(graph):
    """Coloration optimale d'un graphe parfait réduit."""
    return nx.coloring.greedy_color(graph, strategy="largest_first")


def display_graph(graph, title="Graphe actuel", coloring=None):
    """Affiche le graphe avec les couleurs des sommets."""
    pos = nx.spring_layout(graph, seed=42)
    plt.figure(figsize=(8, 6))
    if coloring:
        color_map = [coloring.get(node, 'lightblue') for node in graph.nodes]
        nx.draw(graph, pos, with_labels=True, node_color=color_map, cmap=plt.cm.tab10, node_size=2000, font_weight="bold")
    else:
        nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=2000, font_weight="bold")
    plt.title(title)
    st.pyplot(plt.gcf())
    plt.close()


# Interface Streamlit
st.title("Contraction et Coloration de Graphes")
st.sidebar.title("Configuration du Graphe")

# Étape 1 : Configurer le graphe initial
edges_input = st.sidebar.text_area(
    "Ajouter des arêtes (format : 1,2 ; 2,3)",
    value="1,9 ; 2,4 ; 2,5 ; 2,8 ; 2,9 ; 3,5 ; 3,8 ; 3,9 ; 4,6 ; 4,7 ; 5,6 ; 5,7 ; 6,8 ; 6,9 ; 7,8 ; 7,1 ; 7,9",
)

if "G_initial" not in st.session_state:
    st.session_state["G_initial"] = None
    st.session_state["G_contracted"] = None
    st.session_state["friend_pairs"] = []

if st.sidebar.button("Créer le Graphe"):
    try:
        edges = [tuple(map(int, edge.split(","))) for edge in edges_input.replace(" ", "").split(";")]
        G = nx.Graph()
        G.add_edges_from(edges)
        st.session_state["G_initial"] = G
        st.session_state["G_contracted"] = G.copy()
        st.session_state["friend_pairs"] = find_friend_pairs(G)
        st.sidebar.success("Graphe créé avec succès.")
    except Exception as e:
        st.sidebar.error(f"Erreur : {e}")

# Affichage du graphe initial
if st.session_state["G_initial"]:
    st.subheader("Graphe Initial")
    display_graph(st.session_state["G_initial"], "Graphe Initial")

# Étape 2 : Contraction des sommets
if st.button("Contraction suivante"):
    if st.session_state["friend_pairs"]:
        u, v = st.session_state["friend_pairs"][0]
        G_contracted = st.session_state["G_contracted"]
        
        # Vérifier si les sommets u et v existent toujours dans le graphe
        if u in G_contracted.nodes and v in G_contracted.nodes:
            G_contracted = contract_nodes(G_contracted, u, v)
            st.session_state["G_contracted"] = G_contracted
            st.session_state["friend_pairs"] = find_friend_pairs(G_contracted)
            st.write(f"Contraction effectuée : ({u}, {v})")
            display_graph(G_contracted, f"Graphe après contraction de ({u}, {v})")
        else:
            st.warning(f"Les sommets {u} et/ou {v} n'existent plus dans le graphe.")
    else:
        st.warning("Plus aucune paire d'amis à contracter.")

# Étape 3 : Coloration finale
if st.button("Coloration finale"):
    G_final = st.session_state["G_contracted"]
    if G_final:
        st.subheader("Graphe Final Coloré")
        final_coloring = color_graph(G_final)
        display_graph(G_final, "Graphe Final Coloré", coloring=final_coloring)
