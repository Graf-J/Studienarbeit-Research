# BASE TYPES

query = """
    type Query {
        person(id: ID!): Person
        personList(
            or: Or,
            and: And,
            where: Where,
            orderBy: [OrderBy!],
            pagination: Pagination
        ): [Person!]!

        hobby(id: ID!): Hobby
        hobbyList(
            or: Or,
            and: And,
            where: Where,
            orderBy: [OrderBy!],
            pagination: Pagination
        ): [Hobby!]!
    }
"""

mutation = """
    type Mutation {
        addPerson(person: AddPersonInput): ID!
        updatePerson(id: ID!, person: UpdatePersonInput): ID!
        deletePerson(id: ID!): ID!

        connectPersonToPersonViaFriend(from: ID!, to: ID!): [ID!]!
        disconnectPersonFromPersonViaFriend(from: ID!, to: ID!): Boolean
        connectPersonToHobbyViaPerform(from: ID!, to: ID!): [ID!]!
        disconnectPersonFromHobbyViaPerform(from: ID!, to: ID!): Boolean

        addHobby(hobby: AddHobbyInput): ID!
        updateHobby(id: ID!, hobby: UpdateHobbyInput): ID!
        deleteHobby(id: ID!): ID!
    }
"""

# VERTICES

person = """
    type Person {
        id: ID!
        label: String!
        name: String!
        age: Int
        friend(
            or: Or,
            and: And,
            where: Where,
            orderBy: OrderBy,
            pagination: Pagination
        ): [Person!]!
        perform(
            or: Or,
            and: And,
            where: Where,
            orderBy: OrderBy,
            pagination: Pagination
        ): [Hobby!]!
    }
"""

addPersonInput = """
    input AddPersonInput {
        name: String!
        age: Int
    }
"""

updatePersonInput = """
    input UpdatePersonInput {
        name: String
        age: Int
    }
"""

hobby = """
    type Hobby {
        id: ID!
        label: String!
        name: String!
        perform(
            or: Or,
            and: And,
            where: Where,
            orderBy: OrderBy,
            pagination: Pagination
        ): [Person!]!
    }
"""

addHobbyInput = """
    input AddHobbyInput {
        name: String!
    }
"""

updateHobbyInput = """
    input UpdateHobbyInput {
        name: String
    }
"""

# STATEMENTS

where = """
    input Where {
        property: String!
        predicate: Predicate!
        value: String!
    }
"""

_or = """
    input Or {
        statements: [Where!]
        or: Or
        and: And
    }
"""

_and = """
    input And {
        statements: [Where!]
        or: Or
        and: And
    }
"""

predicate = """
    enum Predicate {
        GT,
        GRE,
        LT,
        LTE,
        EQ,
        NEQ
    }
"""

operator = """
    enum Operator {
        AND,
        OR
    }
"""

orderBy = """
    input OrderBy {
        property: String!
        order: Order!
    }
"""

order = """
    enum Order {
        ASC,
        DESC
    }
"""

pagination = """
    input Pagination {
        page: Int!
        pageSize: Int!
    }
"""

type_defs = [
    query,
    mutation,
    person,
    addPersonInput,
    updatePersonInput,
    hobby,
    addHobbyInput,
    updateHobbyInput,
    _or,
    _and,
    where,
    predicate,
    operator,
    orderBy,
    order,
    pagination
]