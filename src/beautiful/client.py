from typing import List

import requests


class BeautifulClient:
    def __init__(
        self,
        url="http://192.168.0.111:5000/gs/position/data/card/coordinates",
        **kwargs,
    ):
        self.url = url
        self.kwargs = kwargs
        self.conn = requests.Session()

    def card_coord(self, card_ids: List[int]):
        """
        Get the coordinates of the cards.
        Args:
            card_ids: card ids.

        Returns: coordinates of the cards.

        """
        response = self.conn.get(self.url, params={"cardIDList": card_ids})
        response.raise_for_status()
        return response.json()
