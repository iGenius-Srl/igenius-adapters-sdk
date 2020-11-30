# Expressions

Expressions are the entities needed to describe mathematical expressions involving binary operators like `=`, `AND` or `OR`. All the described entities are available in the `igenius_adapters_sdk.entities.query`.

## Expression

Informs about the type of expression and value used on the provided attribute.  
An `Expression` is used to map simple espressions between an [`igenius_adapters.sdk.entities.uri.AttributeUri`](uri.md#attribute-uri) and a scalar value.

```python
class Expression(BaseModel):
    attribute_uri: uri.AttributeUri
    operator: str
    value: Any
```

## Multi Expression

Informs about the logical join between expressions.  
With `MultiExpression` you can build complex expressions chaining multiple [`Expression`](#expression)s

```python
class CriteriaType(str, Enum):
    AND = 'and'
    OR = 'or'

class MultiExpression(BaseModel):
    criteria: CriteriaType
    expressions: List[Union['MultiExpression', Expression]]
```

## Where Expression

It's a 1:1 mapping that follow the SQL 'WHERE' statement.

```python
WhereExpression = Union[MultiExpression, Expression]
```
