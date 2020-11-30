# Collection

A `Collection` is a structured set of data such as a database table or CSV file.  
All the described entities are available in the `igenius_adapters_sdk.entities.collection` package.

```python
class Collection(BaseModel):
    uid: str
    attributes_schema: AttributesSchema
```

## Attributes

An `Attribute` schema provides information on the available data and its type.

```python
class Attribute(BaseModel):
    uid: str
    type: AttributeType
```

## AttributesSchema

An `AttributesSchema` contains a list of [`Attributes`](#attributes)

```python
class AttributesSchema(BaseModel):
    attributes: List[Attribute] = Field(default=list())
```

## AttributeTypes

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
