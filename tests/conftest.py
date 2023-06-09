import pytest

from nhlpy.nhl_client import NHLClient

@pytest.fixture(scope='function')
def nhl_client() -> NHLClient:
    yield NHLClient()
