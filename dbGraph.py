# -*- coding:utf-8 -*-

import py2neo
from py2neo import Graph, authenticate, Node, Relationship

HOST = "119.29.181.224"
PORT = "7474"
USER = "neo4j"
PASS = "22sinx*cosx"


class DBGraph():
    def __init__(self):
        authenticate("%s:%s" % (HOST, PORT), USER, PASS)
        self.db = Graph("http://%s:%s/db/data/" % (HOST, PORT))

    # def insert_nodes(self, datum):
    #     for data in datum:
    #         self.insert_node(data["label"], data["name"])

    def insert_node(self, label, name, attrs=()):
        node = Node(label, name=name)
        for attr in attrs:
            node[attr["key"]] = attr["value"]
        self.db.create(node)
        return node

    # def build_relations(self, relations):
    #     for relation in relations:
    #         src = relation["src"]
    #         isA = relation["isA"]
    #         dst = relation["dst"]
    #         attrs = relation["attrs"]
    #         self.build_relation(src, isA, dst, attrs)

    # def build_bidirectional_relations(self, relations):
    #     for relation in relations:
    #         src = relation["src"]
    #         isA = relation["isA"]
    #         dst = relation["dst"]
    #         attrs = relation["attrs"]
    #         self.build_relation(src, isA, dst, attrs)
    #         attrs = relation["antiAttrs"]
    #         self.build_relation(dst, isA, src, attrs)

    def build_relation(self, node1, node2, rel1, rel2="", attr1=(), attr2=()):
        relation = Relationship(node1, rel1, node2)
        for attr in attr1:
            relation[attr["key"]] = attr["value"]
        self.db.create(relation)

        if 0 == len(rel2):
            return
        else:
            relation = Relationship(node2, rel2, node1)
            for attr in attr2:
                relation[attr["key"]] = attr["value"]
            self.db.create(relation)

    def find_node(self, label, property_key="", property_value=""):
        if 0 == len(property_key):
            result_node = self.db.find_one(
                label=label
            )
        else:
            result_node = self.db.find_one(
                label=label,
                property_key=property_key,
                property_value=property_value
            )

        return result_node

    def find_nodes(self):
        pass

    def match_relation(self):
        pass

    def match_relations(self):
        pass

    def process(self):
        label = "submartet_加热"
        a = Node(label=label, name='Alice')
        self.db.create(a)
        find_code_1 = self.db.find_one(label="submartet_加热")
        print find_code_1

        # push 更新属性

        # match_relation = self.db.match_one(rel_type="has_itemid")
        # print match_relation
        # cnt = 1
        # for i in match_relation:
        #     if cnt < 4:
        #         print cnt
        #         print i
        #         print i.start_node()
        #         print i.end_node()
        #         print i.relationships()
        #         print i.nodes()
        #         # i['count'] += 1
        #         # test_graph.push(i)
        #         print "===================="
        #     cnt += 1
        # print cnt

        pass

    def start(self):
        self.process()


if __name__ == '__main__':
    obj = DBGraph()
    obj.start()
