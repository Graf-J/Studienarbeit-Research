from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from gremlin_python.process.traversal import T


class GraphDB:
    def __init__(self, uri):
        self.uri = uri

    @property
    def g(self):
        return self._g

    def get_vertex_by_label(self, label: str, limit: int = 0, valueMap=False) -> list:
        query = self.g.V().hasLabel(label)

        if limit > 0:
            query.limit(limit)

        if valueMap:
            query.valueMap()

        return query.toList()

    def add_vertex(self, label: str, properties: dict):
        query = self.g.addV(label)

        # Add Properties (either as a list or as a string)
        for key, value in properties.items():
            if isinstance(value, list):
                for prop in value:
                    query.property(key, str(prop))
            else:
                query.property(key, str(value))

        # Execute Query and return Vertex
        x = query.next()
        print(dir(x))
        print(type(x.id))
        print(x.label)
        return x

    def __enter__(self):
        self.connection = DriverRemoteConnection(self.uri, 'g')
        self._g = Graph().traversal().withRemote(self.connection)

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()
