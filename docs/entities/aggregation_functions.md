# Aggregation functions

Aggregation functions are structured in a similar way to [GroupBy Functions](groupby_functions.md).
Each aggregation function is an entity with an unique identifier and an [i18n](i18n_translations.md) entity for the relative translation.  
All the described entities are available in the `igenius_adapters_sdk.entities.attribute` package.

```python
class AttributeFunctionSpecs(BaseModel):
    uid: Uid
    i18n: I18n
```

Aggregation function maps function_uid in aggregation block to right function based on its uid field.

## Identity

Answers question: What is the identity of the data?

```python
IDENTITY = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.identity",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-identity",
        description="crystal.topics.data.aggregation.identity.i18n.description",
    ),
)
```

## Average

Answers question: What is the average value of the data?

```python
AVG = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.avg",
    i18n=I18n(
        name="cons-configure-data-editor-agg-fun-average",
        description="crystal.topics.data.aggregation.avg.i18n.description",
    ),
)
```

## Count

Answers question: How many times did condition occur?

```python
COUNT = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.count",
    i18n=I18n(
        name="cons-configure-data-editor-agg-fun-count",
        description="crystal.topics.data.aggregation.count.i18n.description",
    ),
)
```

## Sum

Answers question: What is the sum of the data?

```python
SUM = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.sum",
    i18n=I18n(
        name="cons-configure-data-editor-agg-fun-sum",
        description="crystal.topics.data.aggregation.sum.i18n.description",
    ),
)
```

## Distinct count

Answers question: How many times did condition occur for distinct records?

```python
DISTINCT_COUNT = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.distinct-count",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-distinct-count",
        description="crystal.topics.data.aggregation.distinct-count.i18n.description",
    ),
)
```

## Minimal value

Answers question: What is the minimum value of the data?

```python
MIN = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.min",
    i18n=I18n(
        name="cons-configure-data-editor-agg-fun-min",
        description="crystal.topics.data.aggregation.min.i18n.description",
    ),
)
```

## Maximal value

Answers question: What is the maximal value of the data?

```python
MAX = AttributeFunctionSpecs(
    uid="crystal.topics.data.aggregation.max",
    i18n=I18n(
        name="cons-configure-data-editor-agg-fun-max",
        description="crystal.topics.data.aggregation.max.i18n.description",
    ),
)
```