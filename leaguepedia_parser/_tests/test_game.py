import leaguepedia_parser

regions_names = ['China', 'Europe', 'Korea']
tournaments_names = ['LEC 2020 Spring', 'LCK 2020 Spring', 'LPL 2020 Spring']


def test_regions():
    regions = leaguepedia_parser.get_regions()

    assert all(region in regions for region in regions_names)


def test_tournaments():
    for region in regions_names:
        tournaments = leaguepedia_parser.get_tournaments(region, year=2020)
        assert len(tournaments) > 0


def test_games():
    for tournament_name in tournaments_names:
        games = leaguepedia_parser.get_games(tournament_name)
        assert len(games) > 0


def test_get_details():
    for tournament_name in tournaments_names:
        games = leaguepedia_parser.get_games(tournament_name)

        game = leaguepedia_parser.get_game_details(games[0], True)

        assert 'picksBans' in game

        for team in 'BLUE', 'RED':
            for player in game['teams'][team]['players']:
                assert 'irlName' in player['uniqueIdentifiers']['leaguepedia']
                assert 'birthday' in player['uniqueIdentifiers']['leaguepedia']
                assert 'pageId' in player['uniqueIdentifiers']['leaguepedia']
