from collections import deque


class Graph:
    """An unweighted, directed graph stored as adjacency lists."""

    def __init__(self):
        self.outgoing = {}   # vertex -> list of vertices it points TO
        self.incoming = {}   # vertex -> list of vertices pointing INTO it

    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self.outgoing:
            return False
        self.outgoing[vertex] = []
        self.incoming[vertex] = []
        return True

    def addEdge(self, source, target):
        """Connect source -> target. Returns False if not possible."""
        if source not in self.outgoing or target not in self.outgoing:
            return False                     # both vertices must exist
        if source == target:
            return False                     # a vertex can't point to itself
        if target in self.outgoing[source]:
            return False                     # edge already exists
        self.outgoing[source].append(target)
        self.incoming[target].append(source)
        return True

    def removeEdge(self, source, target):
        """Remove the edge source -> target. Returns False if it doesn't exist."""
        if source not in self.outgoing or target not in self.outgoing[source]:
            return False
        self.outgoing[source].remove(target)  # remove from BOTH lists,
        self.incoming[target].remove(source)  # so they always agree
        return True

    def listIncomingAdjacentVertex(self, vertex):
        """All vertices that have an edge INTO this vertex."""
        return self.incoming[vertex]

    def listOutgoingAdjacentVertex(self, vertex):
        """All vertices this vertex has an edge TO."""
        return self.outgoing[vertex]

    def hasVertex(self, vertex):
        """True if the vertex is in the graph."""
        return vertex in self.outgoing

    def vertices(self):
        """All vertices, in the order they were added."""
        return list(self.outgoing)

    def hasPath(self, start, goal):
        """Breadth-first search: can we reach goal from start by following arrows?"""
        visited = {start}
        queue = deque([start])
        while queue:
            current = queue.popleft()          # take the oldest vertex in the queue
            if current == goal:
                return True
            for nxt in self.outgoing[current]:
                if nxt not in visited:         # never visit a vertex twice
                    visited.add(nxt)
                    queue.append(nxt)
        return False

    def wouldCreateCycle(self, source, target):
        """Adding source -> target makes a loop if target can already reach source."""
        return source == target or self.hasPath(target, source)


if __name__ == "__main__":
    g = Graph()
    for v in ["A", "B", "C", "D"]:
        g.addVertex(v)
    g.addEdge("A", "C")      # A -> C
    g.addEdge("B", "C")      # B -> C
    g.addEdge("C", "D")      # C -> D
    #  A --+
    #      +--> C --> D
    #  B --+

    print("=== TEST 1: Incoming and outgoing ===")
    print("  Incoming to C :", g.listIncomingAdjacentVertex("C"))   # ['A', 'B']
    print("  Outgoing from C:", g.listOutgoingAdjacentVertex("C"))  # ['D']
    print("  Incoming to A :", g.listIncomingAdjacentVertex("A"))   # []

    print("\n=== TEST 2: Duplicate and invalid edges ===")
    print("  Add A -> C again :", g.addEdge("A", "C"))   # False
    print("  Add A -> Z (no Z):", g.addEdge("A", "Z"))   # False

    print("\n=== TEST 3: Paths and cycles ===")
    print("  Path A to D?           :", g.hasPath("A", "D"))            # True
    print("  Path D to A?           :", g.hasPath("D", "A"))            # False
    print("  Would D -> A make loop?:", g.wouldCreateCycle("D", "A"))   # True

    print("\n=== TEST 4: Remove an edge ===")
    print("  Remove B -> C  :", g.removeEdge("B", "C"))               # True
    print("  Incoming to C  :", g.listIncomingAdjacentVertex("C"))    # ['A']
    print("  Remove B -> C again:", g.removeEdge("B", "C"))           # False