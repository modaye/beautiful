import pytest
from requests.exceptions import ConnectTimeout
from beautiful.client import BeautifulClient


def test_client():
    client = BeautifulClient()
    with pytest.raises(ConnectTimeout):
        client.card_coord([1, 2, 3])
