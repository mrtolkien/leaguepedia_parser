from typing import List, TypedDict
from lol_dto.classes.game import LolGame
import lol_id_tools as lit

# TODO Add more fields?
game_players_fields = {
    "ScoreboardPlayers.Name=gameName",
    "ScoreboardPlayers.Role_Number=gameRoleNumber",
    "ScoreboardPlayers.Champion",
    "ScoreboardPlayers.Side",
    "Players.Name=irlName",
    "Players.Country",
    "Players.Birthdate",
    # "Players.ID=currentGameName",
    # "Players.Image",
    # "Players.Team=currentTeam",
    # "Players.Role=currentRole",
    # "Players.SoloqueueIds",
}


role_translation = {"1": "TOP", "2": "JGL", "3": "MID", "4": "BOT", "5": "SUP"}


class LeaguepediaPlayerIdentifier(TypedDict, total=False):
    name: str
    irlName: str
    country: str
    birthday: str  # YYYY-MM-DD
    pageId: int


def add_players(game: LolGame, players: List[dict]) -> LolGame:
    """Adds additional player information from ScoreboardPlayers.
    """
    for player in players:
        team_side = "BLUE" if player["Side"] == "1" else "RED"
        champion_id = lit.get_id(player["Champion"], object_type="champion")

        # We get player by side and champion, which works even for blind picks
        game_player = next(p for p in game["teams"][team_side]["players"] if p["championId"] == champion_id)

        game_player["role"] = role_translation[player["gameRoleNumber"]]

        unique_identifiers = game_player["uniqueIdentifiers"]["leaguepedia"]
        unique_identifiers: LeaguepediaPlayerIdentifier

        assert player["gameName"] == unique_identifiers["name"]

        unique_identifiers["irlName"] = player.get("irlName")
        unique_identifiers["country"] = player.get("Country")
        unique_identifiers["birthday"] = player.get("Birthdate")

        if player.get("pageId"):
            unique_identifiers["pageId"] = int(player["pageId"])

    return game
