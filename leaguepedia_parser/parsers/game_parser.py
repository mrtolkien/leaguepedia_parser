from concurrent.futures.thread import ThreadPoolExecutor
from typing import List, Optional

from lol_dto.classes.game import LolGame
from lol_dto.classes.game.lol_game import LolPickBan

from leaguepedia_parser.site.leaguepedia import leaguepedia
from leaguepedia_parser.transmuters.game import game_fields, transmute_game
from leaguepedia_parser.transmuters.game_players import game_players_fields, add_players
from leaguepedia_parser.transmuters.picks_bans import picks_bans_fields, transmute_picks_bans
from leaguepedia_parser.transmuters.tournament import transmute_tournament, tournaments_fields, LeaguepediaTournament


def get_regions() -> List[str]:
    """Returns a list of all regions that appear in the Tournaments table.

    Returns:
        The list of all region names, simply strings.
    """
    regions_dicts_list = leaguepedia.query(
        tables="Tournaments", fields="Region", group_by="Region")

    return [row["Region"] for row in regions_dicts_list]


def get_tournaments(
    region: str = None, year: int = None, tournament_level: str = "Primary", is_playoffs: bool = None, **kwargs,
) -> List[LeaguepediaTournament]:
    """Returns a list of tournaments.

    Typical usage example:
        get_tournaments('China', 2020)

    Args:
        region: Recommended to get it from get_tournament_regions().
        year: Year to filter on. Defaults to None.
        tournament_level: Primary, Secondary, Major, Secondary, Showmatch. Defaults to Primary.
        is_playoffs: Can be used to filter between playoffs and regular season tournaments.

    Returns:
        A list of tournaments dictionaries.
    """
    # We need to cast is_playoffs as an integer for the cargoquery
    if is_playoffs is not None:
        is_playoffs = 1 if is_playoffs else 0

    # This generates the WHERE part of the cargoquery
    where = " AND ".join(
        [
            # One constraint per variable
            f"Tournaments.{field_name}='{value}'"
            for field_name, value in [
                ("Region", region),
                ("Year", year),
                ("TournamentLevel", tournament_level),
                ("IsPlayoffs", is_playoffs),
            ]
            # We don’t filter on variables that are None
            if value is not None
        ]
    )

    result = leaguepedia.query(
        tables="Tournaments, Leagues",
        join_on="Tournaments.League = Leagues.League",
        fields=f"Leagues.League_Short, {', '.join(f'Tournaments.{field}' for field in tournaments_fields)}",
        where=where,
        **kwargs,
    )

    return [transmute_tournament(tournament) for tournament in result]


def get_games(tournament_name=None, **kwargs) -> List[LolGame]:
    """Returns the list of games played in a tournament.

    Returns basic information about all games played in a tournament.

    Args:
        tournament_name: tournament name, acquired from get_tournaments().

    Returns:
        A list of LolGame with basic game information.
    """

    games = leaguepedia.query(
        tables="ScoreboardGames",
        fields=", ".join(game_fields),
        where=f"ScoreboardGames.OverviewPage ='{tournament_name}'",
        order_by="ScoreboardGames.DateTime_UTC",
        **kwargs,
    )

    return [transmute_game(game) for game in games]


def get_game_details(game: LolGame, add_page_id=False) -> LolGame:
    # TODO Add more scoreboard information in this step
    """Gets most game information available on Leaguepedia.

    Args:
        game: A LolGame with Leaguepedia IDs in its 'sources' dict.
        add_page_id: whether or not to link the player page ID to their object. Mostly for debugging.

    Returns:
        The LolGame with all information available on Leaguepedia.
    """
    try:
        assert "scoreboardIdWiki" in game["sources"]["leaguepedia"]
        assert "uniqueGame" in game["sources"]["leaguepedia"]
    except AssertionError:
        raise ValueError(
            f"Leaguepedia Identifiers not present in the input object.")

    with ThreadPoolExecutor() as executor:
        picks_bans_future = executor.submit(_get_picks_bans, game)
        game_future = executor.submit(_add_game_players, game, add_page_id)

    game = game_future.result()
    game["picksBans"] = picks_bans_future.result()

    return game


def _get_picks_bans(game: LolGame) -> Optional[List[LolPickBan]]:
    """Returns the picks and bans for the game.
    """
    # Double join as required by Leaguepedia
    picks_bans = leaguepedia.query(
        tables="PicksAndBansS7, MatchScheduleGame, ScoreboardGames",
        join_on="PicksAndBansS7.GameID_Wiki = MatchScheduleGame.GameID_Wiki, "
        "MatchScheduleGame.ScoreboardID_Wiki = ScoreboardGames.ScoreboardID_Wiki",
        fields=", ".join(picks_bans_fields),
        where=f"ScoreboardGames.ScoreboardID_Wiki = '{game['sources']['leaguepedia']['scoreboardIdWiki']}'",
    )

    if not picks_bans:
        return None

    return transmute_picks_bans(picks_bans[0])


def _add_game_players(game: LolGame, add_page_id: bool) -> LolGame:
    """Joins on PlayersRedirect to get all players information.
    """
    # TODO Make that more beautiful, not satisfied with black’s formatting
    players = leaguepedia.query(
        tables=f"ScoreboardGames, ScoreboardPlayers, PlayerRedirects, Players"
        + (", _pageData = PD" if add_page_id else ""),
        join_on="ScoreboardGames.UniqueGame = ScoreboardPlayers.UniqueGame, "
        "ScoreboardPlayers.Link = PlayerRedirects.AllName, "
        "PlayerRedirects._pageName = Players._pageName" +
        (", Players._pageName = PD._pageName" if add_page_id else ""),
        fields=", ".join(game_players_fields) +
        (", PD._pageID=pageId" if add_page_id else ""),
        where=f"ScoreboardGames.UniqueGame = '{game['sources']['leaguepedia']['uniqueGame']}'"
        + ("AND PD._isRedirect = 0" if add_page_id else ""),
    )

    return add_players(game, players)

# TODOs
# def _add_player_game_items
