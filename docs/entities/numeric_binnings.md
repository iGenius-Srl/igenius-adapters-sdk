# Numeric binnings

Binning provides a way to capture different values into different bins and return the result in one query.

## Bin

Informs at what ranges the bin operates.

```python
Number = Union[float, int]


class Bin(BaseModel):
    ge: Optional[Number]
    lt: Optional[Number]
```

## Binning rules

Binning rules is a set of bins, a minimal amount of bins is 2.

```python
class BinningRules(BaseModel):
    bins: List[Bin]
```
