import json
from leaguepedia_parser.site.leaguepedia import leaguepedia


def get_team_logo(team_name: str, _retry=True) -> str:
    """Returns the team logo URL.

    Params:
        team_name: Team name, usually gotten from the game dictionary.
        _retry: whether or not to get the team’s full name from Leaguepedia if it was not understood.

    Returns:
        URL pointing to the team’s logo
    """
    result = leaguepedia.site.api(
        action="query",
        format="json",
        prop="imageinfo",
        titles=u"File:{}logo square.png".format(team_name),
        iiprop="url",
    )

    # TODO Clean that up
    try:
        url = None
        pages = result.get("query").get("pages")
        for k, v in pages.items():
            url = v.get("imageinfo")[0].get("url")
    except (TypeError, AttributeError):
        # This happens when the team name was not properly understood.
        if _retry:
            return get_team_logo(get_long_team_name(team_name), False)
        else:
            raise Exception("Logo not found for the given team name")
    return url


def get_long_team_name(team_abbreviation: str) -> str:
    """Returns the long team name for the given team abbreviation using Leaguepedia’s search pages.

    Only issues a query the first time it is called, then stores the data in a cache.
    There is no cache timeout at the moment.

    Args:
        team_abbreviation: A team name abbreviation, like IG or RNG

    Returns:
        The long team name, like "Invictus Gaming" or "Royal Never Give Up"
    """

    # We use only lowercase team abbreviations for simplicity
    team_abbreviation = team_abbreviation.lower()

    if team_abbreviation not in leaguepedia.team_name_cache:
        _load_team_name(team_abbreviation)

    return leaguepedia.team_name_cache[team_abbreviation]


def _load_team_name(team_abbreviation: str):
    """Loads the full name for a given abbreviation.

    Raises:
        KeyError if no team name is found from Leaguepedia.
    """

    result = leaguepedia.site.api("expandtemplates", prop="wikitext", text="{{JsonEncode|Team}}")
    file = json.loads(result["expandtemplates"]["wikitext"])

    if team_abbreviation not in file:
        raise KeyError("No team name found for this abbreviation.")

    value_table = file[team_abbreviation]

    # To be entirely fair, I am not sure what’s going on here
    if isinstance(value_table, str):
        value_table = file[value_table]

    try:
        leaguepedia.team_name_cache[team_abbreviation] = value_table["long"]
    except KeyError:
        raise KeyError("No long name found for this team abbreviation.")
