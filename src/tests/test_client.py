from beautiful.client import BeautifulClient


def test_client():
    client = BeautifulClient()
    assert client.card_coord(card_ids=[1]) == []
