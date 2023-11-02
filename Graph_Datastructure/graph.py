from enum import Enum
from abc import ABCMeta, abstractmethod


class Datatype(Enum):
    STRING = 'String'
    INT = 'Int'
    FLOAT = 'Float'
    BOOLEAN = 'Boolean'
    ID = 'ID'

    @classmethod
    def from_string(cls, value):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"No matching enum property found for '{value}'")


class Property:
    def __init__(self, name: str, datatype: Datatype, required: bool = True):
        self.name: str = name
        self.datatype: Datatype = datatype
        self.required: bool = required

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'datatype': self.datatype.value,
            'required': self.required
        }

    def __repr__(self) -> str:
        return f"{self.name}: {self.datatype.value}{'!' if self.required else ''}"


class Edge:
    def __init__(self, source_vertex: "Vertex", target_vertex: "Vertex", label: str, properties: [Property]):
        self.label: str = label
        self.source_vertex: "Vertex" = source_vertex
        self.target_vertex: "Vertex" = target_vertex
        self.properties: [Property] = properties

    @property
    def has_properties(self) -> int:
        return len(self.properties) != 0
    
    def to_dict(self):
        return {
            'label': self.label,
            'source': self.source_vertex.label,
            'target': self.target_vertex.label,
            'properties': [prop.to_dict() for prop in self.properties]
        }

    def __repr__(self):
        representation = f'({self.source_vertex.label}) '
        representation += f'---[{self.label}]---> '
        representation += f'({self.target_vertex.label})'

        return representation


class Vertex:
    def __init__(self, label: str, properties: [Property]):
        self.label = label
        self.properties = []
        # TODO: Check for duplicates within properties
        self.properties.extend(properties)
        self.out_edges = []
        self.in_edges = []

    def add_out_edge(self, edge: Edge):
        # TODO: Validations
        self.out_edges.append(edge)

    def add_in_edge(self, edge: Edge):
        # TODO: Validations
        self.in_edges.append(edge)

    def to_dict(self) -> dict:
        return {
            'label': self.label, 
            'properties': [prop.to_dict() for prop in self.properties]
        }

    def __repr__(self) -> str:
        # Label
        representation = f'\x1b[1;32mLabel\x1b[0m: {self.label}\n'
        # Properties
        representation += '\x1b[1;34mProperties\x1b[0m:\n'
        for prop in self.properties:
            representation += f"\t{repr(prop)}\n"
        # Out Edges
        representation += '\x1b[1;33mOut\x1b[0m:\n'
        for out_edge in self.out_edges:
            representation += f'\t{repr(out_edge)}\n'
        # In Edges
        representation += '\x1b[1;31mIn\x1b[0m:\n'
        for in_edge in self.in_edges:
            representation += f'\t{repr(in_edge)}\n'

        return representation


class Graph:
    def __init__(self):
        self.vertices: [Vertex] = []
        self.edges: [Edge] = []


    def get_vertex(self, label: str) -> Vertex:
        vertex = next((vertex for vertex in self.vertices if vertex.label == label), None)
        if vertex == None:
            raise Exception('Vertex not found')
        
        return vertex


    def to_dict(self) -> dict:
        return {
            'vertices': [vertex.to_dict() for vertex in self.vertices], 
            'edges': [edge.to_dict() for edge in self.edges]
        }


    def __repr__(self) -> str:
        representation = '-' * 50 + '\n\n'
        for vertex in self.vertices:
            representation += repr(vertex) + '\n'
            representation += '-' * 50 + '\n\n'

        return representation

    # TODO: Add methods to access vertices / edges and parse names


class IGraphBulider(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def add_vertex(vertex: Vertex):
        """Add Vertex to Graph"""

    @staticmethod
    @abstractmethod
    def add_edge(edge: Edge):
        """Add Edge to Graph"""

    @staticmethod
    @abstractmethod
    def build():
        """Returns the constructed Graph"""


class VertexBuilder:
    def __init__(self, graph_builder):
        self.graph_builder = graph_builder
        self.label = None
        self.properties = []

    def with_label(self, label: str):
        self.label = label

        return self

    def with_property(self, name: str, datatype: Datatype, required=True):
        self.properties.append(Property(name, datatype, required))

        return self

    def create(self):
        if self.label == None:
            raise Exception('Label not set')

        vertex = Vertex(self.label, self.properties)
        # TODO: Replace with Add Vertex Method of Graph (for checks)
        self.graph_builder.graph.vertices.append(vertex)

        return self.graph_builder

class EdgeBuilder:
    def __init__(self, graph_builder):
        self.graph_builder = graph_builder
        self.label = None
        self.properties = []
        self.source_vertex = None
        self.target_vertex = None

    def with_source(self, vertex_label: str):
        vertex = self.graph_builder.graph.get_vertex(vertex_label)
        self.source_vertex = vertex

        return self

    def with_target(self, vertex_label: str):
        vertex = self.graph_builder.graph.get_vertex(vertex_label)
        self.target_vertex = vertex

        return self

    def with_label(self, label: str):
        self.label = label

        return self

    def with_property(self, name: str, datatype: Datatype, required=True):
        self.properties.append(Property(name, datatype, required))

        return self

    def create(self):
        if self.label == None:
            raise Exception('Label not set')
        if self.source_vertex == None:
            raise Exception('Source Vertex not set')
        if self.target_vertex == None:
            raise Exception('Target Vertex not set')

        edge = Edge(self.source_vertex, self.target_vertex, self.label, self.properties)
        self.graph_builder.graph.edges.append(edge)
        edge.source_vertex.add_out_edge(edge)
        edge.target_vertex.add_in_edge(edge)

        return self.graph_builder


class GraphBuilder(IGraphBulider):
    def __init__(self):
        self.graph = Graph()

    def add_vertex(self) -> VertexBuilder:
        return VertexBuilder(self)

    def add_edge(self) -> EdgeBuilder:
        # TODO: Validation (no property with same name, no duplicate, not two in outEdge or inEdge with same label, ...)
        return EdgeBuilder(self)

    def build(self) -> Graph:
        # TODO: Gernerate custom edge names, generate id and label for vertices
        return self.graph


class GraphDirector:
    @staticmethod
    def construct_mockdata():
        graph = GraphBuilder() \
            .add_vertex() \
                .with_label('Person') \
                .with_property('name', Datatype.STRING, required=True) \
                .with_property('age', Datatype.INT, required=True) \
                .create() \
            .add_vertex() \
                .with_label('Hobby') \
                .with_property('name', Datatype.STRING, required=True) \
                .create() \
            .add_edge() \
                .with_source('Person') \
                .with_target('Hobby') \
                .with_label('perform') \
                .create() \
            .build()

        return graph
    
    @staticmethod
    def construct(config: dict):
        # TODO: Add config schema check
        builder = GraphBuilder()

        for vertex in config['vertices']:
            vertex_builder = builder.add_vertex().with_label(vertex['label'])
            for property in vertex['properties']:
                vertex_builder.with_property(property['name'], Datatype.from_string(property['datatype']), required=property['required'])
            vertex_builder.create()

        for edge in config['edges']:
            edge_builder = builder.add_edge().with_label(edge['label']).with_source(edge['source']).with_target(edge['target'])
            for property in edge['properties']:
                edge_builder.with_property(property['name'], Datatype.from_string(property['datatype']), required=property['required'])
            edge_builder.create()

        return builder.build()
            
