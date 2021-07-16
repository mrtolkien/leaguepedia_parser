import pytest
import leaguepedia_parser


@pytest.mark.parametrize("team_tuple", [("tsm", "TSM"), ("IG", "Invictus Gaming")])
def test_get_long_team_name(team_tuple):
    assert leaguepedia_parser.get_long_team_name(team_tuple[0]) == team_tuple[1]


def test_get_wrong_team_name():
    with pytest.raises(KeyError):
        leaguepedia_parser.get_long_team_name("mister mv")


@pytest.mark.parametrize("team_name", ["T1", "G2 Esports"])
def test_get_team_logo(team_name):
    assert leaguepedia_parser.get_team_logo(team_name)
