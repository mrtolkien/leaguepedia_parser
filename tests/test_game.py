import pytest

import leaguepedia_parser

regions_names = ["China", "Europe", "Korea"]
tournaments_names = [
    "LEC/2020 Season/Spring Season",
    "LCK/2020 Season/Spring Season",
    "LPL/2020 Season/Spring Season",
]


def test_regions():
    regions = leaguepedia_parser.get_regions()

    assert all(region in regions for region in regions_names)


@pytest.mark.parametrize("region", regions_names)
def test_tournaments(region):
    tournaments = leaguepedia_parser.get_tournaments(region, year=2020)

    for tournament in tournaments:
        print(tournament["overviewPage"])

    assert len(tournaments) > 0


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_games(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)

    assert len(games) > 0


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_get_details(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)

    # First, test without pageId
    leaguepedia_parser.get_game_details(games[0])

    # Then test with pageId
    game = leaguepedia_parser.get_game_details(games[0], True)

    assert game.picksBans

    for team in game.teams:
        assert len(team.players) == 5
        for player in team.players:
            assert hasattr(player.sources.leaguepedia, "irlName")
            assert hasattr(player.sources.leaguepedia, "birthday")
            assert player.sources.leaguepedia.pageId
