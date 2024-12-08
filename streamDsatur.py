import streamlit as st
import heapq


# Fonction pour convertir un numéro de couleur en hexadécimal
def color_to_hex(color_num):
    palette = ["#CA3C66", "#A7E0E0", "#24D26D", "#C49FFF", "#F6FE78", "#FE81CC", "#8A97FE"]
    return palette[(color_num - 1) % len(palette)]

# Classes et algorithme DSatur
class NodeInfo:
    def __init__(self, sat, deg, vertex):
        self.sat = sat
        self.deg = deg
        self.vertex = vertex

class MaxSat:
    def __call__(self, node):
        return (-node.sat, -node.deg, node.vertex)

class Graph:
    def __init__(self, numNodes):
        self.n = numNodes
        self.adj = [[] for _ in range(numNodes)]

    def addEdge(self, u, v):
        u_index = u - 1
        v_index = v - 1
        
        if 0 <= u_index < self.n and 0 <= v_index < self.n:
            self.adj[u_index].append(v_index)
            self.adj[v_index].append(u_index)

    def DSatur(self):
        c = [0] * self.n
        d = [len(self.adj[u]) for u in range(self.n)]
        adjCols = [set() for _ in range(self.n)]
        Q = []

        for u in range(self.n):
            heapq.heappush(Q, (MaxSat()(NodeInfo(0, d[u], u)), u))

        while Q:
            maxPtr, u = heapq.heappop(Q)
            used_colors = set(c[v] for v in self.adj[u] if c[v] != 0)
            color = 1
            while color in used_colors:
                color += 1
            c[u] = color

            for v in self.adj[u]:
                if c[v] == 0:
                    adjCols[v].add(color)
                    d[v] -= 1
                    heapq.heappush(Q, (MaxSat()(NodeInfo(len(adjCols[v]), d[v], v)), v))

        return c

# Début de l'application Streamlit
st.set_page_config(page_title="Coloration de Graphe DSatur", page_icon="🎨", layout="wide")

st.title("🎨 Coloration de Graphe avec DSatur")
st.write("Cette application permet de colorer un graphe à partir de ses sommets et arêtes à l'aide de l'algorithme DSatur.")

# Section : Configuration du graphe
with st.sidebar:
    st.header("Configuration du Graphe")
    num_nodes = st.number_input("Nombre de sommets :", min_value=1, step=1, value=5)
    edges = st.session_state.get("edges", [])

    # Saisie des arêtes
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

    # Affichage des arêtes
    st.subheader("Arêtes ajoutées")
    if edges:
        st.write(edges)
    else:
        st.write("Aucune arête ajoutée.")

# Section : Visualisation et Résultats
st.header("Résultats de la Coloration")

# Graphe original
st.subheader("1️⃣ Visualisation initiale du Graphe")
if edges:
    st.graphviz_chart(
        f"""
        graph G {{
            {"; ".join(f"{u} -- {v}" for u, v in edges)}
        }}
        """
    )
else:
    st.write("Ajoutez des arêtes pour visualiser le graphe.")

# Coloration et Graphe colorié
if st.button("Colorer le graphe", key="color_graph"):
    if num_nodes > 0:
        graph = Graph(num_nodes)
        for u, v in edges:
            graph.addEdge(u, v)

        colors = graph.DSatur()

        # Affichage des couleurs des sommets
        st.write("### Couleurs des Sommets")
        for i, color in enumerate(colors):
            st.write(f"**Sommet {i + 1}** : Couleur **{color}**")

        # Graphe colorié
        st.subheader("2️⃣ Graphe colorié")
        node_colors = [
            f'"{i + 1}" [style=filled, fillcolor="{color_to_hex(color)}"];'
            for i, color in enumerate(colors)
        ]
        graph_viz = f"""
        graph G {{
            {"; ".join(f"{u} -- {v}" for u, v in edges)}
            {" ".join(node_colors)}
        }}
        """
        st.graphviz_chart(graph_viz)
    else:
        st.error("Veuillez entrer un nombre valide de sommets.")


