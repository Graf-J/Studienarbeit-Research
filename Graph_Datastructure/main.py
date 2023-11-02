from graph import GraphDirector
import json

# TODO: Graph Repr Method
# TODO: UML Diagram


def main():
    # graph = GraphDirector.construct_mockdata()
    # print(graph.to_dict())
    # print(json.dumps(vars(graph), indent=4))    

    config = {'vertices': [{'label': 'Person', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}, {'name': 'age', 'datatype': 'Int', 'required': True}]}, {'label': 'Hobby', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}]}], 'edges': [{'label': 'perform', 'source': 'Person', 'target': 'Hobby', 'properties': []}]}
    graph = GraphDirector.construct(config)
    print(graph)



if __name__ == '__main__':
    main()
