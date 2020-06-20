import pytest
import leaguepedia_parser


def test_get_long_team_name():
    assert leaguepedia_parser.get_long_team_name('tsm') == 'Team SoloMid'
    assert leaguepedia_parser.get_long_team_name('IG') == 'Invictus Gaming'

    with pytest.raises(KeyError):
        leaguepedia_parser.get_long_team_name('mister mv')


def test_get_team_logo():
    assert leaguepedia_parser.get_team_logo('T1')
    assert leaguepedia_parser.get_team_logo('G2 Esports')
