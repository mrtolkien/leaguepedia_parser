from dataclasses import dataclass
from typing import List
from lol_dto.classes.game import LolGame, LolGamePlayer
import lol_id_tools as lit


role_translation = {"1": "TOP", "2": "JGL", "3": "MID", "4": "BOT", "5": "SUP"}


@dataclass
class LeaguepediaPlayerIdentifier:
    gameName: str = None  # Defined here because it’s a leaguepedia-specific field
    name: str = None  # Current player name
    irlName: str = None  # IRL name of the player
    country: str = None  # Country of origin
    birthday: str = None  # YYYY-MM-DD
    pageId: int = None  # Page ID on leaguepedia


def add_players(
    game: LolGame, players: List[dict], add_page_id: bool = False
) -> LolGame:
    """
    Adds additional player information from ScoreboardPlayers
    """

    for idx, team in enumerate(game.teams):
        team_side_leaguepedia = "1" if idx == 0 else "2"

        for player_idx, game_player in enumerate(team.players):
            game_player: LolGamePlayer

            try:
                # We get the player object from the Leaguepedia players list
                player_latest_data = next(
                    p
                    for p in players
                    if p["Side"] == team_side_leaguepedia
                    and lit.get_id(p["Champion"], object_type="champion")
                    == game_player.championId
                )
            except StopIteration:
                # Since we cannot get the role properly, we try to infer it from the index
                game_player.role = list(role_translation.values())[player_idx]
                continue

            game_player.role = role_translation[player_latest_data["gameRoleNumber"]]

            leaguepedia_identifier = LeaguepediaPlayerIdentifier(
                name=player_latest_data.get("currentGameName"),
                irlName=player_latest_data.get("irlName"),
                country=player_latest_data.get("Country"),
                birthday=player_latest_data.get("Birthdate"),
            )

            if add_page_id:
                leaguepedia_identifier.pageId = int(player_latest_data["pageId"])

            setattr(game_player.sources, "leaguepedia", leaguepedia_identifier)

    return game
