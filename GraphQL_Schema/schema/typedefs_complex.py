# BASE TYPES

Query = """
    type Query {
        person(id: ID!): Person
        personList(
            vertexLogic: PersonVertexLogic
            orderBy: [PersonVertexOrderBy!]
            pagination: Pagination
        ): [Person!]!

        hobby(id: ID!): Hobby
        hobbyList(
            vertexLogic: PersonVertexLogic
            orderBy: [PersonVertexOrderBy!]
            pagination: Pagination
        ): [Hobby!]!
    }
"""

Mutation = """
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

Person = """
    type Person {
        id: ID!
        label: String!
        name: String!
        age: Int
        friendOut(
            vertexLogic: PersonVertexLogic
            edgeLogic: PersonToPersonFriendEdgeLogic
            vertexOrderBy: [PersonVertexOrderBy!]
            edgeOrderBy: [PersonToPersonFriendEdgeOrderBy!]
            pagination: Pagination
        ): [PersonToPersonFriendEdge!]!
        friendIn(
            vertexLogic: PersonVertexLogic
            edgeLogic: PersonToPersonFriendEdgeLogic
            vertexOrderBy: [PersonVertexOrderBy!]
            edgeOrderBy: [PersonToPersonFriendEdgeOrderBy!]
            pagination: Pagination
        ): [PersonToPersonFriendEdge!]!
        perform(
            vertexLogic: HobbyVertexLogic
            vertexOrderBy: [HobbyVertexOrderBy!]
            pagination: Pagination
        ): [PersonToHobbyPerformEdge!]!
    }
"""
# (no edge-logic and edge-orderby in perform, since perform has no attributes)

AddPersonInput = """
    input AddPersonInput {
        name: String!
        age: Int
    }
"""

UpdatePersonInput = """
    input UpdatePersonInput {
        name: String
        age: Int
    }
"""

Hobby = """
    type Hobby {
        id: ID!
        label: String!
        name: String!
        perform(
            vertexLogic: PersonVertexLogic
            orderBy: HobbyVertexOrderBy
            pagination: Pagination
        ): [HobbyToPersonPerformEdge!]!
    }
"""

AddHobbyInput = """
    input AddHobbyInput {
        name: String!
    }
"""

UpdateHobbyInput = """
    input UpdateHobbyInput {
        name: String
    }
"""

# EDGES
PersonToPersonFriendEdge = """
    type PersonToPersonFriendEdge {
        strength: Float!
        person(vertexLogic: PersonVertexLogic): Person!
    }
"""

PersonToHobbyPerformEdge = """
    type PersonToHobbyPerformEdge {
        hobby(vertexLogic: HobbyVertexLogic): Hobby!
    }
"""

HobbyToPersonPerformEdge = """
    type HobbyToPersonPerformEdge {
        person: Person!
    }
"""

AddPersonToPersonFriendEdgeInput = """
    input AddPersonToPersonFriendEdgeInput {
        strength: Float!
    }
"""

UpdatePersonToPersonFriendEdgeInput = """
    input UpdatePersonToPersonFriendEdgeInput {
        strength: Float
    }
"""
# (for hobby there is no add / update Type, because it has no fields specified)


# Properties

PersonVertexProperty = """
    enum PersonVertexProperty {
        name
        age
    }
"""

HobbyVertexProperty = """
    enum HobbyVertexProperty {
        name
    }
"""

PersonToPersonFriendEdgeProperty = """
    enum PersonToPersonFriendEdgeProperty {
        strength
    }
"""

# PERSONALIZED LOGIC

PersonVertexLogic = """
    input PersonVertexLogic {
        or: PersonVertexOr
        and: PersonVertexAnd
        where: PersonVertexWhere
    }
"""

PersonVertexWhere = """
    input PersonVertexWhere {
        property: PersonVertexProperty!
        predicate: Predicate!
        value: String!
    }
"""

PersonVertexAnd = """
    input PersonVertexAnd {
        statements: [PersonVertexWhere!]
        or: PersonVertexOr
        and: PersonVertexAnd
    }
"""

PersonVertexOr = """
    input PersonVertexOr {
        statements: [PersonVertexWhere!]
        or: PersonVertexOr
        and: PersonVertexAnd
    }
"""

PersonVertexOrderBy = """
    input PersonVertexOrderBy {
        property: PersonVertexProperty!
        order: Order!
        priority: Int
    }
"""

HobbyVertexLogic = """
    input HobbyVertexLogic {
        or: HobbyVertexOr
        and: HobbyVertexAnd
        where: HobbyVertexWhere
    }
"""

HobbyVertexWhere = """
    input HobbyVertexWhere {
        property: HobbyVertexProperty!
        predicate: Predicate!
        value: String!
    }
"""

HobbyVertexAnd = """
    input HobbyVertexAnd {
        statements: [HobbyVertexWhere!]
        or: HobbyVertexOr
        and: HobbyVertexAnd
    }
"""

HobbyVertexOr = """
    input HobbyVertexOr {
        statements: [HobbyVertexWhere!]
        or: HobbyVertexOr
        and: HobbyVertexAnd
    }
"""

HobbyVertexOrderBy = """
    input HobbyVertexOrderBy {
        property: HobbyVertexProperty!
        order: Order!
        priority: Int
    }
"""

PersonToPersonFriendEdgeLogic = """
    input PersonToPersonFriendEdgeLogic {
        or: PersonToPersonFriendEdgeOr
        and: PersonToPersonFriendEdgeAnd
        where: PersonToPersonFriendEdgeWhere
    }
"""

PersonToPersonFriendEdgeWhere = """
    input PersonToPersonFriendEdgeWhere {
        property: PersonToPersonFriendEdgeProperty!
        predicate: Predicate!
        value: String!
    }
"""

PersonToPersonFriendEdgeAnd = """
    input PersonToPersonFriendEdgeAnd {
        statements: [PersonToPersonFriendEdgeWhere!]
        or: PersonToPersonFriendEdgeOr
        and: PersonToPersonFriendEdgeAnd
    }
"""

PersonToPersonFriendEdgeOr = """
    input PersonToPersonFriendEdgeOr {
        statements: [PersonToPersonFriendEdgeWhere!]
        or: PersonToPersonFriendEdgeOr
        and: PersonToPersonFriendEdgeAnd
    }
"""

PersonToPersonFriendEdgeOrderBy = """
    input PersonToPersonFriendEdgeOrderBy {
        property: PersonToPersonFriendEdgeProperty!
        order: Order!
        priority: Int
    }
"""

# (no logic for perform Edge, since there are no properties)

# GENERAL LOGIC

Predicate = """
    enum Predicate {
        GT
        GRE
        LT
        LTE
        EQ
        NEQ
    }
"""

Order = """
    enum Order {
        ASC
        DESC
    }
"""

Pagination = """
    input Pagination {
        page: Int!
        pageSize: Int!
    }
"""

type_defs = [
    Query,
    Mutation,

    Person,
    AddPersonInput,
    UpdatePersonInput,
    PersonToPersonFriendEdge,
    PersonToHobbyPerformEdge,
    HobbyToPersonPerformEdge,
    AddPersonToPersonFriendEdgeInput,
    UpdatePersonToPersonFriendEdgeInput,
    Hobby,
    AddHobbyInput,
    UpdateHobbyInput,

    PersonVertexProperty,
    HobbyVertexProperty,
    PersonToPersonFriendEdgeProperty,

    PersonVertexLogic,
    PersonVertexWhere,
    PersonVertexOr,
    PersonVertexAnd,
    PersonVertexOrderBy,

    HobbyVertexLogic,
    HobbyVertexWhere,
    HobbyVertexOr,
    HobbyVertexAnd,
    HobbyVertexOrderBy,

    PersonToPersonFriendEdgeLogic,
    PersonToPersonFriendEdgeWhere,
    PersonToPersonFriendEdgeOr,
    PersonToPersonFriendEdgeAnd,
    PersonToPersonFriendEdgeOrderBy,

    Predicate,
    Order,
    Pagination
]

# To consider when implementing:
#   - If recursive Edge: only one Edge-Type necessary
#   - If no attributes for Edge: No data in addEdge-mutation and no update-mutation
#   - Check that no reserved keywords are used before generation (would fail to compile schema)
#   - Check that no duplicates will get generated (would fail to compile schema)
#   - Only one Edge per Label between Vertices possible (always check in advance if Edge alredy exists)
#   - OrderBy List can be specified in GraphQL-Query as Object. Ariadne translates it to List with length of one
#   - With JanusGraph do I not have to query by attribute when applying order to list
#   - [DISCUSS]: Statements, or, and are linked with the and_ internally:
#       * Advantage: Better readability with where and nice for short logic expressions
#       * Disadvantage: Can maybe be a little bit misleading
#   - weird edge names in type schema, to avoid edge label duplicate issues (field has to be unique in schema, but there may be more edges with the same name)
#       * <label>: if there are no name conflicts for vertex with in and outgoing edges (name as simple as possible for readability)
#       * <label>In | <label>|Out: if there is a name conflict for in and outgoing edges, but <label> only exists once for in and out edges
#       * <fromVertex><toVertex><label>: if there are multiple edges with same label, but is it clear if it's an incoming or outgoing edge
#       * <fromVertex><toVertex><label>In | <fromVertex><toVertex><label>Out: if there multiple edges with same label and in / out is not clear
#       -> constraint: between two vertex-types there can only be one edge-type with the same label
