from fastapi import FastAPI
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL

from schema import type_defs

import json

query = QueryType()

@query.field('personList')
def resolve_persons(_, info, **arguments):
    print(json.dumps(arguments['or'], indent=4))
    return [{ 'id': 3, 'name': 'Marcus' }]

schema = make_executable_schema(type_defs, query)

app = FastAPI()

app.mount('/graphql/', GraphQL(schema, debug=True))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='app:app', host='0.0.0.0', port=3000, reload=True)