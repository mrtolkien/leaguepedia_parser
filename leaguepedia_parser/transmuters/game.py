import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timezone

import lol_id_tools as lit
from lol_dto.classes.game import (
    LolGame,
    LolGamePlayer,
    LolGameTeamEndOfGameStats,
)
from lol_dto.classes.sources.riot_lol_api import RiotGameSource

from leaguepedia_parser.transmuters.game_players import LeaguepediaPlayerIdentifier


@dataclass
class LeaguepediaGameIdentifier:
    gameId: str
    matchId: str

    matchHistoryUrl: str
    overviewPage: str

    tournamentName: str


@dataclass
class LeaguepediaTeamIdentifier:
    name: str = None


def transmute_game(source_dict: dict) -> LolGame:
    """
    Transforms a ScoreboardGames row into a LolGame

    Some fields like team gold and kills are not present. Get_game_details should be used for it.
    """

    game = LolGame(
        start=datetime.fromisoformat(source_dict["DateTime UTC"])
        .replace(tzinfo=timezone.utc)
        .isoformat(timespec="seconds"),
        gameInSeries=int(source_dict["N GameInMatch"]),
        patch=source_dict["Patch"],
        duration=int(float(source_dict["Gamelength Number"] or 0) * 60),
        vod=source_dict["VOD"],
        winner="BLUE" if source_dict["Winner"] == "1" else "RED",
    )

    setattr(
        game.sources,
        "leaguepedia",
        LeaguepediaGameIdentifier(
            gameId=source_dict["GameId"],
            matchId=source_dict["MatchId"],
            matchHistoryUrl=source_dict["MatchHistory"],
            overviewPage=source_dict["OverviewPage"],
            tournamentName=source_dict["Tournament"],
        ),
    )

    for team, idx in [(game.teams.BLUE, 1), (game.teams.RED, 2)]:
        team.bans = [
            lit.get_id(champion_name, object_type="champion")
            for champion_name in source_dict[f"Team{idx}Bans"].split(",")
        ]

        team.endOfGameStats = LolGameTeamEndOfGameStats(
            turretKills=int(source_dict[f"Team{idx}Towers"] or 0),
            dragonKills=int(source_dict[f"Team{idx}Dragons"] or 0),
            riftHeraldKills=int(source_dict[f"Team{idx}RiftHeralds"] or 0),
            baronKills=int(source_dict[f"Team{idx}Barons"] or 0),
        )

        for player_idx, champion_name in enumerate(
            source_dict[f"Team{idx}Picks"].split(",")
        ):
            player_object = LolGamePlayer(
                championId=lit.get_id(champion_name, object_type="champion"),
            )

            setattr(
                player_object.sources,
                "leaguepedia",
                LeaguepediaPlayerIdentifier(
                    gameName=source_dict[f"Team{idx}Players"].split(",")[idx]
                ),
            )

            team.players.append(player_object)

        setattr(
            team.sources,
            "leaguepedia",
            LeaguepediaTeamIdentifier(name=source_dict[f"Team{idx}"]),
        )

    # For Riot API games, I directly parse the URL for the game to have its actual identifiers.
    if source_dict.get("MatchHistory") and "gameHash" in source_dict["MatchHistory"]:
        parsed_url = urllib.parse.urlparse(
            urllib.parse.urlparse(source_dict["MatchHistory"]).fragment
        )

        query = urllib.parse.parse_qs(parsed_url.query)
        platform_id, game_id = parsed_url.path.split("/")[1:]
        game_hash = query["gameHash"][0]

        setattr(
            game.sources,
            "riotLolApi",
            RiotGameSource(gameId=game_id, platformId=platform_id, gameHash=game_hash),
        )

    return game
