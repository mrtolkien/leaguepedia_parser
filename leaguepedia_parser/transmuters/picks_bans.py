from typing import List
from lol_dto.classes.game.lol_game import LolPickBan
import lol_id_tools as lit

# Ordered in the draft order for pro play as of June 2020
picks_bans_fields = [
    "Team1Ban1",
    "Team2Ban1",
    "Team1Ban2",
    "Team2Ban2",
    "Team1Ban3",
    "Team2Ban3",
    "Team1Pick1",
    "Team2Pick1",
    "Team2Pick2",
    "Team1Pick2",
    "Team1Pick3",
    "Team2Pick3",
    "Team2Ban4",
    "Team1Ban4",
    "Team2Ban5",
    "Team1Ban5",
    "Team2Pick4",
    "Team1Pick4",
    "Team1Pick5",
    "Team2Pick5",
]


def transmute_picks_bans(input_dict) -> List[LolPickBan]:
    pb_list = []

    for field in picks_bans_fields:
        pb_list.append(
            LolPickBan(
                championName=input_dict[field],
                championId=lit.get_id(input_dict[field], object_type="champion"),
                isBan="Ban" in field,
                team="BLUE" if "Team1" in field else "RED",
            )
        )

    return pb_list
