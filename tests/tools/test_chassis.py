import asyncio

import pytest

from igenius_adapters_sdk.tools import chassis
from tests import factories as shf


@pytest.mark.parametrize(
    "result",
    [pytest.param([{"col1": "foo", "col2": 140}, {"col1": "bar", "col2": 3.4}, {"col1": "baz", "col2": None}])],
)
@pytest.mark.asyncio
async def test_dry_run(result):
    def engine(query):
        return result

    async def async_engine(query):
        await asyncio.sleep(0.1)
        return result

    query = shf.SelectQueryFactory()
    ch = chassis.Chassis(query=query, engine=engine)
    assert result == ch.run()

    ch = chassis.Chassis(query=query, engine=async_engine)
    assert result == await ch.async_run()
