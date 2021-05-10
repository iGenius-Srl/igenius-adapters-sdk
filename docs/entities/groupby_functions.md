# GroupBy Functions

Aggregation functions are structured in a similar way to [Aggregation Functions](aggregation_functions.md).
Each group by function is an entity with an unique identifier and an [i18n](i18n_translations.md) entity for the relative translation.  
All the described entities are available in the `igenius_adapters_sdk.entities.attribute`.

```python
class AttributeFunctionSpecs(BaseModel):
    uid: Uid
    i18n: I18n
```

## Identity

Groups record together when values of the given field are identical.

```python
IDENTITY = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.identity",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-identity",
        description="crystal.topics.data.group-by.identity.i18n.description",
    ),
)
```

## Same day

Groups record together when Datetime field values are on the same day.

```python
DATE_TRUNC_DAY = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-day",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-day",
        description="crystal.topics.data.group-by.date-trunc-day.i18n.description",
    ),
)
```

## Same week

Groups record together when Datetime field values are on the same week.

```python
DATE_TRUNC_WEEK = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-week",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-week",
        description="crystal.topics.data.group-by.date-trunc-week.i18n.description",
    ),
)
```

## Same month

Groups record together when Datetime field values are on the same month.

```python
DATE_TRUNC_MONTH = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-month",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-month",
        description="crystal.topics.data.group-by.date-trunc-month.i18n.description",
    ),
)
```

## Same quarter

Groups record together when Datetime field values are in the same quarter.

Jan, Feb, Mar is the first quarter, etc.

```python
DATE_TRUNC_QUARTER = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-quarter",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-quarter",
        description="crystal.topics.data.group-by.date-trunc-quarter.i18n.description",
    ),
)
```

## Same semester

Groups record together when Datetime field values are on the same semester.

The semester is considered half of the year. Months from January to June is the first semester, July to December is the second semester.

```python
DATE_TRUNC_QUARTER = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-quarter",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-quarter",
        description="crystal.topics.data.group-by.date-trunc-quarter.i18n.description",
    ),
)
```

## Same year

Groups record together when Datetime field values are on the same year.

```python
DATE_TRUNC_YEAR = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.date-trunc-year",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-year",
        description="crystal.topics.data.group-by.date-trunc-year.i18n.description",
    ),
)
```

## Numeric binning

Groups record together when values of the given field are captured to the same bin.

Example: First bin contains records with field value between 0 and 300, while the second bin with a value between 301 and 600.

```python
NUMERIC_BINNING = AttributeFunctionSpecs(
    uid="crystal.topics.data.group-by.numeric_binning",
    i18n=I18n(
        name="cons-conf-core-data-editor-aggregation-function-numeric-binning",
        description="crystal.topics.data.group-by.numeric_binning.i18n.description",
    ),
)
```
