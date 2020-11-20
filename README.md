# iGenius Adapters SDK

This is the Software Development Kit for iGenius Web Connectors development.  
You can use our SDK in your project to be able to handle correctly the data structures that will be used by iGenius services to call your web connector adapter.

## How to install

With Poetry

```bash
poetry add igenius-adapters-sdk
```

With pip

```bash
pip install igenius-adapters-sdk
```

## How to develop

You can bootstrap your environment running

```bash
poetry install
```

## Folder structure

Our SDK has the main objective to expose our data structures that are the business objects of our application: we call them `Entities` and thet are included in a package with the same name.

```bash
-- src
   |- igenius_adapters_sdk
      |- entities
```

## Data structure

Our datasource adapters system is based on a relational database structure, so our `entities` are a mapping of this kind of data organisation.

## Entities

`Entities` can be simple Python custom types or Pydantic models. The second option give the great possibility to be able to define our `Entities` using Python code, with great validation capabilities at runtime.

You can use our entities as a contract between our backend services and your datasource connector. In this way you can verify the correctness both of the input and the output of your API endpoint.

### Collections

Collections is a structured set of data such as a database table or CSV file.

```python
class Collection(BaseModel):
    uid: str
    attributes_schema: AttributesSchema
```

#### AttributesSchema

Attributes schema provides information on the available data and its type.

```python
class Attribute(BaseModel):
    uid: str
    type: AttributeType
```

#### AttributeTypes

Attribute types provide a way to determine if a certain action is available on the attribute. There are 4 main attribute types and UNKNOWN for all that do not fall into the previous 4 categories. Attribute types are unified way between different adapters to describe data source schema.

* boolean: The boolean attribute has true/ false state. Eg. BOOLEAN type in PostgreSQL but RAW(1) in Oracle databases.
* categorical: Every attribute that can hold characters. Eg. VARCHAR, TEXT.
* datetime: Every attribute that can hold information about the date. Eg. DATE, TIMESTAMP.
* numeric: Every attribute that can hold numeric values. Eg. INT, FLOAT, DECIMAL.
* unknown: Special attribute type for those whose data and possible operations on them isn't clear. Eg. ROWID, JSONB.

```python
class AttributeType(str, Enum):
    BOOLEAN = 'crystal.topics.data.attribute-types.boolean'
    CATEGORICAL = 'crystal.topics.data.attribute-types.categorical'
    DATETIME = 'crystal.topics.data.attribute-types.datetime'
    NUMERIC = 'crystal.topics.data.attribute-types.numeric'
    UNKNOWN = 'crystal.topics.data.attribute-types.unknown'
```

### URIs

#### Function URI

Informs about the function to be used, its type, and optionally for binning provides parameters.

```python
class FunctionUri(BaseModel):
    function_type: Literal['group_by', 'aggregation']
    function_uid: str
    function_params: Optional[Union[numeric_binning.BinningRules]]
```

#### Data source URI

Informs about the data source that is used.

```python
class DatasourceUri(UriModel):
    datasource_uid: DatasourceUid
```

#### Collection URI

Informs about the collection that is used.

```python
class CollectionUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid
```

#### Attribute URI

Informs about the data source, collection, and attribute that is used.

```python
Uid = str

AttributeUid = NewType('AttributeUid', Uid)
CollectionUid = NewType('CollectionUid', Uid)
DatasourceUid = NewType('DatasourceUid', Uid)


class AttributeUri(UriModel):
    datasource_uid: DatasourceUid
    collection_uid: CollectionUid
    attribute_uid: AttributeUid
```

### Data attributes

#### Order attribute

Determines the order of the result data if provided.

```python
class OrderByDirection(str, Enum):
    DESC = 'desc'
    ASC = 'asc'

class OrderByAttribute(BaseModel):
    alias: str
    direction: OrderByDirection = OrderByDirection.ASC
```

#### Static value

Provides raw data from an attribute.

```python
class StaticValueAttribute(BaseModel):
    value: str
    alias: str
```

#### Base attribute

Attribute model that is followed by Aggregation and GroupBy Attribute.

```python
class BaseAttribute(BaseModel, abc.ABC):
    attribute_uri: uri.AttributeUri
    alias: str
```

#### Aggregation attribute

Provides aggregated data as a result.

```python
class AggregationAttribute(BaseAttribute):
    function_uri: FunctionUri
```

#### Binning attribute

Provides binned data as a result.

```python
class BinningAttribute(BaseAttribute):
    function_uri: FunctionUri
```

### Numeric binning

Binning provides a way to capture different values into different bins and return the result in one query.

#### Bin

Informs at what ranges the bin operates.

```python
Number = Union[float, int]


class Bin(BaseModel):
    ge: Optional[Number]
    lt: Optional[Number]
```

#### Binning rules

Binning rules is a set of bins, a minimal amount of bins is 2.

```python
class BinningRules(BaseModel):
    bins: List[Bin]
```

### Parameters

#### Operation Properties Schema

Provides properties for operation.  
For example, checking if the value is greater than 7, requires function 'greater than' and single value '7'.

```python
class OperationPropertiesSchema:
    class NoValue(BaseModel):
        class Config:
            extra = Extra.forbid

    class SingleValue(BaseModel):
        data: str

        class Config:
            extra = Extra.forbid

    class RangeValue(BaseModel):
        start: str
        end: str

        class Config:
            extra = Extra.forbid
```

#### Operation Schema Spec

Connects operation model with its schema.

```python
class OperationSchemaSpec(BaseModel):
    model: Type[BaseModel]
    jsonschema: Mapping[str, Any]

    class Config:
        arbitrary_types_allowed = True
```

#### Operation Schemas

Provides information on the requested operations.

```python
class OperationSchemas:
    NO_VALUE = OperationSchemaSpec(
        model=OperationPropertiesSchema.NoValue,
        jsonschema=OperationPropertiesSchema.NoValue.schema(),
    )
    SINGLE_VALUE = OperationSchemaSpec(
        model=OperationPropertiesSchema.SingleValue,
        jsonschema=OperationPropertiesSchema.SingleValue.schema(),
    )
    RANGE_VALUE = OperationSchemaSpec(
        model=OperationPropertiesSchema.RangeValue,
        jsonschema=OperationPropertiesSchema.RangeValue.schema(),
    )
```

#### Parameter Operation Spec

Provides information on what operation needs what parameters.

```python
class ParamOperationSpecs(BaseModel):
    uid: Uid = Field(..., description='uid of the operation')
    i18n: I18n
    properties_schema: Mapping[str, Any] = Field(
        ..., description='jsonschema of expected payload when using the operation'
    )
```

#### Equal

Provided single value checks if the record is equal to that value.

```python
EQUAL = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.equal',
    i18n=I18n(
        name='crystal.topics.data.param-operation.equal.i18n.name',
        description='crystal.topics.data.param-operation.equal.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Different

Provided single value checks if the record is different from that value.

```python
DIFFERENT = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.different',
    i18n=I18n(
        name='crystal.topics.data.param-operation.different.i18n.name',
        description='crystal.topics.data.param-operation.different.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Greater than

Provided single value checks if the record is greater than that value.

```python
GREATER_THAN = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.greater-than',
    i18n=I18n(
        name='crystal.topics.data.param-operation.greater-than.i18n.name',
        description='crystal.topics.data.param-operation.greater-than.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Less than

Provided single value checks if the record is lesser than that value.

```python
LESS_THAN = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.less-than',
    i18n=I18n(
        name='crystal.topics.data.param-operation.less-than.i18n.name',
        description='crystal.topics.data.param-operation.less-than.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Greater than or equal to

Provided single value checks if the record is greater than or equal to that value.

```python
GREATER_THAN_OR_EQUAL_TO = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.greater-than-or-equal-to',
    i18n=I18n(
        name='crystal.topics.data.param-operation.greater-than-or-equal-to.i18n.name',
        description='crystal.topics.data.param-operation.greater-than-or-equal-to.i18n.description'  # noqa: E501
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Less than or equal to

Provided single value checks if the record is lesser than or equal to that value.

```python
LESS_THAN_OR_EQUAL_TO = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.less-than-or-equal-to',
    i18n=I18n(
        name='crystal.topics.data.param-operation.less-than-or-equal-to.i18n.name',
        description='crystal.topics.data.param-operation.less-than-or-equal-to.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Between

Provided two values checks if the record is between those values.

```python
BETWEEN = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.between',
    i18n=I18n(
        name='crystal.topics.data.param-operation.between.i18n.name',
        description='crystal.topics.data.param-operation.between.i18n.description'
    ),
    properties_schema=OperationSchemas.RANGE_VALUE.jsonschema,
)
```

#### Contains

Provided single value checks if the record contains that value.

```python
CONTAINS = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.contains',
    i18n=I18n(
        name='crystal.topics.data.param-operation.contains.i18n.name',
        description='crystal.topics.data.param-operation.contains.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### IN

Provided multiple value checks if the record contains one or more of those values.

```python
IN = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.in',
    i18n=I18n(
        name='crystal.topics.data.param-operation.in.i18n.name',
        description='crystal.topics.data.param-operation.in.i18n.description'
    ),
    properties_schema=OperationSchemas.MULTIPLE_VALUE.jsonschema,
)
```

#### Not contains

Provided single value checks if the record does not contain that value.

```python
NOT_CONTAINS = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.not-contains',
    i18n=I18n(
        name='crystal.topics.data.param-operation.not-contains.i18n.name',
        description='crystal.topics.data.param-operation.not-contains.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Starts with

Provided single value checks if the record starts with that value.

```python
STARTS_WITH = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.starts-with',
    i18n=I18n(
        name='crystal.topics.data.param-operation.starts-with.i18n.name',
        description='crystal.topics.data.param-operation.starts-with.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Ends with

Provided single value checks if the record ends with that value.

```python
ENDS_WITH = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.ends-with',
    i18n=I18n(
        name='crystal.topics.data.param-operation.ends-with.i18n.name',
        description='crystal.topics.data.param-operation.ends-with.i18n.description'
    ),
    properties_schema=OperationSchemas.SINGLE_VALUE.jsonschema,
)
```

#### Empty

Provided no values checks if the record is empty.

```python
EMPTY = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.empty',
    i18n=I18n(
        name='crystal.topics.data.param-operation.empty.i18n.name',
        description='crystal.topics.data.param-operation.empty.i18n.description'
    ),
    properties_schema=OperationSchemas.NO_VALUE.jsonschema,
)
```

#### Not empty

Provided no values checks if the record is not empty.

```python
NOT_EMPTY = ParamOperationSpecs(
    uid='crystal.topics.data.param-operation.not-empty',
    i18n=I18n(
        name='crystal.topics.data.param-operation.not-empty.i18n.name',
        description='crystal.topics.data.param-operation.not-empty.i18n.description'
    ),
    properties_schema=OperationSchemas.NO_VALUE.jsonschema,
)
```

### Aggregation functions

Each aggregation function is an entity that follows the same model as GroupBy function

```python
class AttributeFunctionSpecs(BaseModel):
    uid: Uid
    i18n: I18n
```

Aggregation function maps function_uid in aggregation block to right function based on its uid field.

#### Identity

Answers question: What is the identity of the data?

```python
IDENTITY = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.identity',
    i18n=I18n(
        name='crystal.topics.data.aggregation.identity.i18n.name',
        description='crystal.topics.data.aggregation.identity.i18n.description',
    )
)
```

#### Average

Answers question: What is the average value of the data?

```python
AVG = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.avg',
    i18n=I18n(
        name='crystal.topics.data.aggregation.avg.i18n.name',
        description='crystal.topics.data.aggregation.avg.i18n.description',
    )
)
```

#### Count

Answers question: How many times did condition occur?

```python
COUNT = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.count',
    i18n=I18n(
        name='crystal.topics.data.aggregation.count.i18n.name',
        description='crystal.topics.data.aggregation.count.i18n.description',
    )
)
```

#### Sum

Answers question: What is the sum of the data?

```python
SUM = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.sum',
    i18n=I18n(
        name='crystal.topics.data.aggregation.sum.i18n.name',
        description='crystal.topics.data.aggregation.sum.i18n.description',
    )
)
```

#### Distinct count

Answers question: How many times did condition occur for distinct records?

```python
DISTINCT_COUNT = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.distinct-count',
    i18n=I18n(
        name='crystal.topics.data.aggregation.distinct-count.i18n.name',
        description='crystal.topics.data.aggregation.distinct-count.i18n.description',
    )
)
```

#### Minimal value

Answers question: What is the minimum value of the data?

```python
MIN = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.min',
    i18n=I18n(
        name='crystal.topics.data.aggregation.min.i18n.name',
        description='crystal.topics.data.aggregation.min.i18n.description',
    )
)
```

#### Maximal value

Answers question: What is the maximal value of the data?

```python
MAX = AttributeFunctionSpecs(
    uid='crystal.topics.data.aggregation.max',
    i18n=I18n(
        name='crystal.topics.data.aggregation.max.i18n.name',
        description='crystal.topics.data.aggregation.max.i18n.description',
    )
)
```

### GroupBy Functions

Each GroupBy function is an entity that follows the same model as an aggregation function

```python
class AttributeFunctionSpecs(BaseModel):
    uid: Uid
    i18n: I18n
```

GroupBy function maps function_uid in groups block to right function based on its uid field.

#### Identity

Groups record together when values of the given field are identical.

```python
IDENTITY = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.identity',
    i18n=I18n(
        name='crystal.topics.data.group-by.identity.i18n.name',
        description='crystal.topics.data.group-by.identity.i18n.description',
    )
)
```

#### Same day

Groups record together when Datetime field values are on the same day.

```python
DATE_TRUNC_DAY = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-day',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-day.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-day.i18n.description',
    )
)
```

#### Same week

Groups record together when Datetime field values are on the same week.

```python
DATE_TRUNC_WEEK = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-week',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-week.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-week.i18n.description',
    )
)
```

#### Same month

Groups record together when Datetime field values are on the same month.

```python
DATE_TRUNC_MONTH = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-month',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-month.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-month.i18n.description',
    )
)
```

#### Same quarter

Groups record together when Datetime field values are in the same quarter.

Jan, Feb, Mar is the first quarter, etc.

```python
DATE_TRUNC_QUARTER = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-quarter',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-quarter.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-quarter.i18n.description',
    )
)
```

#### Same semester

Groups record together when Datetime field values are on the same semester.

The semester is considered half of the year. Months from January to June is the first semester, July to December is the second semester.

```python
DATE_TRUNC_SEMESTER = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-semester',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-semester.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-semester.i18n.description',
    )
)
```

#### Same year

Groups record together when Datetime field values are on the same year.

```python
DATE_TRUNC_YEAR = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.date-trunc-year',
    i18n=I18n(
        name='crystal.topics.data.group-by.date-trunc-year.i18n.name',
        description='crystal.topics.data.group-by.date-trunc-year.i18n.description',
    )
)
```

#### Numeric binning

Groups record together when values of the given field are captured to the same bin.

Example: First bin contains records with field value between 0 and 300, while the second bin with a value between 301 and 600.

```python
NUMERIC_BINNING = AttributeFunctionSpecs(
    uid='crystal.topics.data.group-by.numeric_binning',
    i18n=I18n(
        name='crystal.topics.data.group-by.numeric_binning.i18n.name',
        description='crystal.topics.data.group-by.numeric_binning.i18n.description',
    )
)
```

### Joins

Join two collections on an attribute.

#### Join Type

Informs about the type of join that is used.

```python
class JoinType(str, Enum):
    INNER = 'inner'
    LEFT_OUTER = 'left-outer'
    RIGHT_OUTER = 'right-outer'
```

#### Join Part

Informs about the attribute and collection that is used.

```python
class JoinPart(BaseModel):
    from_: 'From'
    on: uri.AttributeUri
```

#### Join

Informs about the attributes, collections and type of the join that is used.

```python
class Join(BaseModel):
    left: JoinPart
    right: JoinPart
    type: JoinType
```

### Expressions

#### Expression

Informs about the type of expression and value used on the provided attribute.

```python
class Expression(BaseModel):
    attribute_uri: uri.AttributeUri
    operator: str
    value: Any
```

#### Multi Expression

Informs about the logical join between expressions.

```python
class CriteriaType(str, Enum):
    AND = 'and'
    OR = 'or'

class MultiExpression(BaseModel):
    criteria: CriteriaType
    expressions: List[Union['MultiExpression', Expression]]
```

#### Where Expression

Expressions that follow the SQL 'WHERE' statement.

```python
WhereExpression = Union[MultiExpression, Expression]
```

### Queries

Inform about the data source that is used, query statements, and order.

All queries follow BaseQuery model.

```python
class BaseQuery(BaseModel, abc.ABC):
    from_: From
    where: Optional[WhereExpression]
    order_by: Optional[List[data.OrderByAttribute]]
    limit: int = Field(None, gt=0)
    offset: int = Field(None, ge=0)
```

#### Select Query

Fetches simple data.

```python
class SelectQuery(BaseQuery):
    attributes: List[Union[data.ProjectionAttribute, data.StaticValueAttribute]]
    distinct: bool = False
```

#### Aggregation Query

Fetches aggregated data.

```python
class AggregationQuery(BaseQuery):
    aggregations: List[Union[data.AggregationAttribute, data.StaticValueAttribute]]
```

#### GroupBy Query

Fetches grouped data.

```python
class GroupByQuery(BaseQuery):
    aggregations: List[Union[data.AggregationAttribute, data.StaticValueAttribute]]
    groups: List[data.BinningAttribute]
```

#### Query

All used types of queries.

```python
Query = Union[GroupByQuery, AggregationQuery, SelectQuery]
```

### I18n translations

I18n model provides translations for the applications.

```python
class I18n(BaseModel):
    name: LocaliseKey
    description: LocaliseKey
```
### Description

Description of the data source is a process of gathering information on the available data and building its schema for further use during execution. One can call description on the /collections/actions/describe path. The response consists of a list of Collections.

Example POST payload:

```python
{
  "host": "oracle",
  "port": 1521,
  "username": "test",
  "password": "test",
  "database": "test.localdomain"
}
```

Example response payload:

```python
[ 
  {
    "uid": "test.customer",
    "attributes_schema": {
      "attributes": [
        {
          "uid": "id",
          "type": "crystal.topics.data.attribute-types.categorical"
        },
        {
          "uid": "name",
          "type": "crystal.topics.data.attribute-types.categorical"
        },
        {
          "uid": "creation",
          "type": "crystal.topics.data.attribute-types.datetime"
        },
        {
          "uid": "country",
          "type": "crystal.topics.data.attribute-types.categorical"
        },
        {
          "uid": "points",
          "type": "crystal.topics.data.attribute-types.numeric"
        }
      ]
    }
  }
]
```

Untangling this response: our test.localdomain oracle database has one table named test.customer that has columns: id, name, creation, country, and points.

Also, creation column is some sort of datetime field - exacts are Datasource dependant.

### Execution

Execution is the phase in which data is fetched from the data source using the adapter. Calls payload consists of connection_params that provide from which data source data will be fetched and query that informs about requested parameters.

path: `/query/actions/execute`

Example of `POST` payload:

```python
{
  "connection_params": {
    ...
  },
  "query": {
    ...
  }
}
```

#### Connection Params

Same as for description.

#### Query

A query is a unified across adapters JSON formatted way of describing what kind of data and how processed one wants to get. Names of the fields can be obtained in the description phase.

Example `POST` payload:

```python
{
  "from_": {
    "datasource_uid": "test_datasource_uid_66",
    "collection_uid": "test.customer"
  },
  "where": "None",
  "order_by": "None",
  "limit": "None",
  "offset": "None",
  "aggregations": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_193",
        "collection_uid": "test.customer",
        "attribute_uid": "points"
      },
      "alias": "alias_avg",
      "function_uri": {
        "function_type": "aggregation",
        "function_uid": "crystal.topics.data.aggregation.avg",
        "function_params": "None"
      }
    }
  ],
  "groups": [
    {
      "attribute_uri": {
        "datasource_uid": "test_datasource_uid_194",
        "collection_uid": "test.customer",
        "attribute_uid": "creation"
      },
      "alias": "alias_date_trunc_month",
      "function_uri": {
        "function_type": "group_by",
        "function_uid": "crystal.topics.data.group-by.date-trunc-month",
        "function_params": "None"
      }
    }
  ]
}
```

This request asks for average points grouped by the month of customer creation.

Example response payload:

```python
{
  "records": [
    {
      "alias_date_trunc_month": "2019-11-01T00:00:00",
      "alias_avg": 75
    },
    {
      "alias_date_trunc_month": "2019-08-01T00:00:00",
      "alias_avg": 64
    },
    {
      "alias_date_trunc_month": "2019-05-01T00:00:00",
      "alias_avg": 1
    },
    {
      "alias_date_trunc_month": "2020-02-01T00:00:00",
      "alias_avg": 66
    },
    {
      "alias_date_trunc_month": "2020-03-01T00:00:00",
      "alias_avg": 55
    }
  ]
}
```
