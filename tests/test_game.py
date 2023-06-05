import pytest
import leaguepedia_parser

regions_names = ["China", "Europe", "Korea"]

tournaments_names = [
    "LEC/2020 Season/Spring Season",
    "LEC/2021 Season/Spring Season",
    "LCK/2020 Season/Spring Season",
    "LCK/2021 Season/Spring Season",
    "LPL/2020 Season/Spring Season",
    "LPL/2021 Season/Spring Season",
    "2023 Mid-Season Invitational"
]


def test_regions():
    regions = leaguepedia_parser.get_regions()

    assert all(region in regions for region in regions_names)


@pytest.mark.parametrize("region", regions_names)
def test_tournaments(region):
    tournaments = leaguepedia_parser.get_tournaments(region, year=2020)

    assert len(tournaments) > 0

    for tournament in tournaments:
        assert tournament.overviewPage
        assert tournament.name
        assert tournament.tournamentLevel == "Primary"


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_games(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)

    assert len(games) > 0

    for game in games:
        for team in game.teams:
            for player in team.players:
                assert player.championId
                assert not player.role


@pytest.mark.parametrize("tournament_name", tournaments_names)
def test_get_details(tournament_name):
    games = leaguepedia_parser.get_games(tournament_name)
    game = games[0]

    # First, test without pageId
    leaguepedia_parser.get_game_details(game)

    # Then test with pageId
    game = leaguepedia_parser.get_game_details(game, True)

    assert game.picksBans

    for team in game.teams:
        assert len(team.players) == 5

        for player in team.players:
            assert hasattr(player.sources.leaguepedia, "irlName")
            assert hasattr(player.sources.leaguepedia, "birthday")
            assert player.sources.leaguepedia.pageId
            assert player.role
