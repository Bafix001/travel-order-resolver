import networkx as nx
import matplotlib.pyplot as plt
import itertools

def build_delivery_graph(locations):
    """
    Crée un graphe où chaque ville/rue est un nœud.
    Calcule la distance 'à vol d'oiseau' entre tous les points.
    """
    G = nx.Graph()
    
    # 1. On simule des coordonnées GPS (x, y) pour chaque adresse extraite
    # Dans un vrai projet, on utiliserait une API de Géocodage
    coords = {loc: (i*2, (i**2)%5) for i, loc in enumerate(locations)}
    coords['DEPOT'] = (0, 0) # On ajoute un point de départ
    
    for loc, pos in coords.items():
        G.add_node(loc, pos=pos)
        
    # 2. On relie tous les points entre eux (Graphe Complet)
    for u, v in itertools.combinations(G.nodes, 2):
        pos_u = G.nodes[u]['pos']
        pos_v = G.nodes[v]['pos']
        # Distance euclidienne
        dist = ((pos_u[0]-pos_v[0])**2 + (pos_u[1]-pos_v[1])**2)**0.5
        G.add_edge(u, v, weight=round(dist, 2))
        
    return G, coords

def solve_tsp(G, start_node='DEPOT'):
    """Résout le problème du voyageur de commerce (simplifié)."""
    # Algorithme du plus proche voisin
    path = [start_node]
    nodes_to_visit = list(G.nodes)
    nodes_to_visit.remove(start_node)
    
    current_node = start_node
    while nodes_to_visit:
        next_node = min(nodes_to_visit, key=lambda node: G[current_node][node]['weight'])
        path.append(next_node)
        nodes_to_visit.remove(next_node)
        current_node = next_node
        
    path.append(start_node) # Retour au dépôt
    return path

# --- TEST DU GRAPH OPTIMIZER ---
if __name__ == "__main__":
    # On simule les adresses que resolve_itinerary.py nous a données
    mes_destinations = ["r. d'Anjou", "r. de la Harpe", "r. Saint-Honoré"]
    
    graph, positions = build_delivery_graph(mes_destinations)
    itineraire = solve_tsp(graph)
    
    print("📍 Itinéraire optimisé :")
    print(" -> ".join(itineraire))