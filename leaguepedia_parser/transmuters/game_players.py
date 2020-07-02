import logging
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

    for team_side in game["teams"]:
        team_side_leaguepedia = "1" if team_side == "BLUE" else "2"

        for idx, game_player in enumerate(game["teams"][team_side]["players"]):
            try:
                # We get the player object from the Leaguepedia players list
                player = next(
                    p
                    for p in players
                    if p["Side"] == team_side_leaguepedia
                    and lit.get_id(p["Champion"], object_type="champion") == game_player["championId"]
                )

                game_player["role"] = role_translation[player["gameRoleNumber"]]

                unique_identifiers = game_player["uniqueIdentifiers"]["leaguepedia"]
                unique_identifiers: LeaguepediaPlayerIdentifier

                try:
                    assert player["gameName"] == unique_identifiers["name"]
                except AssertionError:
                    logging.warning(f"Names not matching for player {player['gameName']}/{unique_identifiers['name']}")

                unique_identifiers["irlName"] = player.get("irlName")
                unique_identifiers["country"] = player.get("Country")
                unique_identifiers["birthday"] = player.get("Birthdate")

                if player.get("pageId"):
                    unique_identifiers["pageId"] = int(player["pageId"])

            except StopIteration:
                # Since we cannot get the role properly, we try to infer it
                game_player["role"] = list(role_translation.values())[idx]

    return game
