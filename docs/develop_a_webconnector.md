# Develop a Web Connector

> This example is for developing a **web connector** using Python and FastAPI.

You'll implement a simple datasource adapter for the OpenWeather APIs.

**The code is given intentionally simple and straightforward in order to focus on the base concepts, not on the implementation**.

## Requirements

* Python >= 3.8
* [Poetry](https://python-poetry.org) >= 1.1
* [FastAPI](https://fastapi.tiangolo.com) >= 0.63.0

## Base concepts

A Web Connector is a data adapter that exposes your data to iGenius Crystal backend.  
It's a web service and you only need to implement three endpoint to be able to talk with Crystal:

* `/test_connection`: used by iGenius backend services to check the connection between them and the Web Connector, in order to know if the connector is available. In this endpoint you can also test the connection between your Web Connectior and your custom data source. In this way, you can tell to iGenius backend services if your data source is ready to be queried
* `/collections/actions/describe`: returns to iGenius backend the list of available collections in the connected datasource. A collection is a structured set of data such as a database table or CSV file
* `/query/actions/execute`: returns the result of the query requested by Crystal

## Project bootstrap

First of all, you need to bootstrap your project.  
The first step is to initialize our project (here we use [Poetry](https://python-poetry.org))

```bash
$ poetry new webconnector
```

We suggest to move the `webconnector` directory into a `src` directory. So, you'll en up with a structure like this:

```
|- src
    |- webconnector
        |- __init__.py
|- tests
    |- __init__.py
    |- test_webconnector.py
|- poetry.lock
|- pyproject.toml
|- README.rst
```

Next you can install [FastAPI](https://fastapi.tiangolo.com) and [Uvicorn](https://www.uvicorn.org) (we'll need it later to run our webservice) with

```bash
$ poetry add fastapi uvicorn
```

and iGenius Adapters SDK with

```bash
$ poetry add igenius-adapters-sdk
```

and, finally, you can install your project itself

```bash
$ poetry install
```

## Endpoint `/test_connection`

Now you can start to implement our first endpoint: `/test_connection`.
You'll keep it simple, so you'll always return a successful outcome.

Let's start writing the route:

**`src/webconnector/routers/test_connection.py`**

```python
import logging
from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger("webconnector")
logger.setLevel("INFO")

router = APIRouter()


class CheckConnectionResponse(BaseModel):
    outcome: str


class CheckConnectionFailResponse(CheckConnectionResponse):
    details: str


@router.get(
    "/test_connection",
    responses={
        200: {
            "description": (
                "Successful response, the Web Connector is ready to accept requests."
            )
        }
    },
    response_model=Union[CheckConnectionFailResponse, CheckConnectionResponse],
)
def test_connection():
    logger.info("Checking connection...")

    return {"outcome": "success"}
```

Now you can define the main FastAPI application.

**`src/webconnector/app.py`**

```python
from fastapi import FastAPI

from webconnector.routers import test_connection

app = FastAPI(title="Crystal WebConnector Datasource Adapter")

app.include_router(test_connection.router, tags=["crystal endpoints"])
```

And the entrypoint of our webservice.

**`src/main.py`**

```python
import os

import uvicorn

if __name__ == '__main__':
    host = os.environ.get('WEB_HOST', '0.0.0.0')
    port = int(os.environ.get('WEB_PORT', 8090))
    uvicorn.run(
        'webconnector.app:app',
        host=host,
        port=port,
        log_level='info',
        reload=True
    )
```

### Run `/test_connection` endpoint

If everything went fine, you can execute your webservice with:

```bash
$ poetry run python src/main.py
INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
INFO:     Started reloader process [44110] using statreload
INFO:     Started server process [44114]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

And you can access your first endpoint at [http://127.0.0.1:8090/test_connection](http://127.0.0.1:8090/test_connection) with your browser. Here is a sample output with curl:

```bash
$ curl -i -X GET http://127.0.0.1:8090/test_connection
HTTP/1.1 200 OK
date: Tue, 05 Jan 2021 11:50:28 GMT
server: uvicorn
content-length: 21
content-type: application/json

{"outcome":"success"}
```

## Endpoint `/collections/actions/describe`

You'll keep this project very simple, so the **describe collections** endpoint will expose only a collection.

### The schema

Based on OpenWeather APIs, you'll map a [`Collection`](entities/collection.md#collection) named `Cities` with these attributes:

| name     | type        | filterable | sortable |
| -------- | ----------- | ---------- | -------- |
| id       | categorical | true       | true     |
| name     | categorical | true       | true     |
| country  | categorical | true       | true     |
| temp_min | numeric     | true       | true     |
| temp_max | numeric     | true       | true     |

### Mapping the schema using iGenius Adapters SDK entities

To describe a collection, you need to use the entities by our iGenius Adapters SDK. You should start from [`Attribute`](entities/collection.md#attributes) that will be aggregated into [`AttributesSchema`](/collection.md#attributesschema) that will be collected into a [`Collection`](entities/collection.md#Collection).

```python
tc_id_attr = Attribute(
    uid="id",
    type=AttributeType.CATEGORICAL,
    filterable=True,
    sortable=True,
)
tc_name_attr = Attribute(
    uid="name",
    type=AttributeType.CATEGORICAL,
    filterable=True,
    sortable=True,
)
tc_country_attr = Attribute(
    uid="country",
    type=AttributeType.CATEGORICAL,
    filterable=True,
    sortable=True,
)
tc_min_temp_attr = Attribute(
    uid="temp_min",
    type=AttributeType.NUMERIC,
    filterable=True,
    sortable=True,
)
tc_max_temp_attr = Attribute(
    uid="temp_max",
    type=AttributeType.NUMERIC,
    filterable=True,
    sortable=True,
)
cities_schema = AttributesSchema(
    attributes=[
        tc_id_attr,
        tc_name_attr,
        tc_country_attr,
        tc_min_temp_attr,
        tc_max_temp_attr,
    ]
)
top_cities = Collection(
    uid="openweather.cities", attributes_schema=cities_schema
)
```

### The route

The resulting route will be:

**`src/webconnector/routers/describe_collections.py`**

```python
import logging
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from igenius_adapters_sdk.entities.collection import (
    Collection,
    AttributesSchema,
    Attribute,
    AttributeType,
)

logger = logging.getLogger("webconnector")
logger.setLevel("INFO")

router = APIRouter()


class DescribeCollectionsResponse(BaseModel):
    collections: List[Collection]


class DescribeCollectionsError(Exception):
    pass


@router.post(
    "/collections/actions/describe",
    responses={200: {"description": "Successful response"}},
    response_model=DescribeCollectionsResponse,
)
def describe_collections():
    tc_id_attr = Attribute(
        uid="id",
        type=AttributeType.CATEGORICAL,
        filterable=True,
        sortable=True,
    )
    tc_name_attr = Attribute(
        uid="name",
        type=AttributeType.CATEGORICAL,
        filterable=True,
        sortable=True,
    )
    tc_country_attr = Attribute(
        uid="country",
        type=AttributeType.CATEGORICAL,
        filterable=True,
        sortable=True,
    )
    tc_min_temp_attr = Attribute(
        uid="temp_min",
        type=AttributeType.NUMERIC,
        filterable=True,
        sortable=True,
    )
    tc_max_temp_attr = Attribute(
        uid="temp_max",
        type=AttributeType.NUMERIC,
        filterable=True,
        sortable=True,
    )
    cities_schema = AttributesSchema(
        attributes=[
            tc_id_attr,
            tc_name_attr,
            tc_country_attr,
            tc_min_temp_attr,
            tc_max_temp_attr,
        ]
    )
    top_cities = Collection(
        uid="openweather.cities", attributes_schema=cities_schema
    )
    collections = [top_cities]
    return {
        "collections": collections,
    }
```

And the router inclusion in `app.py`.

**`src/webconnector/app.py`**

```python
...

app.include_router(test_connection.router, tags=["crystal endpoints"])
app.include_router(describe_collections.router, tags=["crystal endpoints"])
```

### Run `/collections/actions/describe` endpoint

If everything went fine, you can access your first endpoint at [http://127.0.0.1:8090/collections/actions/describe](http://127.0.0.1:8090/collections/actions/describe). Here you have an HTTP POST, so we suggest to use a REST client or simply curl with [jq](https://stedolan.github.io/jq/):

```bash
$ curl -s -X POST http://127.0.0.1:8091/collections/actions/describe | jq
{
  "collections": [
    {
      "uid": "accuweather.top_cities",
      "attributes_schema": {
        "attributes": [
          {
            "uid": "key",
            "type": "crystal.topics.data.attribute-types.categorical",
            "filterable": true,
            "sortable": true
          },
          {
            "uid": "english_name",
            "type": "crystal.topics.data.attribute-types.categorical",
            "filterable": true,
            "sortable": true
          },
          {
            "uid": "country",
            "type": "crystal.topics.data.attribute-types.categorical",
            "filterable": true,
            "sortable": true
          },
          {
            "uid": "temp_min",
            "type": "crystal.topics.data.attribute-types.numeric",
            "filterable": false,
            "sortable": false
          },
          {
            "uid": "temp_max",
            "type": "crystal.topics.data.attribute-types.numeric",
            "filterable": false,
            "sortable": false
          }
        ]
      }
    }
  ]
}
```

## Endpoint `/query/actions/execute`

Here you'll have a good part of our business logic, since it is the endpoint that will translate the query coming from Crystal to a result set.  
In this example, you'll work on a simple request: a list of cities with current min and max temperature.

### The payload

Let's start with the payload that will be translated into a [`Query`](entities/queries.md#query) entity.

```json
{
    "connection_params": {
        "token": "#########"
    },
    "query": {
        "from_": {
            "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
            "collection_uid": "openweather.cities"
        },
        "where": null,
        "order_by": null,
        "limit": 1000,
        "offset": 0,
        "aggregations": [
            {
                "attribute_uri": {
                    "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
                    "collection_uid": "openweather.cities",
                    "attribute_uid": "id"
                },
                "alias": "id",
                "function_uri": {
                    "function_type": "aggregation",
                    "function_uid": "crystal.topics.data.aggregation.identity",
                    "function_params": null
                }
            },
            {
                "attribute_uri": {
                    "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
                    "collection_uid": "openweather.cities",
                    "attribute_uid": "name"
                },
                "alias": "name",
                "function_uri": {
                    "function_type": "aggregation",
                    "function_uid": "crystal.topics.data.aggregation.identity",
                    "function_params": null
                }
            },
            {
                "attribute_uri": {
                    "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
                    "collection_uid": "openweather.cities",
                    "attribute_uid": "country"
                },
                "alias": "country",
                "function_uri": {
                    "function_type": "aggregation",
                    "function_uid": "crystal.topics.data.aggregation.identity",
                    "function_params": null
                }
            },
            {
                "attribute_uri": {
                    "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
                    "collection_uid": "openweather.cities",
                    "attribute_uid": "temp_min"
                },
                "alias": "temp_min",
                "function_uri": {
                    "function_type": "aggregation",
                    "function_uid": "crystal.topics.data.aggregation.identity",
                    "function_params": null
                }
            },
            {
                "attribute_uri": {
                    "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
                    "collection_uid": "openweather.cities",
                    "attribute_uid": "temp_max"
                },
                "alias": "temp_max",
                "function_uri": {
                    "function_type": "aggregation",
                    "function_uid": "crystal.topics.data.aggregation.identity",
                    "function_params": null
                }
            }
        ]
    }
}
```

### Payload analysis

In this example query, you are requesting all the fields of our table.

Here you have two main keys at the root of our payload:

* `connection_params`: it's the place where Crystal puts the authentication key that you have configured on Crystal website
* `query`: it's the paylod that will be translated automatically to a [`Query`](entities/queries.md#query) entity by [Pydantic](https://pydantic-docs.helpmanual.io)

> In this payload you can notice the key `datasource_uid`: it's the UID of the datasource linked to your Web Connector and it's assigned automatically by Crystal. You don't have to parse it.

In this payload you can see the attributes defined as [`AggregationAttribute`](entities/data_attributes.md#aggregation-attribute). You can play with this example trying adding or removing attributes.  
For the purpose of this example, we have only a [`Collection`](entities/collection.md#collection), so in our code we'll parse only the attribute_id. Since in our adapter we are also not handling aliases, we'll ignore the `alias` key.  
On the `function_uri` key you can say that, since here you only have single values and not any particular aggregation, you are handling identities. In Crystal jargon, and identity is a single value.

```json
{
    "attribute_uri": {
        "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
        "collection_uid": "openweather.cities",
        "attribute_uid": "name"
    },
    "alias": "name",
    "function_uri": {
        "function_type": "aggregation",
        "function_uid": "crystal.topics.data.aggregation.identity",
        "function_params": null
    }
}
```

So, to handle correctly a request with this payload, you should implement something like this for your endpoint:

**`src/webconnector/routers/execute_query.py`**

```python
import http.client
import json
from typing import Any, Dict, List

from fastapi import APIRouter
from igenius_adapters_sdk.entities.query import Query
from pydantic import BaseModel


APP_ID = "0cf87ce325a3b4f09fa5642abe66bf34"

router = APIRouter()


class ConnectionParamsRequest(BaseModel):
    token: str


class ExecuteQueryError(Exception):
    pass


class ExecuteQueryResponse(BaseModel):
    records: List[Dict[str, Any]]


@router.post(
    "/query/actions/execute",
    responses={200: {"description": "Successful response"}},
    response_model=ExecuteQueryResponse,
)
def execute_query(
    connection_params: ConnectionParamsRequest,
    query: Query,
):
    fields = [
        aggregation.attribute_uri.attribute_uid for aggregation in query.aggregations
    ]

    with open("./assets/city.list.json") as json_file:
        data = [
            {"id": record["id"], "name": record["name"], "country": record["country"]}
            for record in json.load(json_file)[:10]
        ]

    records = []
    for city in data:
        conn = http.client.HTTPSConnection("api.openweathermap.org")
        conn.request("GET", f"/data/2.5/weather?id={city['id']}&appid={APP_ID}", "", {})
        res = conn.getresponse()
        response_data = res.read()
        response = json.loads(response_data.decode("utf-8"))

        complete_record = {
            "id": city["id"],
            "name": city["name"],
            "country": city["country"],
            "temp_min": response["main"]["temp_min"],
            "temp_max": response["main"]["temp_max"],
        }

        record = {key: complete_record[key] for key in fields}
        records.append(record)

    return {"records": records}
```

Now we can add our route to the application:

**`src/webconnector/app.py`**

```python
...

app.include_router(test_connection.router, tags=["crystal endpoints"])
app.include_router(describe_collections.router, tags=["crystal endpoints"])
app.include_router(execute_query.router, tags=["crystal endpoints"])
```

### Run `/query/actions/execute` endpoint

> Pay attention to `--data-raw`: to avoid a verbose command, there's an ellipsis. You must use the complete data structure previously shown in this documentation

```bash
$ curl --location --request POST 'http://localhost:8091/query/actions/execute' \
--header 'Content-Type: application/json' \
--data-raw '{
    "connection_params": {
        "token": "#########"
    },
    "query": {
        "from_": {
            "datasource_uid": "2b55dd12-9e9b-4bc1-967e-be497abdfc1f",
            "collection_uid": "openweather.cities"
        },
        "where": null,
        "order_by": null,
        "limit": 1000,
        "offset": 0,
        "aggregations": [
            ...
        ]
    }
}'
```
