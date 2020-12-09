# Parameters

## Operation Properties Schema

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

## Operation Schema Spec

Connects operation model with its schema.

```python
class OperationSchemaSpec(BaseModel):
    model: Type[BaseModel]
    jsonschema: Mapping[str, Any]

    class Config:
        arbitrary_types_allowed = True
```

## Operation Schemas

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

## Parameter Operation Spec

Provides information on what operation needs what parameters.

```python
class ParamOperationSpecs(BaseModel):
    uid: Uid = Field(..., description='uid of the operation')
    i18n: I18n
    properties_schema: Mapping[str, Any] = Field(
        ..., description='jsonschema of expected payload when using the operation'
    )
```

## Equal

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

## Different

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

## Greater than

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

## Less than

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

## Greater than or equal to

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

## Less than or equal to

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

## Between

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

## Contains

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

## IN

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

## Not contains

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

## Starts with

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

## Empty

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

## Not empty

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
