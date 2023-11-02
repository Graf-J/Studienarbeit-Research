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

        connectPersonToPersonViaFriend(from: ID!, to: ID!, data: AddPersonToPersonFriendEdgeInput!): Boolean
        disconnectPersonFromPersonViaFriend(from: ID!, to: ID!): Boolean
        updatePersonToPersonViaFriend(from: ID!, to: ID!, data: UpdatePersonToPersonFriendEdgeInput!): Boolean

        connectPersonToHobbyViaPerform(from: ID!, to: ID!): Boolean
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
        ): [PersonToPersonFriendEdge!]!
        perform(
            or: Or,
            and: And,
            where: Where,
            orderBy: OrderBy,
            pagination: Pagination
        ): [PersonToHobbyPerformEdge!]!
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
        ): [HobbyToPersonPerformEdge!]!
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

# EDGES
personToPersonFriendEdge = """
    type PersonToPersonFriendEdge {
        strength: Float!
        person: Person!
    }
"""

personToHobbyPerformEdge = """
    type PersonToHobbyPerformEdge {
        hobby: Hobby!
    }
"""

hobbyToPersonPerformEdge = """
    type HobbyToPersonPerformEdge {
        person: Person!
    }
"""

addPersonToPersonFriendEdgeInput = """
    input AddPersonToPersonFriendEdgeInput {
        strength: Float!
    }
"""

updatePersonToPersonFriendEdgeInput = """
    input UpdatePersonToPersonFriendEdgeInput {
        strength: Float
    }
"""
# (for hobby there is no add / update Type, because it has no fields specified)

# LOGIC

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
    personToPersonFriendEdge,
    personToHobbyPerformEdge,
    hobbyToPersonPerformEdge,
    addPersonToPersonFriendEdgeInput,
    updatePersonToPersonFriendEdgeInput,
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

# To consider when implementing:
#   - If recursive Edge: only one Edge-Type necessary
#   - If no attributes for Edge: No data in addEdge-mutation and no update-mutation
#   - Check that no reserved keywords are used before generation (would fail to compile schema)
#   - Check that no duplicates will get generated (would fail to compile schema)
#   - Only one Edge per Label between Vertices possible (always check in advance if Edge alredy exists)