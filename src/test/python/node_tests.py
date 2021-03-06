from unittest import TestCase

from assertpy import assert_that

from grapple.graph import Graph


class TestNode(TestCase):

    def test__when__init__given__nothing__then__properties_are_set(self):
        graph = Graph()
        ident = graph.next_ident()
        node = graph.create_node()

        assert_that(node.graph).is_equal_to(graph)
        assert_that(node.ident).is_equal_to(ident)
        assert_that(node.labels).is_empty()

    def test__when__relations__given__nothing__then__relations(self):
        graph = Graph()
        node = graph.create_node()
        relation_a = graph.create_node().create_relation_to(node)
        relation_b = node.create_relation_to(graph.create_node())

        assert_that(node.relations).contains_only(relation_a, relation_b)

    def test__when__delete__given____then__graph_none_ident_released(self):
        graph = Graph()
        ident = graph.next_ident()
        node = graph.create_node()
        node.delete()

        assert_that(node.graph).is_none()
        assert_that(graph.next_ident()).is_equal_to(ident)

    def test__when__delete__given__relations__then__exception(self):
        graph = Graph()
        node = graph.create_node()
        node.create_relation_to(graph.create_node())

        assert_that(node.delete) \
            .raises(Exception) \
            .when_called_with() \
            .is_equal_to('Node not empty')

    def test__when__add_labels__given__labels__then__labels(self):
        graph = Graph()
        node = graph.create_node()
        node.add_labels('label1', 'label2', 'label1')

        assert_that(node.labels).contains_only('label1', 'label2')

    def test__when__remove_labels__given__labels_and_outlier__then__remaining_labels(self):
        graph = Graph()
        node = graph.create_node()
        node.add_labels('label1', 'label2')
        node.remove_labels('label2', 'label3')

        assert_that(node.labels).contains_only('label1')
