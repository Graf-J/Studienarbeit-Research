from neptune import GraphDB
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.process.traversal import P
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import Order

import json


# Create Test-Data-Set

# Create Vertices with Properties
def add_vertices():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        v = db.g.addV('person').property(
            'name', 'rosalie').property('age', '13').next()
        print(v.id)


# Query Vertixes with Projcet Queries
def query_vertices():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().hasLabel('person').project('id', 'label', 'name', 'age', 'sex') \
            .by(__.id_()) \
            .by(__.label()) \
            .by(__.values('name')) \
            .by(__.values('age')) \
            .by(__.coalesce(__.values('sex'), __.constant(None))) \
            .toList()

        print(json.dumps(res, indent=4))


# Advanced Query (has, order, pagination)
def query_vertices_advanced():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().hasLabel('person').has('age', P.gt('13')).has('age', P.lt(50)).project('id', 'label', 'name', 'age') \
            .by(__.id_()) \
            .by(__.label()) \
            .by(__.values('name')) \
            .by(__.values('age')) \
            .order().by('age', Order.desc).skip(0).limit(2).toList()

        print(json.dumps(res, indent=4))


# Connect Vertices with Edge with Label
def connect_vertices(from_vertex_id, to_vertex_id):
    with GraphDB('ws://localhost:8182/gremlin') as db:
        source_vertex = db.g.V(from_vertex_id).next()
        target_vertex = db.g.V(to_vertex_id).next()
        count = db.g.V(source_vertex).outE().hasLabel(
            'mariage').where(__.inV().has_id(target_vertex.id)).count().next()

        # Only add edge, if not already exists
        if count == 0:
            db.g.V(from_vertex_id).as_('source').V(to_vertex_id).as_('target') \
                .addE('mariage').from_('source').to('target').property('strength', '0.98').iterate()
        else:
            print('Edge already exists!')


# Disconnect Vertices with Edge with Label
def disconnect_vertices(from_vertex_id, to_vertex_id):
    with GraphDB('ws://localhost:8182/gremlin') as db:
        source_vertex = db.g.V(from_vertex_id).next()
        target_vertex = db.g.V(to_vertex_id).next()
        db.g.V(source_vertex).outE().hasLabel(
            'mariage').where(__.inV().has_id(target_vertex.id)).drop().iterate()


# Nested Query (out, in, coalesce)
def query_vertices_nested():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().has('name', 'stefan').project('id', 'name', 'mariage') \
            .by(__.id_()) \
            .by(__.values('name')) \
            .by(
                __.coalesce(
                    __.outE('mariage').has('strength', P.gt(
                        0.9)).inV().project('name', 'age')
                    .by(__.values('name'))
                    .by(__.values('age')),
                    __.constant(None))
        ).next()

        print(json.dumps(res, indent=4))


# Update Vertex
def update_vertex():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        db.g.V().has('name', 'lioba').property(
            'age', '42').property('sex', 'female').next()


# Delete Vertex
def delete_vertex():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        db.g.V().has('name', 'rosalie').drop().iterate()


# Query Complex Conditions
def query_conditions():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().or_(
            __.has('name', 'lioba'),
            __.has('name', 'stefan'),
            __.and_(
                __.has('age', P.lt('22')),
                __.has('age', P.gt('15'))
            )
        ).values('name').toList()

        print(res)


def query_with_edges():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().has('name', 'stefan').project('id', 'name', 'mariage') \
            .by(__.id_()) \
            .by(__.values('name')) \
            .by(
                __.outE('mariage').has('strength', P.gt(0.9)).where(
                    __.inV().has('name', 'lioba')).project('strength', 'person')
                .by(__.values('strength'))
                .by(
                    __.inV().project('name', 'age')
                    .by(__.values('name'))
                        .by(__.values('age'))
                ).fold()
        ).next()

        print(json.dumps(res, indent=4))


def query_with_edges_with_order():
    with GraphDB('ws://localhost:8182/gremlin') as db:
        res = db.g.V().has('name', 'stefan').project('id', 'name', 'mariage') \
            .by(__.id_()) \
            .by(__.values('name')) \
            .by(
                __.outE('mariage').has('strength', P.gt("0.7")).where(
                    __.inV().has('name', P.neq('Fish'))).order().by('strength', Order.asc).by(__.inV().values('age'), Order.desc).project('strength', 'person')
                .by(__.values('strength'))
                .by(
                    __.inV().project('name', 'age')
                    .by(__.values('name'))
                        .by(__.values('age'))
                ).fold()
        ).next()

        print(json.dumps(res, indent=4))


def update_edge(from_vertex_id, to_vertex_id):
    with GraphDB('ws://localhost:8182/gremlin') as db:
        source_vertex = db.g.V(from_vertex_id).next()
        target_vertex = db.g.V(to_vertex_id).next()
        db.g.V(source_vertex).outE().hasLabel(
            'mariage').where(__.inV().has_id(target_vertex.id)).property('strength', '0.8').iterate()


def main():
    # query_vertices()
    # query_vertices_advanced()
    # connect_vertices(20520, 12392)
    # query_vertices_nested()
    # update_vertex()
    # delete_vertex()
    # query_conditions()
    # disconnect_vertices(20520, 8296)
    # query_with_edges()
    update_edge(20520, 8296)
    query_with_edges_with_order()


if __name__ == '__main__':
    main()
