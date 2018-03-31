from typing import Optional, List

from grapple.bom.relation import Relation


class Node(object):

    def __init__(self, graph: 'Graph', ident: int) -> None:
        self._graph = graph
        self._ident = ident
        self._relations = {}

    @property
    def graph(self) -> Optional['Graph']:
        return self._graph

    @property
    def ident(self) -> int:
        return self._ident

    @property
    def relations(self) -> List['Relation']:
        return list(self._relations.values())

    # noinspection PyProtectedMember
    def create_relation_to(self, node: 'Node') -> 'Relation':
        if node.graph != self._graph:
            raise ValueError("'node' is invalid: <%s>" % node)
        ident = self._graph.next_ident()
        relation = Relation(self._graph, ident, self, node)
        self._graph.lock_ident(ident)
        self._graph._relations[ident] = relation
        self._relations[ident] = relation
        node._relations[ident] = relation
        return relation

    # noinspection PyProtectedMember
    def delete(self) -> None:
        if self._relations:
            raise Exception('Node not empty')
        self._graph._nodes.pop(self._ident)
        self._graph.release_ident(self._ident)
        self._graph = None