import networkx as nx

from DBST import dbst_sat
from .solver import BTSPSolverSat
from .util import Node, Edge, Iterable, List, Set, Optional, all_edges_sorted, squared_distance


def __find_minimum_spanning_tree(points: Iterable[Node]) -> List[Edge]:
    """
    Find the minimum spanning tree of the given points.
    This is done by encoding the problem as a SAT problem and solving it.
    """
    greedy = dbst_sat.greedy.GreedyDBST(points, 3)
    greedy_edges = greedy.solve()
    solver = dbst_sat.solver.DBSTSolverSAT(points, 3, solution=greedy_edges)
    solver.solve()
    return solver.best_solution


def __get_odd_degree_vertex_form_solution(solution: List[Edge]) -> Set[Node]:
    """
    Return the set of vertices with odd degree in the given solution.
    """
    graph = nx.Graph()
    graph.add_edges_from(solution)
    return {v for v in graph.nodes if graph.degree[v] % 2 == 1}


# Find a minimum-weight perfect matching M in the induced subgraph given by the vertices
def __find_minimum_weight_perfect_matching(nodes) -> List[Edge]:
    """
    Find a minimum-weight perfect matching M in the induced subgraph given by the vertices
    """
    graph = nx.complete_graph(nodes)
    return list(nx.algorithms.matching.min_weight_matching(graph))


def __combine(mst_solution, min_match):
    """
    Combine the edges of MST and matching, such that the resulting graph has only even degree vertices.
    then form an Eulerian circuit
    """
    graph = nx.MultiGraph()
    graph.add_edges_from(mst_solution)
    graph.add_edges_from(min_match)
    try:
        if not nx.is_eulerian(graph):
            raise nx.NetworkXError("G is not Eulerian.")
        else:
            # return [u for u, v in nx.algorithms.eulerian_circuit(graph)]
            return list(nx.algorithms.eulerian_circuit(graph))
    except nx.NetworkXError as e:
        print("Exception:", e)
        return []


def __shortcutting(edges:list[Edge]) -> List[Edge]:
    """
    Make the circuit found in previous step into a Hamiltonian circuit by skipping repeated vertices (shortcutting).
    """
    vertex_sequence = [u for u, v in edges]
    new_vertex_sequence = []
    for vertex in vertex_sequence:
        if vertex not in new_vertex_sequence:
            new_vertex_sequence.append(vertex)
    edges = []
    for i in range(len(new_vertex_sequence) - 1):
        start = new_vertex_sequence[i]
        end = new_vertex_sequence[i + 1]
        edge = (start, end)
        edges.append(edge)
    edges.append((new_vertex_sequence[-1], new_vertex_sequence[0]))
    return edges


def best_result(point):
    mst_solution = __find_minimum_spanning_tree(point)
    odd_degree_vertices = __get_odd_degree_vertex_form_solution(mst_solution)
    min_match = __find_minimum_weight_perfect_matching(odd_degree_vertices)
    circuit = __combine(mst_solution, min_match)

    simplified_circuit = __shortcutting(circuit)
    if len(simplified_circuit) == 0:
        print("no solution")
        return 0
    else:
        print("bottleneck edge is:", max((squared_distance(*e) for e in simplified_circuit)))
    return [u for u, v in circuit], circuit, simplified_circuit, mst_solution
