import dataclasses
from typing import Optional
from leaguepedia_parser.site.leaguepedia import leaguepedia


@dataclasses.dataclass
class TeamAssets:
    thumbnail_url: str
    logo_url: str
    long_name: str  # Aka display name


def get_all_team_assets(team_link: str) -> TeamAssets:
    """

    Args:
        team_link: a field coming from Team1/Team2 in ScoreboardGames

    Returns:
        A TeamAssets object

    """
    result = leaguepedia.site.client.api(
        action="query",
        format="json",
        prop="imageinfo",
        titles=f"File:{team_link}logo square.png|File:{team_link}logo std.png",
        iiprop="url",
    )

    pages = result["query"]["pages"]

    urls = []
    for v in pages.values():
        urls.append(v["imageinfo"][0]["url"])

    long_name = leaguepedia.site.cache.get("Team", team_link, "link")

    return TeamAssets(
        thumbnail_url=urls[1],
        logo_url=urls[0],
        long_name=long_name,
    )


def get_team_logo(team_name: str, _retry=True) -> str:
    """
    Returns the team logo URL

    Params:
        team_name: Team name, usually gotten from the game dictionary
        _retry: whether or not to get the team’s full name from Leaguepedia if it was not understood

    Returns:
        URL pointing to the team’s logo
    """
    return _get_team_asset(f"File:{team_name}logo square.png", team_name, _retry)


def get_team_thumbnail(team_name: str, _retry=True) -> str:
    """
    Returns the team thumbnail URL

    Params:
        team_name: Team name, usually gotten from the game dictionary
        _retry: whether or not to get the team’s full name from Leaguepedia if it was not understood

    Returns:
        URL pointing to the team’s thumbnail
    """
    return _get_team_asset(f"File:{team_name}logo std.png", team_name, _retry)


def _get_team_asset(asset_name: str, team_name: str, _retry=True) -> str:
    """
    Returns the team thumbnail URL

    Params:
        team_name: Team name, usually gotten from the game dictionary
        _retry: whether or not to get the team’s full name from Leaguepedia if it was not understood

    Returns:
        URL pointing to the team’s logo
    """
    result = leaguepedia.site.client.api(
        action="query",
        format="json",
        prop="imageinfo",
        titles=asset_name,
        iiprop="url",
    )

    try:
        url = None
        pages = result.get("query").get("pages")
        for k, v in pages.items():
            url = v.get("imageinfo")[0].get("url")

    except (TypeError, AttributeError):
        # This happens when the team name was not properly understood.
        if _retry:
            return get_team_logo(get_long_team_name_from_trigram(team_name), False)
        else:
            raise Exception("Logo not found for the given team name")

    return url


def get_long_team_name_from_trigram(
    team_abbreviation: str,
    event_overview_page: str = None,
) -> Optional[str]:
    """
    Returns the long team name for the given team abbreviation using Leaguepedia’s search pages

    Only issues a query the first time it is called, then stores the data in a cache
    There is no cache timeout at the moment

    Args:
        team_abbreviation: A team name abbreviation, like IG or RNG
        event_overview_page: The overviewPage field of the tournament, useful for disambiguation

    Returns:
        The long team name, like "Invictus Gaming" or "Royal Never Give Up"
    """

    # We use only lowercase team abbreviations for simplicity
    team_abbreviation = team_abbreviation.lower()

    if event_overview_page:
        return leaguepedia.site.cache.get_team_from_event_tricode(
            event_overview_page, team_abbreviation
        )

    else:
        return leaguepedia.site.cache.get("Team", team_abbreviation, "link")
