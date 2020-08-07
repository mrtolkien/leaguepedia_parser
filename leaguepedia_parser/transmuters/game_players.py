from typing import List, TypedDict
from lol_dto.classes.game import LolGame
import lol_id_tools as lit


role_translation = {"1": "TOP", "2": "JGL", "3": "MID", "4": "BOT", "5": "SUP"}


class LeaguepediaPlayerIdentifier(TypedDict, total=False):
    gameName: str  # Defined here because it’s a leaguepedia-specific field
    name: str  # Current player name
    irlName: str  # IRL name of the player
    country: str  # Country of origin
    birthday: str  # YYYY-MM-DD
    pageId: int  # Page ID on leaguepedia


def add_players(game: LolGame, players: List[dict], add_page_id: bool = False) -> LolGame:
    """Adds additional player information from ScoreboardPlayers.
    """

    for team_side in game["teams"]:
        team_side_leaguepedia = "1" if team_side == "BLUE" else "2"

        for idx, game_player in enumerate(game["teams"][team_side]["players"]):
            try:
                # We get the player object from the Leaguepedia players list
                player_latest_data = next(
                    p
                    for p in players
                    if p["Side"] == team_side_leaguepedia
                    and lit.get_id(p["Champion"], object_type="champion") == game_player["championId"]
                )

                game_player["role"] = role_translation[player_latest_data["gameRoleNumber"]]

                unique_identifiers = LeaguepediaPlayerIdentifier(
                    name=player_latest_data.get("currentGameName"),
                    irlName=player_latest_data.get("irlName"),
                    country=player_latest_data.get("Country"),
                    birthday=player_latest_data.get("Birthdate"),
                )

                if add_page_id:
                    unique_identifiers["pageId"] = int(player_latest_data["pageId"])

                game_player["uniqueIdentifiers"] = {"leaguepedia": unique_identifiers}

            except StopIteration:
                # Since we cannot get the role properly, we try to infer it
                game_player["role"] = list(role_translation.values())[idx]

    return game
