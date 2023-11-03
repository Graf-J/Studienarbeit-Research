from unittest.mock import Mock
from graph import GraphDirector, Vertex, Edge

class StateStack:
    current_vertex: Vertex
    current_edge: Edge

    def push(element):
        pass

    def pop():
        pass

def main():
    config = {'vertices': [{'label': 'Person', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}, {'name': 'age', 'datatype': 'Int', 'required': True}]}, {'label': 'Hobby', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}]}], 'edges': [{'label': 'perform', 'source': 'Person', 'target': 'Hobby', 'properties': []}]}
    graph = GraphDirector.construct(config)

    # This happens inside the Resolver
    currentVertex = graph.get_vertex('Person')


def build_gremlin_query_entry_list(g, selections):
    fields = [selection.name.value for selection in selections]

    g = g.V().hasLabel(StateStack.current_vertex.label).project(*fields)

    g = build_projection_query_vertex(g, selections, fields)

    return g


def build_gremlin_query_entry_single(g, selections):
    g.V()


def build_projection_query_vertex(g, selections, fields):
    for idx, field in enumerate(fields):
        field_type = StateStack.current_vertex.get_type(field)
        if field_type.type == 'property':
            if field_type.name == 'id':
                g.by(__.id_())
            elif field_type.name == 'label':
                g.by(__.label())
            else:
                if field_type.required:
                    g.by(__.values(field))
                else:
                    g.by(__.coalesce(__.values(field), None))
        elif field.type == 'outEdge':
            StateStack.push(StateStack.current_vertex.get_out_edge(field))
            g = build_out_query()
        else:
            g = build_in_query()

def build_out_query():
    pass

def build_in_query():
    pass


if __name__ == '__main__':
    main()