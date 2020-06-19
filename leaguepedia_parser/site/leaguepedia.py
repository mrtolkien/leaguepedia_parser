import mwclient


class LeaguepediaSite:
    """A ghost loaded class that handles Leaguepedia connection and some caching.

    Full documentation: https://lol.gamepedia.com/Help:API_Documentation
    """

    def __init__(self, limit=500):
        self._site = None
        self.limit = limit

        # A simple cache to save team name searches
        # TODO Handle caching with sqlite for local persistence and timeouts
        self.team_name_cache = {}

    @property
    def site(self):
        if not self._site:
            self._load_site()

        return self._site

    def _load_site(self):
        """Creates site class fields.

        Used for ghost loading the class during package import.
        """
        # If not, we create the self.client object as our way to interact with the wiki
        self._site = mwclient.Site("lol.gamepedia.com", path="/")

    def query(self, **kwargs) -> list:
        """Issues a cargo query to leaguepedia.

        Params are usually:
            tables, join_on, fields, order_by, where

        Returns:
            List of rows from the query.
        """
        result = []

        # We check if we hit the API limit
        while len(result) % self.limit == 0:
            result.extend(
                [
                    row["title"]
                    for row in self.site.api("cargoquery", limit=self.limit, offset=len(result), **kwargs)["cargoquery"]
                ]
            )

            # If the cargoquery is empty, we stop the loop
            # TODO Find a better syntax
            if not result:
                break

        return result


# Ghost loaded instance shared by all other classes
leaguepedia = LeaguepediaSite()
