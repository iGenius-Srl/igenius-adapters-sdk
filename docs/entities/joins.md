# Joins

Join two collections on an attribute.

## Join Type

Informs about the type of join that is used.

```python
class JoinType(str, Enum):
    INNER = 'inner'
    LEFT_OUTER = 'left-outer'
    RIGHT_OUTER = 'right-outer'
```

## Join Part

Informs about the attribute and collection that is used.

```python
class JoinPart(BaseModel):
    from_: 'From'
    on: uri.AttributeUri
```

## Join

Informs about the attributes, collections and type of the join that is used.

```python
class Join(BaseModel):
    left: JoinPart
    right: JoinPart
    type: JoinType
```
