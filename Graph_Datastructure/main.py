from graph import GraphDirector
import json


def main():
    # graph = GraphDirector.construct_mockdata()

    config = {'vertices': [{'label': 'Person', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}, {'name': 'age', 'datatype': 'Int', 'required': True}]}, {'label': 'Hobby', 'properties': [{'name': 'id', 'datatype': 'ID', 'required': True}, {'name': 'label', 'datatype': 'String', 'required': True}, {'name': 'name', 'datatype': 'String', 'required': True}]}], 'edges': [{'label': 'perform', 'source': 'Person', 'target': 'Hobby', 'properties': []}]}
    graph = GraphDirector.construct(config)

    # print(graph)
    print(json.dumps(graph.to_dict(), indent=4))



if __name__ == '__main__':
    main()
